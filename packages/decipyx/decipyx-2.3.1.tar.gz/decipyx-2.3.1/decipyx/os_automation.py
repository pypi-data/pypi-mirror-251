from cgitb import text
from pywinauto.application import Application
from pywinauto import mouse
from pywinauto import clipboard
import pywinauto.keyboard as tc
import pyautogui as Pagui
import sqlite3
from time import sleep
import keyboard as kb


class janelaInternet:

    def __init__(self):
        self.Tela = ''
        self.ListaTeclasComando = ('ENTER', 'ESC', 'HOME', 'END', 'UP', 'DOWN')
        self.ListaDigitaTeclasComando = ('{ENTER}', '{VK_ESCAPE}', '{VK_HOME}', '{VK_END}', '{VK_UP}', '{VK_DOWN}')
        self.app = Application().connect(title_re="^Terminal 3270.*")
        self.dlg = self.app.top_window()

    def seleciona_janela(self):
        """
        Seleciona a janela atualmente conectada.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - Nenhum.
        """
        self.dlg = self.app.top_window()
        sleep(1)

    def salva_tela_arq_texto(self, Arquivo):
        """
        Salva o conteúdo da janela atual em um arquivo de texto.
        
        Parâmetros:
        - Arquivo: Nome do arquivo onde o conteúdo será salvo.
        
        Retorna:
        - Nenhum.
        """
        self.dlg.type_keys('^S')
        sleep(1)
        tc.send_keys(Arquivo)
        sleep(1)
        tc.send_keys('{ENTER}')

    def vai_para_barra_de_endereco(self):
        """
        Navega para a barra de endereços da janela atual.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - Nenhum.
        """
        self.dlg.type_keys('{F6}')  # vai para a barra de endereco
        sleep(1)

    def endereco_web(self, Endereco):
        """
        Navega para o endereço web fornecido.
        
        Parâmetros:
        - Endereco: Endereço web para o qual navegar.
        
        Retorna:
        - Nenhum.
        """
        self.dlg.type_keys('{F6}')  # vai para a barra de endereco
        sleep(1)
        self.dlg.type_keys('{DELETE 1000}')
        self.dlg.type_keys(Endereco)
        self.dlg.type_keys('{ENTER}')
        sleep(5)

    def mouse_clk(self, botao, x, y):
        """
        Clica com o mouse em coordenadas específicas.
        
        Parâmetros:
        - botao: Botão do mouse para clicar ('esquerdo' ou 'direito').
        - x: Coordenada x do clique.
        - y: Coordenada y do clique.
        
        Retorna:
        - Nenhum.
        """
        if botao == 'esquerdo':
            mouse.click(button='left', coords=(x, y))

    def tab(self, N):
        """
        Simula a tecla Tab.
        
        Parâmetros:
        - N: Número de vezes que a tecla Tab deve ser pressionada.
        
        Retorna:
        - Nenhum.
        """
        n_tabs = N
        if N < 0:
            self.dlg.type_keys('{VK_SHIFT down}')
            n_tabs = abs(N)
        argumento = "{TAB " + str(n_tabs) + "}"
        self.dlg.type_keys(argumento)
        if N < 0:
            self.dlg.type_keys('{VK_SHIFT up}')

    def digita(self, texto):
        """
        Digita o texto fornecido na janela atual.
        
        Parâmetros:
        - texto: Texto a ser digitado.
        
        Retorna:
        - Nenhum.
        """
        sleep(1)
        self.dlg.type_keys(texto)
        sleep(1)

    def digita_com_ctrl(self, texto):
        """
        Digita o texto fornecido com a tecla Ctrl pressionada.
        
        Parâmetros:
        - texto: Texto a ser digitado com Ctrl.
        
        Retorna:
        - Nenhum.
        """
        self.dlg.type_keys('{VK_LCONTROL down}')
        sleep(1)
        self.dlg.type_keys(texto)
        sleep(1)
        self.dlg.type_keys('{VK_LCONTROL up}')
        sleep(1)

    def digita_com_shift(self, texto):
        """
        Digita o texto fornecido com a tecla Shift pressionada.
        
        Parâmetros:
        - texto: Texto a ser digitado com Shift.
        
        Retorna:
        - Nenhum.
        """
        self.dlg.type_keys('{VK_SHIFT down}')
        sleep(1)
        self.dlg.type_keys(texto)
        sleep(1)
        self.dlg.type_keys('{VK_SHIFT up}')
        sleep(1)

    def digita_num_keypad(self, N):
        """
        Digita números usando o teclado numérico.
        
        Parâmetros:
        - N: Números a serem digitados usando o teclado numérico.
        
        Retorna:
        - Nenhum.
        """ 
        for digito in N:
            if digito == '0':
                self.dlg.type_keys('{VK_NUMPAD0}')
            if digito == '1':
                self.dlg.type_keys('{VK_NUMPAD1}')
            if digito == '2':
                self.dlg.type_keys('{VK_NUMPAD2}')
            if digito == '3':
                self.dlg.type_keys('{VK_NUMPAD3}')
            if digito == '4':
                self.dlg.type_keys('{VK_NUMPAD4}')
            if digito == '5':
                self.dlg.type_keys('{VK_NUMPAD5}')
            if digito == '6':
                self.dlg.type_keys('{VK_NUMPAD6}')
            if digito == '7':
                self.dlg.type_keys('{VK_NUMPAD7}')
            if digito == '8':
                self.dlg.type_keys('{VK_NUMPAD8}')
            if digito == '9':
                self.dlg.type_keys('{VK_NUMPAD9}')

    def enter(self):
        """
        Simula a tecla Enter.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - Nenhum.
        """
        sleep(1)
        self.dlg.type_keys('{ENTER}')
        sleep(1)

    def copia_tela(self):
        """
        Copia o conteúdo da janela atual para a área de transferência.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - Resultado: Conteúdo copiado da janela.
        """
        clipboard.EmptyClipboard()
        self.dlg.type_keys('^a')
        sleep(1)
        self.dlg.type_keys('^c')
        sleep(1)
        try:
            Resultado = clipboard.GetData()
        except:
            Resultado = ''
        return Resultado

    def detecta_tela(self, TextoProcurado):
        """
        Verifica se o texto fornecido está presente na janela atual.
        
        Parâmetros:
        - TextoProcurado: Texto a ser verificado na janela.
        
        Retorna:
        - True se o texto estiver presente, False caso contrário.
        """
        self.dlg.type_keys('^a')
        sleep(1)
        self.dlg.type_keys('^c')
        sleep(1)
        if TextoProcurado in clipboard.GetData():
            return True
        else:
            return False

    def copia_selecao(self):
        """
        Copia o texto selecionado na janela atual para a área de transferência.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - O texto selecionado copiado para a área de transferência.
        """
        self.dlg.type_keys('^c')
        sleep(1)
        return clipboard.GetData()

    def colar(self):
        """
        Cola o conteúdo da área de transferência na janela atual.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - O conteúdo colado da área de transferência.
        """
        self.dlg.type_keys('^v')
        sleep(1)
        return clipboard.GetData()

    def voltar_pagina_anterior(self):
        """
        Navega para a página anterior na janela atual.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - Nenhum.
        """
        self.dlg.type_keys('%{VK_LEFT}')
        sleep(1)

    def recarrega_tela(self):
        """
        Recarrega a janela atual.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - Nenhum.
        """
        self.dlg.type_keys('^r')
        sleep(1)
        self.dlg.type_keys('{Enter}')
        sleep(1)

    def fecha_janela(self):
        """
        Fecha a janela atual.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - Nenhum.
        """
        self.dlg.type_keys('^{F4}')  # control-F4, fecha a janela
        sleep(1)

    def fecha_guia(self):
        """
        Fecha a guia atual.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - Nenhum.
        """
        self.dlg.type_keys('^w')  # control-F4, fecha a guia
        sleep(1)

    def proxima_guia(self):
        """
        Navega para a próxima guia.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - Nenhum.
        """
        self.dlg.type_keys('^{TAB}')
        sleep(1)

    def pagina_anterior(self):
        """
        Navega para a página anterior.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - Nenhum.
        """
        self.dlg.type_keys('%{LEFT}')  # alt-seta pra esquerda, volta para a pagina anterior
        sleep(1)

    def __tecla_comando__(self, Tecla):
        """
        Método privado para simular o pressionamento de uma tecla de comando.
        
        Parâmetros:
        - Tecla: Nome da tecla de comando a ser pressionada.
        
        Retorna:
        - Nenhum.
        """
        Posicao = self.ListaTeclasComando.index(Tecla)
        TeclaComando = self.ListaDigitaTeclasComando[Posicao]
        self.dlg.type_keys(TeclaComando)
        sleep(0.5)

    def digita_tecla_comando(self, Tecla):
        """
        Digita uma tecla de comando na janela atual.
        
        Parâmetros:
        - Tecla: Nome da tecla de comando a ser digitada.
        
        Retorna:
        - Nenhum.
        """
        # essa rotina aperta a Tecla
        # que nao e uma letra. Tipo seta para baixo e tal
        dlg = self.app.top_window()
        self.__TeclaComando__(Tecla)

class janela3270:
    def __init__(self):
        self.Tela = ''
        self.delay = 0.1
        self.app = Application().connect(title_re="^Terminal 3270.*")
        self.dlg = self.app.top_window()
        self.ListaTeclasComando = ('ENTER', 'PF1', 'PF2', 'PF3', 'PF4', 'PF5', 'PF6', 'PF7',
                                   'PF8', 'PF9', 'PF10', 'PF11', 'PF12', 'PA1', 'PA2', 'END',
                                   'HOME', 'TAB')
        self.ListaDigitaTeclasComando = ('{ENTER}', '{F1}', '{F2}', '{F3}', '{F4}', '{F5}', '{F6}', '{F7}',
                                         '{F8}', '{F9}', '{F10}', '{F11}', '{F12}', '{PGUP}', '{PGDN}', '{END}',
                                         '{HOME}', '{TAB}')

    def seleciona_janela(self):
        """
        Seleciona a janela atualmente conectada.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - Nenhum.
        """
        self.dlg = self.app.top_window()
        sleep(1)

    def espaco(self, N):
        """
        Simula a tecla espaço.
        
        Parâmetros:
        - N: Número de vezes que a tecla espaço deve ser pressionada.
        
        Retorna:
        - Nenhum.
        """
        n_espacos = N
        argumento = "{SPACE " + str(n_espacos) + "}"
        self.dlg.type_keys(argumento)

    def tab(self, N):
        """
        Simula a tecla Tab.
        
        Parâmetros:
        - N: Número de vezes que a tecla Tab deve ser pressionada.
        
        Retorna:
        - Nenhum.
        """
        n_tabs = N
        if N < 0:
            self.dlg.type_keys('{VK_SHIFT down}')
            n_tabs = abs(N)
        argumento = "{TAB " + str(n_tabs) + "}"
        self.dlg.type_keys(argumento)
        if N < 0:
            self.dlg.type_keys('{VK_SHIFT up}')

    def posiciona_cursor_na_linha_siafi(self, tabs):
        """
        Posiciona o cursor na linha SIAFI.
        
        Parâmetros:
        - tabs: Número de vezes que a tecla Tab deve ser pressionada.
        
        Retorna:
        - Nenhum.
        """
        self.dlg.type_keys('{HOME}')
        self.tab(tabs)

    def digita(self, texto):
        """
        Digita o texto fornecido na janela atual.
        
        Parâmetros:
        - texto: Texto a ser digitado.
        
        Retorna:
        - Nenhum.
        """
        sleep(self.delay)
        texto = str(texto)
        texto = texto.replace(' ', '{SPACE}')
        self.dlg.type_keys(texto)
        sleep(self.delay)

    def __enter__(self):
        """
        Simula a tecla Enter.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - Nenhum.
        """
        sleep(self.delay)
        self.dlg.type_keys('{ENTER}')
        sleep(self.delay)

    def tecla_comando(self, Tecla):
        """
        Simula o pressionamento de uma tecla de comando.
        
        Parâmetros:
        - Tecla: Nome da tecla de comando a ser pressionada.
        
        Retorna:
        - Nenhum.
        """
        Posicao = self.ListaTeclasComando.index(Tecla)
        sleep(self.delay)
        self.dlg.type_keys(self.ListaDigitaTeclasComando[Posicao])
        sleep(self.delay)

    def copia_tela(self):
        """
        Copia o conteúdo da janela atual para a área de transferência.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - O conteúdo copiado da janela.
        """
        self.dlg.type_keys('^a')
        sleep(self.delay)
        self.dlg.type_keys('^c')
        sleep(self.delay)
        self.Tela = clipboard.GetData()
        return clipboard.GetData()

    def vira_tela_siafi_tecla(self, Tecla):
        """
        Navega para uma outra tela SIAFI usando uma tecla específica.
        
        Parâmetros:
        - Tecla: Tecla de comando a ser pressionada.
        
        Retorna:
        - O conteúdo da nova tela.
        """
        self.dlg = self.app.top_window()
        TelaInicial = self.copia_tela()
        self.Tela = TelaInicial
        self.tecla_comando(Tecla)
        while self.Tela == TelaInicial:
            sleep(self.delay)
            self.Tela = self.copia_tela()
        return self.Tela

    def pega_texto_tela(self, tela, L1, C1, L2, C2):
        """
        Recupera um trecho específico de texto da tela SIAFI.
        
        Parâmetros:
        - Tela: Conteúdo da tela SIAFI.
        - L1, C1: Coordenadas iniciais da linha e coluna.
        - L2, C2: Coordenadas finais da linha e coluna.
        
        Retorna:
        - Trecho de texto entre as coordenadas fornecidas.
        """
        D1 = (L1 - 1) * 82 + C1 - 1
        D2 = (L2 - 1) * 82 + C2
        return tela[D1:D2]

    def espera_tela_siafi_texto_localizacao(self, L1, C1, L2, C2, Texto, tecla_comando):
        """
        Espera até que um texto específico apareça em uma localização específica da tela SIAFI.
        
        Parâmetros:
        - L1, C1: Coordenadas iniciais da linha e coluna.
        - L2, C2: Coordenadas finais da linha e coluna.
        - Texto: Texto esperado na localização.
        - tecla_comando: Tecla de comando a ser pressionada enquanto espera.
        
        Retorna:
        - Nenhum.
        """
        TelaEncontrada = 0
        while TelaEncontrada == 0:
            sleep(self.delay)
            self.Tela = self.copia_tela()
            if self.pega_texto_siafi(self.Tela, L1, C1, L2, C2) == Texto:
                TelaEncontrada = 1
            else:
                self.vira_tela_siafi_tecla(tecla_comando)

    def espera_tela_siafi_texto_qualquer_lugar(self, tuple_Texto, tecla_comando):
        """
        Espera até que um conjunto de textos apareça em qualquer lugar da tela SIAFI.
        
        Parâmetros:
        - tuple_Texto: Tupla contendo os textos esperados.
        - tecla_comando: Tecla de comando a ser pressionada enquanto espera.
        
        Retorna:
        - Coordenadas do texto encontrado.
        """
        self.D1 = 0
        self.D2 = 0
        self.L = 0
        self.C1 = 0
        self.C2 = 0
        self.Encontrou = False

        def buscaTextos():
            for Texto in tuple_Texto:
                if Texto in self.Tela:
                    self.D1 = self.Tela.find(Texto) + 1
                    self.D2 = self.D1  + len(Texto)
                    self.L = self.D1  // 82 + 1
                    self.C1 = self.D1  % 82
                    self.C2 = self.C1 + len(Texto) - 1
                    self.CoordenadasTexto = (self.L, self.C1, self.L, self.C2, tuple_Texto.index(Texto))
                    self.Encontrou = True
                    return

        self.Tela = self.copia_tela()
        buscaTextos()
        while not (self.Encontrou):
            self.Tela = self.vira_tela_siafi_tecla(tecla_comando)
            buscaTextos()
        return self.CoordenadasTexto

    def acessa_sistema_depois_da_primeira_senha(self, Sistema):
        """
        Acessa um sistema específico após a autenticação inicial.
        
        Parâmetros:
        - Sistema: Nome do sistema a ser acessado.
        
        Retorna:
        - Nenhum.
        """
        IdentificaTela = 'NOME'
        while IdentificaTela == 'NOME':
            self.digita(Sistema)
            self.vira_tela_siafi_tecla('ENTER')
            sleep(20)
            self.Tela = self.copia_tela()
            IdentificaTela = self.pega_texto_siafi(self.Tela, 8, 10, 8, 13)
        Sistema = Sistema.upper()
        if Sistema == 'SIASG':
            self.digita('x')
            self.vira_tela_siafi_tecla('ENTER')
            self.vira_tela_siafi_tecla('ENTER')
        if Sistema == 'SIAFI':
            self.digita('x')
            self.vira_tela_siafi_tecla('ENTER')
       
    def acessar_terminal_3270(self, dlg, comando):
        """
        Acessa o Terminal 3270, especificamente o Siape Hod (tela preta).

        Esta função simula a interação do usuário com o Terminal 3270, 
        utilizando teclas de função e comandos para navegação e execução de tarefas.

        Parâmetros:
        dlg: Uma instância de uma janela de diálogo ou interface de terminal que permite a interação via teclado.
        comando: Uma string de comando a ser digitada no terminal após a navegação inicial, 
        sendo o primeiro caractere, obrigatoriamente o '>'. Ex: >CDCONVINC

        A função executa os seguintes passos:
        1. Aguarda 5 segundos para estabilizar a conexão com o terminal.
        2. Pressiona a tecla de função F3.
        3. Pressiona a tecla de função F2.
        4. Digita o comando fornecido.
        5. Aguarda 2 segundos para processamento.
        6. Simula a tecla Enter para executar o comando.
        7. Pressiona a tecla TAB.
        8. Aguarda mais 2 segundos para qualquer atualização na tela.
        """
        sleep(5)
        dlg.type_keys('{F3}')
        dlg.type_keys('{F2}')
        dlg.type_keys(comando)
        sleep(2)
        kb.press("Enter")
        dlg.type_keys('{TAB}')
        sleep(2)

class janela3270PyAutoGui:
    def __init__(self, NaoServeParaNada):  
        self.Tela = ''
        self.delay = 0.1
        self.ListaTeclasComando = ('ENTER', 'PF1', 'PF2', 'PF3', 'PF4', 'PF5', 'PF6', 'PF7',
                                   'PF8', 'PF9', 'PF10', 'PF11', 'PF12', 'PA1', 'PA2', 'END',
                                   'HOME')
        self.ListaDigitaTeclasComando = ('enter', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6f', 'f7',
                                         'f8', 'f9', 'f10', 'f11', 'f12', 'pgup', 'pgdn', 'end',
                                         'home')
        sleep(5)

    def espaco(self, N):
        """
        Simula a pressão da tecla espaço N vezes.
        
        Parâmetros:
        - N: Número de vezes que a tecla espaço deve ser pressionada.
        
        Retorna:
        - Nenhum.
        """
        for n_espacos in range(1, N + 1):
            Pagui.press('space')
    
    def tab(self, N):
        """
        Simula a pressão da tecla tab N vezes.
        
        Parâmetros:
        - N: Número de vezes que a tecla tab deve ser pressionada.
        
        Retorna:
        - Nenhum.
        """
        for n_tabs in range(1, abs(N) + 1):
            if N < 0:
                Pagui.hotkey('shift', 'tab')
            else:
                Pagui.press('tab')

    def posiciona_cursor_na_linha_siafi(self, tabs):
        """
        Posiciona o cursor na linha especificada do SIAFI.
        
        Parâmetros:
        - tabs: Número de vezes que a tecla tab deve ser pressionada.
        
        Retorna:
        - Nenhum.
        """
        Pagui.press('home')
        self.tab(tabs)

    def digita(self, texto):
        """
        Simula a digitação de um texto.
        
        Parâmetros:
        - texto: Texto a ser digitado.
        
        Retorna:
        - Nenhum.
        """
        sleep(self.delay)
        Pagui.write(texto)
        sleep(self.delay)

    def __enter__(self):
        """
        Simula a pressão da tecla enter.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - Nenhum.
        """
        sleep(self.delay)
        Pagui.press('enter')
        sleep(self.delay)

    def tecla_comando(self, Tecla):
        """
        Pressiona uma tecla de comando especificada.
        
        Parâmetros:
        - Tecla: Nome da tecla de comando a ser pressionada.
        
        Retorna:
        - Nenhum.
        """
        Posicao = self.ListaTeclasComando.index(Tecla)
        sleep(self.delay)
        Pagui.press(self.ListaDigitaTeclasComando[Posicao])
        sleep(self.delay)

    def copia_tela(self):
        """
        Copia o conteúdo da tela.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - Conteúdo da tela copiado.
        """
        Pagui.hotkey('ctrl', 'a')
        sleep(self.delay)
        Pagui.hotkey('ctrl', 'c')
        sleep(self.delay)
        self.Tela = clipboard.GetData()
        return self.Tela

    def vira_tela_siafi_tecla(self, Tecla):
        """
        Muda a tela SIAFI pressionando uma tecla específica.
        
        Parâmetros:
        - Tecla: Nome da tecla a ser pressionada.
        
        Retorna:
        - Conteúdo da tela após a mudança.
        """
        TelaInicial = self.copia_tela()
        self.Tela = TelaInicial
        self.__tecla_comando__(Tecla)
        while self.Tela == TelaInicial:
            sleep(self.delay)
            self.Tela = self.copia_tela()
        return self.Tela

    def pega_texto_siafi(self, Tela, L1, C1, L2, C2):
        """
        Extrai um trecho do texto da tela SIAFI com base nas coordenadas fornecidas.
        
        Parâmetros:
        - Tela: Conteúdo da tela SIAFI.
        - L1, C1: Coordenadas iniciais de onde começar a extração.
        - L2, C2: Coordenadas finais de onde terminar a extração.
        
        Retorna:
        - Trecho do texto extraído da tela SIAFI.
        """
        Tela = Tela.replace('\n', '')
        Tela = Tela.replace('\r', '')
        D1 = (L1 - 1) * 80 + C1 - 1
        D2 = (L2 - 1) * 80 + C2
        return Tela[D1:D2]

    def espera_tela_siafi_texto_localizacao(self, L1, C1, L2, C2, Texto, tecla_comando):
        """
        Espera até que um texto específico apareça em uma localização específica da tela SIAFI.
        
        Parâmetros:
        - L1, C1: Coordenadas iniciais para procurar o texto.
        - L2, C2: Coordenadas finais para procurar o texto.
        - Texto: Texto a ser procurado.
        - tecla_comando: Tecla a ser pressionada enquanto espera.
        
        Retorna:
        - Nenhum.
        """
        TelaEncontrada = 0
        while TelaEncontrada == 0:
            sleep(self.delay)
            self.Tela = self.copia_tela()
            if self.pega_texto_siafi(self.Tela, L1, C1, L2, C2) == Texto:
                TelaEncontrada = 1
            else:
                self.vira_tela_siafi_tecla(tecla_comando)

    def acessa_sistema_depois_da_primeira_senha(self, Sistema):
        """
        Acessa um sistema específico após a inserção da primeira senha.
        
        Parâmetros:
        - Sistema: Nome do sistema a ser acessado.
        
        Retorna:
        - Nenhum.
        """
        IdentificaTela = 'NOME'
        while IdentificaTela == 'NOME':
            self.digita(Sistema)
            self.vira_tela_siafi_tecla('ENTER')
            sleep(20)
            self.Tela = self.copia_tela()
            IdentificaTela = self.pega_texto_siafi(self.Tela, 8, 10, 8, 13)
        Sistema = Sistema.upper()
        if Sistema == 'SIASG':
            self.digita('x')
            self.vira_tela_siafi_tecla('ENTER')
            self.vira_tela_siafi_tecla('ENTER')
        if Sistema == 'SIAFI':
            self.digita('x')
            self.vira_tela_siafi_tecla('ENTER')

class ObjetoBancoDados:

    def __init__(self, ArqBancoDados):
        self.BancoDados = sqlite3.connect(ArqBancoDados)
        self.ArqBancoDados = ArqBancoDados

    def open(self):
        """
        Abre uma conexão com o banco de dados.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - Nenhum.
        """
        self.banco_dados = sqlite3.connect(self.arq_banco_dados)

    def close(self):
        """
        Fecha a conexão com o banco de dados.
        
        Parâmetros:
        - Nenhum.
        
        Retorna:
        - Nenhum.
        """
        self.banco_dados.close()

    def create(self, nome_tabela, estrutura: str):
        """
        Cria uma tabela no banco de dados com base em uma estrutura definida.
        
        Parâmetros:
        - nome_tabela: Nome da tabela a ser criada.
        - estrutura: Lista de listas que define a estrutura da tabela.
        
        Retorna:
        - Nenhum.
        """
        sql = 'CREATE TABLE "' + nome_tabela + '" (\n'
        indice = ''
        for campo in estrutura:
            linha = '  "' + campo[0] + '"            '
            tipo_campo = campo[1].upper()
            if tipo_campo == 'A':
                linha += 'VARCHAR(' + str(campo[2]) + ')'
            elif tipo_campo == 'I':
                linha += 'INTEGER'
            elif tipo_campo == 'N':
                linha += 'REAL'
            if campo[3]:
                linha += 'NOT NULL'
            if campo[4]:
                indice += '"' + campo[0] + '",'
            linha += ',\n'
            sql += linha

        if len(indice) > 0:
            indice = indice[:-1]
            indice = '  CONSTRAINT "INDICE" PRIMARY KEY(' + indice + ')\n'
            sql += indice
        else:
            sql = sql[:-2]
        sql += '\n)'
        print(sql)
        try:
            self.bd = self.banco_dados.cursor()
            self.bd.execute(sql)
            self.banco_dados.commit()
        except sqlite3.Error as erro:
            print("Erro ao criar tabela:", erro)

def Vacuum(self):
    self.BD = self.BancoDados.cursor()
    self.BD.execute("VACUUM")

class ObjetoTabela:

    def __init__(self, objeto_banco_dados, nome_tabela):
        """
        Inicializa o objeto de tabela com um objeto de banco de dados e nome de tabela.
        
        Parâmetros:
        - objeto_banco_dados: Objeto de banco de dados com o qual a tabela está associada.
        - nome_tabela: Nome da tabela no banco de dados.
        
        Retorna:
        - Nenhum.
        """
        self.banco_dados = objeto_banco_dados
        self.tabela = nome_tabela
        self.bd = self.banco_dados.cursor()

    def select(self, lista_campos: list, lista_campos_ordem: list, lista_asc_ou_desc: list, condicao_where: str):
        """
        Realiza uma operação SELECT no banco de dados.
        
        Parâmetros:
        - lista_campos: Lista dos campos que devem ser retornados.
        - lista_campos_ordem: Lista dos campos que devem ser ordenados.
        - lista_asc_ou_desc: Lista que indica se a ordenação de cada campo é ascendente ou descendente.
        - condicao_where: Condição WHERE para filtrar os registros retornados.
        
        Retorna:
        - Resultado da consulta SQL.
        """
        # ... [conteúdo do método]
        sql = 'SELECT ' + ','.join(lista_campos) + ' FROM ' + self.tabela + '\n'
        if condicao_where and condicao_where.strip():
            sql += 'WHERE ' + condicao_where + '\n'
        if lista_campos_ordem:
            sql += 'ORDER BY '
            for index, campo_ordem in enumerate(lista_campos_ordem):
                order = "ASC" if lista_asc_ou_desc[index] else "DESC"
                sql += f"{campo_ordem} {order},"
            sql = sql.rstrip(',')
        self.bd.execute(sql)
        return self.bd.fetchall()

    def delete(self, condicao_where: str):
        """
        Realiza uma operação DELETE no banco de dados.
        
        Parâmetros:
        - condicao_where: Condição WHERE para determinar quais registros serão excluídos.
        
        Retorna:
        - Nenhum.
        """
        sql = 'DELETE FROM ' + self.tabela
        if condicao_where and condicao_where.strip():
            sql += ' WHERE ' + condicao_where
        try:
            self.bd.execute(sql)
            self.banco_dados.commit()
        except sqlite3.Error as erro:
            print("Erro ao excluir: ", erro)

    def insert(self, lista_inclusoes: list):
        """
        Realiza uma operação INSERT no banco de dados.
        
        Parâmetros:
        - lista_inclusoes: Lista de registros a serem inseridos, onde cada registro é uma lista de valores.
        
        Retorna:
        - Nenhum.
        """
        for registro in lista_inclusoes:
            campos = ', '.join(['?' for _ in registro])
            sql = f'INSERT INTO {self.tabela} VALUES({campos})'
            try:
                self.bd.execute(sql, registro)
                self.banco_dados.commit()
            except sqlite3.Error as erro:
                print("Erro ao inserir: ", erro)

    def update(self, lista_nome_campos: list, lista_valores_campos: list, condicao_where: str):
        """
        Realiza uma operação UPDATE no banco de dados.
        
        Parâmetros:
        - lista_nome_campos: Lista dos campos a serem atualizados.
        - lista_valores_campos: Lista dos novos valores para os campos.
        - condicao_where: Condição WHERE para determinar quais registros serão atualizados.
        
        Retorna:
        - Nenhum.
        """
        set_statements = ', '.join([f"{campo} = ?" for campo in lista_nome_campos])
        sql = f'UPDATE {self.tabela} SET {set_statements} WHERE {condicao_where}'
        try:
            self.bd.execute(sql, lista_valores_campos)
            self.banco_dados.commit()
        except sqlite3.Error as erro:
            print("Erro ao alterar: ", erro)

class NavegacaoViaTeclado:

    def __init__(self):
        """
        Inicializa a classe NavegacaoViaTeclado.
        """
    pass
    
    def clica_teclas(self, *keys):
        """
        Pressiona sequencialmente uma série de teclas, com um intervalo entre elas.
        
        Parâmetros:
        - *keys: Teclas a serem pressionadas em sequência.
        
        Retorna:
        - Nenhum.
        """
        for key in keys:
            kb.press(key)
            sleep(1)
            kb.release(key)

    def clica_tecla_direcional(self, direction):
        """
        Pressiona uma tecla direcional (por exemplo, "Up", "Down", "Left", "Right") com um intervalo.
        
        Parâmetros:
        - direction (str): A direção da tecla direcional a ser pressionada.
        
        Retorna:
        - Nenhum.
        """
        kb.press(direction)
        sleep(1)
        kb.release(direction)

    def clica_tecla(self, key):
        """
        Pressiona uma única tecla com um intervalo.
        
        Parâmetros:
        - key (str): A tecla a ser pressionada.
        
        Retorna:
        - Nenhum.
        """
        kb.press(key)
        sleep(1)
        kb.release(key)

    def clica_teclas_combinadas(self, *keys):
        """
        Pressiona uma combinação de teclas com um intervalo entre elas.
        
        Parâmetros:
        - *keys: Teclas a serem pressionadas em sequência.
        
        Retorna:
        - Nenhum.
        """
        # Pressiona todas as teclas da combinação, mas não as solta
        for key in keys:
            kb.press(key)
            sleep(1)
        
        # Solta todas as teclas da combinação
        for key in keys:
            kb.release(key)
