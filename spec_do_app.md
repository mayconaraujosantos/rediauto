gemini ai como criar um app para windows para redimensionar automaticamente as janelas na area de trabalho

Para criar um aplicativo no Windows que redimensiona janelas automaticamente, você pode usar Python com a biblioteca pywin32 ou C# com o Visual Studio.Ferramentas e LinguagensPython: Rápido de escrever, usa a biblioteca win32gui para achar e mudar o tamanho das janelas.C# / .NET: Nativo do Windows, usa a API do Windows para um controle mais forte e visual bonito.Passos Básicos (Exemplo com Python)Instalar o Python no seu computador.Baixar a ferramenta de controle de janelas com o comando pip install pywin32.Criar um código que usa EnumWindows para achar o nome da janela aberta.Usar a função MoveWindow para mudar a posição e o tamanho da janela usando coordenadas de pixels da tela.Transformar o código em um arquivo executável .exe com o programa pyinstaller.Se quiser, posso te ajudar a:Escrever o código completo em Python para redimensionar as janelas.Mostrar como fazer um arquivo executável para rodar direto no Windows.Explicar como usar C# se preferir criar um programa com botões na tela.


vamos fazer usando python, para ilustrar o que quero, quando eu ja tiver um programa redimencionado para direita ou esquerda, quando abrir outro programa ele deve redimencionar para area nao usada automaticamente


Para criar esse sistema, precisamos monitorar o surgimento de novas janelas e calcular o espaço livre na tela.O script abaixo faz exatamente isso: ele detecta a janela ativa atual (que você já posicionou) e, assim que uma nova janela surge, ele a move para ocupar a metade restante da tela.Requisitos IniciaisPrimeiro, instale as bibliotecas necessárias para controlar as janelas e gerenciar os processos:

pip install pywin32 pyautogui

import time
import win32gui
import win32process
import pyautogui

def obter_janela_focada():
    """Retorna o identificador da janela que o usuário está usando."""
    return win32gui.GetForegroundWindow()

def obter_posicao_janela(hwnd):
    """Retorna as coordenadas (esquerda, topo, direita, baixo) da janela."""
    return win32gui.GetWindowRect(hwnd)

def redimensionar_janela(hwnd, x, y, largura, altura):
    """Muda a posição e o tamanho de uma janela específica."""
    win32gui.MoveWindow(hwnd, x, y, largura, altura, True)

def monitorar_e_posicionar():
    # Pega o tamanho total da sua tela atual
    largura_tela, altura_tela = pyautogui.size()
    largura_metade = largura_tela // 2

    print("=== Monitor de Janelas Ativo ===")
    print("Posicione uma janela em um dos lados. O próximo programa aberto ocupará o lado oposto.")

    # Guarda a primeira janela que já deve estar aberta e posicionada
    janela_atual = obter_janela_focada()
    
    while True:
        time.sleep(0.5) # Evita sobrecarregar o processador
        
        nova_janela = obter_janela_focada()
        
        # Detecta se uma nova janela ganhou o foco do sistema
        if nova_janela != janela_atual and nova_janela != 0:
            nome_janela = win32gui.GetWindowText(nova_janela)
            
            # Ignora cliques na barra de tarefas ou na Área de Trabalho
            if nome_janela not in ["", "Program Manager", "Start"]:
                try:
                    # Verifica onde a primeira janela estava posicionada
                    esq, topo, dir_proc, baixo = obter_posicao_janela(janela_atual)
                    
                    # Se a primeira janela estava do lado esquerdo
                    if esq < largura_metade and dir_proc <= largura_metade + 50:
                        print(f"Detectado: '{nome_janela}' -> Movendo para a DIREITA.")
                        redimensionar_janela(nova_janela, largura_metade, 0, largura_metade, altura_tela)
                    
                    # Se a primeira janela estava do lado direito
                    elif esq >= largura_metade - 50:
                        print(f"Detectado: '{nome_janela}' -> Movendo para a ESQUERDA.")
                        redimensionar_janela(nova_janela, 0, 0, largura_metade, altura_tela)
                        
                except Exception as e:
                    pass
                
                # Atualiza a referência para a última janela tratada
                janela_atual = nova_janela

if __name__ == "__main__":
    monitorar_e_posicionar()

Como Testar o FuncionamentoAbra um programa (como o Bloco de Notas) e use o atalho Win + Seta para Esquerda para fixá-lo na metade esquerda.Execute o script Python acima.Abra qualquer outro programa (como o Navegador). O script vai detectar a abertura e jogá-lo direto para a metade direita da tela.Podemos evoluir esse projeto. O que gostaria de fazer agora?Ajustar o código para funcionar com múltiplos monitoresCriar uma interface visual simples para ligar e desligar o scriptGerar o arquivo executável (.exe) para rodar direto no Windows