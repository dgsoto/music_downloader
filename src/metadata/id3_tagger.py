# src/metadata/id3_tagger.py

import mutagen
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TXXX, TCON, USLT
import click
from rich.console import Console

console = Console()

def apply_tags(file_path: str, title: str, artist: str, album: str = None):
    """
    Aplica etiquetas de metadatos (ID3) a un archivo de audio.
    """
    try:
        # Abre el archivo para etiquetado
        audio = mutagen.File(file_path, easy=True)
        if not audio:
            console.log(f"[bold red]❌ Error:[/bold red] Formato de archivo no soportado para etiquetado: {file_path}")
            return False

        audio['title'] = title
        audio['artist'] = artist
        if album:
            audio['album'] = album
        
        audio.save()
        console.log(f"  [bold green]✅ Metadatos aplicados:[/bold green] {title} por {artist}")
        return True
    except Exception as e:
        console.log(f"[bold red]❌ Error al aplicar metadatos:[/bold red] {e}")
        return False

def get_metadata_from_source(file_path: str) -> dict:
    """
    Simulación de búsqueda de metadatos. En un proyecto real, se usaría
    una API como la de MusicBrainz.
    """
    # En un proyecto real, buscarías metadatos en MusicBrainz o similar.
    # Aquí simulamos la obtención de metadatos del nombre del archivo.
    base_name = file_path.split("/")[-1].replace(".mp4", "").replace(".mp3", "")
    parts = base_name.split(" - ")
    if len(parts) >= 2:
        artist = parts[0].strip()
        title = parts[1].strip()
        return {"title": title, "artist": artist}
    return {"title": base_name, "artist": "Desconocido"}