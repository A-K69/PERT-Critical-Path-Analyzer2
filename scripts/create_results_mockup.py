from __future__ import annotations

import json
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "PHASE17_RESULTS_DESIGN_MOCKUP_IMAGE1.png"
GT = ROOT / "tests/test_data/ground_truth/1.json"

W, H = 1920, 1200
img = Image.new("RGB", (W, H), "#080d16")
d = ImageDraw.Draw(img)

font_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
]
bold_paths = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf",
]
def font(size, bold=False):
    for p in (bold_paths if bold else font_paths):
        if Path(p).exists(): return ImageFont.truetype(p, size)
    return ImageFont.load_default()

F10, F12, F14, F16, F18, F22, F28, F36 = [font(x) for x in (10,12,14,16,18,22,28,36)]
FB10, FB12, FB14, FB16, FB18, FB22, FB28, FB36 = [font(x, True) for x in (10,12,14,16,18,22,28,36)]

# Palette
BG = "#080d16"; PANEL = "#101827"; PANEL2 = "#121e30"; CARD = "#162337"
GRID = "#1b3148"; MUTED = "#8193aa"; TEXT = "#e9f1fa"; CYAN = "#39c6ff"
BLUE = "#5b8cff"; GREEN = "#25d6a2"; AMBER = "#f5b84b"; RED = "#ff6f78"

# Background glow/grid
overlay = Image.new("RGBA", (W,H), (0,0,0,0)); od=ImageDraw.Draw(overlay)
for x in range(32, 1470, 48): od.line((x, 120, x, 1120), fill=(42,72,102,35), width=1)
for y in range(120, 1120, 48): od.line((32, y, 1470, y), fill=(42,72,102,35), width=1)
img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB"); d=ImageDraw.Draw(img)

# top bar
d.rectangle((0,0,W,74), fill="#0b1321")
d.rectangle((0,72,W,74), fill=CYAN)
d.text((34,20), "PERT // CONTROL CENTER", font=FB18, fill=TEXT)
d.text((390,26), "RESULTS", font=FB14, fill=CYAN)
d.text((520,27), "Image analysis  /  1.png", font=F14, fill=MUTED)
d.rounded_rectangle((1600,18,1878,56), radius=18, fill="#123229", outline="#237e68", width=1)
d.ellipse((1620,30,1632,42), fill=GREEN)
d.text((1646,26), "AUTHORITATIVE RESULT", font=FB12, fill=GREEN)

# title + trust row
d.text((34,104), "Project network intelligence", font=FB28, fill=TEXT)
d.text((34,145), "Validated graph · CPM-backed · interactive review surface", font=F14, fill=MUTED)
d.rounded_rectangle((1130,102,1470,149), radius=12, fill="#122a33", outline="#237e68", width=1)
d.text((1152,117), "✓  BACKEND VALIDATED", font=FB14, fill=GREEN)
d.rounded_rectangle((1490,102,1820,149), radius=12, fill="#17243a", outline="#31527d", width=1)
d.text((1512,117), "◉  IMAGE SOURCE  1.png", font=FB14, fill=CYAN)

# KPI cards
def kpi(x, title, value, accent, sub):
    d.rounded_rectangle((x,180,x+235,270), radius=14, fill=CARD, outline="#253d5a", width=1)
    d.rectangle((x,180,x+5,270), fill=accent)
    d.text((x+18,196), title.upper(), font=FB10, fill=MUTED)
    d.text((x+18,216), value, font=FB28, fill=accent)
    d.text((x+18,252), sub, font=F10, fill=MUTED)
for args in [(34,"PROJECT DURATION","54 d",CYAN,"CPM verified"),(284,"ACTIVITIES","22",BLUE,"all detected"),(534,"DEPENDENCIES","28",BLUE,"unique relations"),(784,"CRITICAL PATHS","16",AMBER,"zero-float paths"),(1034,"CRITICAL ACTIVITIES","22",GREEN,"validated"),(1284,"DATA CONFIDENCE","96%",GREEN,"multi-factor evidence")]: kpi(*args)

# main network panel
NX, NY, NW, NH = 34, 296, 1420, 782
d.rounded_rectangle((NX,NY,NX+NW,NY+NH), radius=18, fill=PANEL, outline="#28445e", width=1)
d.text((NX+24,NY+20), "NETWORK EXPLORER", font=FB14, fill=TEXT)
d.text((NX+24,NY+48), "Critical-path emphasis · click any node for activity details", font=F12, fill=MUTED)
# toolbar
d.rounded_rectangle((NX+870,NY+17,NX+1010,NY+50), radius=10, fill="#1b2e49", outline="#365e8b", width=1); d.text((NX+890,NY+27), "CPM VIEW  ▾", font=FB10, fill=CYAN)
d.rounded_rectangle((NX+1020,NY+17,NX+1120,NY+50), radius=10, fill="#17362f", outline="#287c67", width=1); d.text((NX+1040,NY+27), "Fit view", font=FB10, fill=GREEN)
d.rounded_rectangle((NX+1130,NY+17,NX+1225,NY+50), radius=10, fill="#1b2e49", outline="#365e8b", width=1); d.text((NX+1155,NY+27), "+  −", font=FB12, fill=TEXT)
# legend
d.ellipse((NX+24,NY+88,NX+36,NY+100), fill=AMBER); d.text((NX+44,NY+84), "Critical path", font=F10, fill=MUTED)
d.ellipse((NX+150,NY+88,NX+162,NY+100), fill=BLUE); d.text((NX+170,NY+84), "Validated activity", font=F10, fill=MUTED)
d.line((NX+290,NY+94,NX+330,NY+94), fill="#4a6686", width=2); d.text((NX+342,NY+84), "Dependency", font=F10, fill=MUTED)

# graph layout from image 1 positions, scaled to panel
with GT.open() as f: gt=json.load(f)
acts=gt["activities"]; edges=[(e["source"],e["target"]) for e in gt["dependencies"]]
pos={a["id"]: (a["position"][0],a["position"][1]) for a in acts}
durs={a["id"]: a["duration"] for a in acts}
minx,maxx=min(x for x,y in pos.values()),max(x for x,y in pos.values()); miny,maxy=min(y for x,y in pos.values()),max(y for x,y in pos.values())
area=(NX+46, NY+130, NX+NW-46, NY+NH-34); ax,ay,bx,by=area
sx=(bx-ax)/(maxx-minx+20); sy=(by-ay)/(maxy-miny+20)
# preserve diagram aspect but fit
s=min(sx,sy)*0.86
cx=(ax+bx)/2; cy=(ay+by)/2
scaled={k:(cx+(x-(minx+maxx)/2)*s, cy+(y-(miny+maxy)/2)*s) for k,(x,y) in pos.items()}
# edges first
selected={"A","B","D","F","I","J","K","L","N","O","P","Q","R","S","T","U","V"}
sel_edges={(a,b) for a,b in edges if a in selected and b in selected}
for a,b in edges:
    x1,y1=scaled[a]; x2,y2=scaled[b]
    color=AMBER if (a,b) in sel_edges else "#3b536f"
    width=4 if (a,b) in sel_edges else 2
    # elbow-ish direct line
    d.line((x1,y1,x2,y2), fill=color, width=width)
    ang=math.atan2(y2-y1,x2-x1); L=11
    p1=(x2-L*math.cos(ang-0.45),y2-L*math.sin(ang-0.45)); p2=(x2-L*math.cos(ang+0.45),y2-L*math.sin(ang+0.45))
    d.polygon([(x2,y2),p1,p2], fill=color)
# nodes
for a in acts:
    aid=a["id"]; x,y=scaled[aid]; critical=aid in selected
    nw,nh=72,48
    fill="#183248" if not critical else "#273129"
    outline=AMBER if critical else CYAN
    d.rounded_rectangle((x-nw/2,y-nh/2,x+nw/2,y+nh/2), radius=10, fill=fill, outline=outline, width=2)
    d.text((x-8,y-20), aid, font=FB16, fill=TEXT)
    d.text((x-22,y+1), f"{a['duration']}d", font=F10, fill=MUTED)
    if critical:
        d.ellipse((x+24,y-19,x+32,y-11), fill=AMBER)
# overlay selected path label
d.rounded_rectangle((NX+28,NY+NH-62,NX+360,NY+NH-28), radius=9, fill="#2b2515", outline="#a87828", width=1)
d.text((NX+44,NY+NH-54), "● Selected critical path · 54 days", font=FB10, fill=AMBER)

# right inspector
RX,RY,RW,RH=1480,296,406,782
d.rounded_rectangle((RX,RY,RX+RW,RY+RH), radius=18, fill=PANEL, outline="#28445e", width=1)
d.text((RX+24,RY+20), "ACTIVITY INSPECTOR", font=FB14, fill=TEXT)
d.text((RX+24,RY+48), "Selected node · click to change", font=F12, fill=MUTED)
# selected activity card
sx0,sy0=RX+24,RY+88
d.rounded_rectangle((sx0,sy0,RX+RW-24,sy0+112), radius=14, fill="#1a3042", outline=CYAN, width=2)
d.text((sx0+20,sy0+16), "F", font=FB36, fill=CYAN)
d.text((sx0+82,sy0+20), "Integration / setup", font=FB16, fill=TEXT)
d.text((sx0+82,sy0+52), "Activity ID · F", font=F12, fill=MUTED)
d.rounded_rectangle((sx0+285,sy0+18,sx0+348,sy0+44), radius=12, fill="#3e3016", outline=AMBER, width=1); d.text((sx0+299,sy0+24), "CRITICAL", font=FB10, fill=AMBER)
# detail rows
rows=[("Duration","4 days",CYAN),("Early start","5 days",TEXT),("Early finish","9 days",TEXT),("Late start","5 days",TEXT),("Late finish","9 days",TEXT),("Total float","0 days",AMBER)]
y=sy0+142
for lab,val,col in rows:
    d.line((RX+24,y-8,RX+RW-24,y-8), fill="#223850", width=1)
    d.text((RX+30,y+8),lab,font=F12,fill=MUTED); d.text((RX+RW-140,y+8),val,font=FB14,fill=col); y+=46
# evidence card
y+=8
d.rounded_rectangle((RX+24,y,RX+RW-24,y+152), radius=14, fill="#132636", outline="#28506f", width=1)
d.text((RX+42,y+18), "DATA INTEGRITY", font=FB12, fill=GREEN)
d.text((RX+42,y+52), "✓ CPM values from backend result", font=F12, fill=TEXT)
d.text((RX+42,y+78), "✓ Graph matches 28 unique edges", font=F12, fill=TEXT)
d.text((RX+42,y+104), "✓ Zero-float state verified", font=F12, fill=TEXT)
d.text((RX+42,y+130), "↗ Open evidence trace", font=FB12, fill=CYAN)
# footer
footer_y=1128
d.text((34,footer_y), "Source: 1.png  ·  AON  ·  22 activities  ·  28 dependencies", font=F12, fill=MUTED)
d.text((1410,footer_y), "Last validation  •  just now", font=F12, fill=GREEN)
img.save(OUT, "PNG", optimize=True)
print(OUT)
