# src/cli.py

import click
import pyfiglet
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from commands import convert_command, download_command, interactive_command, search_command, organize_command

console = Console()

ascii_banner = pyfiglet.figlet_format("Music-CLI-PRO", font="slant")
console.print(Panel(ascii_banner, style="bold magenta", expand=False),  justify="center")
console.print("[bold cyan]By Diego Gonzales Soto.[/bold cyan]\n", justify="center")

# --- Configuración de la CLI usando `click` ---

@click.group(
    help="CLI profesional para descargar, convertir y gestionar música.",
    no_args_is_help=True
)
@click.version_option(version='3.0.0', prog_name='Music-CLI-PRO')
def cli():
    """Punto de entrada principal de la aplicación."""
    # Impresión de la tabla de comandos estilizada
    table = Table(title="Comandos Disponibles", show_header=True, header_style="bold magenta", box=box.ROUNDED)
    table.add_column("Comando", style="bold cyan")
    table.add_column("Descripción", style="dim")
    
    # Agrega los comandos y sus descripciones con iconos
    commands = [
        ("download", "📥 Descarga una o varias URLs de música."),
        ("search", "🔍 Busca música en las fuentes disponibles."),
        ("interactive", "🤖 Inicia un modo interactivo de descarga."),
        ("convert", "🎶 Convierte un archivo de audio/video a MP3."),
        ("organize", "📁 Renombra y organiza archivos de música en un directorio."),
    ]

    for name, help_text in commands:
        table.add_row(name, help_text)

    # Imprime el banner y la tabla de comandos
    console.print("\n", justify="center")
    console.print("[bold yellow]Music-CLI-PRO[/bold yellow]", justify="center")
    console.print("[dim]Herramienta de descarga y gestión de música[/dim]", justify="center")
    console.print("\n", justify="center")
    console.print(table, justify="center")
    console.print("\n[bold]Para más detalles, usa:[/bold] [italic]python src/cli.py <comando> --help[/italic]", style="dim")


# Registra los comandos desde los módulos
cli.add_command(download_command.download)
cli.add_command(search_command.search)
cli.add_command(interactive_command.interactive)
cli.add_command(convert_command.convert)
cli.add_command(organize_command.organize)

if __name__ == '__main__':
    cli()