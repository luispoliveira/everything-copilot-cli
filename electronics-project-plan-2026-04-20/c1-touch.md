# C1 — IR Touch Frame Setup & Zone Mapping

**Challenge**: Detect which of 25–30 mineral zones a visitor touches on the vitrina front glass.
**Difficulty**: 🟡 Medium
**Estimated duration**: 4 weeks (including on-site calibration)

---

## 1. Overview

Each of the 3 glass panels has one CJTouch 84" IR touch frame mounted on its **exterior face**. Each frame connects to the Raspberry Pi 5 via USB. Python reads touch coordinates using the `evdev` library and maps them to zone numbers using a configuration file.

**Why IR frames instead of capacitive pads?**
25–30 independent zones far exceeds what capacitive touch hardware can handle (ESP32 has only 10 touch pins). An IR frame detects any touch across its entire surface — zones are defined purely in software as coordinate rectangles. One frame covers one glass panel.

**Why exterior mounting?**
IR beams travel through air. Glass blocks infrared light at the wavelengths used. The frame must be mounted on the outer face of the glass so visitors' fingers break the beams directly.

---

## 2. Hardware Specifications

### CJTouch 84" IR Touch Frame (CIP840AP-K1)

| Specification | Value |
|---------------|-------|
| Active area | 1859 × 1046 mm |
| Touch resolution | 4096 × 4096 (raw USB HID coordinates) |
| USB VID/PID | 1FF7:0013 |
| Interface | USB 2.0 Full Speed (USB-A) |
| OS support | Linux native (USB HID, no driver needed) |
| Power | 5V via USB, ~100mA per frame |
| Protection | IP64 (dust and splash resistant) |
| Bezel | 17mm aluminium (visible when mounted) |
| Price | ~€100/unit |

**3 frames required** → ~€300 total

### USB Connection

| USB Device | RPi5 Port |
|------------|-----------|
| IR Frame 0 (Pano 1) | USB-A (via powered hub) |
| IR Frame 1 (Pano 2) | USB-A (via powered hub) |
| IR Frame 2 (Pano 3) | USB-A (via powered hub) |
| Enttec DMX USB Pro | USB-A (direct RPi5 port) |

**Note**: RPi5 has 2× USB-A 3.0 + 2× USB-A 2.0 = 4 ports. 4 USB devices fit exactly, but a powered hub is strongly recommended to avoid power brownouts (each frame draws 100mA; RPi5 USB budget is 600mA total shared across all ports).

**Recommended hub**: Anker USB 3.0 7-port powered hub with 12V/3A PSU (~€35). Connect the 3 IR frames to the hub. Connect Enttec directly to RPi5.

---

## 3. Zone Layout

```
PANO 1 (Frame 0)         PANO 2 (Frame 1)         PANO 3 (Frame 2)
┌─────────────────┐      ┌─────────────────┐      ┌─────────────────┐
│                 │      │                 │      │                 │
│  [Zone 1–~10]   │      │  [Zone ~11–20]  │      │  [Zone ~21–30]  │
│                 │      │                 │      │                 │
│  Z1  Z2  Z3     │      │  Z11 Z12 Z13    │      │  Z21 Z22 Z23    │
│  Z4  Z5  Z6     │      │  Z14 Z15 Z16    │      │  Z24 Z25 Z26    │
│  Z7  Z8  Z9 Z10 │      │  Z17 Z18 Z19 Z20│      │  Z27 Z28 Z29 Z30│
│                 │      │                 │      │                 │
│  (central band) │      │  (central band) │      │  (central band) │
└─────────────────┘      └─────────────────┘      └─────────────────┘
 IR frame 1859×1046mm     IR frame 1859×1046mm     IR frame 1859×1046mm
 Coords: 0–4095 × 0–4095  Coords: 0–4095 × 0–4095  Coords: 0–4095 × 0–4095
```

**Important**: Zones are defined in the central band of each panel. The IR frame active area (1859×1046mm) is smaller than the glass panel (2316×1500mm approx.). Zones should be defined in the central region where minerals are displayed — edges of the frame have no mineral behind them.

---

## 4. Zone Configuration File

Zones are defined in `zones.json`. Each zone specifies:
- `frame`: which IR frame (0, 1, or 2)
- `x_min`, `x_max`, `y_min`, `y_max`: bounding rectangle in 4096×4096 coordinate space
- `zone_id`: the zone number (1–30)
- `label`: mineral name (for logging)

```json
{
  "zones": [
    {"zone_id": 1,  "frame": 0, "x_min": 200,  "x_max": 600,  "y_min": 1200, "y_max": 2000, "label": "Pirite"},
    {"zone_id": 2,  "frame": 0, "x_min": 700,  "x_max": 1100, "y_min": 1200, "y_max": 2000, "label": "Calcopirite"},
    {"zone_id": 3,  "frame": 0, "x_min": 1200, "x_max": 1600, "y_min": 1200, "y_max": 2000, "label": "Esfalerite"},
    {"zone_id": 4,  "frame": 0, "x_min": 1700, "x_max": 2100, "y_min": 1200, "y_max": 2000, "label": "Galena"},
    {"zone_id": 5,  "frame": 0, "x_min": 2200, "x_max": 2600, "y_min": 1200, "y_max": 2000, "label": "Siderite"},
    {"zone_id": 6,  "frame": 0, "x_min": 2700, "x_max": 3100, "y_min": 1200, "y_max": 2000, "label": "Goethite"},
    {"zone_id": 7,  "frame": 0, "x_min": 3200, "x_max": 3600, "y_min": 1200, "y_max": 2000, "label": "Magnetite"},
    {"zone_id": 8,  "frame": 0, "x_min": 200,  "x_max": 600,  "y_min": 2200, "y_max": 3000, "label": "Limonite"},
    {"zone_id": 9,  "frame": 0, "x_min": 700,  "x_max": 1100, "y_min": 2200, "y_max": 3000, "label": "Barite"},
    {"zone_id": 10, "frame": 0, "x_min": 1200, "x_max": 1600, "y_min": 2200, "y_max": 3000, "label": "Calcite"},
    {"zone_id": 11, "frame": 1, "x_min": 200,  "x_max": 600,  "y_min": 1200, "y_max": 2000, "label": "Mineral 11"},
    {"zone_id": 12, "frame": 1, "x_min": 700,  "x_max": 1100, "y_min": 1200, "y_max": 2000, "label": "Mineral 12"},
    {"zone_id": 13, "frame": 1, "x_min": 1200, "x_max": 1600, "y_min": 1200, "y_max": 2000, "label": "Mineral 13"},
    {"zone_id": 14, "frame": 1, "x_min": 1700, "x_max": 2100, "y_min": 1200, "y_max": 2000, "label": "Mineral 14"},
    {"zone_id": 15, "frame": 1, "x_min": 2200, "x_max": 2600, "y_min": 1200, "y_max": 2000, "label": "Mineral 15"},
    {"zone_id": 16, "frame": 1, "x_min": 2700, "x_max": 3100, "y_min": 1200, "y_max": 2000, "label": "Mineral 16"},
    {"zone_id": 17, "frame": 1, "x_min": 3200, "x_max": 3600, "y_min": 1200, "y_max": 2000, "label": "Mineral 17"},
    {"zone_id": 18, "frame": 1, "x_min": 200,  "x_max": 600,  "y_min": 2200, "y_max": 3000, "label": "Mineral 18"},
    {"zone_id": 19, "frame": 1, "x_min": 700,  "x_max": 1100, "y_min": 2200, "y_max": 3000, "label": "Mineral 19"},
    {"zone_id": 20, "frame": 1, "x_min": 1200, "x_max": 1600, "y_min": 2200, "y_max": 3000, "label": "Mineral 20"},
    {"zone_id": 21, "frame": 2, "x_min": 200,  "x_max": 600,  "y_min": 1200, "y_max": 2000, "label": "Mineral 21"},
    {"zone_id": 22, "frame": 2, "x_min": 700,  "x_max": 1100, "y_min": 1200, "y_max": 2000, "label": "Mineral 22"},
    {"zone_id": 23, "frame": 2, "x_min": 1200, "x_max": 1600, "y_min": 1200, "y_max": 2000, "label": "Mineral 23"},
    {"zone_id": 24, "frame": 2, "x_min": 1700, "x_max": 2100, "y_min": 1200, "y_max": 2000, "label": "Mineral 24"},
    {"zone_id": 25, "frame": 2, "x_min": 2200, "x_max": 2600, "y_min": 1200, "y_max": 2000, "label": "Mineral 25"},
    {"zone_id": 26, "frame": 2, "x_min": 2700, "x_max": 3100, "y_min": 1200, "y_max": 2000, "label": "Mineral 26"},
    {"zone_id": 27, "frame": 2, "x_min": 3200, "x_max": 3600, "y_min": 1200, "y_max": 2000, "label": "Mineral 27"},
    {"zone_id": 28, "frame": 2, "x_min": 200,  "x_max": 600,  "y_min": 2200, "y_max": 3000, "label": "Mineral 28"},
    {"zone_id": 29, "frame": 2, "x_min": 700,  "x_max": 1100, "y_min": 2200, "y_max": 3000, "label": "Mineral 29"},
    {"zone_id": 30, "frame": 2, "x_min": 1200, "x_max": 1600, "y_min": 2200, "y_max": 3000, "label": "Mineral 30"}
  ]
}
```

> **Note**: The coordinate values above are illustrative placeholders. **You must calibrate real coordinates on-site** (see Task F1.3). The coordinate space is 0–4095 on both axes regardless of physical panel size.

---

## 5. Software Tasks

### F1.1 — Install evdev and identify IR frame devices 🟢

**What**: Install the `evdev` Python library and identify which `/dev/input/eventN` device corresponds to each IR frame.

**Why**: Linux sees each IR frame as a separate input device. Before reading touch coordinates, you need to know which device file belongs to which panel.

**Prerequisites**: RPi5 running Raspberry Pi OS Bookworm. SSH access. Basic Python knowledge.

**Resources**:
- [evdev documentation](https://python-evdev.readthedocs.io/en/latest/)
- [Linux input subsystem](https://www.kernel.org/doc/html/latest/input/input.html)

**Steps**:
1. SSH into the RPi5
2. Install evdev: `pip3 install evdev`
3. Plug in one IR frame at a time. After plugging in, run:
   ```bash
   python3 -c "import evdev; [print(d.path, d.name) for d in [evdev.InputDevice(p) for p in evdev.list_devices()]]"
   ```
4. You will see an entry like: `/dev/input/event3  USB USB TouchController`
5. Plug in all 3 frames and run the command again. Note which `/dev/input/eventN` matches each frame (they will appear in plug-in order)
6. Verify a frame is working:
   ```python
   import evdev
   dev = evdev.InputDevice('/dev/input/event3')  # adjust number
   for event in dev.read_loop():
       if event.type == evdev.ecodes.EV_ABS:
           print(event)
   ```
   Touch the frame — you should see ABS_X and ABS_Y events printing.
7. Create `device_map.json` to record your device assignments:
   ```json
   {
     "frame_0": "/dev/input/event3",
     "frame_1": "/dev/input/event4",
     "frame_2": "/dev/input/event5"
   }
   ```

**Troubleshooting**:
- If no events appear: check `lsusb` — look for VID 1FF7. If not listed, try a different USB cable.
- If device path changes after reboot: use udev rules to fix paths (see F1.5).

**Definition of Done**: All 3 frames appear in `evdev.list_devices()`. Touching each frame prints ABS_X/ABS_Y events. `device_map.json` created with correct paths.

**Estimated time**: 1 hour

---

### F1.2 — Read raw touch coordinates from all 3 frames 🟢

**What**: Write a Python script that reads touch events simultaneously from all 3 IR frames and prints (frame_index, x, y) for every touch.

**Why**: You need to understand the raw coordinate system before defining zone rectangles. Also validates that all 3 frames report coordinates correctly.

**Steps**:
1. Create `touch_reader_test.py`:
   ```python
   import evdev
   import threading
   import json

   with open('device_map.json') as f:
       device_map = json.load(f)

   def read_frame(frame_index, device_path):
       dev = evdev.InputDevice(device_path)
       print(f"Listening on Frame {frame_index}: {device_path} ({dev.name})")
       x, y = 0, 0
       for event in dev.read_loop():
           if event.type == evdev.ecodes.EV_ABS:
               if event.code == evdev.ecodes.ABS_X:
                   x = event.value
               elif event.code == evdev.ecodes.ABS_Y:
                   y = event.value
               elif event.code == evdev.ecodes.ABS_MT_POSITION_X:
                   x = event.value
               elif event.code == evdev.ecodes.ABS_MT_POSITION_Y:
                   y = event.value
           elif event.type == evdev.ecodes.EV_SYN:
               print(f"Frame {frame_index}: x={x:4d}  y={y:4d}")

   threads = []
   for i, (key, path) in enumerate(device_map.items()):
       t = threading.Thread(target=read_frame, args=(i, path), daemon=True)
       t.start()
       threads.append(t)

   for t in threads:
       t.join()
   ```
2. Run: `python3 touch_reader_test.py`
3. Touch each corner of each frame — record the min/max X and Y values you observe
4. Expected: coordinates range 0–4095 on both axes
5. Record observations: what is the X value at the left edge? Right edge? Top? Bottom?

**Definition of Done**: All 3 frames print (frame, x, y) when touched simultaneously. You have recorded approximate min/max coordinate ranges for each frame.

**Estimated time**: 1 hour

---

### F1.3 — Define zones and implement zone mapper 🟡

**What**: Write a Python class that takes (frame_index, x, y) and returns the zone number (1–30) or `None` if outside all zones.

**Why**: This is the core logic of the touch subsystem. Every subsequent system depends on knowing which zone was touched.

**Steps**:
1. Update `zones.json` with correct coordinates from F1.2 measurements. To find zone boundaries:
   - Touch the top-left corner of each mineral specimen's expected touch area on the glass → record (frame, x, y)
   - Touch the bottom-right corner → record (frame, x, y)
   - Use these as `x_min`, `y_min`, `x_max`, `y_max` for that zone
   - Add 100 units of margin on each side to make zones easier to hit

2. Create `zone_mapper.py`:
   ```python
   import json
   from typing import Optional

   class ZoneMapper:
       def __init__(self, config_path: str = 'zones.json'):
           with open(config_path) as f:
               data = json.load(f)
           self.zones = data['zones']

       def get_zone(self, frame: int, x: int, y: int) -> Optional[int]:
           """
           Returns zone_id if (frame, x, y) falls within a defined zone.
           Returns None if touch is outside all zones.
           """
           for zone in self.zones:
               if (zone['frame'] == frame and
                   zone['x_min'] <= x <= zone['x_max'] and
                   zone['y_min'] <= y <= zone['y_max']):
                   return zone['zone_id']
           return None

       def get_label(self, zone_id: int) -> str:
           for zone in self.zones:
               if zone['zone_id'] == zone_id:
                   return zone.get('label', f'Zone {zone_id}')
           return f'Zone {zone_id}'
   ```

3. Test the mapper with a quick script:
   ```python
   from zone_mapper import ZoneMapper
   mapper = ZoneMapper()
   # Simulate a touch in zone 1's area
   zone = mapper.get_zone(frame=0, x=400, y=1600)
   print(f"Zone: {zone}")  # should print 1
   # Outside all zones
   zone = mapper.get_zone(frame=0, x=10, y=10)
   print(f"Zone: {zone}")  # should print None
   ```

4. Walk through each zone physically (touch the glass at each mineral location) and verify correct zone is returned.

**Definition of Done**: `ZoneMapper.get_zone()` returns correct zone IDs for test coordinates. All 30 zones verified by physical touch on bench or on-site.

**Estimated time**: 3 hours (plus on-site calibration time)

---

### F1.4 — Implement the TouchReader class 🟡

**What**: A Python class that reads from all 3 IR frames in background threads and calls a callback function whenever a valid zone touch is detected.

**Why**: The coordinator needs to be notified of touches without blocking. Background threads handle each frame independently.

**Steps**:
1. Create `touch_reader.py`:
   ```python
   import evdev
   import threading
   import json
   import logging
   from typing import Callable, Optional
   from zone_mapper import ZoneMapper

   logger = logging.getLogger(__name__)

   class TouchReader:
       def __init__(self, device_map_path: str, zones_path: str,
                    on_zone_touch: Callable[[int], None]):
           with open(device_map_path) as f:
               self.device_map = json.load(f)
           self.mapper = ZoneMapper(zones_path)
           self.on_zone_touch = on_zone_touch
           self._threads = []
           self._running = False

       def start(self):
           self._running = True
           for i, (key, path) in enumerate(self.device_map.items()):
               t = threading.Thread(
                   target=self._read_frame,
                   args=(i, path),
                   daemon=True,
                   name=f'touch-frame-{i}'
               )
               t.start()
               self._threads.append(t)
           logger.info(f"TouchReader started: {len(self._threads)} frames")

       def stop(self):
           self._running = False

       def _read_frame(self, frame_index: int, device_path: str):
           try:
               dev = evdev.InputDevice(device_path)
               logger.info(f"Frame {frame_index} opened: {dev.name}")
               x, y = 0, 0
               last_zone: Optional[int] = None
               for event in dev.read_loop():
                   if not self._running:
                       break
                   if event.type == evdev.ecodes.EV_ABS:
                       if event.code in (evdev.ecodes.ABS_X, evdev.ecodes.ABS_MT_POSITION_X):
                           x = event.value
                       elif event.code in (evdev.ecodes.ABS_Y, evdev.ecodes.ABS_MT_POSITION_Y):
                           y = event.value
                   elif event.type == evdev.ecodes.EV_SYN:
                       zone = self.mapper.get_zone(frame_index, x, y)
                       if zone is not None and zone != last_zone:
                           last_zone = zone
                           label = self.mapper.get_label(zone)
                           logger.info(f"Touch: Frame {frame_index} ({x},{y}) → Zone {zone} ({label})")
                           self.on_zone_touch(zone)
                   elif event.type == evdev.ecodes.EV_KEY:
                       # Touch released (BTN_TOUCH = 0)
                       if event.code == evdev.ecodes.BTN_TOUCH and event.value == 0:
                           last_zone = None
           except OSError as e:
               logger.error(f"Frame {frame_index} read error: {e}")
   ```

2. Test with a standalone script:
   ```python
   import logging
   logging.basicConfig(level=logging.INFO)
   from touch_reader import TouchReader

   def on_touch(zone_id):
       print(f">>> ZONE {zone_id} TOUCHED")

   reader = TouchReader('device_map.json', 'zones.json', on_touch)
   reader.start()
   input("Press Enter to quit\n")
   reader.stop()
   ```

3. Touch each zone — verify correct zone ID is printed.

**Definition of Done**: All 30 zones trigger the callback with the correct zone ID. Multiple frames can be touched simultaneously without errors. No crash after 30 minutes of testing.

**Estimated time**: 3 hours

---

### F1.5 — Fix device paths with udev rules 🟢

**What**: Create udev rules so that each IR frame always gets the same `/dev/input/` path after a reboot, regardless of plug-in order.

**Why**: Linux assigns `/dev/input/eventN` numbers based on plug-in order. After a reboot, the numbers can change. This would break `device_map.json`. udev rules fix paths based on USB VID/PID and port.

**Steps**:
1. Identify USB port for each frame:
   ```bash
   udevadm info --attribute-walk /dev/input/event3 | grep -E 'idVendor|idProduct|KERNELS'
   ```
2. Create `/etc/udev/rules.d/99-vitrina-touch.rules`:
   ```
   # CJTouch IR Frame — assign stable symlinks based on USB physical port
   SUBSYSTEM=="input", ATTRS{idVendor}=="1ff7", ATTRS{idProduct}=="0013", \
     KERNELS=="1-1.1", SYMLINK+="input/vitrina-frame0"
   SUBSYSTEM=="input", ATTRS{idVendor}=="1ff7", ATTRS{idProduct}=="0013", \
     KERNELS=="1-1.2", SYMLINK+="input/vitrina-frame1"
   SUBSYSTEM=="input", ATTRS{idVendor}=="1ff7", ATTRS{idProduct}=="0013", \
     KERNELS=="1-1.3", SYMLINK+="input/vitrina-frame2"
   ```
   (Replace `1-1.1` etc. with actual USB port addresses from step 1)
3. Reload rules: `sudo udevadm control --reload-rules && sudo udevadm trigger`
4. Update `device_map.json` to use the stable paths:
   ```json
   {
     "frame_0": "/dev/input/vitrina-frame0",
     "frame_1": "/dev/input/vitrina-frame1",
     "frame_2": "/dev/input/vitrina-frame2"
   }
   ```
5. Reboot and verify: `ls -la /dev/input/vitrina-frame*`

**Definition of Done**: After reboot, `/dev/input/vitrina-frame0/1/2` exist and each points to the correct frame. TouchReader works immediately without reconfiguration.

**Estimated time**: 1.5 hours

---

## 6. Physical Mounting

**IR frame must be on the EXTERIOR face of each glass panel.**

Mounting options:
1. **Adhesive standoffs**: Apply 4 × M4 threaded standoffs to the glass using epoxy adhesive. Frame bolts onto standoffs. Leaves 5mm gap between frame and glass (acceptable — IR beams still detect touch at the glass surface).
2. **Channel extrusion**: Fabricate a thin aluminium channel around the glass perimeter. Frame slides into channel. Cleanest look, easier to service.
3. **Double-sided tape (temporary)**: Use VHB tape for initial testing only. Not suitable for permanent installation.

**Cable routing**:
- USB-A cables run from each frame down the back of the vitrina to the powered hub
- Hub connects to RPi5 via USB-A 3.0
- Use cable management clips to route cables neatly along the frame edge
- Label each USB cable: "Frame 0 – Pano 1", "Frame 1 – Pano 2", "Frame 2 – Pano 3"

---

## 7. Testing Checklist

- [ ] All 3 frames appear in `evdev.list_devices()` simultaneously
- [ ] Raw coordinates print correctly for all 3 frames (F1.2)
- [ ] Zone mapper returns correct zone for test coordinates (F1.3)
- [ ] All 30 zones trigger callback when physically touched (F1.4)
- [ ] No zone triggers when touching outside defined rectangles
- [ ] No false triggers after 10 minutes idle
- [ ] Device paths survive reboot (F1.5)
- [ ] 2 frames touched simultaneously: both zones reported independently

---

*C1 — Touch | Plan v2.0 — 2026-04-20*
