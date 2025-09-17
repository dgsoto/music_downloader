# src/sources/youtube.py

import os
import sys
from pytube import YouTube, Playlist
#from base_source import BaseSource
from typing import List
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from sources.base_source import BaseSource

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
            if 'list=' in url:
                playlist = Playlist(url)
                console.print(f"[bold magenta]Descargando playlist:[/bold magenta] {playlist.title}")
                with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}")) as progress:
                    task = progress.add_task("Descargando videos...", total=len(playlist.video_urls))
                    for video_url in playlist.video_urls:
                        yt = YouTube(video_url)
                        audio_stream = yt.streams.filter(only_audio=True).first()
                        if audio_stream:
                            safe_title = self._sanitize_filename(yt.title)
                            out_file = audio_stream.download(output_path=output_path, filename=f"{safe_title}.mp3")
                            downloaded_files.append(out_file)
                            progress.console.print(f"  [green]✔[/green] {yt.title}")
                        progress.advance(task)
            else:
                print("url: ", url)
                yt = YouTube(url)

                print("yt.title: ", yt.__dict__)
                print("yt.author: ", yt.stream_monostate.__dict__)
                audio_stream = yt.streams.filter(only_audio=True).first()
                if audio_stream:   
                    safe_title = self._sanitize_filename(yt.title)
                    out_file = audio_stream.download(output_path=output_path, filename=f"{safe_title}.mp3")
                    downloaded_files.append(out_file)
                    console.print(f"[green]✔ Descargado:[/green] {yt.title}")
                else:
                    console.print(f"[red]No se encontró stream de audio para este video.[/red]")
        except Exception as e:
            console.print(f"[bold red]❌ Error al descargar de YouTube:[/bold red] {e}")
            sys.exit(1)
        return downloaded_files

    def search(self, query: str) -> List[dict]:
        """
        Simulación de búsqueda en YouTube (pytube no tiene una API de búsqueda oficial).
        """
        return [
            {"title": "Ejemplo de Canción 1", "artist": "Artista Ejemplo", "url": "https://www.youtube.com/watch?v=video1"},
            {"title": "Ejemplo de Canción 2", "artist": "Artista Ejemplo", "url": "https://www.youtube.com/watch?v=video2"},
            {"title": "Otra Canción", "artist": "Otro Artista", "url": "https://www.youtube.com/watch?v=video3"},
        ]

    def _sanitize_filename(self, name: str) -> str:
        """Limpia el nombre del archivo para evitar caracteres inválidos."""
        return "".join(c for c in name if c.isalnum() or c in " .-_").rstrip()