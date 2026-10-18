"""Record a fixed-size page or live URL (e.g. demo/problem-story.html) to a looping GIF.
Usage: python3 demo/media/record_page_gif.py <page.html|https://url> <out.gif> <seconds> [width] [height]"""
import io, sys, time
from pathlib import Path
from PIL import Image
from playwright.sync_api import sync_playwright
src, out, secs = sys.argv[1], sys.argv[2], float(sys.argv[3])
url = src if src.startswith('http') else Path(src).resolve().as_uri()
H = int(sys.argv[5]) if len(sys.argv) > 5 else 720
width, fps = int(sys.argv[4]) if len(sys.argv) > 4 else 960, 10
frames, stamps = [], []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1280, "height": H})
    pg.goto(url); pg.wait_for_load_state("networkidle"); pg.evaluate("document.fonts.ready")
    pg.evaluate("location.reload()"); pg.wait_for_load_state("networkidle")  # restart the timeline with fonts cached
    t0 = time.time(); nxt = t0
    while time.time() - t0 < secs:
        frames.append(Image.open(io.BytesIO(pg.screenshot(clip={"x": 0, "y": 0, "width": 1280, "height": H}))).convert("RGB")); stamps.append(time.time())
        nxt += 1 / fps; time.sleep(max(0, nxt - time.time()))
    b.close()
durs = [int((stamps[k + 1] - stamps[k]) * 1000) for k in range(len(stamps) - 1)] + [1500]
h = round(H * width / 1280)
small = [f.resize((width, h), Image.LANCZOS) for f in frames]
pal = Image.new("RGB", (width, h * 3)); [pal.paste(small[int(len(small) * q)], (0, h * k)) for k, q in enumerate((.15, .5, .75))]
pal = pal.quantize(colors=160, method=Image.Quantize.MEDIANCUT)
q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in small]
q[0].save(out, save_all=True, append_images=q[1:], duration=durs, loop=0, optimize=True, disposal=1)
print(len(frames), "frames", width, "x", h, "->", out)
