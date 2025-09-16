import click
import os
import sys
from rich.console import Console
from rich.status import Status
from pathlib import Path
from typing import List

from metadata import id3_tagger
from sources.soundcloud import SoundCloudSource
from sources.youtube import YouTubeSource
#from ..sources.youtube import YouTubeSource
#from ..sources.soundcloud import SoundCloudSource
#from ..metadata import id3_tagger

console = Console()

def get_providers():
    """Retorna una lista de todos los proveedores de descarga disponibles."""
    return [YouTubeSource(), SoundCloudSource()]

def rename_and_organize(file_path: str, title: str, artist: str, output_dir: str) -> str:
    """
    Renombra y organiza un archivo en un formato consistente.
    Formato: "Artista - Título.mp3"
    """
    file_extension = Path(file_path).suffix
    valid_title = "".join(c for c in title if c.isalnum() or c.isspace()).strip()
    valid_artist = "".join(c for c in artist if c.isalnum() or c.isspace()).strip()
    new_name = f"{valid_artist} - {valid_title}{file_extension}"
    new_path = Path(output_dir) / new_name

    try:
        os.rename(file_path, new_path)
        console.log(f"  [bold green]✅ Archivo renombrado a:[/bold green] {new_name}")
        return str(new_path)
    except Exception as e:
        console.log(f"[bold red]❌ Error al renombrar el archivo:[/bold red] {e}")
        return file_path

@click.command(name='download', help="📥 Descarga una o varias URLs de música.")
@click.argument('urls', nargs=-1)
@click.option('--output', '-o', type=click.Path(file_okay=False, writable=True), default='./downloads', help='Directorio de salida.')
def download(urls: List[str], output: str):
    """
    Descarga una o varias URLs. Acepta URLs de canciones o listas de reproducción.
    """
    if not urls:
        console.log("[bold red]❌ Error:[/bold red] Debes proporcionar al menos una URL.")
        return

    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    console.log(f"El directorio de descarga es: [bold green]{output_path.resolve()}[/bold green]")
    
    providers = get_providers()
    
    for url in urls:
        console.print("-" * 40)
        source_found = False
        with console.status("Analizando URL...") as status:
            for provider in providers:
                if provider.is_valid_url(url):
                    status.stop()
                    console.log(f"[bold green]Fuente identificada:[/bold green] {provider.get_source_name()}")
                    files = provider.download(url, str(output_path))
                    
                    for file_path in files:
                        metadata = id3_tagger.get_metadata_from_source(file_path)
                        if metadata:
                            id3_tagger.apply_tags(file_path, metadata['title'], metadata['artist'])
                            rename_and_organize(file_path, metadata['title'], metadata['artist'], str(output_path))
                        
                    source_found = True
                    break
        
        if not source_found:
            console.log(f"[bold red]❌ URL no soportada:[/bold red] {url}")
    
    console.print("-" * 40)
    console.print("[bold cyan]✨ Proceso de descarga finalizado. ✨[/bold cyan]")
