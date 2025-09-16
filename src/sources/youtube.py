# src/sources/youtube.py

import os
import sys
from pytube import YouTube, Playlist
import click
from .base_source import BaseSource
from typing import List
from rich.console import Console

console = Console()

class YouTubeSource(BaseSource):
    """
    Proveedor para descargar música de YouTube, incluyendo listas de reproducción.
    """
    def is_valid_url(self, url: str) -> bool:
        return "youtube.com" in url or "youtu.be" in url

    def get_source_name(self) -> str:
        return "YouTube"

    def download(self, url: str, output_path: str) -> List[str]:
        downloaded_files = []
        try:
            # Revisa si la URL es de una lista de reproducción
            if 'list=' in url:
                playlist = Playlist(url)
                console.log(f"[bold]Descargando lista de reproducción:[/bold] {playlist.title}")
                for video_url in playlist.video_urls:
                    yt = YouTube(video_url)
                    audio_stream = yt.streams.filter(only_audio=True).first()
                    if audio_stream:
                        console.log(f"  [bold]• Descargando:[/bold] {yt.title}")
                        out_file = audio_stream.download(output_path=output_path)
                        downloaded_files.append(out_file)
            else:
                yt = YouTube(url)
                audio_stream = yt.streams.filter(only_audio=True).first()
                if audio_stream:
                    console.log(f"[bold]Descargando:[/bold] {yt.title}")
                    out_file = audio_stream.download(output_path=output_path)
                    downloaded_files.append(out_file)

        except Exception as e:
            console.log(f"[bold red]❌ Error al descargar de YouTube:[/bold red] {e}")
            sys.exit(1)
        
        return downloaded_files

    def search(self, query: str) -> List[dict]:
        """
        Simulación de búsqueda en YouTube (pytube no tiene una API de búsqueda oficial).
        En un proyecto real, se usaría la API de YouTube.
        """
        # Para un proyecto real, necesitarías la API de YouTube.
        # Aquí se simulan resultados para fines de demostración.
        return [
            {"title": "Ejemplo de Canción 1", "artist": "Artista Ejemplo", "url": "https://www.youtube.com/watch?v=video1"},
            {"title": "Ejemplo de Canción 2", "artist": "Artista Ejemplo", "url": "https://www.youtube.com/watch?v=video2"},
            {"title": "Otra Canción", "artist": "Otro Artista", "url": "https://www.youtube.com/watch?v=video3"},
        ]