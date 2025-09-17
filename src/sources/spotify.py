import click
import os
from .base_source import BaseSource
from .youtube import YouTubeSource
from typing import List
from rich.console import Console
from rich.prompt import Prompt
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

console = Console()

class SpotifySource(BaseSource):
    """
    Proveedor para descargar música desde Spotify.
    Se usa la API de Spotify para obtener metadatos y luego se busca la canción en YouTube.
    """
    def __init__(self):
        super().__init__()
        try:
            client_id = os.environ.get("SPOTIPY_CLIENT_ID")
            client_secret = os.environ.get("SPOTIPY_CLIENT_SECRET")
            if not client_id or not client_secret:
                console.log("[bold red]❌ Error:[/bold red] Variables de entorno SPOTIPY_CLIENT_ID y SPOTIPY_CLIENT_SECRET no encontradas.")
                console.log("Obtén tus credenciales en el 'Spotify Developer Dashboard'.")
                self.sp = None
            else:
                self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))
                self.youtube_source = YouTubeSource()
        except Exception as e:
            console.log(f"[bold red]❌ Error al inicializar Spotipy:[/bold red] {e}")
            self.sp = None

    def is_valid_url(self, url: str) -> bool:
        return "spotify.com" in url

    def get_source_name(self) -> str:
        return "Spotify"

    def download(self, url: str, output_path: str) -> List[str]:
        if not self.sp:
            return []
        
        console.log(f"[bold]Analizando URL de Spotify:[/bold] {url}")
        
        # Lógica para manejar URLs de tracks o playlists
        if "track" in url:
            try:
                track = self.sp.track(url)
                title = track['name']
                artist = track['artists'][0]['name']
                query = f"{artist} - {title} official audio"
                
                console.log(f"  [bold]Encontrado:[/bold] '{title}' de {artist}. Buscando en YouTube...")
                
                # Usamos el proveedor de YouTube para la descarga real
                youtube_results = self.youtube_source.search(query)
                if youtube_results:
                    return self.youtube_source.download(youtube_results[0]['url'], output_path)
                else:
                    console.log("[bold yellow]No se encontraron resultados en YouTube para descargar.[/bold yellow]")
                    return []
            except Exception as e:
                console.log(f"[bold red]❌ Error al obtener detalles del track:[/bold red] {e}")
                return []
        
        elif "playlist" in url:
            try:
                playlist_id = url.split('/')[-1].split('?')[0]
                playlist_items = self.sp.playlist_items(playlist_id)
                
                downloaded_files = []
                for item in playlist_items['items']:
                    track = item['track']
                    title = track['name']
                    artist = track['artists'][0]['name']
                    query = f"{artist} - {title} official audio"
                    
                    console.log(f"  [bold]Procesando track de playlist:[/bold] '{title}' de {artist}")
                    youtube_results = self.youtube_source.search(query)
                    if youtube_results:
                        files = self.youtube_source.download(youtube_results[0]['url'], output_path)
                        downloaded_files.extend(files)
                    else:
                        console.log(f"[bold yellow]No se encontraron resultados en YouTube para '{title}'.[/bold yellow]")
                
                return downloaded_files
            except Exception as e:
                console.log(f"[bold red]❌ Error al procesar la playlist:[/bold red] {e}")
                return []
        
        else:
            console.log("[bold red]❌ URL de Spotify no soportada. Solo tracks y playlists.[/bold red]")
            return []

    def search(self, query: str) -> List[dict]:
        if not self.sp:
            return []
        
        console.log(f"[bold]Buscando en Spotify:[/bold] {query}")
        try:
            results = self.sp.search(q=query, limit=10, type='track')
            formatted_results = []
            for item in results['tracks']['items']:
                formatted_results.append({
                    'title': item['name'],
                    'artist': item['artists'][0]['name'],
                    'url': item['external_urls']['spotify']
                })
            return formatted_results
        except Exception as e:
            console.log(f"[bold red]❌ Error en la búsqueda de Spotify:[/bold red] {e}")
            return []