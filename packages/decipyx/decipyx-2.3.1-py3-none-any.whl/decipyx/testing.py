from time import sleep
import sys

# Adicione o diretório ao sys.path primeiro
sys.path.append(r'C:\Users\ufam\OneDrive - mtegovbr\Documentos\Alexandria\socratica')

# Agora você pode importar com segurança o módulo socratica.os_automation
import keyboard as kb
import socratica.os_automation as scrt
from pywinauto import *
from pywinauto.application import Application
from pywinauto.findwindows import ElementNotFoundError

intervalo = 1
app = Application().connect(title_re="^Terminal 3270.*")
dlg = app.window(title_re="^Terminal 3270.*")
Acesso = scrt.janela3270()
sleep(intervalo)
dlg.type_keys('{F3}')
sleep(intervalo)
dlg.type_keys('{F2}')
erro_message = Acesso.pega_texto_siape(Acesso.copia_tela(), 11, 15, 11, 51).strip()
print(erro_message)
dlg.type_keys('TROCAHAB')

kb.press("alt")
kb.press("a")
sleep(intervalo)
kb.release("a")
kb.release("alt")
sleep(intervalo)

# Pressionar as teclas de seta para navegar até o menu "Arquivo"
kb.press("Right")
sleep(intervalo)
kb.release("Right")
sleep(intervalo)
kb.press("alt")
kb.press("i")
sleep(intervalo)
kb.release("i")
kb.release("alt")
sleep(intervalo)
kb.press("alt")
kb.press("i")
sleep(intervalo)
kb.release("i")
kb.release("alt")
sleep(intervalo)
kb.press("Enter")
sleep(intervalo)
kb.release("Enter")
sleep(intervalo)
sleep(intervalo)
app = Application().connect(title_re="Imprimir")
sleep(intervalo)

sleep(3)

# Obter a janela
window = app.window(title_re="Imprimir")

# Ativar a janela
window.set_focus()
