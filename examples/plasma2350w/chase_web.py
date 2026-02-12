"""
Plasma Chase — LED chase animation with WiFi web control.

For Pimoroni Plasma 2350W + WS2812 (NeoPixel) LED strip.
A single LED chases around the strip with a fading trail.
Speed, colour, and paint mode are controllable from a web browser
or via the onboard Button A.

Upload this file alongside secrets.py to the board and run it,
or save a main.py that does ``import chase_web``.
"""

import time
import plasma
import network
import uasyncio
from machine import Pin, PWM

# ─── Configuration ────────────────────────────────────────────────────────────

NUM_LEDS        = 60
TRAIL_LENGTH    = 4       # fading trail behind the chaser head
DEFAULT_SPEED   = 25      # 0 = paused, 1‑100
ONBOARD_DIM     = 0.15    # onboard LED default brightness (0‑1)
PAINT_DIM       = 0.4     # painted LEDs shown at 40 %
TRAFFIC_MS      = 800     # how long the onboard LED flickers after a request
LONG_PRESS_MS   = 600
DOUBLE_PRESS_MS = 300

SWATCHES = [
    "ff0000", "ff8800", "ffff00", "00ff00", "00ffff", "0000ff",
    "8800ff", "ff00ff", "ff1493", "ffffff", "ffaa55", "88ff00",
]

# Pre‑compute squared fade factors for the trail (avoids per‑frame math)
_TRAIL_FADES = tuple(
    ((1.0 - t / (TRAIL_LENGTH + 1)) ** 2) for t in range(1, TRAIL_LENGTH + 1)
)

COLOR_SEQUENCE = [
    (255,   0,   0), (255, 136,   0), (255, 255,   0),
    (0,   255,   0), (0,   255, 255), (0,     0, 255),
    (136,   0, 255), (255,   0, 255), (255,  20, 147),
    (255, 255, 255),
]


# ─── Onboard RGB LED ─────────────────────────────────────────────────────────

class OnboardLED:
    """PWM driver for the Plasma 2350W active‑low RGB LED (GPIOs 16‑18)."""

    _MAX = 65535

    def __init__(self):
        self._r = PWM(Pin(16), freq=1000, duty_u16=self._MAX)
        self._g = PWM(Pin(17), freq=1000, duty_u16=self._MAX)
        self._b = PWM(Pin(18), freq=1000, duty_u16=self._MAX)
        self._traffic_until = 0

    def set(self, r, g, b, brightness=ONBOARD_DIM):
        """Display *r, g, b* (0‑255) scaled by *brightness* (0‑1)."""
        scale = brightness * 257
        self._r.duty_u16(self._MAX - int(r * scale))
        self._g.duty_u16(self._MAX - int(g * scale))
        self._b.duty_u16(self._MAX - int(b * scale))

    def off(self):
        """Turn LED fully off."""
        self._r.duty_u16(self._MAX)
        self._g.duty_u16(self._MAX)
        self._b.duty_u16(self._MAX)

    def signal_traffic(self):
        """Trigger a brief white flicker (call on each web request)."""
        self._traffic_until = time.ticks_add(time.ticks_ms(), TRAFFIC_MS)

    def update(self, r, g, b):
        """Per‑frame update: flicker during traffic, else mimic *r, g, b*."""
        now = time.ticks_ms()
        if time.ticks_diff(self._traffic_until, now) > 0:
            if (now // 60) % 2:
                self.set(255, 255, 255, 0.25)
            else:
                self.off()
        else:
            self.set(r, g, b)


# ─── Chase State ──────────────────────────────────────────────────────────────

class ChaseState:
    """Mutable state shared between animation, web server, and button."""

    def __init__(self):
        self.speed   = DEFAULT_SPEED
        self.r, self.g, self.b = 255, 0, 0
        self.paint   = False
        self.painted = [(0, 0, 0)] * NUM_LEDS
        self._cidx   = 0

    @property
    def color(self):
        return (self.r, self.g, self.b)

    @color.setter
    def color(self, rgb):
        self.r, self.g, self.b = rgb

    @property
    def hex(self):
        return "#{:02x}{:02x}{:02x}".format(self.r, self.g, self.b)

    def set_hex(self, h):
        """Set colour from a hex string like ``ff8800``."""
        h = h.lstrip("#")
        self.r = int(h[0:2], 16)
        self.g = int(h[2:4], 16)
        self.b = int(h[4:6], 16)

    def next_color(self):
        """Cycle to the next colour in the preset sequence."""
        self._cidx = (self._cidx + 1) % len(COLOR_SEQUENCE)
        self.color = COLOR_SEQUENCE[self._cidx]

    def toggle_paint(self):
        self.paint = not self.paint
        if not self.paint:
            self.clear_canvas()

    def clear_canvas(self):
        self.painted = [(0, 0, 0)] * NUM_LEDS

    def toggle_pause(self):
        self.speed = 0 if self.speed > 0 else DEFAULT_SPEED


# ─── Singletons ──────────────────────────────────────────────────────────────

led_strip = plasma.WS2812(NUM_LEDS, color_order=plasma.COLOR_ORDER_BGR)
led_strip.start()

onboard = OnboardLED()
state   = ChaseState()
button  = Pin(12, Pin.IN, Pin.PULL_UP)


# ─── WiFi ─────────────────────────────────────────────────────────────────────

def wifi_connect():
    """Connect to WiFi with visual feedback on the onboard LED.

    Returns (ip_address, wlan_object).
    """
    from secrets import WIFI_SSID, WIFI_PASSWORD

    wlan = network.WLAN(network.STA_IF)

    # Fresh start — avoids stale state after a soft reboot
    wlan.disconnect()
    wlan.active(False)
    time.sleep(1)
    wlan.active(True)
    time.sleep(1)
    wlan.config(pm=0xa11140)                       # disable CYW43 power saving

    print(f"Connecting to {WIFI_SSID}…")
    wlan.connect(WIFI_SSID, WIFI_PASSWORD)

    blink = True
    for _ in range(30):
        s = wlan.status()
        if s == 3:
            break
        if s < 0:
            onboard.off()
            raise RuntimeError(f"WiFi failed (status {s})")
        onboard.set(255, 0, 0, 0.3) if blink else onboard.off()
        blink = not blink
        print(f"  waiting… (status={s})")
        time.sleep(1)
    else:
        onboard.off()
        raise RuntimeError("WiFi connection timed out")

    onboard.set(0, 255, 0, 0.3)                   # success — green
    time.sleep(2)

    ip = wlan.ifconfig()[0]
    print(f"Connected!  →  http://{ip}")
    return ip, wlan


# ─── Chase Animation ─────────────────────────────────────────────────────────

def _draw_trail(head, r, g, b, base=None):
    """Render a fading trail behind *head*. *base* supplies painted colours."""
    _set = led_strip.set_rgb          # cache method lookup
    _dim = PAINT_DIM
    for i, ff in enumerate(_TRAIL_FADES):
        idx = (head - 1 - i) % NUM_LEDS
        fr, fg, fb = int(r * ff), int(g * ff), int(b * ff)
        if base:
            pr, pg, pb = base[idx]
            fr = max(int(pr * _dim), fr)
            fg = max(int(pg * _dim), fg)
            fb = max(int(pb * _dim), fb)
        _set(idx, fr, fg, fb)


async def chase_loop():
    """Animate a single chaser with fading trail around the strip."""
    offset = 0
    _set   = led_strip.set_rgb         # cache hot method lookups
    _sleep = uasyncio.sleep
    _n     = NUM_LEDS
    _dim   = PAINT_DIM

    while True:
        r, g, b = state.r, state.g, state.b
        head = offset % _n

        if state.paint:
            painted = state.painted
            painted[head] = (r, g, b)
            for i in range(_n):
                pr, pg, pb = painted[i]
                _set(i, int(pr * _dim), int(pg * _dim), int(pb * _dim))
            _set(head, r, g, b)
            _draw_trail(head, r, g, b, base=painted)
        else:
            for i in range(_n):
                _set(i, 0, 0, 0)
            _set(head, r, g, b)
            _draw_trail(head, r, g, b)

        onboard.update(r, g, b)

        if state.speed == 0:
            await _sleep(0.1)
            continue

        offset = (offset + 1) % _n
        await _sleep(max(0.01, 0.21 - state.speed * 0.002))


# ─── Button Handler ──────────────────────────────────────────────────────────

async def button_loop():
    """Poll Button A — short: next colour · double: pause · long: paint."""
    while True:
        if button.value() == 0:                                # pressed
            t0 = time.ticks_ms()
            long_fired = False

            while button.value() == 0:                         # wait release
                held = time.ticks_diff(time.ticks_ms(), t0)
                if not long_fired and held >= LONG_PRESS_MS:
                    state.toggle_paint()
                    print(f"[BTN] Paint {'ON' if state.paint else 'OFF'}")
                    long_fired = True
                await uasyncio.sleep_ms(20)

            if not long_fired:
                # Look for a second tap within the double‑press window
                second = False
                t1 = time.ticks_ms()
                while time.ticks_diff(time.ticks_ms(), t1) < DOUBLE_PRESS_MS:
                    if button.value() == 0:
                        second = True
                        while button.value() == 0:
                            await uasyncio.sleep_ms(20)
                        break
                    await uasyncio.sleep_ms(20)

                if second:
                    state.toggle_pause()
                    print(f"[BTN] Speed → {state.speed}")
                else:
                    state.next_color()
                    print(f"[BTN] Colour → {state.hex}")

        await uasyncio.sleep_ms(50)


# ─── Web UI ──────────────────────────────────────────────────────────────────

_SWATCH_HTML = "".join(
    f'<div class="sw" style="background:#{h}" onclick="c(\'{h}\')"></div>'
    for h in SWATCHES
)

_PAGE = """\
HTTP/1.0 200 OK\r
Content-Type: text/html\r
Connection: close\r
\r
<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Plasma Chase</title>
<style>
*{{box-sizing:border-box}}
body{{
  font-family:-apple-system,sans-serif;
  background:#1a1a2e;color:#eee;
  display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  min-height:100vh;margin:0;
}}
h1{{color:#e94560}}
.card{{
  background:#16213e;border-radius:16px;
  padding:2em;margin:1em;width:min(90vw,360px);
  box-shadow:0 4px 24px rgba(0,0,0,.4);
}}
label{{display:block;margin:1em 0 .3em;font-size:1.1em}}
input[type=color]{{width:100%;height:60px;border:none;border-radius:8px;cursor:pointer}}
input[type=range]{{width:100%;accent-color:#e94560}}
.val{{text-align:center;font-size:1.4em;margin-top:.3em}}
.swatches{{display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin-top:1em}}
.sw{{aspect-ratio:1;border-radius:8px;border:2px solid #0002;cursor:pointer;transition:transform .1s}}
.sw:active{{transform:scale(.9)}}
</style></head><body>
<h1>&#x2728; Plasma Chase</h1>
<div class="card">
  <label>Quick Colours</label>
  <div class="swatches">{swatches}</div>
  <label for="color">Custom Colour</label>
  <input type="color" id="color" value="{hex}">
  <label for="speed">Speed</label>
  <input type="range" id="speed" min="0" max="100" value="{speed}">
  <div class="val" id="sval">{speed}</div>
  <label style="display:flex;align-items:center;gap:.6em;margin-top:1.2em;cursor:pointer">
    <input type="checkbox" id="rem" {checked}
           style="width:22px;height:22px;accent-color:#e94560">
    <span>Remember (paint mode)</span>
  </label>
</div>
<script>
function send(p){{fetch('/?'+p).catch(()=>{{}})}}
function c(h){{send('color='+h);document.getElementById('color').value='#'+h}}
document.getElementById('color').addEventListener('input',e=>c(e.target.value.substring(1)));
const sl=document.getElementById('speed'),sv=document.getElementById('sval');
sl.addEventListener('input',e=>{{sv.textContent=e.target.value;send('speed='+e.target.value)}});
document.getElementById('rem').addEventListener('change',e=>send('remember='+(e.target.checked?'1':'0')));
</script></body></html>"""


def build_page():
    """Render the control page with current state baked in."""
    return _PAGE.format(
        swatches=_SWATCH_HTML,
        hex=state.hex,
        speed=state.speed,
        checked="checked" if state.paint else "",
    )


# ─── Request Parser ──────────────────────────────────────────────────────────

_RESP_204 = "HTTP/1.0 204 No Content\r\nConnection: close\r\n\r\n"


def parse_request(raw):
    """Apply query‑string parameters from raw HTTP request bytes.

    Returns True if parameters were found (caller can send a minimal 204
    instead of the full page).
    """
    try:
        line = raw.split(b"\r\n")[0].decode()
        if "?" not in line:
            return False
        query = line.split("?")[1].split(" ")[0]
        for part in query.split("&"):
            key, val = part.split("=")
            if key == "speed":
                state.speed = max(0, min(100, int(val)))
            elif key == "color":
                state.set_hex(val)
            elif key == "remember":
                state.paint = val == "1"
                if not state.paint:
                    state.clear_canvas()
        return True
    except Exception as e:
        print(f"[WEB] Parse error: {e}")
        return False


# ─── Web Server ──────────────────────────────────────────────────────────────

async def web_server(wlan):
    """Async HTTP server on port 80."""

    async def handle(reader, writer):
        onboard.signal_traffic()
        try:
            data = await reader.read(1024)
            if data:
                path = data.split(b" ")[1].decode()
                print(f"[WEB] {path}")
                has_params = parse_request(data)
            else:
                has_params = False
            # AJAX param updates get a tiny 204; full page only on first load
            writer.write(_RESP_204 if has_params else build_page())
            await writer.drain()
            onboard.signal_traffic()
        except Exception as e:
            print(f"[WEB] Error: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

    await uasyncio.start_server(handle, "0.0.0.0", 80)
    print("[WEB] Listening on :80")

    while True:
        if not wlan.isconnected():
            print("[WEB] ⚠ WiFi disconnected!")
        await uasyncio.sleep(10)


# ─── Entry Point ─────────────────────────────────────────────────────────────

async def _run(wlan):
    await uasyncio.gather(chase_loop(), web_server(wlan), button_loop())


def start():
    """Boot → green LED → blink red (WiFi) → green → run."""
    onboard.set(0, 255, 0, 0.3)
    print("Booting…")

    ip, wlan = wifi_connect()

    try:
        uasyncio.run(_run(wlan))
    except KeyboardInterrupt:
        pass
    finally:
        for i in range(NUM_LEDS):
            led_strip.set_rgb(i, 0, 0, 0)
        onboard.off()
        print("Bye!")


start()
