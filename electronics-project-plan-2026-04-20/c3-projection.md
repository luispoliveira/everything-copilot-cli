# C3 — Rear Projection System

**Challenge**: Display informational mineral content on the vitrina rear panel via a short-throw projector, switching content based on the active zone.
**Difficulty**: 🟡 Medium
**Estimated duration**: 3 weeks

---

## 1. Overview

A short-throw projector is mounted behind the vitrina, projecting onto a rear projection film applied to the interior face of the back panel. When a visitor touches zone N, the Pygame application (running on the RPi5 HDMI output) switches to display content for zone N. During standby, the screen is black.

**Why Pygame?** Pygame runs on Linux/RPi5, supports full-screen display on a secondary HDMI output, and can load and display images quickly. No browser, no network dependency.

---

## 2. Component Selection

| Component | Model | Qty | Est. Cost | Reference |
|-----------|-------|-----|-----------|-----------|
| Short-throw projector | BenQ MW560 (or Epson EB-W06) | 1 | ~€500 | [BenQ MW560](https://www.benq.com/en-us/projector/meeting-room/mw560.html) |
| Rear projection film | Self-adhesive, grey tint, 1.2m wide | TBD (measure panel) | ~€15/m² | [Pro Display](https://prodisplay.com/products/rear-projection-film/) |
| HDMI cable | 3m, standard | 1 | ~€15 | — |

**BenQ MW560 key specs**:
- 4000 ANSI lumens (adequate for museum ambient light with rear projection film)
- Throw ratio: 1.55:1 (at 1.5m throw → 0.97m wide image)
- Native WXGA (1280×800)
- HDMI input

**Projection geometry check**:
- Vitrina back panel width: ~6,950mm total (3 panels × ~2,316mm)
- If projecting across the full back: one projector cannot cover 6.95m
- **Recommended approach**: Project onto the CENTRE panel only (Pano 2), or use 3 small projectors (one per panel). Confirm this with the exhibition designer before purchasing.
- At 1.5m throw, MW560 projects ~0.97m wide. At 3m throw → ~1.93m wide.
- **For single projector covering ~2m**: position projector ~3m away from panel.

---

## 3. Rear Projection Film Application

**Steps** (done on-site with vitrina panel accessible):
1. Clean the interior glass surface with IPA (isopropyl alcohol) — must be spotless
2. Cut film to exact panel dimensions (leave 5mm overhang on each edge)
3. Spray glass surface lightly with water + 1 drop dish soap (helps reposition film)
4. Peel film backing, apply to glass slowly from one edge, use a squeegee to push out bubbles
5. Trim edges with a sharp knife
6. Allow 24 hours to cure before projecting
7. Test: project a white test pattern — film should diffuse light evenly

**Film sourcing**: Order from Pro Display (UK) or Rear Projection Film Store (EU). Specify width and whether matte or grey tint (grey tint improves contrast in ambient light).

---

## 4. Software Tasks

### S3.1 — Install Pygame and configure dual display 🟢

**What**: Install Pygame on the RPi5 and verify it can open a full-screen window on the projector (HDMI display index 1).

**Prerequisites**: RPi5 running Bookworm desktop (or Lite with Xorg). Projector connected via HDMI and powered on.

**Resources**:
- [Pygame docs](https://www.pygame.org/docs/)
- [RPi5 dual display](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#display)

**Steps**:
1. Install: `pip3 install pygame`
2. Verify dual display is active:
   ```bash
   # Check connected displays
   xrandr --listmonitors
   # Should show 2 monitors: HDMI-1 (primary) and HDMI-2 (projector)
   ```
   If RPi5 only shows one display with nothing connected to primary HDMI, the projector may become display 0. Test both index 0 and 1.
3. Test full-screen on projector:
   ```python
   import pygame
   import sys

   pygame.init()
   # Try display index 1 (projector), fallback to 0
   num_displays = pygame.display.get_num_displays()
   display_index = 1 if num_displays > 1 else 0
   print(f"Using display index {display_index} of {num_displays}")

   screen = pygame.display.set_mode((1280, 800), pygame.FULLSCREEN, display=display_index)
   screen.fill((255, 0, 0))  # red — visually confirm which display is active
   pygame.display.flip()

   pygame.time.wait(3000)
   pygame.quit()
   sys.exit()
   ```
4. Run the script. The projector should show a red screen for 3 seconds.
5. If it appears on the wrong display, change `display_index`.

**Definition of Done**: Red full-screen appears on the projector output, not on any monitor connected to the primary HDMI.

**Estimated time**: 1 hour

---

### S3.2 — Build the ProjectionDisplay class 🟡

**What**: A Python class that the coordinator uses to show mineral content or a black standby screen on the projector.

**Steps**:
1. Create `projection.py`:
   ```python
   import pygame
   import os
   import logging
   from typing import Optional

   logger = logging.getLogger(__name__)

   DISPLAY_WIDTH = 1280
   DISPLAY_HEIGHT = 800
   CONTENT_DIR = os.path.join(os.path.dirname(__file__), 'content')

   class ProjectionDisplay:
       def __init__(self, display_index: int = 1):
           pygame.init()
           num_displays = pygame.display.get_num_displays()
           if display_index >= num_displays:
               logger.warning(
                   f"Display index {display_index} not available "
                   f"({num_displays} displays). Using 0."
               )
               display_index = 0
           self.screen = pygame.display.set_mode(
               (DISPLAY_WIDTH, DISPLAY_HEIGHT),
               pygame.FULLSCREEN | pygame.NOFRAME,
               display=display_index
           )
           pygame.display.set_caption("Vitrina Lousal — Projection")
           pygame.mouse.set_visible(False)
           self._image_cache: dict = {}
           self.show_standby()
           logger.info(f"ProjectionDisplay ready on display {display_index}")

       def show_standby(self):
           """Black screen for standby state."""
           self.screen.fill((0, 0, 0))
           pygame.display.flip()
           logger.debug("Projection: standby (black)")

       def show_zone(self, zone_id: int):
           """Display content image for zone_id."""
           img = self._load_image(zone_id)
           if img:
               self.screen.blit(img, (0, 0))
           else:
               # Fallback: show zone number if image missing
               self.screen.fill((10, 10, 40))
               font = pygame.font.SysFont('sans', 120)
               text = font.render(f"Zone {zone_id}", True, (255, 255, 255))
               rect = text.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2))
               self.screen.blit(text, rect)
           pygame.display.flip()
           logger.debug(f"Projection: showing zone {zone_id}")

       def _load_image(self, zone_id: int) -> Optional[pygame.Surface]:
           if zone_id in self._image_cache:
               return self._image_cache[zone_id]
           path = os.path.join(CONTENT_DIR, f'zone_{zone_id}.jpg')
           if not os.path.exists(path):
               logger.warning(f"Content missing: {path}")
               return None
           try:
               img = pygame.image.load(path)
               img = pygame.transform.scale(img, (DISPLAY_WIDTH, DISPLAY_HEIGHT))
               self._image_cache[zone_id] = img
               logger.info(f"Image cached: zone_{zone_id}.jpg")
               return img
           except Exception as e:
               logger.error(f"Failed to load {path}: {e}")
               return None

       def preload_all(self, total_zones: int = 30):
           """Pre-load all zone images at startup to avoid delay on first touch."""
           logger.info(f"Preloading {total_zones} content images...")
           for z in range(1, total_zones + 1):
               self._load_image(z)
           logger.info("Preload complete.")

       def process_events(self) -> bool:
           """Call this in the main loop. Returns False if quit requested."""
           for event in pygame.event.get():
               if event.type == pygame.QUIT:
                   return False
               if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                   return False
           return True

       def close(self):
           pygame.quit()
   ```

2. Test manually:
   ```python
   import time
   from projection import ProjectionDisplay

   disp = ProjectionDisplay(display_index=1)
   disp.preload_all()
   for zone in range(1, 31):
       disp.show_zone(zone)
       time.sleep(0.5)
   disp.show_standby()
   time.sleep(2)
   disp.close()
   ```

**Definition of Done**: All zone images display correctly. Standby shows black. Missing image shows fallback zone number text. Switch between zones takes < 200ms after preload.

**Estimated time**: 3 hours

---

### S3.3 — Prepare 30 mineral content assets 🟢

**What**: Create 30 content images (`zone_1.jpg` through `zone_30.jpg`) in 1280×800px format, one per mineral.

**Why**: The projection system needs actual content. Even placeholder images are needed for integration testing.

**Image content guidelines** (per image):
- Mineral name (large, legible)
- Scientific name (smaller)
- 2–3 sentence description
- Origin / formation location
- A photograph or illustration of the mineral
- Consistent design language (museum branding if available)

**Steps**:
1. Create `content/` directory in the project root
2. For each of the 30 zones, create `zone_N.jpg` at 1280×800px
3. Use Canva, Adobe Express, or Figma with a consistent template
4. Export as JPEG, quality 85%, file size < 2MB each
5. Name files exactly: `zone_1.jpg`, `zone_2.jpg`, …, `zone_30.jpg`
6. Verify: `ls content/zone_*.jpg | wc -l` should print `30`

**For testing purposes**: Create placeholder images with just the zone number on a coloured background using Python:
```python
from PIL import Image, ImageDraw, ImageFont
import os

os.makedirs('content', exist_ok=True)
for i in range(1, 31):
    img = Image.new('RGB', (1280, 800), color=(20, 30, 60))
    draw = ImageDraw.Draw(img)
    draw.text((400, 300), f"Zone {i}", fill=(255,255,255))
    draw.text((400, 450), f"Mineral Name Here", fill=(180,180,180))
    img.save(f'content/zone_{i}.jpg', quality=85)
print("Placeholder images created.")
```
Install Pillow: `pip3 install Pillow`

**Definition of Done**: 30 JPEG files in `content/`, all load without error in `ProjectionDisplay.preload_all()`.

**Estimated time**: 2 hours (placeholders) + variable time for real content (up to 2 weeks with content team)

---

## 5. Projector Calibration (on-site)

Do this after applying the rear projection film:

1. Mount projector at correct distance (calculated from throw ratio and desired image size)
2. Power on, switch input to HDMI
3. Run `python3 -c "from projection import ProjectionDisplay; d=ProjectionDisplay(); d.show_zone(1)"` — displays zone 1 content
4. Adjust projector focus until image is sharp
5. Adjust keystone correction (vertical tilt) until image is rectangular
6. Adjust zoom to fit the projection area
7. Verify image is centred on the film area
8. If image is not bright enough in ambient light: check room lighting, consider blackout film on adjacent glass surfaces

---

## 6. Testing Checklist

- [ ] Pygame opens full-screen on projector (not on primary RPi5 HDMI port)
- [ ] `show_standby()` — projector shows black
- [ ] `show_zone(N)` for N=1..30 — correct image displays
- [ ] `preload_all()` — no errors, all 30 images cached
- [ ] Image switch time < 500ms (measure with stopwatch)
- [ ] Missing image fallback: rename a file, verify fallback text appears
- [ ] Projector focused and keystone-corrected on-site
- [ ] Content legible from 1m visitor distance

---

*C3 — Projection | Plan v2.0 — 2026-04-20*
