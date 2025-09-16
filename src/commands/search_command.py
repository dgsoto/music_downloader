# src/commands/search_command.py

import click
import sys
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table
from rich.status import Status
from typing import List

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
    # Lógica de renombrado (copiada del comando download)
    pass

@click.command(name='search', help="🔍 Busca música en las fuentes disponibles.")
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
                    # Llama al comando download del otro archivo
                    from ..cli import cli
                    ctx = click.Context(cli)
                    ctx.invoke(cli.commands['download'], urls=[download_url], output='./downloads')
                    source_found = True
                    break
            if not source_found:
                 console.log("[bold red]❌ La URL seleccionada no es soportada para la descarga.[/bold red]")
        else:
            console.log("[bold red]ID inválido. Cancelando.[/bold red]")
    except ValueError:
        console.log("Cancelando.")