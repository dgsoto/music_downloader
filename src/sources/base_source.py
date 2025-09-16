from abc import ABC, abstractmethod
from typing import List

class BaseSource(ABC):
    """
    Clase base abstracta que define la interfaz para los proveedores de fuentes de descarga.
    Cada nueva fuente (YouTube, SoundCloud, etc.) debe heredar de esta clase.
    """
    @abstractmethod
    def is_valid_url(self, url: str) -> bool:
        """Verifica si la URL es válida para esta fuente."""
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """Devuelve el nombre legible de la fuente."""
        pass

    @abstractmethod
    def download(self, url: str, output_path: str) -> List[str]:
        """
        Descarga el contenido de la URL en la ruta especificada.
        Retorna una lista de las rutas de los archivos descargados.
        """
        pass

    @abstractmethod
    def search(self, query: str) -> List[dict]:
        """
        Busca contenido en la fuente y retorna una lista de resultados.
        Cada resultado es un diccionario con 'title', 'artist' y 'url'.
        """
        pass