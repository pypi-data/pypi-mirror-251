import pandas as pd
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, QMessageBox
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QComboBox, QMenu, QMenuBar, QAction, QListWidget, QMainWindow, QInputDialog, QDialog, QTextEdit, QDesktopWidget
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import json
import sys
sys.path.append(r'C:\Users\ufam\OneDrive - mtegovbr\Documentos\decipyx\alexandria')
from socratica.estilos import dark_stylesheet
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import pyqtSignal, QIODevice, Qt, QThread
from PyQt5.QtWidgets import QApplication, QComboBox, QLineEdit, QCompleter
from PyQt5.QtCore import QStringListModel

class UserManager:
    def __init__(self):
        self.users = {'Admin': 'superadmin'}  
        self.load_users()

    def load_users(self):
        try:
            with open('users.json', 'r') as f:
                self.users = json.load(f)
        except FileNotFoundError:
            # Se o arquivo não existir, um dicionário vazio é usado
            self.users = {}

    def save_users(self):
        with open('users.json', 'w') as f:
            json.dump(self.users, f)

    def add_user(self, username, password):
        self.users[username] = password
        self.save_users()

    def delete_user(self, username):
        if username in self.users:
            del self.users[username]
            self.save_users()

    def update_user(self, username, new_password):
        if username in self.users:
            self.users[username] = new_password
            self.save_users()

    def get_users(self):
        return self.users
    
    def get_usernames(self):
        return [username for username, _ in self.users.items()]
    
    def authenticate(self, username, password):
        return self.users.get(username) == password
    
class LongRunningTask(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)

    # run method gets called when we start the thread
    def run(self):
        # tarefa demorada aqui
        # ...
        self.signal.emit("tarefa terminada")

# Sua função para iniciar a tarefa
def start_long_running_task():
    thread = LongRunningTask()
    thread.signal.connect(task_finished)
    thread.start()

# Sua função que será chamada quando a tarefa estiver terminada
def task_finished(param_from_thread):
    print("Tarefa terminada!", param_from_thread)

class TerminalOutput(QIODevice):
    textWritten = pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))
    
class LoginDialog(QDialog):
    def __init__(self, user_manager):
        super(LoginDialog, self).__init__()
        self.user_manager = user_manager

        layout = QVBoxLayout()

        self.username_field = QLineEdit(self)
        self.username_field.setPlaceholderText("Username")
        layout.addWidget(self.username_field)

        self.password_field = QLineEdit(self)
        self.password_field.setEchoMode(QLineEdit.Password)
        self.password_field.setPlaceholderText("Password")
        layout.addWidget(self.password_field)

        login_button = QPushButton('Login', self)
        login_button.clicked.connect(self.check_credentials)
        layout.addWidget(login_button)

        self.setLayout(layout)

    def check_credentials(self):
        username = self.username_field.text()
        password = self.password_field.text()

        if self.user_manager.authenticate(username, password):
            self.accept()
        else:
            QMessageBox.warning(self, 'Error', 'Bad user or password')

class ItemSetManager:
    def __init__(self, filename='conjuntos.json'):
        self.item_sets = {}
        self.filename = filename
        self.load_data()

    def load_data(self):
        try:
            with open(self.filename, 'r') as f:
                self.item_sets = json.load(f)
        except FileNotFoundError:
            self.item_sets = {}

    def save_data(self):
        with open(self.filename, 'w') as f:
            json.dump(self.item_sets, f)

    def create_item_set(self, set_name):
        self.item_sets[set_name] = {}
        self.save_data()

    def delete_item_set(self, set_name):
        if set_name in self.item_sets:
            del self.item_sets[set_name]
            self.save_data()

    def add_item_to_set(self, set_name, item_name, quantity):
        if set_name in self.item_sets:
            self.item_sets[set_name][item_name] = quantity
            self.save_data()

    def remove_item_from_set(self, set_name, item_name):
        if set_name in self.item_sets and item_name in self.item_sets[set_name]:
            del self.item_sets[set_name][item_name]
            self.save_data()

    def get_item_sets(self):
        return self.item_sets

    def count_items_in_set(self, set_name):
        if set_name in self.item_sets:
            return sum(self.item_sets[set_name].values())
        return 0

class ConjuntoManager:
    def __init__(self):
        self.conjuntos = {}
        self.load_data()

    def save_data(self):
        with open("conjuntos.json", "w") as f:
            json.dump(self.conjuntos, f)
    
    def load_data(self):
        try:
            with open("conjuntos.json", "r") as f:
                self.conjuntos = json.load(f)
        except FileNotFoundError:
            self.conjuntos = {}

    def create_conjunto(self, set_name):
        self.conjuntos[set_name] = {}
        self.save_data()
    
    def delete_conjunto(self, set_name):
        if set_name in self.conjuntos:
            del self.conjuntos[set_name]
        self.save_data()
    
    def add_item_to_conjunto(self, set_name, item_name, quantity):
        if set_name in self.conjuntos:
            self.conjuntos[set_name][item_name] = quantity
        self.save_data()
    
    def remove_item_from_conjunto(self, set_name, item_name):
        if set_name in self.conjuntos and item_name in self.conjuntos[set_name]:
            del self.conjuntos[set_name][item_name]
        self.save_data()
    
    def get_conjuntos(self):
        self.save_data()
        return self.conjuntos
    
    def count_items_in_conjunto(self, set_name):
        if set_name in self.conjuntos:
            return sum(self.conjuntos[set_name].values())
        return 0

class UserManagementWindow(QWidget):
    def __init__(self, user_manager):
        super().__init__()
        self.user_manager = user_manager
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText('Username')
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText('Password')
        layout.addWidget(self.password_input)

        add_button = QPushButton("Adicionar Usuário")
        add_button.clicked.connect(self.add_user)
        layout.addWidget(add_button)

        delete_button = QPushButton("Deletar Usuário")
        delete_button.clicked.connect(self.delete_user)
        layout.addWidget(delete_button)

        update_button = QPushButton("Atualizar Usuário")
        update_button.clicked.connect(self.update_user)
        layout.addWidget(update_button)

        self.user_list = QListWidget()
        layout.addWidget(self.user_list)
        
        refresh_button = QPushButton("Listar Usuários")
        refresh_button.clicked.connect(self.list_users)
        layout.addWidget(refresh_button)

        self.setLayout(layout)
        self.setWindowTitle('Gerenciamento de Usuários')

    def add_user(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if username and password:
            self.user_manager.add_user(username, password)
            QMessageBox.information(self, 'Sucesso', f'Usuário {username} adicionado.')
        else:
            QMessageBox.warning(self, 'Erro', 'Ambos os campos devem ser preenchidos.')

    def delete_user(self):
        username = self.username_input.text()
        if username:
            self.user_manager.delete_user(username)
            QMessageBox.information(self, 'Sucesso', f'Usuário {username} deletado.')
        else:
            QMessageBox.warning(self, 'Erro', 'O campo de username deve ser preenchido.')

    def update_user(self):
        username = self.username_input.text()
        new_password = self.password_input.text()
        
        if username and new_password:
            self.user_manager.update_user(username, new_password)
            QMessageBox.information(self, 'Sucesso', f'Senha do usuário {username} atualizada.')
        else:
            QMessageBox.warning(self, 'Erro', 'Ambos os campos devem ser preenchidos.')

    def list_users(self):
        self.user_list.clear()
        usernames = self.user_manager.get_usernames()
        for username in usernames:
            self.user_list.addItem(f"{username}")

class ItemManagementWindow(QWidget):
    def __init__(self, item_set_manager):
        super(ItemManagementWindow, self).__init__()
        self.item_set_manager = item_set_manager
        self.initUI()

    def load_conjuntos_from_file(self):
        try:
            with open('conjuntos.json', 'r') as f:
                self.conjuntos = json.load(f)
        except FileNotFoundError:
            self.conjuntos = {}

    def save_conjuntos_to_file(self):
        with open('conjuntos.json', 'w') as f:
            json.dump(self.conjuntos, f)

    def add_item(self):
        conjunto_name = self.set_name_combo.currentText()
        item_name = self.item_name_combo.currentText()  # Agora estamos usando o QComboBox
        item_quantity = int(self.item_quantity_input.text())
        if conjunto_name and item_name and item_quantity:
            if conjunto_name in self.conjuntos:
                self.conjuntos[conjunto_name][item_name] = item_quantity
                self.save_conjuntos_to_file()
                QMessageBox.information(self, 'Sucesso', f'Item {item_name} adicionado ao conjunto {conjunto_name}.')
                self.save_conjuntos_to_file()
                # Limpar os campos
                self.clear_fields()

    def remove_item(self):
        conjunto_name = self.set_name_combo.currentText()
        item_name = self.item_name_combo.text()
        if conjunto_name and item_name:
            if conjunto_name in self.conjuntos and item_name in self.conjuntos[conjunto_name]:
                del self.conjuntos[conjunto_name][item_name]
                self.save_conjuntos_to_file()
                QMessageBox.information(self, 'Sucesso', f'Item {item_name} removido do conjunto {conjunto_name}.')
                # Limpar os campos
                self.clear_fields()

    def show_items(self):
        conjunto_name = self.set_name_combo.currentText()
        if conjunto_name:
            if conjunto_name in self.conjuntos:
                items = self.conjuntos[conjunto_name]
                self.item_table.setRowCount(0)
                for item, quantity in items.items():
                    row_position = self.item_table.rowCount()
                    self.item_table.insertRow(row_position)
                    self.item_table.setItem(row_position, 0, QTableWidgetItem(item))
                    self.item_table.setItem(row_position, 1, QTableWidgetItem(str(quantity)))
                # Limpar os campos
                self.clear_fields()

    def initUI(self):
        layout = QVBoxLayout()

        self.load_conjuntos_from_file()

        # ComboBox para selecionar o conjunto de itens
        self.set_name_combo = QComboBox(self)
        self.set_name_combo.addItems(list(self.conjuntos.keys()))
        self.set_name_combo.insertItem(0, 'Selecione o conjunto')
        layout.addWidget(self.set_name_combo)

        # ComboBox para selecionar o item (apenas itens de baseEquipamentos)
        self.item_name_combo = QComboBox(self)
        self.item_name_combo.insertItem(0, 'Selecione o item')
        layout.addWidget(self.item_name_combo)

        # Campo de entrada para a quantidade do item
        self.item_quantity_input = QLineEdit(self)
        self.item_quantity_input.setPlaceholderText('Quantidade do Item')
        layout.addWidget(self.item_quantity_input)

        # Botão para adicionar item
        add_item_button = QPushButton('Adicionar Item')
        add_item_button.clicked.connect(self.add_item)
        layout.addWidget(add_item_button)

        # Botão para remover item
        remove_item_button = QPushButton('Remover Item')
        remove_item_button.clicked.connect(self.remove_item)
        layout.addWidget(remove_item_button)

        # Botão para mostrar itens
        show_items_button = QPushButton('Mostrar Itens')
        show_items_button.clicked.connect(self.show_items)
        layout.addWidget(show_items_button)

        # Tabela para exibir itens
        self.item_table = QTableWidget(self)
        self.item_table.setColumnCount(2)
        self.item_table.setHorizontalHeaderLabels(['Item', 'Quantidadeu'])
        layout.addWidget(self.item_table)

        self.setLayout(layout)
        self.setWindowTitle('Gerenciamento de Itens')
    
    def clear_fields(self):
        self.set_name_combo.setCurrentIndex(0)
        self.item_name_combo.setCurrentIndex(0)
        self.item_quantity_input.clear()

class ConjuntoManagerWindow(QWidget):
    def __init__(self, conjunto_manager):
        super().__init__()
        self.conjunto_manager = conjunto_manager
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.set_name_input = QLineEdit(self)
        self.set_name_input.setPlaceholderText('Nome do Conjunto')
        layout.addWidget(self.set_name_input)

        add_set_button = QPushButton("Adicionar Conjunto")
        add_set_button.clicked.connect(self.add_conjunto)
        layout.addWidget(add_set_button)

        delete_set_button = QPushButton("Deletar Conjunto")
        delete_set_button.clicked.connect(self.delete_conjunto)
        layout.addWidget(delete_set_button)

        self.setLayout(layout)
        self.setWindowTitle('Gerenciar Conjuntos')

    def add_conjunto(self):
        set_name = self.set_name_input.text()
        if set_name:
            self.conjunto_manager.create_conjunto(set_name)
            QMessageBox.information(self, 'Sucesso', f'Conjunto {set_name} adicionado.')
        else:
            QMessageBox.warning(self, 'Erro', 'O nome do conjunto não pode estar vazio.')

    def delete_conjunto(self):
        set_name = self.set_name_input.text()
        if set_name:
            self.conjunto_manager.delete_conjunto(set_name)
            QMessageBox.information(self, 'Sucesso', f'Conjunto {set_name} deletado.')
        else:
            QMessageBox.warning(self, 'Erro', 'O nome do conjunto não pode estar vazio.')

    def add_item_to_conjunto(self):
        set_name = self.set_name_input.text()
        item_name = self.item_name_input.text()
        quantity = self.quantity_input.text()
        if set_name and item_name and quantity.isdigit():
            self.conjunto_manager.add_item_to_conjunto(set_name, item_name, int(quantity))
            QMessageBox.information(self, 'Sucesso', f'Item {item_name} adicionado ao conjunto {set_name}.')
        else:
            QMessageBox.warning(self, 'Erro', 'Todos os campos devem ser preenchidos corretamente.')

    def remove_item_from_conjunto(self):
        set_name = self.set_name_input.text()
        item_name = self.item_name_input.text()
        if set_name and item_name:
            self.conjunto_manager.remove_item_from_conjunto(set_name, item_name)
            QMessageBox.information(self, 'Sucesso', f'Item {item_name} removido do conjunto {set_name}.')
        else:
            QMessageBox.warning(self, 'Erro', 'O nome do conjunto e do item não podem estar vazios.')

class GuiAutomation(QMainWindow):
    def __init__(self, user_manager, item_manager, conjunto_manager):
        super(GuiAutomation, self).__init__()

        self.user_manager = user_manager
        self.item_manager = item_manager
        self.conjunto_manager = conjunto_manager

        self.setWindowTitle('Sistema de Auditoria')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        pixmap = QPixmap(r"C:\Users\ufam\OneDrive - mtegovbr\Documentos\Python\decipyx\logo\decipyx-logo-zip-file\png\logo-no-background2.png")
        label = QLabel()
        label.setAlignment(Qt.AlignCenter)  # Centralizar a imagem verticalmente
        label.setPixmap(pixmap)

        layout.addWidget(label)

        central_widget.setLayout(layout)
            
        menubar = self.menuBar()
        file_menu = menubar.addMenu('Arquivo')
        about_action = QAction('Sobre o Programa', self)
        about_action.triggered.connect(self.show_about_dialog)
        file_menu.addAction(about_action)

        exit_action = QAction('Sair', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        manage_menu = menubar.addMenu('Gerenciar')

        user_management_action = QAction('Gerenciamento de Usuários', self)
        user_management_action.triggered.connect(self.open_user_management_window)
        manage_menu.addAction(user_management_action)

        manage_items_action = QAction('Gerenciar Itens', self)
        manage_items_action.triggered.connect(self.manage_sets)
        manage_menu.addAction(manage_items_action)
        
        manage_conjuntos_action = QAction('Gerenciar Conjuntos', self)
        manage_conjuntos_action.triggered.connect(self.manage_conjuntos)
        manage_menu.addAction(manage_conjuntos_action)
        
        audit_menu = menubar.addMenu('Auditoria')
        
        perform_audit_action = QAction('Realizar Auditoria', self)
        perform_audit_action.triggered.connect(self.perform_audit_gui)
        audit_menu.addAction(perform_audit_action)
        
        self.statusBar().showMessage('Pronto')
        
        self.show()

    def manage_users(self):
        self.user_management_window.show()
    
    def manage_sets(self):
        self.item_management_window.show()

    def manage_conjuntos(self):
        self.conjunto_management_window.show()
        
    def perform_audit_gui(self):
        self.item_manager.load_data()


    def show_about_dialog(self):
        QMessageBox.about(self, "Sobre o Sistema de Auditoria",
                        "Este é um sistema de auditoria para controle de dispositivos e equipamentos IoT em geral do Projeto SUPER.\n"
                        "\nDesenvolvido por Andrey Bessa - 2023")
        
    def open_user_management_window(self):
        username, ok1 = QInputDialog.getText(self, 'Login', 'Nome de usuário:')
        password, ok2 = QInputDialog.getText(self, 'Login', 'Senha:', QLineEdit.Password)
        
        if ok1 and ok2:
            if username == 'Admin' and password == 'superadmin':
                # Abre a janela de gerenciamento de usuários
                # self.user_management_window.show()
                QMessageBox.information(self, 'Sucesso', 'Bem-vindo, Admin!')
                self.manage_users()
            else:
                QMessageBox.warning(self, 'Acesso Negado', 'Somente o usuário Admin com a senha superadmin pode acessar o gerenciamento de usuários.')

    def show(self):
        super(GuiAutomation, self).show()

class FilteredComboBox(QComboBox):
    """
    Uma subclasse de QComboBox que suporta filtragem automática dos itens
    com base no texto digitado pelo usuário.

    A lista de itens é filtrada em tempo real conforme o usuário digita,
    exibindo apenas os itens que contêm o texto inserido.
    """

    def __init__(self, parent=None):
        """
        Inicializa o FilteredComboBox.

        :param parent: O widget pai do combobox, se houver.
        """
        super().__init__(parent)
        self.setEditable(True)
        self.setInsertPolicy(self.NoInsert)
        
        self.originalModel = QStringListModel(self)
        self.completerModel = QStringListModel(self)
        
        # Definir o completador com o modelo
        completer = QCompleter(self.completerModel, self)
        self.setCompleter(completer)

        self.lineEdit().textEdited.connect(self.on_text_edited)

    def setItems(self, items):
        """
        Define os itens a serem exibidos no combobox.

        :param items: Uma lista de strings para exibir no combobox.
        """
        self.originalModel.setStringList(items)
        self.completerModel.setStringList(items)

    def on_text_edited(self, text):
        """
        Método chamado quando o texto na caixa de edição é alterado.

        Filtra os itens do combobox para mostrar apenas aqueles que contêm o texto digitado.

        :param text: O texto atual na caixa de edição.
        """
        filteredItems = [item for item in self.originalModel.stringList() if text in item]
        self.completerModel.setStringList(filteredItems)

        # Verificar se o popup do completador está visível e forçar a abertura
        if self.completer() and not self.completer().popup().isVisible():
            self.completer().setCompletionPrefix(text)
            self.completer().complete()

if __name__ == "__main__":
    app = QApplication([])
    app.setStyleSheet(dark_stylesheet)

    user_manager     = UserManager()  # Substitua pelo código real para criar uma instância UserManager
    item_manager     = ItemSetManager()  # Substitua pelo código real para criar uma instância ItemSetManager
    conjunto_manager = ConjuntoManager()  # Substitua pelo código real para criar uma instância ConjuntoManager

    main_window = GuiAutomation(user_manager, item_manager, conjunto_manager)
    app.exec_()
