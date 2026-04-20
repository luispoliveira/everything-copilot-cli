# Vitrina Interativa de Minerais — Lousal

**Implementation Plan** | Date: 2026-04-20 | Version: 2.0

---

## 1. Executive Summary

The Lousal Mineral Display Case is a museum-grade interactive installation featuring a 6,950 mm wide vitrina divided into 3 glass panels. Visitors touch one of **25–30 zones** on the front glass via an IR touch frame, triggering a coordinated response: the corresponding mineral spotlight brightens, all others dim, and informational content is projected onto the rear panel. The system automatically returns to standby after 45 seconds of inactivity.

**Central controller**: Raspberry Pi 5 (8GB), Raspberry Pi OS Bookworm 64-bit, headless.
**Touch**: 3× CJTouch 84" IR Touch Frames (one per glass panel), USB HID → evdev, 25–30 software-defined zones.
**Lighting**: 25–30 dimmable GU10 spotlights, 1:1 mapping to zones, controlled via DMX512 (Enttec DMX USB Pro → 32-channel dimmer rack).
**Projection**: Short-throw projector → rear projection film → HDMI from RPi5, Pygame full-screen.
**Coordination**: Python state machine on RPi5, no ESP32, no MQTT broker, no WiFi dependency for touch.

- **Overall complexity**: 🔴 Complex (multi-subsystem, 230V AC, museum continuous operation, 25–30 zones)
- **Estimated total duration**: 20 weeks (to September 2026 deadline)
- **Budget**: ~€2,550 materials, well within €5,000 total

---

## 2. System Architecture

```
┌────────────────────────────────────────────────────────────────────────┐
│                      VITRINA FRONTAL (6950mm)                          │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐       │
│  │   PANO 1         │ │   PANO 2         │ │   PANO 3         │       │
│  │  Zones  1–~10    │ │  Zones ~11–20    │ │  Zones ~21–30    │       │
│  │ [IR Frame 0]     │ │ [IR Frame 1]     │ │ [IR Frame 2]     │       │
│  │  (exterior face) │ │  (exterior face) │ │  (exterior face) │       │
│  └──────────────────┘ └──────────────────┘ └──────────────────┘       │
│        ↑ touch             ↑ touch              ↑ touch               │
│  ┌─────┴───────────────────┴────────────────────┴──────────┐          │
│  │          25–30 spotlights (ceiling inside vitrina)        │          │
│  │          Zone N → Spotlight N  (1:1 mapping)              │          │
│  └──────────────────────────────────────────────────────────┘          │
│  ┌────────────────────────────────────────────────────────────┐        │
│  │  Rear projection film (back interior panel)                │        │
│  └────────────────────────────────────────────────────────────┘        │
└────────────────────────────────────────────────────────────────────────┘
         │ USB (×3)                                  │ HDMI
         ▼                                           ▼
┌─────────────────────────────────────────────────────────────┐
│               RASPBERRY PI 5 (8GB)                          │
│                                                             │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────────┐ │
│  │ evdev reader │  │ DMX control  │  │ Pygame projection │ │
│  │ (3 IR frames)│  │ (pyenttec)   │  │ (HDMI display 1)  │ │
│  └──────┬───────┘  └──────┬───────┘  └────────┬──────────┘ │
│         │                 │                    │            │
│  ┌──────┴─────────────────┴────────────────────┴──────────┐ │
│  │              coordinator.py (state machine)             │ │
│  │    STANDBY ←──────────────────── ACTIVE(zone N)        │ │
│  │       ↑              45s timeout        ↑              │ │
│  │       └──────────── touch event ────────┘              │ │
│  └────────────────────────────────────────────────────────┘ │
│                                                             │
│  systemd service: vitrina.service (auto-start on boot)      │
└─────────────────────────┬───────────────────────────────────┘
                          │ USB Serial
                          ▼
              ┌───────────────────────┐
              │ Enttec DMX USB Pro    │
              │ (USB → DMX512)        │
              └───────────┬───────────┘
                          │ DMX512 XLR
                          ▼
              ┌───────────────────────┐
              │ 32-ch DMX Dimmer Rack │
              │ CH 1–30 = Zone 1–30   │
              └───────────┬───────────┘
                          │ 230V AC (⚡ electrician required)
                          ▼
              ┌───────────────────────────────────┐
              │ 25–30 × GU10 LED 7W 2700K         │
              │ Spotlight N on DMX channel N       │
              └───────────────────────────────────┘
```

**Data flow (touch event):**

1. Visitor touches Zone N on front glass
2. IR frame detects touch → USB HID event → RPi5 evdev
3. Python maps (frame_id, x, y) → zone number N
4. State machine transitions STANDBY → ACTIVE(N)
5. DMX: channel N = 255, all others = 40
6. Pygame: display content for zone N on projector
7. 45s inactivity → return to STANDBY (all lights 160, projection black)

---

## 3. Sub-Plan Index

Each challenge is documented in its own file:

| File                                     | Challenge                                                | Complexity  |
| ---------------------------------------- | -------------------------------------------------------- | ----------- |
| [c1-touch.md](c1-touch.md)               | IR Touch Frame setup, evdev, zone mapping                | 🟡 Medium   |
| [c2-lighting.md](c2-lighting.md)         | DMX512, 32ch dimmer rack, 25–30 spotlights               | 🔴 Advanced |
| [c3-projection.md](c3-projection.md)     | Short-throw projector, Pygame display, 30 content assets | 🟡 Medium   |
| [c4-coordinator.md](c4-coordinator.md)   | Python state machine, threading, systemd                 | 🟡 Medium   |
| [c5-installation.md](c5-installation.md) | Physical install, 230V safety, cable management          | 🔴 Advanced |

---

## 4. Budget Estimate

| Item                                                      | Est. Cost                                      |
| --------------------------------------------------------- | ---------------------------------------------- |
| Raspberry Pi 5 (8GB) + official PSU + active cooling case | ~€120                                          |
| 3× CJTouch 84" IR Touch Frame (CIP840AP-K1)               | ~€300                                          |
| Powered USB hub (7-port, 5V 4A)                           | ~€35                                           |
| Enttec DMX USB Pro (USB→DMX)                              | ~€90                                           |
| 32-ch DMX dimmer rack (e.g. 2× Showtec DimRack 16ch)      | ~€700                                          |
| 30× GU10 dimmable LED 7W 2700K                            | ~€150                                          |
| 30× GU10 spotlight fixture/mount                          | ~€450                                          |
| Short-throw projector (BenQ MW560 or equiv.)              | ~€500                                          |
| Rear projection film (self-adhesive)                      | ~€100                                          |
| USB-A cables (3×2m for IR frames)                         | ~€20                                           |
| DMX XLR cables + terminator                               | ~€40                                           |
| HDMI cable (3m)                                           | ~€15                                           |
| microSD card 64GB (RPi5 OS)                               | ~€15                                           |
| Misc (enclosures, cable clips, terminals, labels)         | ~€50                                           |
| **Total materials**                                       | **~€2,585**                                    |
| **Remaining budget** (of €5,000)                          | **~€2,415** (electrician labour + contingency) |

---

## 5. Implementation Roadmap

### Phase 0 — Environment Setup (Weeks 1–2)

- Flash Raspberry Pi OS Bookworm 64-bit to microSD
- Configure SSH, headless boot, static IP
- Install Python deps: `evdev`, `pyenttec`, `pygame`
- Order all components
- Set up Git repository

### Phase 1 — Touch (Weeks 3–6)

- Mount IR frames on test bench
- Implement evdev reader for 3 frames (see c1-touch.md)
- Define zone config (zones.json)
- Validate all 25–30 zones

### Phase 2 — Lighting (Weeks 5–8, parallel with Phase 1)

- Electrician wires spotlights and dimmer rack
- Install Enttec DMX USB Pro
- Implement DMX scenes (see c2-lighting.md)
- Validate all 30 DMX channels

### Phase 3 — Projection (Weeks 7–10)

- Position and calibrate projector
- Apply rear projection film
- Build Pygame display app (see c3-projection.md)
- Prepare 30 content assets

### Phase 4 — Integration (Weeks 10–14)

- Implement coordinator state machine (see c4-coordinator.md)
- Wire all subsystems together
- Configure systemd auto-start
- Full end-to-end test on bench

### Phase 5 — On-Site Installation (Weeks 15–17)

- Execute physical installation (see c5-installation.md)
- Electrician sign-off on 230V
- On-site calibration of IR frames and projector

### Phase 6 — Validation & Handover (Weeks 18–20)

- 72-hour soak test
- Staff training
- Operator manual
- Remote access setup for developer

---

## 6. Glossary

| Term           | Definition                                                                                                                                                                              |
| -------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| evdev          | Linux kernel input event interface. Python `evdev` library reads raw input events (touch, keys) from `/dev/input/eventN` devices.                                                       |
| IR Touch Frame | A rectangular frame containing an infrared LED/photodetector grid. Any object breaking the IR beams registers as a touch. Works at the face of the frame — cannot detect through glass. |
| DMX512         | Digital Multiplex protocol for lighting control. 512 channels per universe, each 0–255. Industry standard for stage and architectural lighting.                                         |
| USB HID        | Human Interface Device — a USB device class that includes touchscreens. Plug-and-play on Linux, no special driver needed.                                                               |
| pyenttec       | Python library for controlling the Enttec DMX USB Pro dongle. Sends DMX universes over USB serial.                                                                                      |
| Pygame         | Python library for game/multimedia applications. Used here for full-screen content display on the projector.                                                                            |
| systemd        | Linux service manager. Configured to auto-start the coordinator on RPi5 boot.                                                                                                           |
| State machine  | A program pattern where the system is always in one state (STANDBY or ACTIVE) and transitions on events (touch, timeout).                                                               |
| Zone           | A software-defined rectangular region within an IR frame's coordinate space. Touching within the rectangle triggers that zone's content.                                                |
| Throw ratio    | Projector spec: distance-to-width ratio. 1.5:1 means 1.5m throw per 1m of projected image width.                                                                                        |
| GU10           | Standard twist-lock spotlight bulb fitting. Common in track and ceiling spotlights.                                                                                                     |
| XLR            | Locking 3-pin connector used for DMX signal cables.                                                                                                                                     |

---

_Plan v2.0 — 2026-04-20 | Vitrina Interativa de Minerais — Lousal_
