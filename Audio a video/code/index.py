import os
import requests
from moviepy.editor import *
import yt_dlp

# 👉 Reemplaza este link con el tuyo
YOUTUBE_URL = "https://www.youtube.com/watch?v=VgbV3s_lcwU&ab_channel=cultopedia"  # Diana Uribe - Historia del Medio Oriente - Cap. 01 Origen de la Civilización

# Paso 1: Descargar solo el audio del video
def download_audio(youtube_url, output_filename="audio"):
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
    return output_filename

# Paso 2: Descargar una imagen por defecto
def download_default_image(image_filename="default.jpg"):
    print("Descargando imagen por defecto...")
    url = "https://via.placeholder.com/1280x720.png?text=Tu+Audio+Aqui"
    response = requests.get(url)
    with open(image_filename, 'wb') as f:
        f.write(response.content)
    return image_filename

# Paso 3: Crear el video
def create_video(audio_file, image_file, output_video="video_final.mp4"):
    print("Creando video...")
    audio_clip = AudioFileClip(audio_file)
    image_clip = ImageClip(image_file).set_duration(audio_clip.duration)
    image_clip = image_clip.set_audio(audio_clip)
    image_clip = image_clip.set_fps(24).resize(height=720)  # ajustar tamaño
    image_clip.write_videofile(output_video, codec='libx264', audio_codec='aac')

# Ejecutar el flujo
audio = download_audio(YOUTUBE_URL)
image = download_default_image()
create_video(audio, image)
