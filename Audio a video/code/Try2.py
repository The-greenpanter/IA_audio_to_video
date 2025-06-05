import whisper
import moviepy.editor as mp
import requests
import os
import yt_dlp
from PIL import Image
import unicodedata

def limpiar_texto(texto):
    # Reemplaza caracteres mal codificados comunes
    reemplazos = {
        '¾': 'ó',
        'ß': 'á',
        '³': 'ó',
        '¡': 'í',
        'è': 'é',
        '¥': 'ñ',
        '¨': 'ú',
    }
    for k, v in reemplazos.items():
        texto = texto.replace(k, v)
    
    # Elimina tildes excepto la ñ
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn' or c in 'ñÑ'
    )
    return texto


# === CONFIGURACIÓN ===
AUDIO_FILE = "audio.mp3"  # Cambia esto por tu archivo
DURATION_PER_IMAGE = 10  # segundos por imagen
IMAGE_SEARCH_URLS = [
    "https://via.placeholder.com/1280x720.png?text=Cristobal+Colon",
    "https://via.placeholder.com/1280x720.png?text=Mapa+Antiguo",
    "https://via.placeholder.com/1280x720.png?text=Puerto+de+Palos"
]
# 👉 Reemplaza este link con el tuyo
YOUTUBE_URL = "https://www.youtube.com/watch?v=VgbV3s_lcwU&ab_channel=cultopedia"  # Diana Uribe - Historia del Medio Oriente - Cap. 01 Origen de la Civilización

# Paso 1: Descargar solo el audio del video
def download_audio(youtube_url, output_filename="audio.mp3"):
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
    return output_filename

download_audio(YOUTUBE_URL, AUDIO_FILE)

# === 1. TRANSCRIBE EL AUDIO ===
print("Transcribiendo audio...")
model = whisper.load_model("base")
result = model.transcribe(AUDIO_FILE)
text = limpiar_texto(result["text"])
print("Transcripción:", text)

# Guardar transcripción en un archivo
with open("transcripcion.txt", "w", encoding="utf-8") as f:
    f.write(text)


# === 2. DESCARGA IMÁGENES ===
print("Descargando imágenes...")
image_files = []
for idx, url in enumerate(IMAGE_SEARCH_URLS):
    filename = f"image{idx}.jpg"
    r = requests.get(url)
    with open(filename, "wb") as f:
        f.write(r.content)
    image_files.append(filename)


# === 3. CREA CLIPS DE IMAGEN CON AUDIO ===
print("Creando clips...")
clips = []
audio = mp.AudioFileClip(AUDIO_FILE)
total_duration = audio.duration
image_duration = total_duration / len(image_files)

for image in image_files:
    img_clip = mp.ImageClip(image).set_duration(image_duration).resize((1280, 720))
    clips.append(img_clip)

video = mp.concatenate_videoclips(clips).set_audio(audio)

# === 4. EXPORTA EL VIDEO FINAL ===
print("Exportando video final...")
video.write_videofile("video_final.mp4", fps=24)

# === 5. LIMPIEZA ===
for file in image_files:
    os.remove(file)

print("✅ Listo: video_final.mp4 creado.")
