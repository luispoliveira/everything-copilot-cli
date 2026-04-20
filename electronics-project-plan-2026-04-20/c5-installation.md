# C5 — Physical Installation, 230V Safety & Handover

**Challenge**: Install all components in the final museum configuration, including safe 230V AC distribution, cable management, and staff handover.
**Difficulty**: 🔴 Advanced (230V AC — qualified electrician required)
**Estimated duration**: 2 weeks (installation week + testing week)

---

> ⚡ **DANGER: MAINS VOLTAGE (230V AC)**
>
> The developer is responsible ONLY for low-voltage components:
>
> - Raspberry Pi 5 (5V USB-C)
> - IR touch frames (5V USB)
> - Powered USB hub (12V DC, handled by its own PSU)
> - DMX XLR signal cables (5V logic level)
> - HDMI cable
>
> The following MUST be done by a **licensed electrician**:
>
> - All 230V AC wiring
> - Spotlight fixture wiring
> - Dimmer rack mains connection
> - Fused IEC inlet installation
> - Final inspection and sign-off before energizing
>
> Do NOT attempt 230V work yourself. Do NOT energize the system without electrician sign-off.

---

## 1. Physical Layout Diagram

```
VITRINA — SIDE VIEW (cross section)

        VISITOR SIDE                             REAR
        ────────────────────────────────────────────────
                                               Spotlights
        [Mineral 1] [Mineral 2] ... [Mineral N]  ↓  ↓  ↓
                                              ┌───────────┐
        ════════════════════════════════════  │  ceiling  │
        Glass panel (exterior face)           └─────┬─────┘
            │                                       │ 230V cables (electrician)
        ┌───┤ IR Frame (exterior mounted)            │
        │   │ (17mm aluminium bezel)                 ▼
        │   │                              ┌───────────────┐
        │   │                              │ DMX Dimmer    │
        │   │                              │ Rack 1+2      │
        │   │                              │ (rear of      │
        │   │                              │  vitrina)     │
        │   │                              └──────┬────────┘
        │   │                                     │ XLR (DMX signal)
        │   │                              ┌──────┴────────┐
        │   │                              │ Enttec DMX    │
        │   │                              │ USB Pro       │
        │   │                              └──────┬────────┘
        │   │                                     │ USB
        │   └───────────────────── USB cable ─────┤
        │                                         │
        │                              ┌──────────┴────────┐
        └──────────────── USB cable ───┤ Powered USB Hub   │
                                       │ (3 frames + hub)  │
                                       └──────────┬────────┘
                                                  │ USB-A
                                       ┌──────────┴────────┐
                                       │ Raspberry Pi 5    │
                                       │ (8GB)             │
                                       │ - SSH accessible  │
                                       │ - systemd service │
                                       └──────────┬────────┘
                                                  │ HDMI
                                                  ▼
                                       ┌───────────────────┐
                                       │ Short-throw       │
                                       │ Projector         │
                                       └───────────────────┘
                                                  │ Light beam
                                                  ▼
                           ═══════════════════════════════════
                           Rear projection film (back panel)
```

---

## 2. RPi5 Enclosure & Mounting

**Recommended location**: Rear of vitrina, in a ventilated ABS enclosure (220×150×100mm), accessible by museum staff via a key-locked rear panel.

**Requirements**:

- Ventilation slots or small fan (RPi5 runs warm under load)
- Access to all 4 USB-A ports (3 for hub, 1 spare) and USB-C power port
- Access to both micro-HDMI ports (one for projector, one spare for maintenance)
- Status LED visible through enclosure or via small hole
- Fixed mounting (vibration-resistant screws)

**Labelling**: Attach label to enclosure: "Raspberry Pi 5 — Vitrina Lousal. Do not disconnect. Contact: [developer name, phone]"

---

## 3. IR Frame Mounting

**Per panel (×3 frames)**:

1. Clean exterior glass surface with IPA (isopropyl alcohol), dry with lint-free cloth
2. Mark frame position: frame active area should be centred horizontally on the glass panel and at the correct height for the mineral display band
3. Apply 4× adhesive M4 threaded standoffs at frame corner positions (or use the mounting brackets supplied with the frame)
4. Allow adhesive to cure 24 hours before mounting frame
5. Mount frame to standoffs — do not overtighten (glass can crack)
6. Route USB-A cable from frame along the bottom edge of the glass, secured with adhesive cable clips every 200mm
7. Label cable at both ends: "Frame 0 – Pano 1", "Frame 1 – Pano 2", "Frame 2 – Pano 3"
8. Connect to powered USB hub

**Verification after mounting**:

```bash
# SSH into RPi5
lsusb | grep 1FF7
# Should show 3 lines — one per frame
```

---

## 4. Spotlight Installation (electrician brief)

Provide this sheet to the electrician:

```
ELECTRICIAN INSTALLATION BRIEF
Project: Vitrina Interativa de Minerais — Lousal
Date: [date]
Contact: [developer name, phone]

SCOPE:
- Install 30× GU10 recessed spotlight fixtures on vitrina interior ceiling
- Wire each fixture to a dedicated output on the DMX dimmer rack
- Wire dimmer rack mains input from building circuit (see below)

FIXTURE POSITIONS:
- Fixture N is positioned directly above Mineral Zone N
- Zones 1–10: Pano 1 ceiling (left panel)
- Zones 11–20: Pano 2 ceiling (centre panel)
- Zones 21–30: Pano 3 ceiling (right panel)
- Physical positions marked with numbered tape labels

WIRING:
- Each fixture: 1.5mm² 2-core + earth cable, brown=live, blue=neutral, green/yellow=earth
- Cable labelled at both ends with zone number (1–30)
- All cables routed inside vitrina cable trunking, not visible to visitors

DIMMER RACK:
- Rack 1 (24ch): located at rear of vitrina. Set DMX start address = 001.
  Output 1 = Zone 1, Output 2 = Zone 2, ..., Output 24 = Zone 24
- Rack 2 (8ch): daisy-chained from Rack 1. Set DMX start address = 025.
  Output 1 = Zone 25, ..., Output 6 = Zone 30. Outputs 7–8 not connected.

MAINS SUPPLY:
- Fused IEC inlet: 6A fuse (total load = 30 × 7W = 210W)
- Supply from dedicated 16A circuit breaker in building distribution board
- Circuit breaker must be accessible to museum staff (not locked)
- Label circuit breaker: "Vitrina Lousal — Iluminação"

SIGN-OFF REQUIRED:
Before system energizing, electrician must:
1. Perform insulation resistance test (all circuits)
2. Verify earth continuity on all fixtures
3. Verify correct fixture-to-dimmer-output wiring (lamp 1 responds to dimmer output 1, etc.)
4. Sign the installation sign-off sheet (provided separately)
```

---

## 5. Projector Installation

1. **Mounting**: Project from behind the vitrina onto the rear projection film. Mount projector on a stable bracket or shelf. Height: centre of lens at same height as centre of projected area.
2. **Distance**: Calculate from throw ratio (MW560 = 1.55:1). For 2m wide image → 3.1m throw. Measure vitrina depth — confirm projector fits.
3. **Cables**: HDMI cable from RPi5 to projector. Route through cable trunking. Label: "HDMI — RPi5 to Projector".
4. **Power**: 230V socket for projector (electrician installs dedicated socket at projector position)
5. **Calibration** (after film applied and projector mounted):
   - Display test pattern: `python3 -c "from projection import ProjectionDisplay; d=ProjectionDisplay(); import time; time.sleep(60)"`
   - Adjust focus, zoom, keystone
   - Verify image fills the film area and is sharp at edges

---

## 6. Cable Management

| Cable                       | Route                                           | Label              |
| --------------------------- | ----------------------------------------------- | ------------------ |
| USB-A: Frame 0 → Hub        | Along Pano 1 bottom edge, cable channel to rear | "Frame 0 – Pano 1" |
| USB-A: Frame 1 → Hub        | Along Pano 2 bottom edge, cable channel to rear | "Frame 1 – Pano 2" |
| USB-A: Frame 2 → Hub        | Along Pano 3 bottom edge, cable channel to rear | "Frame 2 – Pano 3" |
| USB-A: Hub → RPi5           | In RPi5 enclosure cable channel                 | "Hub → RPi5"       |
| USB-A: Enttec → RPi5        | Inside RPi5 enclosure                           | "DMX USB"          |
| XLR: Enttec → Dimmer Rack 1 | Cable trunking, rear vitrina                    | "DMX Signal"       |
| XLR: Rack 1 → Rack 2        | Between racks                                   | "DMX Chain"        |
| XLR: Rack 2 → Terminator    | End of chain                                    | "DMX Term."        |
| HDMI: RPi5 → Projector      | Cable trunking, along floor                     | "HDMI – Video"     |
| USB-C: PSU → RPi5           | Inside RPi5 enclosure                           | "RPi5 Power"       |

**Rules**:

- 230V cables and low-voltage cables in separate cable channels (minimum 50mm separation)
- All cable ends labelled at both ends
- No cables crossing visitor paths
- Excess cable coiled and secured with velcro tie — never wound tightly around itself

---

## 7. Pre-Opening Checklist

### Developer tasks

- [ ] RPi5 flashed with Raspberry Pi OS Bookworm 64-bit
- [ ] SSH enabled, static IP configured
- [ ] All Python deps installed (`evdev`, `pyenttec`, `pygame`, `sdnotify`)
- [ ] IR frame udev rules created and tested (`/dev/input/vitrina-frame0/1/2`)
- [ ] DMX udev rule created (`/dev/vitrina-dmx`)
- [ ] `zones.json` calibrated on-site (all 30 zones verified)
- [ ] `device_map.json` correct for this installation
- [ ] 30 content images in `content/` folder
- [ ] `coordinator.py` tested end-to-end
- [ ] `vitrina.service` systemd service enabled and auto-starts after reboot
- [ ] Log rotation configured
- [ ] Projector focused and keystone-corrected
- [ ] 72-hour soak test completed with no crashes

### Electrician tasks (sign-off required)

- [ ] 30 spotlight fixtures installed and wired to dimmer rack outputs
- [ ] Dimmer Rack 1 DMX address = 001
- [ ] Dimmer Rack 2 DMX address = 025
- [ ] XLR daisy-chain verified: Rack 1 out → Rack 2 in → terminator
- [ ] Insulation resistance test passed
- [ ] Earth continuity verified on all fixtures
- [ ] Each dimmer output verified to correct spotlight (test with DMX test script)
- [ ] Fused IEC inlet installed (6A fuse)
- [ ] Dedicated circuit breaker installed and labelled
- [ ] **SIGN-OFF FORM COMPLETED**

---

## 8. Operator Manual Summary (for museum staff)

### Normal operation

- The system starts automatically when the RPi5 is powered on
- No daily action required

### If spotlights do not respond to touch

1. Check that the RPi5 enclosure power LED is on
2. SSH or check: `sudo systemctl status vitrina.service`
3. If stopped: `sudo systemctl restart vitrina.service`
4. If still not working: call developer: [phone]

### If projector shows nothing

1. Check projector is powered on and HDMI input selected
2. Check HDMI cable connection at both ends
3. Restart the vitrina service: `sudo systemctl restart vitrina.service`

### If nothing works after power cut

1. Wait 60 seconds after power is restored — the system auto-starts
2. If still no response after 2 minutes: contact developer

### Emergency: switch off the installation

1. Press the circuit breaker labelled "Vitrina Lousal — Iluminação"
2. Power down the RPi5 safely via SSH: `sudo shutdown now`
3. Or: hold RPi5 power button 5 seconds

### Developer remote access

- Developer can access the RPi5 via SSH on the local museum network: `ssh pi@[IP]`
- Log file: `/var/log/vitrina/vitrina.log`
- Live log: `sudo journalctl -u vitrina.service -f`

---

## 9. Spare Parts to Keep On-Site

| Item                       | Qty | Reason                          |
| -------------------------- | --- | ------------------------------- |
| GU10 LED 7W 2700K dimmable | 4   | Bulb replacement                |
| USB-A cable 2m             | 2   | Replacement for IR frame cables |
| Fuse 6A T (slow-blow)      | 3   | IEC inlet fuse replacement      |
| microSD card 64GB          | 1   | RPi5 OS backup card             |

---

_C5 — Installation | Plan v2.0 — 2026-04-20_
