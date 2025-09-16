# src/cli.py

import click
import sys
import os
import glob
import pyfiglet
from pathlib import Path
from typing import List, Optional
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.status import Status
from rich.progress import Progress, SpinnerColumn, TextColumn

# Importamos los módulos de nuestra estructura modular
from sources.base_source import BaseSource
from sources.youtube import YouTubeSource
#from .sources.youtube import YouTubeSource
from sources.soundcloud import SoundCloudSource
from converters import audio_converter
from metadata import id3_tagger

# Instancia de la consola de `rich` para una UI atractiva
console = Console()


def print_banner():
    ascii_banner = pyfiglet.figlet_format("Music-CLI-PRO", font="slant")
    console.print(Panel(ascii_banner, style="bold magenta", expand=False))
    console.print("[bold cyan]CLI profesional para descargar, convertir y gestionar música.[/bold cyan]\n")

print_banner()

def get_providers() -> List[BaseSource]:
    """Retorna una lista de todos los proveedores de descarga disponibles."""
    return [YouTubeSource(), SoundCloudSource()]

# --- Funcionalidades de Archivo ---

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

# --- Configuración de la CLI usando `click` ---

@click.group(help="CLI profesional para descargar, convertir y gestionar música.")
@click.version_option(version='3.0.0', prog_name='Music-CLI-PRO')
def cli():
    """Punto de entrada principal de la aplicación."""
    pass

@cli.command(help="Busca música en las fuentes disponibles.")
@click.argument('query', type=str)
def search(query: str):
    """
    Busca música en las fuentes disponibles.
    """
    providers = get_providers()
    
    with Status("Buscando...", spinner="dots") as status:
        all_results = []
        for provider in providers:
            status.update(f"Buscando '{query}' en [bold cyan]{provider.get_source_name()}[/bold cyan]...")
            results = provider.search(query)
            all_results.extend(results)
    
    if not all_results:
        console.log("[bold red]No se encontraron resultados.[/bold red]")
        sys.exit(1)

    table = Table(title=f"Resultados de la búsqueda para '{query}'", show_header=True, header_style="bold blue")
    table.add_column("ID", style="dim", width=5)
    table.add_column("Título", style="cyan")
    table.add_column("Artista", style="magenta")
    table.add_column("URL")
    
    for i, result in enumerate(all_results):
        table.add_row(str(i), result['title'], result['artist'], result['url'])
    
    console.print(table)
    
    choice = Prompt.ask("Ingresa el ID del resultado para descargar, o cualquier otra cosa para cancelar")
    try:
        index = int(choice)
        if 0 <= index < len(all_results):
            download_url = all_results[index]['url']
            
            # Instancia el downloader y descarga
            providers_for_download = get_providers()
            source_found = False
            for provider in providers_for_download:
                if provider.is_valid_url(download_url):
                    console.log(f"[bold green]Fuente identificada:[/bold green] {provider.get_source_name()}")
                    files = provider.download(download_url, './downloads')
                    
                    for file_path in files:
                        console.log("Aplicando metadatos y renombrando...")
                        id3_tagger.apply_tags(file_path, all_results[index]['title'], all_results[index]['artist'])
                        rename_and_organize(file_path, all_results[index]['title'], all_results[index]['artist'], './downloads')
                    source_found = True
                    break
            if not source_found:
                 console.log("[bold red]❌ La URL seleccionada no es soportada para la descarga.[/bold red]")
        else:
            console.log("[bold red]ID inválido. Cancelando.[/bold red]")
    except ValueError:
        console.log("Cancelando.")


@cli.command(help="Descarga una o varias URLs.")
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

@cli.command(help="Inicia un modo interactivo de descarga.")
def interactive():
    """
    Inicia un modo interactivo para guiar al usuario.
    """
    console.print("[bold cyan]Bienvenido al modo interactivo de Music-CLI-PRO.[/bold cyan]")
    console.print("Ingresa 'q' para salir en cualquier momento.")
    
    while True:
        mode = Prompt.ask("¿Qué deseas hacer?", choices=["download", "convert", "organize", "search", "quit"], default="download")
        if mode == 'quit':
            break

        if mode == 'download':
            url = Prompt.ask("Ingresa la URL de la canción o lista de reproducción")
            if url == 'q': break
            output_dir = Prompt.ask("Ingresa el directorio de salida", default="./downloads")
            
            # Llama al comando de descarga
            ctx = click.Context(cli)
            ctx.invoke(download, urls=[url], output=output_dir)

        elif mode == 'search':
            query = Prompt.ask("Ingresa el término de búsqueda")
            if query == 'q': break
            ctx = click.Context(cli)
            ctx.invoke(search, query=query)

        elif mode == 'convert':
            file_path = Prompt.ask("Ingresa la ruta del archivo a convertir")
            if file_path == 'q': break
            output_dir = Prompt.ask("Ingresa el directorio de salida", default="./downloads")
            audio_converter.convert_to_mp3(file_path, output_dir)
            
        elif mode == 'organize':
            folder_path = Prompt.ask("Ingresa la carpeta a organizar", default="./downloads")
            # Implementar lógica de organización avanzada aquí
            console.print("[bold yellow]La funcionalidad de organización de carpetas está en desarrollo.[/bold yellow]")

    console.print("[bold green]¡Hasta la próxima![/bold green]")


@cli.command(help="Convierte un archivo de audio/video a MP3.")
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False))
@click.option('--output', '-o', type=click.Path(file_okay=False, writable=True), default='./downloads', help='Directorio de salida para el archivo convertido.')
def convert(input_file: str, output: str):
    """
    Comando para convertir un archivo.
    Acepta una ruta de archivo de entrada y un directorio de salida.
    """
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    console.log(f"El directorio de salida para la conversión es: [bold green]{output_path.resolve()}[/bold green]")
    
    audio_converter.convert_to_mp3(input_file, str(output_path))
    
    console.print("-" * 40)
    console.print("[bold cyan]✨ Proceso de conversión finalizado. ✨[/bold cyan]")

if __name__ == '__main__':
    cli()