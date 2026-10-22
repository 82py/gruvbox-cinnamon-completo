#!/usr/bin/python3
"""Gera prévias a partir dos SVGs distribuídos, sem ler a sessão ou mídias pessoais."""
from pathlib import Path
import importlib.util,io
from PIL import Image,ImageDraw,ImageFont
import gi
gi.require_version('GdkPixbuf','2.0')
from gi.repository import GdkPixbuf
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/imagens'
BASE=ROOT/'payload/.local/share/icons/Gruvbox-Plus-Dark'
SYSTEM=ROOT/'payload/.local/share/icons/Gruvbox-Sistema-Colorido'
spec=importlib.util.spec_from_file_location('colors',ROOT/'scripts/folder_colors.py')
colors=importlib.util.module_from_spec(spec);spec.loader.exec_module(colors)
BG='#282828';CARD='#32302f';TEXT='#ebdbb2';MUTED='#bdae93';LINE='#504945'
def font(size,bold=False):
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans'+('-Bold' if bold else '')+'.ttf',size)
def icon(path,size):
    pix=GdkPixbuf.Pixbuf.new_from_file_at_scale(str(path),size,size,True)
    ok,data=pix.save_to_bufferv('png',[],[])
    if not ok:raise RuntimeError(str(path))
    return Image.open(io.BytesIO(data)).convert('RGBA')
def place(image,path,x,y,size):
    art=icon(path,size);image.paste(art,(int(x+(size-art.width)/2),int(y+(size-art.height)/2)),art)
def label(draw,x,y,text,size=22,fill=TEXT,bold=False):draw.text((x,y),text,font=font(size,bold),fill=fill)
def center(draw,x,y,text,size=22,fill=TEXT):
    f=font(size);w=draw.textbbox((0,0),text,font=f)[2];draw.text((x-w/2,y),text,font=f,fill=fill)
def palette(draw,w,h):
    values=['#cc241d','#d65d0e','#d79921','#98971a','#689d6a','#458588']
    for n,c in enumerate(values):draw.rectangle((n*w/len(values),h-10,(n+1)*w/len(values),h),fill=c)
OUT.mkdir(parents=True,exist_ok=True)
hero=Image.new('RGB',(1440,520),BG);d=ImageDraw.Draw(hero)
label(d,56,35,'GRUVBOX',72,bold=True);label(d,58,122,'Cinnamon Completo',42,fill='#d79921')
label(d,60,188,'Icons  /  Panel  /  Workspaces  /  Rain',26,fill=MUTED)
label(d,1095,55,'Pir (82py)',25,bold=True);label(d,1095,94,'Mint Cinnamon · X11',18,fill=MUTED)
items=[('Folders',BASE/'places/scalable/folder-jade.svg'),('Rain',BASE/'apps/scalable/rain-gruvbox.svg'),('WhatsApp',BASE/'apps/scalable/whatsapp.svg'),('Yubico',BASE/'apps/scalable/yubioath.svg'),('PDF',BASE/'apps/scalable/masterpdfeditor.svg'),('Sound',SYSTEM/'scalable/actions/xsi-audio-volume-high-symbolic.svg'),('Wi-Fi',SYSTEM/'scalable/actions/xsi-network-wireless-signal-excellent.svg'),('Bluetooth',SYSTEM/'scalable/status/blueman-active.svg')]
for i,(name,path) in enumerate(items):
    x=56+i*168;d.rounded_rectangle((x,258,x+152,452),radius=18,fill=CARD,outline=LINE,width=2)
    place(hero,path,x+28,280,96);center(d,x+76,405,name,22)
label(d,60,475,'Actual artwork from the package · Original projects credited in CREDITOS.md',18,fill=MUTED);palette(d,1440,520)
hero.save(OUT/'gruvbox-cinnamon-preview.png',optimize=True)
chart=Image.new('RGB',(1200,1240),BG);d=ImageDraw.Draw(chart)
label(d,46,30,'25 folder colors',44,bold=True);label(d,48,94,'Cores das pastas · Gruvbox Plus',24,fill=MUTED)
for i,color in enumerate(colors.COLORS):
    x=40+(i%5)*232;y=160+(i//5)*204
    d.rounded_rectangle((x,y,x+216,y+184),radius=14,fill=CARD,outline=LINE,width=2)
    place(chart,BASE/('places/scalable/folder-'+color+'.svg'),x+48,y+12,120)
    center(d,x+108,y+145,color,23)
label(d,44,1200,'SVGs reais do pacote / Actual package SVGs · SylEleuth & contributors',17,fill=MUTED);palette(d,1200,1240)
chart.save(OUT/'folder-colors.png',optimize=True)
strip=Image.new('RGB',(1440,230),BG);d=ImageDraw.Draw(strip)
for i,color in enumerate(['blue','jade','green','olive','gold','orange','rust','red','sapphire','plasma']):
    x=30+i*140;place(strip,BASE/('places/scalable/folder-'+color+'.svg'),x+14,24,104);center(d,x+66,145,color,20)
label(d,42,198,'10 of 25 options · See all colors / Veja todas as cores',17,fill=MUTED)
strip.save(OUT/'folder-colors-preview.png',optimize=True)
print('Prévias geradas a partir dos ícones reais do pacote.')
