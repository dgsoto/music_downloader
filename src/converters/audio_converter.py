# src/converters/audio_converter.py

import click
import os
from pydub import AudioSegment
from pathlib import Path
from rich.console import Console

console = Console()

def convert_to_mp3(input_file: str, output_dir: str):
    """
    Convierte un archivo de audio o video a formato MP3.
    Requiere la instalación de FFmpeg.
    """
    if not os.path.exists(input_file):
        console.log(f"[bold red]❌ Error: El archivo de entrada no existe: {input_file}[/bold red]")
        return
    
    file_name = Path(input_file).stem
    output_path = Path(output_dir) / f"{file_name}.mp3"

    try:
        console.log(f"  [bold]Convirtiendo:[/bold] {os.path.basename(input_file)} a MP3...")
        # Detecta automáticamente el formato de entrada
        audio = AudioSegment.from_file(input_file)
        audio.export(output_path, format="mp3")
        console.log(f"  [bold green]✅ Conversión completada:[/bold green] {output_path.name}")
    except Exception as e:
        console.log(f"  [bold red]❌ Error durante la conversión:[/bold red] {e}")
        console.log("[bold yellow]  Asegúrate de que FFmpeg esté instalado y en tu PATH.[/bold yellow]")