# src/commands/convert_command.py

import click
from rich.console import Console
from pathlib import Path

from converters import audio_converter


console = Console()

@click.command(name='convert', help="🎶 Convierte un archivo de audio/video a MP3.")
@click.argument('input_file', type=click.Path(exists=True, dir_okay=False))
@click.option('--output', '-o', type=click.Path(file_okay=False, writable=True), default='./downloads', help='Directorio de salida para el archivo convertido.')
def convert(input_file: str, output: str):
    """
    Comando para convertir un archivo a MP3.
    Acepta una ruta de archivo de entrada y un directorio de salida.
    """
    output_path = Path(output)
    output_path.mkdir(parents=True, exist_ok=True)
    console.log(f"El directorio de salida para la conversión es: [bold green]{output_path.resolve()}[/bold green]")
    
    audio_converter.convert_to_mp3(input_file, str(output_path))
    
    console.print("-" * 40)
    console.print("[bold cyan]✨ Proceso de conversión finalizado. ✨[/bold cyan]")
