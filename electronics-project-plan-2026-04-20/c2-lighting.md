# C2 — DMX Lighting Control (25–30 Spotlights)

**Challenge**: Control 25–30 individual dimmable spotlights inside the vitrina, one per mineral zone, via DMX512 from the Raspberry Pi 5.
**Difficulty**: 🔴 Advanced (involves 230V AC — qualified electrician required for mains wiring)
**Estimated duration**: 3 weeks

---

> ⚡ **DANGER: MAINS VOLTAGE (230V AC)**
>
> This section involves work with mains electricity (230V AC in Europe).
> **Risk of LETHAL electric shock.**
>
> Mandatory precautions:
> - ALWAYS disconnect mains power before touching any wiring inside the vitrina
> - All 230V AC wiring MUST be performed or verified by a **licensed electrician**
> - Keep low-voltage components (RPi5, DMX signal cable) physically separated from 230V wiring
> - Use minimum 1.5mm² wire cross-section for all 230V circuits
> - Install a fused IEC inlet rated for total load (30 × 7W = 210W — use 6A fuse minimum)
> - The developer only works with: RPi5 (5V), USB cables, and DMX XLR signal cables
> - Never work alone on energized circuits
> - Have 230V wiring inspected before energizing for the first time

---

## 1. Overview

Each of the 25–30 mineral zones has a dedicated GU10 spotlight mounted on the vitrina ceiling directly above it. Spotlights are connected to a 32-channel DMX-controlled dimmer rack. The RPi5 sends DMX commands via the Enttec DMX USB Pro USB dongle.

**1:1 mapping rule**: Zone N → DMX channel N → Spotlight N. No exceptions.

| Zone touched | DMX channel N | Action |
|---|---|---|
| Zone 5 touched | CH 5 = 255 | Spotlight 5 at full, all others dimmed |
| Standby | CH 1–30 = 160 | All at 63% ambient |
| Timeout | CH 1–30 = 160 | Return to ambient |

---

## 2. Component Selection

| Component | Model | Qty | Est. Cost | Reference | Notes |
|-----------|-------|-----|-----------|-----------|-------|
| DMX USB Interface | Enttec DMX USB Pro (SKU 70304) | 1 | ~€90 | [enttec.com](https://www.enttec.com/product/controls/dmx-usb-interfaces/dmx-usb-pro/) | USB→DMX512 bridge |
| DMX Dimmer Rack | Showtec DimRack 24 (24ch) | 1 | ~€450 | [highlite.com](https://www.highlite.com) | 24 × 230V dimmer channels |
| DMX Dimmer Pack (ext.) | Showtec Multidim MK3 8ch or 2nd rack | 1 | ~€200 | — | Covers zones 25–30 |
| GU10 LED Bulb | Philips 7W 2700K dimmable | 32 (2 spare) | ~€5 | — | Warm white, dimmable |
| GU10 Spotlight Fixture | Recessed/surface mount | 30 | ~€15 | — | Ceiling mount inside vitrina |
| DMX XLR cable 3-pin | 2m and 5m lengths | 4 | ~€8 | [thomann.de](https://www.thomann.de) | Signal chain |
| DMX terminator | 3-pin XLR 120Ω | 1 | ~€5 | — | End of DMX chain |
| Fused IEC inlet | 6A fused, panel mount | 1 | ~€8 | — | Mains input for dimmer rack |

**Total C2 estimated cost: ~€900–1,100** (before electrician labour)

**Why Showtec DimRack 24 instead of dimmer packs?**
- A rack-mount dimmer is designed for permanent installation, more reliable than portable dimmer packs
- 24 channels in one unit, DIN-rail or rack mountable
- If 25–30 zones, add a second 8-ch or 12-ch unit daisy-chained on the same DMX line

**Alternative if DimRack 24 is unavailable**: 2× Showtec Multidim MK3 16ch packs daisy-chained.

---

## 3. DMX Channel Mapping

**Rule**: Zone N = DMX channel N. Always.

| Zone | Mineral | DMX Channel | Spotlight position |
|------|---------|-------------|-------------------|
| 1 | Pirite | CH 1 | Pano 1, position 1 |
| 2 | Calcopirite | CH 2 | Pano 1, position 2 |
| … | … | … | … |
| 10 | Calcite | CH 10 | Pano 1, position 10 |
| 11 | Mineral 11 | CH 11 | Pano 2, position 1 |
| … | … | … | … |
| 20 | Mineral 20 | CH 20 | Pano 2, position 10 |
| 21 | Mineral 21 | CH 21 | Pano 3, position 1 |
| … | … | … | … |
| 30 | Mineral 30 | CH 30 | Pano 3, position 10 |

**DMX dimmer rack address configuration**:
- Rack/Pack 1: set starting address to **001** via rotary or DIP switches (covers CH 1–24)
- Rack/Pack 2: set starting address to **025** (covers CH 25–30, channels 31–32 unused)
- Daisy-chain: XLR output of Rack 1 → XLR input of Rack 2 → DMX terminator on Rack 2 output

---

## 4. Signal Path (developer-safe, low voltage)

```
RPi5 USB-A port
    │
    ▼
Enttec DMX USB Pro
(USB → RS-485 / DMX512)
    │ XLR 3-pin (signal only, 5V logic)
    ▼
Rack 1 DMX IN
(Showtec DimRack 24, channels 1–24)
    │ XLR 3-pin (daisy-chain)
    ▼
Rack 2 DMX IN
(8–12ch dimmer, channels 25–30)
    │ XLR 3-pin
    ▼
DMX Terminator (120Ω)
```

The developer only handles the USB cable and XLR cables above. Everything below the dimmer rack outputs is 230V AC and is handled exclusively by the electrician.

---

## 5. Power Path (⚡ 230V AC — electrician only)

```
Building mains supply (230V AC, ≥16A circuit)
    │
    ▼
Fused IEC inlet (6A fuse for 210W total load)
    │
    ▼
Dimmer Rack 1 mains input
    ├─ Output CH 1  → Spotlight 1 (GU10 fixture)
    ├─ Output CH 2  → Spotlight 2
    ├─ …
    └─ Output CH 24 → Spotlight 24
    │
    ▼
Dimmer Rack 2 mains input (daisy-chain from Rack 1 mains)
    ├─ Output CH 25 → Spotlight 25
    ├─ …
    └─ Output CH 30 → Spotlight 30
```

**Cable sizing** (for electrician reference):
- Mains feed to dimmer rack: 2.5mm² cable, 16A breaker
- Spotlight feeds (7W each): 1.5mm² cable, adequate for all loads on this circuit

---

## 6. Software Tasks

### S2.1 — Install pyenttec and test DMX output 🟢

**What**: Install the Python library for the Enttec DMX USB Pro and send test values to confirm spotlights respond.

**Prerequisites**: RPi5 with Raspberry Pi OS. Enttec device connected via USB. Dimmer rack powered and DMX addresses set correctly.

**Resources**:
- [pyenttec on PyPI](https://pypi.org/project/pyenttec/)
- [Enttec DMX USB Pro Manual](https://www.enttec.com/product/controls/dmx-usb-interfaces/dmx-usb-pro/)

**Steps**:
1. Install: `pip3 install pyenttec`
2. Find the serial port:
   ```bash
   ls /dev/ttyUSB*   # should show /dev/ttyUSB0 when Enttec is connected
   # or
   ls /dev/serial/by-id/  # shows stable path by USB serial number
   ```
3. Test script — fade all channels 1–30 from off to full:
   ```python
   import enttec_usb_dmx_pro as enttec
   import time

   dmx = enttec.EnttecDMXUSBPro('/dev/ttyUSB0')  # adjust if needed

   print("Fading all 30 channels to full...")
   for value in range(0, 256, 5):
       universe = [0] * 513  # index 0 unused, channels 1-512
       for ch in range(1, 31):
           universe[ch] = value
       dmx.send_dmx(universe)
       time.sleep(0.03)

   print("Testing individual channels...")
   for zone in range(1, 31):
       universe = [0] * 513
       universe[zone] = 255
       dmx.send_dmx(universe)
       print(f"  Zone {zone} at full (all others off)")
       time.sleep(0.5)

   # Return to standby
   universe = [0] * 513
   for ch in range(1, 31):
       universe[ch] = 160
   dmx.send_dmx(universe)
   print("Standby scene set.")
   ```
4. Observe: each spotlight should light up in sequence

**Troubleshooting**:
- `No such file /dev/ttyUSB0`: check `lsusb` for FTDI device (Enttec uses FTDI chip). Install driver: `sudo apt install libftdi1`
- Spotlights don't respond: check DMX address on dimmer rack matches channel number. Check XLR cable is wired pin 2 = hot, pin 3 = cold, pin 1 = shield.
- Some channels work, others don't: check daisy-chain XLR between racks. Check DMX terminator is installed.

**Definition of Done**: Each of the 30 spotlights responds individually to DMX commands. Fade animation is visually smooth.

**Estimated time**: 2 hours

---

### S2.2 — Implement DMXController class with lighting scenes 🟡

**What**: Create a Python class encapsulating all lighting scenes needed by the coordinator.

**Why**: Isolating lighting logic into a class makes the coordinator cleaner and allows independent testing.

**Steps**:
1. Create `dmx_controller.py`:
   ```python
   import enttec_usb_dmx_pro as enttec
   import logging
   import time
   from typing import Optional

   logger = logging.getLogger(__name__)

   TOTAL_ZONES = 30
   STANDBY_LEVEL = 160   # ~63% — soft ambient
   HIGHLIGHT_LEVEL = 255  # 100% — active zone
   DIM_LEVEL = 40         # ~16% — inactive zones during highlight
   TRANSITION_STEPS = 20
   TRANSITION_DELAY = 0.04  # 0.8 second total fade

   class DMXController:
       def __init__(self, port: str = '/dev/ttyUSB0', total_zones: int = TOTAL_ZONES):
           self.port = port
           self.total_zones = total_zones
           self._dmx: Optional[enttec.EnttecDMXUSBPro] = None
           self._current_universe = [0] * 513
           self._connect()

       def _connect(self):
           try:
               self._dmx = enttec.EnttecDMXUSBPro(self.port)
               logger.info(f"DMX connected: {self.port}")
           except Exception as e:
               logger.error(f"DMX connection failed: {e}")
               self._dmx = None

       def _send(self, universe: list):
           if self._dmx is None:
               self._connect()
           if self._dmx:
               try:
                   self._dmx.send_dmx(universe)
                   self._current_universe = universe[:]
               except Exception as e:
                   logger.error(f"DMX send error: {e}")
                   self._dmx = None

       def set_standby(self):
           """All zones at ambient level."""
           universe = [0] * 513
           for ch in range(1, self.total_zones + 1):
               universe[ch] = STANDBY_LEVEL
           self._send(universe)
           logger.debug("DMX: standby scene")

       def set_highlight(self, zone: int):
           """Zone N at full brightness, all others dimmed."""
           if not (1 <= zone <= self.total_zones):
               logger.warning(f"Invalid zone: {zone}")
               return
           universe = [0] * 513
           for ch in range(1, self.total_zones + 1):
               universe[ch] = DIM_LEVEL
           universe[zone] = HIGHLIGHT_LEVEL
           self._send(universe)
           logger.debug(f"DMX: highlight zone {zone}")

       def set_blackout(self):
           """All channels off. Use for shutdown."""
           universe = [0] * 513
           self._send(universe)
           logger.debug("DMX: blackout")

       def is_connected(self) -> bool:
           return self._dmx is not None
   ```

2. Test each method manually:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   from dmx_controller import DMXController
   import time

   dmx = DMXController('/dev/ttyUSB0')
   dmx.set_standby()
   time.sleep(2)
   for zone in range(1, 31):
       dmx.set_highlight(zone)
       time.sleep(0.3)
   dmx.set_standby()
   ```

**Definition of Done**: `set_standby()` — all 30 at medium. `set_highlight(N)` — zone N bright, others dim. No crashes over 30-minute test.

**Estimated time**: 2 hours

---

### S2.3 — Fix DMX device path with udev rule 🟢

**What**: Create a udev rule so the Enttec DMX USB Pro always appears as `/dev/vitrina-dmx` after reboot.

**Steps**:
1. Find Enttec USB serial: `udevadm info /dev/ttyUSB0 | grep SERIAL`
2. Add to `/etc/udev/rules.d/99-vitrina-touch.rules` (same file as IR frame rules):
   ```
   # Enttec DMX USB Pro
   SUBSYSTEM=="tty", ATTRS{idVendor}=="0403", ATTRS{idProduct}=="6001", \
     ATTRS{serial}=="YOUR_SERIAL_HERE", SYMLINK+="vitrina-dmx"
   ```
3. Reload: `sudo udevadm control --reload-rules && sudo udevadm trigger`
4. Update `DMXController` to use `/dev/vitrina-dmx`

**Definition of Done**: `/dev/vitrina-dmx` exists and works after reboot.

**Estimated time**: 30 minutes

---

## 7. Spotlight Physical Installation (electrician brief)

The developer should provide this information to the electrician:

- 30× GU10 spotlight fixtures, mounted on vitrina interior ceiling
- Each fixture powered from a dedicated output on the DMX dimmer rack
- Fixtures labelled 1–30, corresponding to DMX channels 1–30
- All fixtures use 2700K warm white dimmable GU10 LED bulbs (7W each)
- Total load: 30 × 7W = 210W (well within a 6A/1380W circuit)
- Dimmer rack: set rack 1 start address = 001, rack 2 start address = 025
- Both racks in the same physical enclosure/location, accessible for maintenance
- Spotlight cables run inside vitrina via cable trunking, not visible to visitors
- Label each spotlight cable at both ends with zone number

---

## 8. Testing Checklist

- [ ] Enttec DMX USB Pro appears as `/dev/vitrina-dmx` after reboot
- [ ] `DMXController._connect()` succeeds without error
- [ ] `set_standby()`: all 30 spotlights at visible ambient level (~60%)
- [ ] `set_highlight(N)` for N=1..30: correct spotlight at full, others dimmed (test all 30)
- [ ] `set_blackout()`: all off
- [ ] No DMX flicker on long run (30 min at standby)
- [ ] DMX auto-reconnects if USB unplugged and replugged
- [ ] Electrician sign-off form completed before 230V energized

---

*C2 — Lighting | Plan v2.0 — 2026-04-20*
