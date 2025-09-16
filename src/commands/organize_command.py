import click
import os
from pathlib import Path
from rich.console import Console
from rich.prompt import Prompt

console = Console()

def rename_and_organize(file_path: str, title: str, artist: str, output_dir: str) -> str:
    """
    Renombra y organiza un archivo en un formato consistente.
    Formato: "Artista - Título.mp3"
    """
    if not os.path.exists(file_path):
        console.log(f"[bold red]❌ Error: El archivo '{file_path}' no existe.[/bold red]")
        return file_path
    
    file_extension = Path(file_path).suffix
    valid_title = "".join(c for c in title if c.isalnum() or c.isspace()).strip()
    valid_artist = "".join(c for c in artist if c.isalnum() or c.isspace()).strip()
    
    # Maneja el caso de que la información sea inválida
    if not valid_title or not valid_artist:
        console.log(f"[bold yellow]⚠️ Advertencia:[/bold yellow] No se pudo obtener metadatos válidos para renombrar.")
        return file_path
        
    new_name = f"{valid_artist} - {valid_title}{file_extension}"
    new_path = Path(output_dir) / new_name

    try:
        os.rename(file_path, new_path)
        console.log(f"  [bold green]✅ Archivo renombrado a:[/bold green] {new_name}")
        return str(new_path)
    except Exception as e:
        console.log(f"[bold red]❌ Error al renombrar el archivo:[/bold red] {e}")
        return file_path

@click.command(name='organize', help="📁 Renombra y organiza archivos de música en un directorio.")
@click.argument('folder_path', type=click.Path(exists=True, file_okay=False))
def organize(folder_path: str):
    """
    Renombra los archivos en una carpeta para seguir el formato "Artista - Título.mp3".
    """
    console.print(f"[bold]Analizando y organizando la carpeta:[/bold] [cyan]{folder_path}[/cyan]")
    
    # Lógica para encontrar archivos de audio
    supported_extensions = ['.mp3', '.m4a', '.wav', '.flac', '.ogg']
    files_to_organize = [
        f for f in Path(folder_path).iterdir()
        if f.is_file() and f.suffix.lower() in supported_extensions
    ]
    
    if not files_to_organize:
        console.log("[bold yellow]No se encontraron archivos de música soportados para organizar.[/bold yellow]")
        return

    # Procesa cada archivo
    for file_path in files_to_organize:
        # Aquí puedes implementar una lógica de búsqueda de metadatos más avanzada
        file_name = file_path.stem
        parts = file_name.split(" - ")
        if len(parts) >= 2:
            artist = parts[0].strip()
            title = parts[1].strip()
            
            rename_and_organize(str(file_path), title, artist, folder_path)
        else:
            console.log(f"[bold yellow]⚠️ Archivo omitido:[/bold yellow] '{file_path.name}' no tiene el formato 'Artista - Título'.")

    console.print("-" * 40)
    console.print("[bold green]✨ Organización finalizada. ✨[/bold green]")
