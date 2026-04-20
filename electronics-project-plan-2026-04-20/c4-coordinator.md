# C4 — Python State Machine & System Coordinator

**Challenge**: A Python application on the RPi5 that wires together touch detection, lighting, and projection into a unified state machine, auto-starting on boot.
**Difficulty**: 🟡 Medium
**Estimated duration**: 3 weeks

---

## 1. Overview

`coordinator.py` is the brain of the installation. It:
1. Starts `TouchReader` (reads 3 IR frames via evdev in background threads)
2. Starts `DMXController` (sends DMX scenes via pyenttec)
3. Starts `ProjectionDisplay` (Pygame full-screen on HDMI)
4. Runs a state machine: `STANDBY` ↔ `ACTIVE(zone_id)`
5. On touch → transition to ACTIVE, highlight DMX channel, show projection content
6. On 45s inactivity → transition back to STANDBY
7. Logs all events to `/var/log/vitrina/vitrina.log`
8. Runs as a `systemd` service (auto-starts on RPi5 boot)

---

## 2. Project File Structure

```
/home/pi/vitrina/
├── coordinator.py       ← main entry point
├── touch_reader.py      ← IR frame evdev reader (from C1)
├── zone_mapper.py       ← zone coordinate lookup (from C1)
├── dmx_controller.py    ← DMX scenes (from C2)
├── projection.py        ← Pygame display (from C3)
├── device_map.json      ← IR frame device paths
├── zones.json           ← zone coordinate definitions
└── content/
    ├── zone_1.jpg
    ├── zone_2.jpg
    └── ... zone_30.jpg
```

---

## 3. Software Tasks

### S4.1 — Install all Python dependencies 🟢

**What**: Install all required Python packages on the RPi5 in one step.

**Steps**:
1. SSH into RPi5
2. Run:
   ```bash
   pip3 install evdev pyenttec pygame Pillow
   ```
3. Verify:
   ```python
   python3 -c "import evdev, enttec_usb_dmx_pro, pygame; print('All imports OK')"
   ```
4. If `evdev` fails: `sudo apt install python3-evdev`
5. If `pygame` has display errors in headless mode: set env variable `SDL_VIDEODRIVER=x11` in systemd service file (see S4.3)

**Definition of Done**: All four imports succeed without errors.

**Estimated time**: 30 minutes

---

### S4.2 — Implement coordinator.py 🟡

**What**: The main application combining all subsystems into the state machine.

**Steps**:
1. Create `/home/pi/vitrina/coordinator.py`:
   ```python
   #!/usr/bin/env python3
   """
   Vitrina Interativa de Minerais — Lousal
   Main coordinator — state machine
   """
   import logging
   import os
   import sys
   import time
   import threading
   from typing import Optional

   from touch_reader import TouchReader
   from dmx_controller import DMXController
   from projection import ProjectionDisplay

   # ── Configuration ────────────────────────────────────────────────
   LOG_DIR = '/var/log/vitrina'
   LOG_FILE = os.path.join(LOG_DIR, 'vitrina.log')
   STANDBY_TIMEOUT = 45       # seconds before returning to standby
   TOTAL_ZONES = 30
   DMX_PORT = '/dev/vitrina-dmx'
   DEVICE_MAP = os.path.join(os.path.dirname(__file__), 'device_map.json')
   ZONES_CONFIG = os.path.join(os.path.dirname(__file__), 'zones.json')
   DISPLAY_INDEX = 1          # projector HDMI output index

   # ── Logging setup ────────────────────────────────────────────────
   os.makedirs(LOG_DIR, exist_ok=True)
   logging.basicConfig(
       level=logging.INFO,
       format='%(asctime)s [%(levelname)s] %(message)s',
       handlers=[
           logging.FileHandler(LOG_FILE),
           logging.StreamHandler(sys.stdout)
       ]
   )
   logger = logging.getLogger(__name__)


   class VitrinaCoordinator:
       def __init__(self):
           self._state = 'STANDBY'
           self._active_zone: Optional[int] = None
           self._timeout_timer: Optional[threading.Timer] = None
           self._lock = threading.Lock()

           logger.info("Initialising DMX controller...")
           self._dmx = DMXController(port=DMX_PORT, total_zones=TOTAL_ZONES)

           logger.info("Initialising projection display...")
           self._projection = ProjectionDisplay(display_index=DISPLAY_INDEX)

           logger.info("Preloading content assets...")
           self._projection.preload_all(TOTAL_ZONES)

           logger.info("Initialising touch reader...")
           self._touch = TouchReader(
               device_map_path=DEVICE_MAP,
               zones_path=ZONES_CONFIG,
               on_zone_touch=self._on_zone_touch
           )

       def start(self):
           logger.info("=== Vitrina Coordinator starting ===")
           self._enter_standby()
           self._touch.start()
           logger.info("System ready. Waiting for touch events.")
           try:
               # Main loop: process Pygame events to keep display responsive
               while True:
                   if not self._projection.process_events():
                       logger.info("Quit event received — shutting down.")
                       break
                   time.sleep(0.05)
           except KeyboardInterrupt:
               logger.info("KeyboardInterrupt — shutting down.")
           finally:
               self.stop()

       def stop(self):
           logger.info("=== Vitrina Coordinator stopping ===")
           self._cancel_timeout()
           self._touch.stop()
           self._enter_standby()
           self._dmx.set_blackout()
           self._projection.close()

       # ── Touch callback (called from TouchReader thread) ──────────
       def _on_zone_touch(self, zone_id: int):
           with self._lock:
               logger.info(f"Touch event: zone {zone_id} | state={self._state} | active={self._active_zone}")
               self._reset_timeout()
               if self._state == 'STANDBY' or self._active_zone != zone_id:
                   self._enter_active(zone_id)

       # ── State transitions ─────────────────────────────────────────
       def _enter_active(self, zone_id: int):
           self._state = 'ACTIVE'
           self._active_zone = zone_id
           self._dmx.set_highlight(zone_id)
           self._projection.show_zone(zone_id)
           logger.info(f"→ ACTIVE zone {zone_id}")

       def _enter_standby(self):
           self._state = 'STANDBY'
           self._active_zone = None
           self._dmx.set_standby()
           self._projection.show_standby()
           logger.info("→ STANDBY")

       # ── Timeout management ────────────────────────────────────────
       def _reset_timeout(self):
           self._cancel_timeout()
           self._timeout_timer = threading.Timer(
               STANDBY_TIMEOUT, self._timeout_callback
           )
           self._timeout_timer.daemon = True
           self._timeout_timer.start()

       def _cancel_timeout(self):
           if self._timeout_timer is not None:
               self._timeout_timer.cancel()
               self._timeout_timer = None

       def _timeout_callback(self):
           with self._lock:
               logger.info(f"Timeout after {STANDBY_TIMEOUT}s — returning to standby")
               self._enter_standby()


   if __name__ == '__main__':
       coordinator = VitrinaCoordinator()
       coordinator.start()
   ```

2. Test manually (subsystems must be working first):
   ```bash
   cd /home/pi/vitrina
   python3 coordinator.py
   ```
3. Touch zone 1 → verify spotlight 1 brightens and projection shows zone 1 content
4. Wait 45 seconds → verify standby returns
5. Touch zone 15 → verify zone 15 activates correctly
6. Touch zone 15 again → verify timer resets but no visual change
7. Touch zone 3 while zone 15 is active → verify immediate switch to zone 3

**Definition of Done**: Full end-to-end flow works for at least 5 different zones. Timeout returns to standby within ±3 seconds. Log file at `/var/log/vitrina/vitrina.log` shows all transitions.

**Estimated time**: 4 hours

---

### S4.3 — Configure systemd auto-start 🟢

**What**: Create a systemd service so coordinator.py starts automatically when the RPi5 boots, and restarts if it crashes.

**Why**: Museum staff must not manually start the software each morning. systemd handles startup, restart-on-crash, and log collection.

**Resources**:
- [systemd service files guide](https://www.freedesktop.org/software/systemd/man/systemd.service.html)
- [RPi systemd tutorial](https://www.raspberrypi.com/documentation/computers/using_linux.html#the-systemd-daemon)

**Steps**:
1. Create `/etc/systemd/system/vitrina.service`:
   ```ini
   [Unit]
   Description=Vitrina Interativa de Minerais — Lousal
   After=graphical-session.target
   Wants=graphical-session.target

   [Service]
   Type=simple
   User=pi
   WorkingDirectory=/home/pi/vitrina
   ExecStart=/usr/bin/python3 /home/pi/vitrina/coordinator.py
   Restart=on-failure
   RestartSec=10
   StandardOutput=journal
   StandardError=journal

   # Required for Pygame to access the display
   Environment=DISPLAY=:0
   Environment=XAUTHORITY=/home/pi/.Xauthority
   Environment=SDL_VIDEODRIVER=x11

   [Install]
   WantedBy=graphical-session.target
   ```

2. Enable and start the service:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable vitrina.service
   sudo systemctl start vitrina.service
   ```

3. Check status:
   ```bash
   sudo systemctl status vitrina.service
   # Should show: active (running)
   ```

4. View live logs:
   ```bash
   sudo journalctl -u vitrina.service -f
   # -f means "follow" (live tail)
   ```

5. Test restart-on-crash: kill the process manually:
   ```bash
   sudo systemctl kill vitrina.service
   # Wait 10 seconds — service should restart automatically
   sudo systemctl status vitrina.service
   ```

6. Test reboot: `sudo reboot`. After ~30 seconds, verify the service is running.

**Troubleshooting**:
- `failed to connect to display :0`: RPi5 must be booted to desktop (not console-only). Or use `After=graphical-session.target`.
- `pygame.error: No available video device`: check `DISPLAY` and `SDL_VIDEODRIVER` env variables in service file.
- Service starts but crashes: `journalctl -u vitrina.service -n 50` to see last 50 log lines.

**Definition of Done**: After `sudo reboot`, the coordinator is running within 45 seconds and touch events work normally — without any manual action.

**Estimated time**: 1.5 hours

---

### S4.4 — Add watchdog and health monitoring 🟢

**What**: Configure systemd watchdog so the coordinator notifies systemd it is healthy every 30 seconds. If it stops notifying (hung/deadlock), systemd kills and restarts it.

**Steps**:
1. Add to `[Service]` section of `vitrina.service`:
   ```ini
   WatchdogSec=60
   NotifyAccess=main
   ```
2. In `coordinator.py`, import and notify:
   ```python
   import sdnotify  # pip3 install sdnotify

   # In VitrinaCoordinator.start(), inside the main loop:
   n = sdnotify.SystemdNotifier()
   n.notify("READY=1")
   while True:
       n.notify("WATCHDOG=1")  # ping every loop iteration
       if not self._projection.process_events():
           break
       time.sleep(0.05)
   ```
3. Install: `pip3 install sdnotify`
4. Reload and restart service: `sudo systemctl daemon-reload && sudo systemctl restart vitrina.service`

**Definition of Done**: `systemctl status vitrina.service` shows `Status: watchdog`. If coordinator loop hangs (simulate with `time.sleep(90)` in loop), systemd kills and restarts within 90s.

**Estimated time**: 1 hour

---

### S4.5 — Set up log rotation 🟢

**What**: Prevent `/var/log/vitrina/vitrina.log` from growing indefinitely over months of operation.

**Steps**:
1. Create `/etc/logrotate.d/vitrina`:
   ```
   /var/log/vitrina/vitrina.log {
       daily
       rotate 30
       compress
       missingok
       notifempty
       create 0644 pi pi
   }
   ```
2. Test: `sudo logrotate -f /etc/logrotate.d/vitrina`
3. Verify old log is compressed: `ls -la /var/log/vitrina/`

**Definition of Done**: Log file is rotated daily, only 30 days kept. No disk-full risk.

**Estimated time**: 20 minutes

---

## 4. Configuration Reference

All tuneable parameters are at the top of `coordinator.py`:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `STANDBY_TIMEOUT` | 45 | Seconds before returning to standby |
| `TOTAL_ZONES` | 30 | Number of active zones |
| `DMX_PORT` | `/dev/vitrina-dmx` | Enttec device path |
| `DISPLAY_INDEX` | 1 | Pygame display index (0=primary, 1=projector) |

Zone coordinates are in `zones.json` (see c1-touch.md).
DMX levels are in `dmx_controller.py` (`STANDBY_LEVEL`, `HIGHLIGHT_LEVEL`, `DIM_LEVEL`).

---

## 5. Testing Checklist

- [ ] `python3 coordinator.py` starts without errors
- [ ] Touch zone 1: spotlight 1 at full, others dim, projection shows zone 1
- [ ] Touch zone 15: correct spotlight + projection
- [ ] Touch zone 30: correct spotlight + projection
- [ ] Wait 45s: returns to standby (all lights ambient, projection black)
- [ ] Touch same zone twice: timer resets, no visual glitch
- [ ] Touch different zone mid-interaction: immediate switch, no delay
- [ ] Kill and restart: service auto-restarts within 15 seconds
- [ ] Reboot RPi5: service running within 45 seconds, no manual action
- [ ] Log file contains all state transitions with timestamps
- [ ] 72-hour soak test: no crashes, no lockups

---

*C4 — Coordinator | Plan v2.0 — 2026-04-20*
