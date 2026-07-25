"""Gera assets/icon.ico: duas janelas lado a lado, representando o split de tela."""

from pathlib import Path

from PIL import Image, ImageDraw

TAMANHO = 256
MARGEM = 20
GAP = 16
COR_ESQUERDA = (59, 130, 246)  # azul
COR_DIREITA = (16, 185, 129)  # verde
COR_BARRA = (17, 24, 39)  # quase preto, barra de título
RAIO = 18
ALTURA_BARRA = 28

SAIDA = Path(__file__).resolve().parent.parent / "assets" / "icon.ico"


def desenhar_janela(draw: ImageDraw.ImageDraw, x0: int, y0: int, x1: int, y1: int, cor: tuple[int, int, int]) -> None:
    draw.rounded_rectangle([x0, y0, x1, y1], radius=RAIO, fill=cor)
    draw.rounded_rectangle(
        [x0, y0, x1, y0 + ALTURA_BARRA],
        radius=RAIO,
        fill=COR_BARRA,
        corners=(True, True, False, False),
    )


def gerar() -> None:
    img = Image.new("RGBA", (TAMANHO, TAMANHO), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    largura_janela = (TAMANHO - 2 * MARGEM - GAP) // 2

    desenhar_janela(draw, MARGEM, MARGEM, MARGEM + largura_janela, TAMANHO - MARGEM, COR_ESQUERDA)
    desenhar_janela(
        draw,
        MARGEM + largura_janela + GAP,
        MARGEM,
        MARGEM + 2 * largura_janela + GAP,
        TAMANHO - MARGEM,
        COR_DIREITA,
    )

    SAIDA.parent.mkdir(exist_ok=True)
    img.save(SAIDA, format="ICO", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print(f"Ícone salvo em {SAIDA}")


if __name__ == "__main__":
    gerar()
