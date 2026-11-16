# Catatan Animasi & Art Direction

## Format dan komposisi
- Kanvas final: 1080×1920, portrait 9:16, 30 fps, tepat 30 detik per bagian.
- Safe area: sisakan 90 px kiri/kanan, 170 px atas, 300 px bawah untuk UI TikTok.
- Subtitle di tengah-bawah (sekitar 70–78% tinggi frame), maksimal dua baris, 6–8 kata per tampilan.
- Subtitle putih tebal, outline hitam tipis + shadow lembut; animasi masuk per kata seperti efek mengetik.
- Jangan menempatkan teks penting di tepi layar.

## Identitas visual
- Latar: navy #080D20 dan gradasi ungu gelap #20113D.
- Aksen cyan #17DFF5 dan magenta #E64CFF; hijau #48E59B hanya untuk status berhasil; merah #FF5368 untuk error.
- Ava adalah robot mungil dengan badan rounded navy, layar wajah gelap, mata cyan, antena, dan panel hologram.
- Ikon flat line-art dengan ketebalan konsisten; sudut rounded; hindari foto, wajah realistis, dan stock footage.
- Glow neon hanya sebagai aksen, jangan sampai mengurangi keterbacaan.

## Gerak dan transisi
- Gunakan easing ease-out untuk elemen masuk dan ease-in untuk keluar.
- Transisi antarbeat: swipe cepat, zoom punch, glitch 2–3 frame, morph shape, atau neon line wipe.
- Gerakan utama mengikuti VO: ikon muncul saat disebut, node menyala ketika langkah dijelaskan, checklist centang saat kalimat selesai.
- Kamera virtual: punch-in 1.04–1.08× pada kata kunci, parallax halus pada panel.
- Hindari shake berlebihan dan teks yang bergerak terlalu cepat untuk dibaca.

## Audio
- VO Indonesia, artikulasi jelas, nada muda energik, tempo natural.
- Musik electronic upbeat minimal, build-up perlahan di bagian 1–3, klimaks ringan bagian 4 lalu fade.
- SFX harus singkat dan tidak menutupi VO: ding, whoosh, UI click, data stream, robotic beep, drawer open, blueprint unfold, error buzz, retry click, approval chime, send whoosh.
- Target mix: VO dominan; musik sekitar -22 LUFS relatif terhadap VO; SFX pendek sekitar -16 dB peak di bawah VO.

## Continuity
- Bagian 1 berakhir dengan kartu konteks melayang ke kanan; Bagian 2 menerima kartu itu.
- Bagian 2 berakhir pada panel tools; Bagian 3 membuka panel yang sama.
- Bagian 3 berakhir dengan kartu draft laporan; Bagian 4 menerima kartu tersebut.
- Bagian 4 menutup dengan CTA statis satu detik, musik fade-out, tanpa loop paksa.

## QA sebelum final
- Pastikan durasi tiap file tepat 30.000 detik dan kompilasi tepat 120.000 detik.
- Periksa sinkronisasi VO/SRT per beat; tidak ada subtitle terpotong atau lebih dari 8 kata per layar.
- Periksa audio peak/clipping, frame hitam, flicker, konsistensi Ava, dan keterbacaan pada layar ponsel.
