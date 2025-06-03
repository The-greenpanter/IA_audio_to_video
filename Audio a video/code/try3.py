import whisper
import moviepy.editor as mp
import requests
import os
import yt_dlp  # Asegúrate de instalar con: pip install yt-dlp

# === CONFIGURACIÓN ===
AUDIO_FILE = "audio.mp3"
DURATION_PER_IMAGE = 10  # Segundos por imagen
IMAGE_SEARCH_URLS = [
    "https://via.placeholder.com/1280x720.png?text=Cristobal+Colon",
    "https://via.placeholder.com/1280x720.png?text=Mapa+Antiguo",
    "https://via.placeholder.com/1280x720.png?text=Puerto+de+Palos"
]
YOUTUBE_URL = "https://www.youtube.com/watch?v=VgbV3s_lcwU"

# === FUNCIÓN: DESCARGAR AUDIO DE YOUTUBE ===
def download_audio(youtube_url, output_filename="audio.mp3"):
    print("Descargando audio de YouTube...")
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_filename,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'quiet': False
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])
    print("✅ Audio descargado.")
    return output_filename

# === PASO 1: DESCARGAR EL AUDIO ===
download_audio(YOUTUBE_URL, AUDIO_FILE)

# === PASO 2: TRANSCRIBIR EL AUDIO ===
print("Transcribiendo audio...")
model = whisper.load_model("base")
result = model.transcribe(AUDIO_FILE)
text = result["text"]
print("📝 Transcripción:\n", text)

# === PASO 3: DESCARGAR IMÁGENES DE FONDO ===
print("Descargando imágenes...")
image_files = []
for idx, url in enumerate(IMAGE_SEARCH_URLS):
    filename = f"image{idx}.jpg"
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)
    image_files.append(filename)

# === PASO 4: CREAR VIDEO CON AUDIO + IMÁGENES ===
print("Creando video...")
audio = mp.AudioFileClip(AUDIO_FILE)
total_duration = audio.duration
image_duration = total_duration / len(image_files)

clips = []
for image in image_files:
    img_clip = mp.ImageClip(image).set_duration(image_duration).resize((1280, 720))
    clips.append(img_clip)

video = mp.concatenate_videoclips(clips).set_audio(audio)

# === PASO 5: EXPORTAR VIDEO ===
print("Exportando video final...")
video.write_videofile("video_final.mp4", fps=24)

# === LIMPIEZA DE IMÁGENES TEMPORALES ===
for file in image_files:
    os.remove(file)

print("🎉 Listo: video_final.mp4 creado.")
