#!/usr/bin/env python3
"""Generate a WhatsApp-optimized link-preview card (1200x630 JPG, <300KB)."""
from PIL import Image, ImageDraw, ImageFont
import math, random

W, H = 1200, 630
img = Image.new("RGB", (W, H), "#fbe3ee")
d = ImageDraw.Draw(img)

# vertical pink gradient
top = (251, 227, 238); bot = (245, 194, 221)
for y in range(H):
    t = y / H
    r = int(top[0] + (bot[0]-top[0])*t)
    g = int(top[1] + (bot[1]-top[1])*t)
    b = int(top[2] + (bot[2]-top[2])*t)
    d.line([(0,y),(W,y)], fill=(r,g,b))

# soft confetti dots + little flowers scattered
random.seed(3)
palette = [(236,111,166),(242,207,90),(167,208,138),(247,192,214),(217,79,140)]
for _ in range(46):
    x = random.randint(0, W); y = random.randint(0, H)
    rr = random.randint(4, 12)
    c = random.choice(palette)
    d.ellipse([x-rr,y-rr,x+rr,y+rr], fill=c)

def flower(cx, cy, s, petal, center):
    for a in range(6):
        ang = math.radians(a*60)
        px = cx + math.cos(ang)*s; py = cy + math.sin(ang)*s
        d.ellipse([px-s*0.7,py-s*0.7,px+s*0.7,py+s*0.7], fill=petal)
    d.ellipse([cx-s*0.6,cy-s*0.6,cx+s*0.6,cy+s*0.6], fill=center)

for (fx,fy,fs) in [(70,110,16),(1130,90,14),(90,540,18),(1120,520,15),(600,40,12)]:
    flower(fx,fy,fs,(247,160,196),(242,207,90))

# Minnie on the left
try:
    minnie = Image.open("assets/minnie.png").convert("RGBA")
    mh = 470
    mw = int(minnie.width * mh / minnie.height)
    minnie = minnie.resize((mw, mh), Image.LANCZOS)
    img.paste(minnie, (40, H-mh-30), minnie)
    text_x = 40 + mw - 30
except Exception as e:
    print("minnie err", e); text_x = 120

# fonts
didot    = ImageFont.truetype("/System/Library/Fonts/Supplemental/Didot.ttc", 150)
snell    = ImageFont.truetype("/System/Library/Fonts/Supplemental/SnellRoundhand.ttc", 86)
georgia  = ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia.ttf", 34)
georgia_b= ImageFont.truetype("/System/Library/Fonts/Supplemental/Georgia Bold.ttf", 34)

gold = (199,154,75); rose = (236,111,166); deep = (217,79,140)

def center_text(txt, font, cy, fill, area_x0, area_x1):
    bb = d.textbbox((0,0), txt, font=font)
    tw = bb[2]-bb[0]; th = bb[3]-bb[1]
    cx = (area_x0+area_x1)//2 - tw//2 - bb[0]
    d.text((cx, cy-bb[1]), txt, font=font, fill=fill)
    return th

ax0, ax1 = text_x, W-40
y = 95
center_text("Emilia", didot, y, gold, ax0, ax1)
y += 165
center_text("Vázquez Montiel", snell, y, rose, ax0, ax1)
y += 110
center_text("MI FIESTA DE 3 AÑOS", georgia, y, gold, ax0, ax1)

# invitation CTA ribbon
ribbon_y = 470
rx0, rx1 = text_x+10, W-70
d.rounded_rectangle([rx0, ribbon_y, rx1, ribbon_y+90], radius=45, fill=(217,79,140))
bb = d.textbbox((0,0), "Toca para abrir tu invitación", font=georgia_b)
tw = bb[2]-bb[0]
d.text(((rx0+rx1)//2 - tw//2 - bb[0], ribbon_y+45-(bb[3]-bb[1])//2-bb[1]),
       "Toca para abrir tu invitación", font=georgia_b, fill="white")

# save optimized jpg
img.save("assets/preview-wa.jpg", "JPEG", quality=86, optimize=True)
import os
print("saved", os.path.getsize("assets/preview-wa.jpg")//1024, "KB", img.size)
