#!/usr/bin/env python3
"""Coloca texto sobre uma foto, no tamanho de post do Instagram, com contraste garantido.

Exemplo:
  python3 texto_sobre_foto.py --entrada foto.jpg --texto "Título do post" \
      --saida post.jpg --tamanho 1080x1350 --posicao baixo
Requer: pip install pillow
"""
import argparse
import sys

from PIL import Image, ImageDraw, ImageFont, ImageOps

FONTES_PADRAO = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "C:\\Windows\\Fonts\\arialbd.ttf",
]


def achar_fonte(caminho, tamanho):
    if caminho:
        try:
            return ImageFont.truetype(caminho, tamanho)
        except OSError:
            sys.exit(f"Não consegui abrir a fonte {caminho!r}. Confira o caminho do arquivo .ttf.")
    for c in FONTES_PADRAO:
        try:
            return ImageFont.truetype(c, tamanho)
        except OSError:
            continue
    sys.exit("Nenhuma fonte encontrada. Passe uma com --fonte /caminho/fonte.ttf")


def quebrar(draw, texto, fonte, largura_max):
    linhas = []
    for paragrafo in texto.split("\n"):
        atual = ""
        for palavra in paragrafo.split():
            teste = f"{atual} {palavra}".strip()
            if draw.textlength(teste, font=fonte) <= largura_max:
                atual = teste
            else:
                if atual:
                    linhas.append(atual)
                atual = palavra
        linhas.append(atual)
    return linhas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--entrada", required=True)
    ap.add_argument("--texto", required=True)
    ap.add_argument("--saida", required=True)
    ap.add_argument("--tamanho", default="1080x1350", help="LARGURAxALTURA")
    ap.add_argument("--posicao", choices=["cima", "centro", "baixo"], default="baixo")
    ap.add_argument("--fonte")
    ap.add_argument("--cor", default="#FFFFFF")
    ap.add_argument("--escurecer", type=float, default=0.45, help="0 a 0.9: força da camada escura")
    ap.add_argument("--tamanho-fonte", type=int, default=0, help="0 = automático")
    a = ap.parse_args()

    try:
        largura, altura = (int(x) for x in a.tamanho.lower().split("x"))
    except ValueError:
        sys.exit('Use --tamanho no formato 1080x1350')
    if not 0 <= a.escurecer <= 0.9:
        sys.exit("--escurecer deve ficar entre 0 e 0.9")

    foto = Image.open(a.entrada)
    foto = ImageOps.exif_transpose(foto).convert("RGB")
    foto = ImageOps.fit(foto, (largura, altura), method=Image.LANCZOS, centering=(0.5, 0.4))

    camada = Image.new("RGBA", (largura, altura), (0, 0, 0, int(255 * a.escurecer)))
    quadro = Image.alpha_composite(foto.convert("RGBA"), camada)
    draw = ImageDraw.Draw(quadro)

    margem = int(largura * 0.09)
    area = largura - 2 * margem
    tam = a.tamanho_fonte or int(largura * 0.085)
    while True:
        fonte = achar_fonte(a.fonte, tam)
        linhas = quebrar(draw, a.texto, fonte, area)
        entrelinha = int(tam * 1.2)
        bloco = entrelinha * len(linhas)
        if (bloco <= altura * 0.5 and all(draw.textlength(l, font=fonte) <= area for l in linhas)) or tam <= 24:
            break
        tam -= 4

    if a.posicao == "cima":
        y = int(altura * 0.10)
    elif a.posicao == "centro":
        y = (altura - bloco) // 2
    else:
        y = int(altura * 0.90) - bloco

    for linha in linhas:
        x = (largura - draw.textlength(linha, font=fonte)) // 2
        draw.text((x, y), linha, font=fonte, fill=a.cor, stroke_width=max(2, tam // 22), stroke_fill=(0, 0, 0))
        y += entrelinha

    saida = quadro.convert("RGB")
    saida.save(a.saida, quality=92)
    print(f"Imagem gerada: {a.saida} ({largura}x{altura}, fonte {tam}px, {len(linhas)} linha(s))")


if __name__ == "__main__":
    main()
