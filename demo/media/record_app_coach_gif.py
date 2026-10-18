"""Record the live patient app chat + agent trace (#coach) to a looping GIF.
Usage: python3 demo/media/record_app_coach_gif.py [url] [out.gif] [seconds] [out_width]"""
import io, sys, time
from PIL import Image
from playwright.sync_api import sync_playwright
url = sys.argv[1] if len(sys.argv) > 1 else "https://heartstep-app.vercel.app/#coach"
out = sys.argv[2] if len(sys.argv) > 2 else "demo/media/app-coach-flow.gif"
secs = float(sys.argv[3]) if len(sys.argv) > 3 else 28
width = int(sys.argv[4]) if len(sys.argv) > 4 else 1000
W, H, fps = 1500, 900, 8
frames, stamps = [], []
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": W, "height": H})
    pg.goto(url.split("#")[0]); pg.wait_for_load_state("networkidle")
    pg.fill("input[name=username]", "somchai"); pg.click("text=Continue"); pg.wait_for_timeout(1500)
    pg.goto(url); pg.reload(); pg.wait_for_load_state("networkidle")
    pg.fill("input[name=username]", "somchai"); pg.click("text=Continue"); pg.wait_for_timeout(1200)
    pg.evaluate("location.hash='#coach'"); pg.wait_for_selector("[data-chat]"); pg.evaluate("document.fonts.ready")
    t0 = time.time(); nxt = t0; clicked = False
    while time.time() - t0 < secs:
        if not clicked and time.time() - t0 > 1.5:
            pg.locator("[data-chat]").first.click(); clicked = True
        frames.append(Image.open(io.BytesIO(pg.screenshot())).convert("RGB")); stamps.append(time.time())
        nxt += 1 / fps; time.sleep(max(0, nxt - time.time()))
    b.close()
durs = [int((stamps[k + 1] - stamps[k]) * 1000) for k in range(len(stamps) - 1)] + [2000]
h = round(H * width / W)
small = [f.resize((width, h), Image.LANCZOS) for f in frames]
pal = Image.new("RGB", (width, h * 3)); [pal.paste(small[int(len(small) * q)], (0, h * k)) for k, q in enumerate((.2, .5, .8))]
pal = pal.quantize(colors=160, method=Image.Quantize.MEDIANCUT)
q = [f.quantize(palette=pal, dither=Image.Dither.NONE) for f in small]
q[0].save(out, save_all=True, append_images=q[1:], duration=durs, loop=0, optimize=True, disposal=1)
print(len(frames), "frames", width, "x", h, "->", out)
