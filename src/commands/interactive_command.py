# src/commands/interactive_command.py

import click
from rich.console import Console
from rich.prompt import Prompt
from rich.table import Table

console = Console()

@click.command(name='interactive', help="🤖 Inicia un modo interactivo de descarga.")
def interactive():
    """
    Inicia un modo interactivo para guiar al usuario.
    """
    console.print("[bold cyan]Bienvenido al modo interactivo de Music-CLI-PRO.[/bold cyan]")
    console.print("Ingresa 'q' para salir en cualquier momento.")
    
    while True:
        mode = Prompt.ask("¿Qué deseas hacer?", choices=["download", "convert", "search", "quit"], default="download")
        if mode == 'quit':
            break

        if mode == 'download':
            url = Prompt.ask("Ingresa la URL de la canción o lista de reproducción")
            if url == 'q': break
            output_dir = Prompt.ask("Ingresa el directorio de salida", default="./downloads")
            
            # Llama al comando de descarga a través del contexto
            from ..cli import cli
            ctx = click.Context(cli)
            ctx.invoke(cli.commands['download'], urls=[url], output=output_dir)

        elif mode == 'search':
            query = Prompt.ask("Ingresa el término de búsqueda")
            if query == 'q': break
            from ..cli import cli
            ctx = click.Context(cli)
            ctx.invoke(cli.commands['search'], query=query)

        elif mode == 'convert':
            file_path = Prompt.ask("Ingresa la ruta del archivo a convertir")
            if file_path == 'q': break
            output_dir = Prompt.ask("Ingresa el directorio de salida", default="./downloads")
            from ..cli import cli
            ctx = click.Context(cli)
            ctx.invoke(cli.commands['convert'], input_file=file_path, output=output_dir)
            
    console.print("[bold green]¡Hasta la próxima![/bold green]")