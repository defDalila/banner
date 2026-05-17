# Build v4 GIFs per user's request:
# - Phrases: "Medical Physicist...", "Dev in training", ".NET Lover..."
# - Cursor: full block "█"
# - Change light blue wave to cyan tones
# - Keep extra spacing and monospace typewriter font

from PIL import Image, ImageDraw, ImageFont, ImagePalette
from pathlib import Path
import math

out_dir = Path("output/")
out_dir.mkdir(parents=True, exist_ok=True)


def fast_vertical_gradient(w, h, start_hex, end_hex):
    start = tuple(int(start_hex[i:i+2], 16) for i in (1,3,5))
    end   = tuple(int(end_hex[i:i+2], 16) for i in (1,3,5))
    col = Image.new("RGB", (1, h))
    for y in range(h):
        t = y/(h-1)
        r = int(start[0]*(1-t) + end[0]*t)
        g = int(start[1]*(1-t) + end[1]*t)
        b = int(start[2]*(1-t) + end[2]*t)
        col.putpixel((0,y), (r,g,b))
    return col.resize((w, h), resample=Image.Resampling.BILINEAR).convert("RGBA")

def make_base(theme, w=1400, h=400):
    if theme=="dark":
        bg = fast_vertical_gradient(w,h,"#091A25","#0f172a")
        wave_color = ("#7BDFF2")   # cyan-400 with alpha (more cyan)
        text_primary = (226,232,240)
        text_secondary = (203,213,225)
        accent = ("#FF5DA3")
        shadow_rgba = (0,0,0,90) 
    else:
        bg = fast_vertical_gradient(w,h,"#f8fafc","#e2e8f0")
        wave_color = (34, 211, 238, 56)   # cyan
        text_primary = (15,23,42)
        text_secondary = (51,65,85)
        accent = (14,165,233)             # blue accent looks nice on light; could also use cyan
        shadow_rgba = (31,41,55,70)

    # Decorative cyan wave
    overlay = Image.new("RGBA", (w,h), (0,0,0,0))
    d = ImageDraw.Draw(overlay)
    y_base = int(h*0.8)
    pts = []
    for x in range(0, w+1, 20):
        y = y_base + int(20*math.sin(x/140.0))
        pts.append((x,y))
    pts += [(w,h),(0,h)]
    d.polygon(pts, fill=wave_color)
    bg.alpha_composite(overlay)

    # Static headers
    d2 = ImageDraw.Draw(bg)
    f_small = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 28)
    f_title = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 78)
    f_name = ImageFont.truetype(r"C:\Windows\Fonts\seguibl.ttf", 88)

    x0 = 80
    y_small = 90
    y_title = 120
    

    def shadow_text(x,y,text,font,fill,offset=2):
        d2.text((x+offset,y+offset), text, font=font, fill=shadow_rgba)
        d2.text((x,y), text, font=font, fill=fill)

    header_small = "Hi There,"
    shadow_text(x0, y_small, header_small, f_small, text_secondary)

    header_title = "I'm "
    title_position = d2.textlength(header_title, font=f_title)
    shadow_text(x0, y_title, header_title, f_title, text_primary)

    header_name  = "Dalila Mendonça"
    name_position = d2.textlength(header_name, font=f_name)


    d2.text((x0+title_position, y_title), header_name, font=f_name, fill=accent)
    base_y = y_title + f_name.size + 6
    # d2.line([(x0+title_position, base_y), (x0+title_position+name_position, base_y)], fill=accent, width=3)

    return bg

def render_frame(base_img, theme, typed, cursor_on=True, extra_spacing=70, cursor_char="█"):
    img = base_img.copy()
    d = ImageDraw.Draw(img)
    text_secondary = ("#ffffff") if theme=="dark" else (51,65,85)
    f_mono = ImageFont.truetype(r"C:\Users\defda\AppData\Local\Microsoft\Windows\Fonts\Orbitron-Regular.ttf", 34)

    x0 = 80
    y_sub  = 240

    cursor = cursor_char if cursor_on else " "
    line = typed + cursor
    d.text((x0, y_sub), line, font=f_mono, fill=text_secondary)

    return img.convert("P", palette=Image.Palette.ADAPTIVE)

def build_typing_sequence(phrase, typing_delay=55, pause_ms=900, deleting_delay=38, end_pause_ms=420):
    frames_text, durations = [], []
    for i in range(1, len(phrase)+1):
        frames_text.append(phrase[:i]); durations.append(typing_delay)
    frames_text.append(phrase); durations.append(pause_ms)
    for i in range(len(phrase), 0, -1):
        frames_text.append(phrase[:i-1]); durations.append(deleting_delay)
    frames_text.append(""); durations.append(end_pause_ms)
    return frames_text, durations

def make_typewriter_gif(filename, theme="dark"):
    base = make_base(theme)
    phrases = [
        "Medical Physicist...",
        "“My new journey began with R for data analysis...",
        "Now, I’m a developer in training...” 
        “And a lover of R and .NET...”,
    ]

    frames_text, durations = [], []
    for p in phrases:
        ft, dt = build_typing_sequence(p)
        frames_text.extend(ft); durations.extend(dt)
    for _ in range(6):
        frames_text.append(""); durations.append(180)

    images = []
    cursor_on = True
    for t in frames_text:
        img = render_frame(base, theme, t, cursor_on=cursor_on, extra_spacing=70, cursor_char="█")
        images.append(img); cursor_on = not cursor_on

    path = out_dir / filename
    images[0].save(path, save_all=True, append_images=images[1:], duration=durations, loop=0, optimize=True, disposal=2)
    return str(path)

if __name__ == "__main__":
    print("Saving:", make_typewriter_gif("dalila-typewriter-dark-v5.gif", theme="dark"))
    print("Saving:", make_typewriter_gif("dalila-typewriter-light-v5.gif", theme="light"))


# background: radial-gradient(1911.03% 66.03% at 3.37% 72.34%, #E9EFEF 0%, #E680E8 31.77%, #A3C4F1 68.75%, #E480EB 100%);
# background-clip: text;
# -webkit-background-clip: text;
# -webkit-text-fill-color: transparent;
