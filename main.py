import os
import sys
import threading
import time
from pathlib import Path

import pystray
import win32api
import win32con
import win32gui
from PIL import Image

# builds com --windowed (sem console) deixam stdout/stderr como None; print() quebraria
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

POLL_INTERVAL = 0.5
IGNORED_TITLES = {"", "Program Manager", "Start"}
MIN_LARGURA_JANELA = 100
TOLERANCIA_MAXIMIZADA = 50
# overlays/tray tools (ex: indicador de bateria do DualSenseX) usam esses estilos
ESTILOS_OVERLAY = win32con.WS_EX_TRANSPARENT | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOOLWINDOW
ICON_PATH = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent)) / "assets" / "icon.ico"

ativo = threading.Event()
ativo.set()
encerrar = threading.Event()


def janela_focada() -> int:
    return win32gui.GetForegroundWindow()


def posicao_janela(hwnd: int) -> tuple[int, int, int, int]:
    return win32gui.GetWindowRect(hwnd)


def mover_janela(hwnd: int, x: int, y: int, largura: int, altura: int) -> None:
    win32gui.MoveWindow(hwnd, x, y, largura, altura, True)


def tamanho_tela() -> tuple[int, int]:
    return win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)


def janelas_de_aplicativo(excluir: int) -> list[int]:
    """Janelas de nível superior, visíveis, não minimizadas e sem dono (exclui tooltips/diálogos)."""
    janelas = []

    def callback(hwnd, _):
        if hwnd == excluir:
            return
        if not win32gui.IsWindowVisible(hwnd) or win32gui.IsIconic(hwnd):
            return
        if win32gui.GetWindow(hwnd, win32con.GW_OWNER) != 0:
            return
        if win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) & ESTILOS_OVERLAY:
            return
        if win32gui.GetWindowText(hwnd) in IGNORED_TITLES:
            return
        janelas.append(hwnd)

    win32gui.EnumWindows(callback, None)
    return janelas


def estado_janela(hwnd: int, largura_tela: int, metade: int) -> str | None:
    """Classifica uma janela como 'esquerda', 'direita', 'maximizada' ou None (irrelevante)."""
    esquerda, _, direita, _ = posicao_janela(hwnd)
    largura_janela = direita - esquerda

    if largura_janela < MIN_LARGURA_JANELA:
        return None
    if largura_janela >= largura_tela - TOLERANCIA_MAXIMIZADA:
        return "maximizada"

    centro = (esquerda + direita) / 2
    if centro < metade:
        return "esquerda"
    if centro > metade:
        return "direita"
    return None


def janela_referencia(excluir: int, largura_tela: int, metade: int) -> tuple[int, str] | tuple[None, None]:
    """Encontra a primeira janela existente relevante e seu estado (lado ocupado ou maximizada)."""
    for hwnd in janelas_de_aplicativo(excluir):
        estado = estado_janela(hwnd, largura_tela, metade)
        if estado:
            return hwnd, estado
    return None, None


def monitorar() -> None:
    largura_tela, altura_tela = tamanho_tela()
    metade = largura_tela // 2

    print("=== Monitor de Janelas Ativo ===")
    print("Posicione uma janela em um dos lados. O próximo programa aberto ocupará o lado oposto.")

    janela_atual = janela_focada()

    while not encerrar.is_set():
        time.sleep(POLL_INTERVAL)

        if not ativo.is_set():
            continue

        nova_janela = janela_focada()

        if nova_janela == janela_atual or nova_janela == 0:
            continue

        titulo = win32gui.GetWindowText(nova_janela)
        if titulo in IGNORED_TITLES:
            continue

        try:
            hwnd_ref, estado = janela_referencia(nova_janela, largura_tela, metade)

            if estado == "esquerda":
                print(f"'{titulo}' -> movendo para a DIREITA")
                mover_janela(nova_janela, metade, 0, metade, altura_tela)
            elif estado == "direita":
                print(f"'{titulo}' -> movendo para a ESQUERDA")
                mover_janela(nova_janela, 0, 0, metade, altura_tela)
            elif estado == "maximizada":
                print(f"'{titulo}' -> janela existente estava maximizada, dividindo a tela")
                mover_janela(hwnd_ref, 0, 0, metade, altura_tela)
                mover_janela(nova_janela, metade, 0, metade, altura_tela)
        except win32gui.error:
            pass

        janela_atual = nova_janela


def imagem_pausada(imagem_ativa: Image.Image) -> Image.Image:
    return imagem_ativa.convert("LA").convert("RGBA")


def alternar_ativo(icon: pystray.Icon, item: pystray.MenuItem) -> None:
    if ativo.is_set():
        ativo.clear()
        icon.icon = icon.icon_pausado
        print("Monitor pausado.")
    else:
        ativo.set()
        icon.icon = icon.icon_ativo
        print("Monitor retomado.")


def sair(icon: pystray.Icon, item: pystray.MenuItem) -> None:
    encerrar.set()
    icon.stop()


def criar_tray() -> pystray.Icon:
    imagem_ativa = Image.open(ICON_PATH)
    menu = pystray.Menu(
        pystray.MenuItem("Ativo", alternar_ativo, checked=lambda item: ativo.is_set()),
        pystray.MenuItem("Sair", sair),
    )
    icon = pystray.Icon("rediauto", imagem_ativa, "Rediauto", menu)
    icon.icon_ativo = imagem_ativa
    icon.icon_pausado = imagem_pausada(imagem_ativa)
    return icon


def main() -> None:
    thread = threading.Thread(target=monitorar, daemon=True)
    thread.start()
    criar_tray().run()


if __name__ == "__main__":
    main()
