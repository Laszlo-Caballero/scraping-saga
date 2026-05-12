import re
import unicodedata
import aiohttp
from typing import Callable, Awaitable, TypeVar
import os

T = TypeVar("T")


def singleton():
    def decorator(cls):
        instances = {}

        def get_instance(*args, **kwargs):
            if cls not in instances:
                instances[cls] = cls(*args, **kwargs)
            return instances[cls]

        return get_instance

    return decorator



class Utils:

    def to_slug(self, text: str) -> str:
        # normalizar acentos (á → a, ñ → n, etc.)
        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ascii", "ignore").decode("ascii")

        # minúsculas
        text = text.lower()

        # reemplazar cualquier cosa que no sea letra/número por guiones
        text = re.sub(r"[^a-z0-9]+", "-", text)

        # quitar guiones al inicio/fin
        text = text.strip("-")

        return text
    
    async def download_image(self, url: str, filename: str, destiny: str) -> None:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    
                    os.makedirs(f"data/images/{destiny}", exist_ok=True)
                    
                    
                    with open(f"data/images/{destiny}/{filename}.webp", "wb") as f:
                        f.write(await resp.read())
                    print("Imagen guardada:", filename)
                else:
                    print("Error:", resp.status)
                    
    async def error_wrapper(self, func: Callable[[], Awaitable[T]]) -> tuple[str | None, T | None]:
        try:
            result = await func()
            return None, result
        except Exception as e:
            print(f"Error en función {func.__name__}: {e}")
            return str(e), None