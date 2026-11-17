#!/usr/bin/env python3
"""
Otimiza fotos para o site (WebP leve, duas larguras).

Uso (na raiz do repositório):
    1. Coloque as fotos originais em _build/fotos/ com o nome da página:
         _build/fotos/seguro-auto.jpg
         _build/fotos/seguro-residencial.png
         ...
       Nomes aceitos: os slugs das páginas (veja PAGINAS em gerar.py)
       e "seguro-alagamento".
    2. python3 _build/otimizar_fotos.py
    3. python3 _build/gerar.py

Saída: img/fotos/<slug>-480.webp, -800.webp e -1200.webp
(cerca de 15 a 150 KB cada). Os originais ficam em _build/ e não são publicados.
"""
import os
import sys

from PIL import Image, ImageOps

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORIGEM = os.path.join(RAIZ, "_build", "fotos")
DESTINO = os.path.join(RAIZ, "img", "fotos")
LARGURAS = (480, 800, 1200)


def main():
    if not os.path.isdir(ORIGEM):
        sys.exit(f"Crie a pasta {ORIGEM} e coloque as fotos lá.")
    os.makedirs(DESTINO, exist_ok=True)
    for nome in sorted(os.listdir(ORIGEM)):
        base, ext = os.path.splitext(nome)
        if ext.lower() not in (".jpg", ".jpeg", ".png", ".webp"):
            continue
        im = ImageOps.exif_transpose(Image.open(os.path.join(ORIGEM, nome))).convert("RGB")
        for w in LARGURAS:
            alvo = im if im.width <= w else im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            saida = os.path.join(DESTINO, f"{base}-{w}.webp")
            alvo.save(saida, "WEBP", quality=72, method=6)
            print(f"{saida}  {os.path.getsize(saida) // 1024} KB")


if __name__ == "__main__":
    main()
