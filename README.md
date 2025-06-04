# Audio a Video con Imágenes Sincronizadas /Diana Uribe Historias del mundo

Este proyecto descarga el audio de un video de YouTube, transcribe el contenido usando Whisper, y crea un video combinando imágenes con la pista de audio sincronizada.

---

## Requisitos

- Python 3.8+
- FFmpeg (debe estar instalado y en el PATH)
- Las siguientes librerías Python:

```bash
pip install whisper moviepy requests yt-dlp pillow
````

---

## Uso

1. Clona o descarga este repositorio.

2. Modifica las variables en el script principal:

   * `YOUTUBE_URL`: URL del video de YouTube del cual quieres extraer el audio.
   * `IMAGE_SEARCH_URLS`: lista de URLs de imágenes para usar en el video (o usa imágenes locales).
   * `AUDIO_FILE`: nombre del archivo de audio resultante.

3. Ejecuta el script:

```bash
python nombre_del_script.py
```

4. El video final se guardará como `video_final.mp4` en la carpeta actual.

---

## Notas

* Asegúrate de tener conexión a internet para descargar el audio y las imágenes (a menos que uses imágenes locales).
* El script crea clips de imágenes y los sincroniza con la duración del audio.
* Puedes modificar la duración por imagen cambiando la variable `DURATION_PER_IMAGE` o ajustando el código para usar la duración total dividida entre imágenes.

---

## Posibles errores comunes

* **Error de conexión para descargar imágenes:** verifica tu conexión y que las URLs sean accesibles.
* **FFmpeg no encontrado:** asegúrate de tener FFmpeg instalado y configurado en tu PATH.
* **Problemas con Whisper:** revisa que la librería esté correctamente instalada y que tu sistema tenga soporte para modelos PyTorch.

---

## Licencia

Este proyecto es libre para uso personal y educativo.



```

¿Quieres que te prepare el README en un archivo listo para usar?
```
