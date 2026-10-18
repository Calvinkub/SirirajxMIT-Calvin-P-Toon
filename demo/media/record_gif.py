import time, io, sys
from PIL import Image
from playwright.sync_api import sync_playwright
SRC = "file:///Users/admin/Project/SirirajxMIT-Calvin-P-Toon/demo/agent-flow-demo.html#gif"
OUT = sys.argv[1] if len(sys.argv) > 1 else "/Users/admin/Project/SirirajxMIT-Calvin-P-Toon/demo/media/agent-flow.gif"
SECONDS, FPS, WIDTH = 27, 8, 960
frames, stamps = [], []
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1240, "height": 820}, device_scale_factor=1)
    pg.goto(SRC); pg.wait_for_load_state("networkidle")
    pg.evaluate("document.fonts.ready")
    clip = pg.locator(".trace").bounding_box()
    clip = {"x": clip["x"], "y": clip["y"], "width": clip["width"], "height": round(clip["width"] * 9 / 16)}
    t0 = time.time(); nxt = t0
    while time.time() - t0 < SECONDS:
        frames.append(Image.open(io.BytesIO(pg.screenshot(clip=clip))).convert("RGB")); stamps.append(time.time())
        nxt += 1 / FPS; time.sleep(max(0, nxt - time.time()))
    b.close()
durs = [int((stamps[i + 1] - stamps[i]) * 1000) for i in range(len(stamps) - 1)] + [2500]
h = int(frames[0].height * WIDTH / frames[0].width)
small = [f.resize((WIDTH, h), Image.LANCZOS) for f in frames]
pal = small[len(small) // 2].quantize(colors=128, method=Image.Quantize.MEDIANCUT)
q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in small]
q[0].save(OUT, save_all=True, append_images=q[1:], duration=durs, loop=0, optimize=True, disposal=1)
print(len(frames), "frames", WIDTH, "x", h, "->", OUT)
