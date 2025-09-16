# src/sources/soundcloud.py

import click
from .base_source import BaseSource
from typing import List
from rich.console import Console

console = Console()

class SoundCloudSource(BaseSource):
    """
    Proveedor para descargar música de SoundCloud.
    """
    def is_valid_url(self, url: str) -> bool:
        return "soundcloud.com" in url

    def get_source_name(self) -> str:
        return "SoundCloud"

    def download(self, url: str, output_path: str) -> List[str]:
        console.log("[bold red]Este proveedor de SoundCloud aún no está implementado.[/bold red]")
        console.log("Para implementarlo, necesitarás usar una librería como 'soundcloud-dl' o la API de SoundCloud.")
        return []

    def search(self, query: str) -> List[dict]:
        console.log("[bold yellow]La búsqueda en SoundCloud aún no está implementada.[/bold yellow]")
        return []