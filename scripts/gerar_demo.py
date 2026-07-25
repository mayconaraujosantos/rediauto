"""Gera assets/demo.png: ilustracao 'antes/depois' do comportamento do app para o README."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

LARGURA, ALTURA = 900, 380
FUNDO = (243, 244, 246)
TEXTO = (17, 24, 39)
COR_JANELA = (156, 163, 175)
COR_ESQUERDA = (59, 130, 246)
COR_DIREITA = (16, 185, 129)
COR_BARRA = (17, 24, 39)
RAIO = 14
ALTURA_BARRA = 20

SAIDA = Path(__file__).resolve().parent.parent / "assets" / "demo.png"


def fonte(tamanho: int, negrito: bool = False) -> ImageFont.FreeTypeFont:
    nome = "arialbd.ttf" if negrito else "arial.ttf"
    try:
        return ImageFont.truetype(nome, tamanho)
    except OSError:
        return ImageFont.load_default()


def texto_centralizado(draw: ImageDraw.ImageDraw, cx: int, y: int, texto_str: str, fnt: ImageFont.FreeTypeFont, cor=TEXTO) -> None:
    bbox = draw.textbbox((0, 0), texto_str, font=fnt)
    largura = bbox[2] - bbox[0]
    draw.text((cx - largura / 2, y), texto_str, font=fnt, fill=cor)


def desenhar_janela(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int, cor) -> None:
    draw.rounded_rectangle([x0, y0, x1, y1], radius=RAIO, fill=cor)
    draw.rounded_rectangle([x0, y0, x1, y0 + ALTURA_BARRA], radius=RAIO, fill=COR_BARRA, corners=(True, True, False, False))


def desenhar_seta(draw: ImageDraw.ImageDraw, x0: int, x1: int, y: int) -> None:
    draw.line([(x0, y), (x1 - 12, y)], fill=TEXTO, width=3)
    draw.polygon([(x1, y), (x1 - 14, y - 8), (x1 - 14, y + 8)], fill=TEXTO)


def gerar() -> None:
    img = Image.new("RGB", (LARGURA, ALTURA), FUNDO)
    draw = ImageDraw.Draw(img)

    titulo_fnt = fonte(22, negrito=True)
    legenda_fnt = fonte(15)

    # painel "antes": uma janela maximizada
    px0, py0, px1, py1 = 40, 70, 340, 320
    texto_centralizado(draw, (px0 + px1) // 2, 30, "Antes", titulo_fnt)
    desenhar_janela(draw, px0, py0, px1, py1, COR_JANELA)
    texto_centralizado(draw, (px0 + px1) // 2, py0 + ALTURA_BARRA + 20, "janela maximizada", legenda_fnt, cor=(255, 255, 255))

    # seta central
    desenhar_seta(draw, 360, 560, (py0 + py1) // 2)
    texto_centralizado(draw, 460, (py0 + py1) // 2 + 16, "abre um novo\nprograma", legenda_fnt)

    # painel "depois": tela dividida
    qx0, qy0, qx1, qy1 = 580, 70, 860, 320
    texto_centralizado(draw, (qx0 + qx1) // 2, 30, "Depois (automático)", titulo_fnt)
    meio = (qx0 + qx1) // 2
    gap = 8
    desenhar_janela(draw, qx0, qy0, meio - gap // 2, qy1, COR_ESQUERDA)
    desenhar_janela(draw, meio + gap // 2, qy0, qx1, qy1, COR_DIREITA)

    SAIDA.parent.mkdir(exist_ok=True)
    img.save(SAIDA)
    print(f"Demo salva em {SAIDA}")


if __name__ == "__main__":
    gerar()
