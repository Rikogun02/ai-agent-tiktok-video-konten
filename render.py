#!/usr/bin/env python3
"""Render one 120-second vertical AI-agent explainer using Pillow + FFmpeg."""
from pathlib import Path
import subprocess, textwrap, wave, math, struct, os

from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "output"
OUT.mkdir(exist_ok=True)
W, H = 1080, 1920
FPS = 30
FONT_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_R = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

SCENES = [
    ("CARA KERJA AI AGENT", "01  TRIGGER & PEMAHAMAN", "Pesan masuk", "Ava memahami tujuan dan konteks tugas.", "TRIGGER  →  PAHAM TUJUAN", "AI agent bukan cuma menjawab. Ia menerima tujuan, memahami instruksi, lalu mulai bekerja."),
    ("MEMORI & PERENCANAAN", "02  INGAT DAN SUSUN STRATEGI", "Memori aktif", "Konteks disimpan, tugas dipecah menjadi langkah.", "MEMORI  →  RENCANA", "Agent memeriksa memori jangka pendek dan panjang. Setelah itu, ia menyusun rencana langkah demi langkah."),
    ("TOOLS & EKSEKUSI", "03  KERJAKAN DAN PERBAIKI", "Pilih tools", "API • Database • Dokumen • Kode", "EKSEKUSI  →  CEK  →  RETRY", "Agent memakai tools untuk mengambil data dan menjalankan tugas. Jika muncul error, ia mengecek, memperbaiki, lalu mencoba lagi."),
    ("HASIL DENGAN KONTROL MANUSIA", "04  APPROVAL & HASIL AKHIR", "Minta persetujuan", "Manusia tetap memegang keputusan penting.", "APPROVE  →  HASIL SELESAI", "Untuk tindakan penting, agent meminta persetujuan manusia. Setelah selesai, hasil dikirim dan manusia tetap memegang kendali."),
]

def font(size, bold=True):
    return ImageFont.truetype(FONT_B if bold else FONT_R, size)

def rounded(draw, xy, radius, fill, outline=None, width=2):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def make_scene(i, data):
    title, kicker, card, desc, flow, _ = data
    im = Image.new("RGB", (W,H), (8,11,30))
    px = im.load()
    # smooth vertical navy-purple gradient
    for y in range(H):
        t = y / H
        c = (int(9+20*t), int(13+3*t), int(34+34*t))
        for x in range(W):
            px[x,y] = c
    d = ImageDraw.Draw(im, "RGBA")
    # ambient neon rings / grid
    for k in range(7):
        x = 140 + k*150
        d.line((x,0,x,H), fill=(44,73,130,35), width=2)
    for y in range(180,H,170):
        d.line((0,y,W,y), fill=(44,73,130,24), width=2)
    d.ellipse((650,-150,1250,450), fill=(115,40,180,38))
    d.ellipse((-220,1250,480,1900), fill=(0,180,220,25))
    # top labels
    rounded(d,(64,74,1016,154),34,(24,31,66,230),(64,84,150,220),2)
    d.text((96,95),"AVA  /  AI AGENT EXPLAINER",font=font(30),fill=(130,235,255,255))
    d.text((70,235),kicker,font=font(35),fill=(255,85,205,255))
    # title
    lines = textwrap.wrap(title, width=22)
    y=330
    for line in lines:
        d.text((70,y),line,font=font(70),fill=(247,249,255,255),stroke_width=1,stroke_fill=(247,249,255,255))
        y += 92
    # mascot panel
    rounded(d,(170,700,910,1235),48,(19,27,62,235),(54,211,239,210),4)
    # robot antenna
    d.line((540,785,540,720),fill=(73,220,255,255),width=12)
    d.ellipse((515,685,565,735),fill=(255,74,205,255))
    # robot head/body
    rounded(d,(330,790,750,1110),90,(48,64,115,255),(93,228,255,255),8)
    rounded(d,(390,865,690,1010),48,(7,14,36,255),(83,125,202,255),4)
    d.ellipse((450,905,505,960),fill=(70,238,255,255))
    d.ellipse((575,905,630,960),fill=(70,238,255,255))
    d.arc((475,940,605,1030),10,170,fill=(255,95,207,255),width=9)
    # side ear lights
    rounded(d,(290,890,340,1015),20,(255,70,190,255))
    rounded(d,(740,890,790,1015),20,(0,210,255,255))
    d.text((425,1145),"AVA  •  ASISTEN AI",font=font(28),fill=(202,226,255,255))
    # content card
    rounded(d,(80,1310,1000,1610),40,(22,31,70,245),(126,83,220,220),3)
    d.text((130,1370),card,font=font(46),fill=(84,229,255,255))
    for j,line in enumerate(textwrap.wrap(desc, width= thirty := 32)):
        d.text((130,1450+j*62),line,font=font(34,False),fill=(238,242,255,255))
    rounded(d,(100,1690,980,1795),35,(46,26,83,235),(255,83,201,230),3)
    d.text((140,1720),flow,font=font(34),fill=(255,255,255,255))
    d.text((70,1850),"AI AGENT  •  OTOMASI  •  KONTROL MANUSIA",font=font(24),fill=(153,174,218,255))
    path=OUT/f"scene-{i+1}.png"
    im.save(path)
    return path

def run(cmd):
    subprocess.run(cmd, check=True)

def main():
    # Combine the four narration beats into one Indonesian narration track.
    narration = " ".join(s[5] for s in SCENES)
    textfile=OUT/"narration.txt"
    textfile.write_text(narration,encoding="utf-8")
    # eSpeak NG is free and runs entirely on the GitHub Actions runner.
    run(["espeak-ng","-v","id","-s","150","-p","48","-a","170","-f",str(textfile),"-w",str(OUT/"voice.wav")])
    images=[make_scene(i,s) for i,s in enumerate(SCENES)]
    clips=[]
    for i,img in enumerate(images):
        clip=OUT/f"clip-{i+1}.mp4"
        # gentle push-in; each section is 30s, no separate final files.
        run(["ffmpeg","-y","-loop","1","-i",str(img),"-t","30","-vf",
             f"scale=1200:2134,zoompan=z='min(1.0+0.00018*on,1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=900:s=1080x1920:fps={FPS},format=yuv420p",
             "-r",str(FPS),"-an","-c:v","libx264","-preset","ultrafast","-crf","25",str(clip)])
        clips.append(clip)
    concat=OUT/"concat.txt"
    concat.write_text("".join(f"file '{p.as_posix()}'\n" for p in clips),encoding="utf-8")
    run(["ffmpeg","-y","-f","concat","-safe","0","-i",str(concat),"-c","copy",str(OUT/"picture.mp4")])
    # Single continuous subtitle file, timed over the 120-second video.
    subs=[]
    for i,s in enumerate(SCENES):
        start=i*30
        end=start+29
        subs.append(f"{i+1}\n00:{start//60:02d}:{start%60:02d},000 --> 00:{end//60:02d}:{end%60:02d},800\n{s[5]}\n")
    (OUT/"captions.srt").write_text("\n".join(subs),encoding="utf-8")
    # Add captions and a subtle generated electronic bed; no external paid service.
    run(["ffmpeg","-y","-i",str(OUT/"picture.mp4"),"-i",str(OUT/"voice.wav"),"-vf",
         "subtitles="+str(OUT/"captions.srt")+":force_style='FontName=DejaVu Sans,FontSize=18,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00101020,BorderStyle=1,Outline=3,Shadow=1,Alignment=2,MarginV=170'",
         "-filter_complex","[1:a]volume=1.0[vo];sine=frequency=110:sample_rate=44100:duration=120,volume=0.025[bed];[vo][bed]amix=inputs=2:duration=first:dropout_transition=2[a]",
         "-map","0:v","-map","[a]","-t","120","-r",str(FPS),"-c:v","libx264","-preset","ultrafast","-crf","24","-c:a","aac","-b:a","128k","-pix_fmt","yuv420p","-movflags","+faststart",str(OUT/"cara-kerja-ai-agent-120-detik.mp4")])
    run(["ffprobe","-v","error","-show_entries","format=duration,size","-of","default=noprint_wrappers=1",str(OUT/"cara-kerja-ai-agent-120-detik.mp4")])
    print("RENDER_OK", OUT/"cara-kerja-ai-agent-120-detik.mp4")

if __name__=="__main__":
    main()
