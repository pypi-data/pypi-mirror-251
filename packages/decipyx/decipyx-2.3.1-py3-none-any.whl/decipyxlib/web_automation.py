from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import random
from selenium.common.exceptions import NoSuchElementException, TimeoutException, NoSuchFrameException, ElementNotInteractableException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
import locale
from datetime import datetime
from selenium.webdriver.support.select import Select
from num2words import num2words
import os
import glob
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

class WebAutomation:
    def __init__(self, browser):
        self.browser = browser
        self.exception  = (NoSuchElementException, ElementNotInteractableException, NoSuchFrameException, TimeoutException)

    def clica_elemento_by_xpath(self, iframe, path):
        """
        Clica em um elemento localizado por XPath dentro de um iframe.

        Args:
            iframe (str): Nome ou ID do iframe onde o elemento está localizado.
            path (str): Caminho XPath do elemento.

        Returns:
            None
        """
        self.browser.switch_to.default_content()
        self.browser.switch_to.frame(iframe)
        self.browser.find_element(By.XPATH, path).click()
        self.browser.switch_to.default_content()

    def clica_elemento_por_texto(self, iframe, texto_parcial):
        """
        Clica em um elemento localizado por um texto parcial dentro de um iframe.
        """
        self.browser.switch_to.default_content()
        self.browser.switch_to.frame(iframe)
        elemento = WebDriverWait(self.browser, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//*[contains(text(), '{texto_parcial}')]"))
        )
        elemento.click()
        self.browser.switch_to.default_content()

    def clica_elemento_mouse_by_xpath_com_scroll(self, iframe, path):
        """
        Clica em um elemento localizado por XPath dentro de um iframe após realizar um scroll.

        Args:
            iframe (str): Nome ou ID do iframe onde o elemento está localizado.
            path (str): Caminho XPath do elemento.

        Returns:
            None
        """
        # Voltar para o contexto padrão
        self.browser.switch_to.default_content()
        
        # Trocar para o iframe especificado
        self.browser.switch_to.frame(iframe)
        
        # Encontrar o elemento no iframe
        element = self.browser.find_element(By.XPATH, path)
        
        # Executar um scroll para que o elemento fique visível
        self.browser.execute_script("arguments[0].scrollIntoView();", element)
        
        # Aguardar um momento para a página rolar até o elemento
        sleep(2)
        
        # Clicar no elemento
        element.click()
        sleep(2)
        
        # Voltar para o contexto padrão
        self.browser.switch_to.default_content()

    def clica_elemento_enter_by_xpath_com_scroll(self, iframe, path):
        """
        Clica em um elemento localizado por XPath dentro de um iframe após realizar um scroll.

        Args:
            iframe (str): Nome ou ID do iframe onde o elemento está localizado.
            path (str): Caminho XPath do elemento.

        Returns:
            None
        """
        # Voltar para o contexto padrão
        self.browser.switch_to.default_content()
        
        # Trocar para o iframe especificado
        self.browser.switch_to.frame(iframe)
        
        # Encontrar o elemento no iframe
        element = self.browser.find_element(By.XPATH, path)
        
        # Executar um scroll para que o elemento fique visível
        self.browser.execute_script("arguments[0].scrollIntoView();", element)
        
        # Aguardar um momento para a página rolar até o elemento
        sleep(2)
        
        # Clicar no elemento
        element.click()
        sleep(2)

        # Simular a tecla Enter
        action = ActionChains(self.browser)
        action.send_keys(Keys.ENTER).perform()
        
        # Voltar para o contexto padrão
        self.browser.switch_to.default_content()

    def clica_elemento_text_by_xpath(self, iframe, path):
        """
        Clica em um elemento localizado por XPath dentro de um iframe.
        Args:
            iframe (str): Nome ou ID do iframe onde o elemento está localizado.
            path (str): Caminho XPath do elemento.
        Returns:
            None
        """
        try:
            self.browser.switch_to.default_content()
            self.browser.switch_to.frame(iframe)
            elemento = self.browser.find_element(By.XPATH, path)
            actions = ActionChains(self.browser)
            actions.move_to_element(elemento).click().perform()
            self.browser.switch_to.default_content()
        except self.exception as e:
            return f"Erro ao clicar no elemento: {e}"
    
    def clica_elemento_by_xpath(self, iframe, path):
        """
        Clica em um elemento localizado por XPath dentro de um iframe.
        Args:
            iframe (str): Nome ou ID do iframe onde o elemento está localizado.
            path (str): Caminho XPath do elemento.
        Returns:
            None
        """
        try:
            self.browser.switch_to.default_content()
            self.browser.switch_to.frame(iframe)
            self.browser.find_element(By.XPATH, path).click()
            self.browser.switch_to.default_content()
        except self.exception as e:
            print(f"Erro ao clicar no elemento: {e}")

    def clica_elemento_tabela_html(self, iframe, valor_alvo):
        """
        Clica em um elemento HTML se ele tiver o valor alvo e estiver na mesma linha que a palavra "Órgãos".

        Parâmetros:
        - valor_alvo (str): O valor que você está procurando, como '17000'.

        Retorna:
        - bool: True se o elemento foi clicado com sucesso, False caso contrário.
        """
        try:
            self.browser.switch_to.frame(iframe)

            # XPath para o elemento com o valor 'Órgãos'
            xpath_orgaos = '//*[@id="TGROW105_10"]/td[4]/div'
            
            # XPath para o elemento com o valor alvo
            xpath_valor_alvo = f'//*[@id="TGROW105_10"]/td[2]/div[text()="{valor_alvo}"]'

            # Verificar se ambos os elementos existem e contêm os textos desejados
            if (self.browser.find_element(By.XPATH, xpath_orgaos).text == 'Órgãos' and
                self.browser.find_element(By.XPATH, xpath_valor_alvo).text == valor_alvo):
                
                # Clicar no elemento com o valor alvo
                self.browser.find_element(By.XPATH, xpath_valor_alvo).click()
                return True

            else:
                print(f"Elemento com valor {valor_alvo} não está na mesma linha que 'Órgãos'.")
                return False

        except self.exception as e:
            print(f"Erro ao tentar clicar no elemento: {e}")
            return False

    def achar_elemento_by_xpath(self, iframe, path):
        """
        Retorna um elemento localizado por XPath dentro de um iframe.

        Args:
            iframe (str): Nome ou ID do iframe onde o elemento está localizado.
            path (str): Caminho XPath do elemento.

        Returns:
            WebElement: O elemento encontrado.
        """
        try:
            self.browser.switch_to.frame(iframe)
            elemento = self.browser.find_element(By.XPATH, path)
            return elemento
        except self.exception as e:
            print(f"Erro ao encontrar elemento ou iframe: {e}")
        finally:
            self.browser.switch_to.default_content()

    def entrar_no_sei(self, login, senha, orgao): ##inclui orgao##aqui
        """
        Acessa um site usando o browser Chrome, maximiza a janela e aguarda pelo tempo especificado.
        
        Parâmetros:
        - url (str): Endereço do site que será acessado.
        - tempo_espera (int): Tempo em segundos que o método deve aguardar após acessar o site.
        
        Retorna:
        - Nenhum.
        """
        # url = 'https://sei.economia.gov.br/sei/'
        # url = 'https://sei.economia.gov.br/sei/controlador.php?acao=procedimento_controlar&infra_sistema=100000100&infra_unidade_atual=110008413&infra_hash=aae589ff7743c67d4340a25e675583fd78fa76651284fa0915d3e578fb6309ed4f68bdfd46783a706c09d9feb0e3388cc8db0e3e892390ee7bdac65027cca176642a09d3bc582a7286be4a0faaa0606166b9f246819dcbfd6888a7d272e3e625'
        url = 'https://sei.economia.gov.br/sei/controlador.php?acao=procedimento_controlar&infra_sistema=100000100&infra_unidade_atual=110008413&infra_hash=2494808ba9db03f3d834f1978bce5ba1cfb338bbea28a37efcb4c468b0eebbb26f81898d8ca1e180601af3d3edfb11ca173a7055d824ec4f6d30a677fbc91fc561ad329d0b0a7896e774f34ac4465c9b7b4d2cd11ab30aea21b3e624878413d7'


        try:
            self.browser.get(url)
            self.browser.maximize_window()
            sleep(3)
            self.browser.find_element(by=By.ID, value='selOrgao').send_keys(orgao) ##aqui
            self.browser.find_element(by=By.ID, value='txtUsuario').send_keys(login)
            self.browser.find_element(by=By.ID, value='pwdSenha').send_keys(senha)
            try: # nem sempre precisa clicar no botao "Acessar" para que o login aconteca
                self.browser.find_element(by=By.ID, value='Acessar').click()
                sleep(1)
            except:
                sleep(1)
        except self.exception as e:
            print(f"Erro ao acessar o site {url}: {e}")

    def inserir_texto_restrito(self, iframe, element_id, text):
        """
        Insere um texto em um elemento localizado por ID dentro de um iframe e pressiona a tecla ENTER.
        Args:
            iframe (str): Nome ou ID do iframe onde o elemento está localizado.
            element_id (str): ID do elemento.
            text (str): Texto a ser inserido no elemento.
        Returns:
            None
        """
        try:
            self.browser.switch_to.frame(iframe)
            wait = WebDriverWait(self.browser, 10)
            # element = wait.until(EC.presence_of_element_located((By.ID, element_id)))
            # Espera explícita antes de enviar as teclas (opcional)
            element = wait.until(EC.element_to_be_clickable((By.ID, element_id)))# Espera até que o elemento possa ser clicado
            element.send_keys(text, text)    
            element.send_keys(Keys.ENTER)  
            sleep(0.5)
            # element.send_keys(Keys.ENTER)  
            self.browser.switch_to.default_content()
        except self.exception as e:
            print(f"Erro ao inserir texto: {e}")

    def inserir_texto_tab_by_id_in_iframe(self, iframe, element_id, text):
        """
        Insere um texto em um elemento localizado por ID dentro de um iframe e pressiona a tecla ENTER.
        Args:
            iframe (str): Nome ou ID do iframe onde o elemento está localizado.
            element_id (str): ID do elemento.
            text (str): Texto a ser inserido no elemento.
        Returns:
            None
        """
        try:
            self.browser.switch_to.frame(iframe)
            wait = WebDriverWait(self.browser, 10)
            # Espera explícita antes de enviar as teclas (opcional)
            element = wait.until(EC.element_to_be_clickable((By.ID, element_id)))# Espera até que o elemento possa ser clicado
            element.send_keys(text)    
            sleep(0.5)
            try:
                element.send_keys(Keys.TAB)
            except StaleElementReferenceException:
                self.browser.switch_to.default_content()
                self.browser.switch_to.frame(iframe)
                element = wait.until(EC.element_to_be_clickable((By.ID, element_id)))
                element.send_keys(Keys.TAB)  
            self.browser.switch_to.default_content()
        except self.exception as e:
            print(f"Erro ao inserir texto: {e}")

    def inserir_texto_tab_enter_by_id_in_iframe(self, iframe, element_id, text):
        """
        Insere um texto em um elemento localizado por ID dentro de um iframe e pressiona a tecla ENTER.
        Args:
            iframe (str): Nome ou ID do iframe onde o elemento está localizado.
            element_id (str): ID do elemento.
            text (str): Texto a ser inserido no elemento.
        Returns:
            None
        """
        try:
            self.browser.switch_to.frame(iframe)
            wait = WebDriverWait(self.browser, 10)
            # Espera explícita antes de enviar as teclas (opcional)
            element = wait.until(EC.element_to_be_clickable((By.ID, element_id)))# Espera até que o elemento possa ser clicado
            element.send_keys(text)    
            sleep(0.5)
            element.send_keys(Keys.TAB, Keys.ENTER)
            sleep(0.5)
            # element.send_keys(Keys.ENTER)  
            self.browser.switch_to.default_content()
        except self.exception as e:
            print(f"Erro ao inserir texto: {e}")

    def inserir_texto_enter_by_id_in_iframe(self, iframe, element_id, text):
        """
        Insere um texto em um elemento localizado por ID dentro de um iframe e pressiona a tecla ENTER.
        Args:
            iframe (str): Nome ou ID do iframe onde o elemento está localizado.
            element_id (str): ID do elemento.
            text (str): Texto a ser inserido no elemento.
        Returns:
            None
        """
        try:
            self.browser.switch_to.frame(iframe)
            wait = WebDriverWait(self.browser, 10)
            # element = wait.until(EC.presence_of_element_located((By.ID, element_id)))
            # Espera explícita antes de enviar as teclas (opcional)
            element = wait.until(EC.element_to_be_clickable((By.ID, element_id)))# Espera até que o elemento possa ser clicado
            element.send_keys(text)    
            element.send_keys(Keys.ENTER)  
            sleep(0.5)
            # element.send_keys(Keys.ENTER)  
            self.browser.switch_to.default_content()
        except self.exception as e:
            print(f"Erro ao inserir texto: {e}")

    def inserir_texto_enter_by_xpath_in_iframe(self, iframe, xpath, text):
        """
        Insere um texto em um elemento localizado por ID dentro de um iframe e pressiona a tecla ENTER.
        Args:
            iframe (str): Nome ou ID do iframe onde o elemento está localizado.
            xpath (str): xpath do elemento.
            text (str): Texto a ser inserido no elemento.
        Returns:
            None
        """
        try:
            self.browser.switch_to.frame(iframe)
            wait = WebDriverWait(self.browser, 10)
            element = wait.until(EC.presence_of_element_located((By.ID, xpath)))
            element.send_keys(text)
            sleep(2)
            element.send_keys(Keys.ENTER)
            self.browser.switch_to.default_content()
        except self.exception as e:
            print(f"Erro ao inserir texto: {e}")
            
    def inserir_texto_enter_by_id(self, element_id, text):
        """
        Insere um texto em um elemento localizado por ID e pressiona a tecla ENTER.
        Args:
            element_id (str): ID do elemento.
            text (str): Texto a ser inserido no elemento.
        Returns:
            None
        """
        try:
            wait = WebDriverWait(self.browser, 10)
            element = wait.until(EC.presence_of_element_located((By.ID, element_id)))
            element.clear()
            element.send_keys(text)
            sleep(2)
            element.send_keys(Keys.ENTER)
            self.browser.switch_to.default_content()
        except self.exception as e:
            print(f"Erro ao inserir texto: {e}")

    def acessar_site_chrome(self, url, tempo_espera): 
        """
        Acessa um site usando o browser Chrome, maximiza a janela e aguarda pelo tempo especificado.
        
        Parâmetros:
        - url (str): Endereço do site que será acessado.
        - tempo_espera (int): Tempo em segundos que o método deve aguardar após acessar o site.
        
        Retorna:
        - Nenhum.
        """
        try:
            self.browser.get(url)
            self.browser.maximize_window()
            self.contagem_regressiva(tempo_espera)
        except self.exception as e:
            print(f"Erro ao acessar o site {url}: {e}")

    def contagem_regressiva(self, segundos):
        """
        Realiza uma contagem regressiva de segundos exibindo mensagens.

        Args:
            segundos (int): O número de segundos para a contagem regressiva.

        Returns:
            None
        """
        try:
            for i in range(segundos, -1, -1):
                if i == 0:
                    print("Iniciando!")
                else:
                    print(f"Iniciando em {i} segundos...")
                sleep(1)
        except self.exception as e:
            print(f"Erro durante a contagem regressiva: {e}")

    def open_browser(self, url, browser_type="firefox"): #aqui self
        try:
            if browser_type == "firefox":
                driver = webdriver.Firefox()
            elif browser_type == "chrome":
                driver = webdriver.Chrome()
            else:
                print(f"Tipo de navegador {browser_type} não suportado!")
                return None

            driver.get(url)
            return driver
        except self.exception as e:
            print(f"Erro ao abrir o browser: {e}")
            return None

    def tempo_aleatorio(self, inicio, fim):
        """
        Retorna um número aleatório entre os valores 'inicio' e 'fim'.
        
        Parâmetros:
        - inicio (int): Valor mínimo para a geração do número aleatório.
        - fim (int): Valor máximo para a geração do número aleatório.
        
        Retorna:
        - int: Número aleatório entre 'inicio' e 'fim'.
        """
        try:
            tempo = random.randint(inicio, fim)
            return tempo
        except self.exception as e:
            print(f"Erro ao gerar tempo aleatório: {e}")
            return (inicio + fim) // 2  # retorna um valor médio entre 'inicio' e 'fim' em caso de erro
    
    def tela_aviso(self, path): 
        """
        Fecha a janela de aviso se encontrada.
        Parâmetros:
        - path (str): XPath do elemento a ser buscado.
        Retorna:
        - Nenhum.
        """
        try:
            self.browser.implicitly_wait(30)
            if self.browser.find_element(By.XPATH, path):  
                self.browser.find_element(By.XPATH, path).click()
        except self.exception as e:
            print(f"Erro ao fechar janela de aviso: {e}")

    def sel_unidade(self, path): 
        """
        Seleciona uma unidade no browser.
        Parâmetros:
        - path (str): XPath do elemento a ser buscado.
        Retorna:
        - Nenhum.
        """
        try:
            self.browser.implicitly_wait(30)
            self.browser.find_element(By.XPATH, path).click()
            sleep(self.tempo_aleatorio())
        except self.exception as e:
            print(f"Erro ao selecionar unidade: {e}")

    def visua_detal(self, path): 
        """
        Seleciona a visualização detalhada no controle de processos.
        Parâmetros:
        - path (str): XPath do elemento a ser buscado.
        Retorna:
        - Nenhum.
        """
        try:
            sleep(self.tempo_aleatorio())
            self.browser.find_element(By.XPATH, path).click()
            sleep(self.tempo_aleatorio())
        except self.exception as e:
            print(f"Erro ao selecionar visualização detalhada: {e}")

    def procura_marcador(self, path): 
        """
        Seleciona a visualização por marcadores e clica no marcador especificado.
        Parâmetros:
        - path (str): XPath do marcador a ser clicado.
        Retorna:
        - Nenhum.
        """
        try:
            self.browser.implicitly_wait(30)
            self.browser.find_element(By.XPATH, path).click()
            sleep(self.tempo_aleatorio())
        except self.exception as e:
            print(f"Erro ao procurar marcador: {e}")
            
    def procura_proc_esp(self, path, processo): 
        """
        Busca por um processo específico usando o XPath fornecido.
        Parâmetros:
        - path (str): XPath do campo de pesquisa do processo.
        - processo (str): Número ou identificação do processo a ser buscado.
        Retorna:
        - Nenhum.
        """
        try:
            tempo = random.randint(3, 7)
            self.browser.implicitly_wait(30)
            self.browser.find_element(By.XPATH, path).click()
            busca_proc = self.browser.find_element(By.XPATH, path)
            busca_proc.send_keys(processo)
            sleep(tempo)
            busca_proc.send_keys(Keys.ENTER)
        except self.exception as e:
            print(f"Erro ao procurar processo específico: {e}")

    def edita_elemento_in_iframe(self, iframe_xpath, element_xpath, new_text):
        """
        Edita o texto de um elemento HTML dentro de um iframe usando Selenium.

        Args:
            iframe_xpath (str): XPath do iframe que contém o elemento.
            element_xpath (str): XPath do elemento a ser editado.
            new_text (str): Novo texto para ser definido no elemento.

        Returns:
            None
        """
        # Mudar para o iframe
        self.browser.switch_to.frame(self.browser.find_element(By.XPATH, iframe_xpath))
        
        # Encontrar o elemento
        element = self.browser.find_element(By.XPATH, element_xpath)             
        # Executar o script para alterar o texto
        self.browser.execute_script("arguments[0].innerText = arguments[1];", element, new_text)
        
        # Voltar ao conteúdo principal (opcional)
        self.browser.switch_to.default_content()

    def troca_habilitacao(self, iframe_elemento, path, iframe_text, element_id, text, elemento_tabela):
        self.clica_elemento_by_xpath(iframe_elemento, path)
        sleep(2)
        self.inserir_texto_enter_by_id_in_iframe(iframe_text, element_id, text)
        sleep(2)
        self.clica_elemento_enter_by_xpath_com_scroll('WA1', elemento_tabela)

class SeiGeral:
    def tempo_aleatorio(self):
        tempo = random.randint(2, 4)
        return tempo

    def tela_aviso(self, navegador):
        try:
            close_btn = WebDriverWait(navegador, 5).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div[2]/div[1]/div[3]/img'))
            )
            navegador.execute_script("arguments[0].click();", close_btn)

        except:
            print("Não foi possível fechar o pop-up.")
            return

    def get_unidades(self, navegador):
        unidades = []

        try:
            WebDriverWait(navegador, 10).until(EC.element_to_be_clickable(
                (By.CSS_SELECTOR, 'div.nav-item:nth-child(3) > div:nth-child(1) > a:nth-child(1)'))).click()
            sleep(self.tempo_aleatorio())  # Simula comportamento humano

            WebDriverWait(navegador, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="selInfraOrgaoUnidade"]'))).send_keys(
                'MGI')  # Escolhe Unidade
            sleep(self.tempo_aleatorio())  # Simula comportamento humano

        except TimeoutException:
            print("Elemento não encontrado ou não clicável dentro do tempo limite.")
        # (O código para acessar a página correta fica aqui)

        rows = navegador.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/form/div[3]/table/tbody/tr')
        for row in rows[1:]:  # Começando de 1 para pular o cabeçalho da tabela
            try:
                second_column_text = row.find_element(By.XPATH, "./td[2]").text
                unidades.append(second_column_text)
            except NoSuchElementException as e:
                print("Erro ao processar uma linha: ", str(e))
                continue
        print(unidades)
        return unidades

    def sel_unidade(self, navegador, unidade):
        # Clica em selação da Unidade

        rows = navegador.find_elements(By.XPATH, '/html/body/div[1]/div/div[2]/form/div[3]/table/tbody/tr')

        found = False

        for row in rows[1:]:
            try:

                second_column_text = row.find_element(By.XPATH, "./td[2]").text

                if unidade in second_column_text:
                    print(f"Texto '{unidade}' encontrado na linha!")

                    first_column_radiobutton = row.find_element(By.XPATH, "./td[1]//input[@type='radio']")
                    is_checked = first_column_radiobutton.get_attribute('checked')

                    if is_checked:

                        navegador.find_element(By.XPATH, '/html/body/div[1]/nav/div/div[3]/div[2]/div[4]/a/img').click()
                    else:

                        navegador.execute_script("arguments[0].click();", first_column_radiobutton)

                    found = True
                    break
                else:
                    print("Texto não encontrado.")

            except NoSuchElementException as e:
                print("Erro ao processar uma linha: ", str(e))
                continue

        if not found:
            print(f"Texto '{unidade}' não foi encontrado em nenhuma linha!")
        sleep(self.tempo_aleatorio())

    def visua_detal(self, navegador):

        sleep(self.tempo_aleatorio())  # Simula comportamento humano

        try:
            WebDriverWait(navegador, 5).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/form/div/div[4]/div[1]/a'))).click()
            sleep(self.tempo_aleatorio())  # Simula comportamento humano
        except TimeoutException:
            print("Elemento não encontrado ou não clicável dentro do tempo limite.")

    def procura_marcador(self, navegador):

        try:
            WebDriverWait(navegador, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="divFiltro"]/div[4]/a'))).click()
            sleep(self.tempo_aleatorio())  # Simula comportamento humano

            WebDriverWait(navegador, 5).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@onclick="filtrarMarcador(74870)"]'))).click()
            sleep(self.tempo_aleatorio())  # Simula comportamento humano
        except TimeoutException:
            print("Um dos elementos não foi encontrado ou não era clicável dentro do tempo limite.")

    def procura_proc_esp(self, navegador, processo):
        # Busca por um processo específico
        tempo = random.randint(3, 7)
        navegador.implicitly_wait(10)
        navegador.find_element(By.XPATH, '//*[@id="txtPesquisaRapida"]').click()
        busca_proc = navegador.find_element(By.XPATH, '//*[@id="txtPesquisaRapida"]')
        busca_proc.send_keys(processo)
        sleep(tempo)
        busca_proc.send_keys(Keys.ENTER)

    def num_processo(self, navegador):
        try:
            WebDriverWait(navegador, 5).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, 'ifrArvore')))
            process = WebDriverWait(navegador, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'infraArvoreNoSelecionado'))).text.strip()
            sleep(self.tempo_aleatorio())  # Simula comportamento humano
            return process
        except TimeoutException:
            print("Um dos elementos não foi encontrado dentro do tempo limite.")
            return None

    def le_relatorio(self, navegador):
        # apoio = Util_suport()
        try:
            # Espera até que o elemento com o XPath especificado esteja presente. O tempo máximo de espera é 10 segundos.
            elemento = WebDriverWait(navegador, 3).until(
                EC.presence_of_element_located((By.XPATH, '//img[@title="Abrir todas as Pastas"]'))
            )
            elemento.click()
        except TimeoutException:
            print("O elemento não foi encontrado no tempo especificado.")

        if navegador.find_elements(By.PARTIAL_LINK_TEXT, "Relatório"):
            relat = navegador.find_elements(By.PARTIAL_LINK_TEXT, "Relatório")
            relat[-1].click()
            navegador.switch_to.default_content()
            navegador.switch_to.frame('ifrVisualizacao')
            navegador.switch_to.frame('ifrArvoreHtml')

        tabelas = navegador.find_elements(By.TAG_NAME, 'table')

        # Vamos guardar as matrículas encontradas aqui
        matriculas_encontradas = []

        # Loop para percorrer todas as tabelas
        for i, tabela in enumerate(tabelas):
            linhas = tabela.find_elements(By.TAG_NAME, 'tr')

            for linha in linhas:
                if "Matrícula SIAPE:" in linha.text:
                    print(f"Encontrado na tabela {i + 1}: {linha.text}")

                    # Usamos Regex para pegar o número da matrícula na linha
                    match = re.search(r'Matrícula SIAPE:\s*(\d{7,8})', linha.text)
                    if match:
                        matricula = match.group(1)
                        matriculas_encontradas.append(matricula)
                        print(f"Matrícula encontrada: {matricula}")

        # Verificar se encontrou alguma matrícula
        benef_mat = matriculas_encontradas[0]
        inst_mat = matriculas_encontradas[1]
        print(f"Matrícula da beneficiária: {benef_mat}")
        print(f"Matrícula do instituidor: {inst_mat}")
        return benef_mat, inst_mat
        sleep(300)

    def captura_dados(self, navegador, process):

        apoio = Util_suport()
        try:
            # Espera até que o elemento com o XPath especificado esteja presente. O tempo máximo de espera é 10 segundos.
            elemento = WebDriverWait(navegador, 10).until(
                EC.presence_of_element_located((By.XPATH, '//img[@title="Abrir todas as Pastas"]'))
            )
            elemento.click()
        except TimeoutException:
            print("O elemento não foi encontrado no tempo especificado.")

        try:
            WebDriverWait(navegador, 5).until(
                EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, "Comprovante de lan")))
            troca = self.troca_marcador(navegador, apoio.verificar_cod_erros(1))
            return apoio.verificar_cod_erros(1)
        except TimeoutException:
            print("O elemento com texto parcial 'Comprovante de lan' não foi encontrado dentro do tempo limite.")

        # Verífica a existencia de Planilha de Cálculo.
        if navegador.find_elements(By.PARTIAL_LINK_TEXT, "Planilha de Cálculo"):

            meses = []
            anos = []
            valores = []
            numero_esquerda = []
            numero_direita = []
            cota_esquerda = []
            cota_direita = []
            nome_benes = []
            mat_bene = []
            cot_parte = []
            mat_inst = ""
            valor2 = 0
            valor3 = 0

            plan = navegador.find_elements(By.PARTIAL_LINK_TEXT, "Planilha de Cálculo")
            plan[-1].click()
            navegador.switch_to.default_content()
            navegador.switch_to.frame('ifrVisualizacao')
            navegador.switch_to.frame('ifrArvoreHtml')

            if navegador.find_element(By.CSS_SELECTOR, "body > table:nth-child(6) > tbody > tr:nth-child(1) > "
                                                             "td:nth-child(2)").get_attribute('textContent').strip():
                assunto = navegador.find_element(By.CSS_SELECTOR,"body > table:nth-child(6) > tbody > tr:nth-child(1) > "
                                                             "td:nth-child(2)").get_attribute('textContent').strip()

            else:
                sleep(1)
                troca = self.troca_marcador(navegador, apoio.verificar_cod_erros(3))
                return apoio.verificar_cod_erros(3)

            if navegador.find_element(By.CSS_SELECTOR, "body > table:nth-child(6) > tbody > tr:nth-child(2) > "
                                                       "td:nth-child(2)").get_attribute('textContent').strip():
                objeto = apoio.extrair_numerais(navegador.find_element(By.CSS_SELECTOR, "body > "
                "table:nth-child(6) > tbody > tr:nth-child(2) > td:nth-child(2)").get_attribute('textContent')).strip()

                objetotxt = apoio.extrair_texto(navegador.find_element(By.CSS_SELECTOR, "body > "
                "table:nth-child(6) > tbody > tr:nth-child(2) > td:nth-child(2)").get_attribute('textContent')).strip()
                print(objeto, objetotxt)

                if len(objeto) != 4:
                    troca = self.troca_marcador(navegador, apoio.verificar_cod_erros(22))
                    return apoio.verificar_cod_erros(22)

            else:
                sleep(1)
                troca = self.troca_marcador(navegador, apoio.verificar_cod_erros(4))
                return apoio.verificar_cod_erros(4)

            if navegador.find_element(By.CSS_SELECTOR, "body > table:nth-child(6) > tbody > tr:nth-child(4) > "
                                                       "td:nth-child(2)").get_attribute('textContent').strip():
                descricao = navegador.find_element(By.CSS_SELECTOR, "body > table:nth-child(6) > tbody > "
                                            "tr:nth-child(4) > td:nth-child(2)").get_attribute('textContent').strip()

            else:
                sleep(1)
                troca = self.troca_marcador(navegador, apoio.verificar_cod_erros(5))
                return apoio.verificar_cod_erros(5)

            if navegador.find_element(By.CSS_SELECTOR, "body > table:nth-child(8) > tbody > tr:nth-child(3) > "
                                                       "td:nth-child(2)").get_attribute('textContent').strip():
                nome_inst = navegador.find_element(By.CSS_SELECTOR, "body > table:nth-child(8)"
                                    " > tbody > tr:nth-child(3) > td:nth-child(2)").get_attribute('textContent').strip()

            else:
                sleep(1)
                troca = self.troca_marcador(navegador, apoio.verificar_cod_erros(5))
                return apoio.verificar_cod_erros(5)

            if navegador.find_element(By.CSS_SELECTOR, "body > table:nth-child(8) > tbody > tr:nth-child(2) > "
                                                       "td:nth-child(2)").get_attribute('textContent').strip():
                sit_func = navegador.find_element(By.CSS_SELECTOR, "body > table:nth-child(8) > tbody > "
                                            "tr:nth-child(2) > td:nth-child(2)").get_attribute('textContent').strip()

            else:
                sleep(1)
                troca = self.troca_marcador(navegador, apoio.verificar_cod_erros(6))
                return apoio.verificar_cod_erros(6)

            if navegador.find_element(By.CSS_SELECTOR, "body > table:nth-child(8) > tbody > tr:nth-child(4) > "
                                                       "td:nth-child(2)").get_attribute('textContent').strip():
                orgao1 = navegador.find_element(By.CSS_SELECTOR, "body > table:nth-child(8) > tbody > tr:nth-child(4) >"
                                                                 " td:nth-child(2)").get_attribute('textContent').strip()

            else:
                sleep(1)
                troca = self.troca_marcador(navegador, apoio.verificar_cod_erros(8))
                return apoio.verificar_cod_erros(8)

            if navegador.find_element(By.CSS_SELECTOR, "body > table:nth-child(8) > tbody > tr:nth-child(5) > "
                                                       "td:nth-child(2)").get_attribute('textContent').strip():
                upag = navegador.find_element(By.CSS_SELECTOR, "body > table:nth-child(8) > tbody > tr:nth-child(5) > "
                                                               "td:nth-child(2)").get_attribute('textContent').strip()

            else:
                sleep(1)
                troca = self.troca_marcador(navegador, apoio.verificar_cod_erros(9))
                return apoio.verificar_cod_erros(9)

            ultim_carac = upag[-1]
            upag1 = '0' * 8 + ultim_carac

            if navegador.find_element(By.CSS_SELECTOR, "body > table:nth-child(8) > tbody > tr:nth-child(6) > "
                                                       "td:nth-child(2)").get_attribute('textContent').strip():
                mat_inst = navegador.find_element(By.CSS_SELECTOR, "body > table:nth-child(8) > tbody > tr:nth-child(6)"
                                                            " > td:nth-child(2)").get_attribute('textContent').strip()

            else:
                sleep(1)
                troca = self.troca_marcador(navegador, apoio.verificar_cod_erros(10))
                return apoio.verificar_cod_erros(10)
            tabela = navegador.find_element(By.XPATH, '/html/body/table[5]')
            if len(mat_inst) > 7:
                troca = self.troca_marcador(navegador, apoio.verificar_cod_erros(21))
                return apoio.verificar_cod_erros(21)
            total = 0
            linhas = tabela.find_elements(By.TAG_NAME, 'tr')

            num_linhas_processadas = 0

            for linha in linhas:
                # Ignorar as duas primeiras linhas (cabeçalho)
                if num_linhas_processadas < 2:
                    num_linhas_processadas += 1
                    continue

                # Extrair as células da linha
                celulas = linha.find_elements(By.TAG_NAME, 'td')

                if celulas[0].text.strip() == "TOTAL":
                    tot_tab = float(apoio.converter_string_para_float(celulas[-1].text.strip()))
                    break  # Sai do loop se a célula [0] contém "TOTAL"

                if celulas[1].text.strip() == "TOTAL":
                    tot_tab = float(apoio.converter_string_para_float(celulas[-1].text.strip()))
                    break  # Sai do loop se a célula [0] contém "TOTAL"

                if celulas[2].text.strip() == "TOTAL":
                    tot_tab = float(apoio.converter_string_para_float(celulas[-1].text.strip()))
                    break  # Sai do loop se a célula [0] contém "TOTAL"

                if celulas[3].text.strip() == "TOTAL":
                    tot_tab = float(apoio.converter_string_para_float(celulas[-1].text.strip()))
                    break  # Sai do loop se a célula [0] contém "TOTAL"

                if all(not celula.text.strip() for celula in celulas):
                    continue  # Pula para a próxima iteração se a linha estiver vazia

                mes = celulas[0].text.strip()
                ano = celulas[1].text.strip()
                valor = celulas[4].text.strip()
                valor2 = apoio.converter_string_para_float(valor)

                valEsq, valDir = apoio.converter_string_para_strings(valor2)
                # total += classes_apoio.Convert_String_To_Float.converter_string_para_float(valor)



                # Adicionar os valores às listas correspondentes
                meses.append(mes)
                anos.append(ano)
                valores.append(valor)
                valor3 = float(valor3) + float(valor2)
                numero_esquerda.append(valEsq)
                numero_direita.append(valDir)

            tabela2 = navegador.find_element(By.XPATH, '/html/body/table[6]')

            total2 = 0
            linhas2 = tabela2.find_elements(By.TAG_NAME, 'tr')

            num_linhas_processadas2 = 0

            for linha2 in linhas2:
                # Ignorar as duas primeiras linhas (cabeçalho)
                if num_linhas_processadas2 < 2:
                    num_linhas_processadas2 += 1
                    continue

                # Extrair as células da linha
                celulas2 = linha2.find_elements(By.TAG_NAME, 'td')

                if all(not celula2.text.strip() for celula2 in celulas2):
                    continue  # Pula para a próxima iteração se a linha estiver vazia

                nome_bene = celulas2[0].text.strip()
                matinee = celulas2[1].text.strip()
                cot_parte2 = celulas2[2].text.strip()
                esquerdaCot, direitaCot = apoio.converter_string_para_strings(cot_parte2)
                info_list = [matinee, cot_parte2]

                # Adicionar os valores às listas correspondentes
                nome_benes.append(nome_bene)
                mat_bene.append(matinee)
                cota_esquerda.append(esquerdaCot)
                cota_direita.append(direitaCot)

                sleep(2)
            folha_comp = [folha + str(comp) for folha, comp in zip(meses, anos)]

            process_limpo = re.sub(r'[^a-zA-Z0-9]', '', process)
            process_limpo = apoio.remover_posicoes(process_limpo, [-1, -1, -3, -3])
            process_parte1 = apoio.remover_posicoes(process_limpo, [5, 6, 7, 8, 9, 10, 11, 12])
            process_parte2 = apoio.remover_posicoes(process_limpo, [0, 1, 2, 3, 4, 11, 12])
            process_parte3 = apoio.remover_posicoes(process_limpo, [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

            valor4 = apoio.arredondar_para_baixo_str(valor3)
            tot_tab1 = apoio.arredondar_para_baixo_str(tot_tab)


            if valor4 != tot_tab1:
                troca = self.troca_marcador(navegador, apoio.verificar_cod_erros(12))
                return apoio.verificar_cod_erros(12)

            seq_mes_ano = apoio.verificar_mes_ano(meses, anos)

            if seq_mes_ano != "Sequência correta.":
                troca = self.troca_marcador(navegador, seq_mes_ano)
                return seq_mes_ano

            infoExtant = {'uniProc': process_parte1, 'idProc': process_parte2, 'anoProc': process_parte3,
                          'assunto': assunto, 'objeto': objeto, 'objetotxt': objetotxt, 'descricao': descricao,
                          'sit_func': sit_func, 'orgao': orgao1, 'upag': upag1, 'nome_inst': nome_inst,
                          'matInst': mat_inst,
                          'mesFol': meses, 'compFol': anos, 'nome_benes': nome_benes, 'matBene': mat_bene,
                          'valorEsq': numero_esquerda,
                          'valorDir': numero_direita, 'cotEsq': cota_esquerda, 'cotDir': cota_direita, 'total': tot_tab}


            return infoExtant


        else:

            troca = self.troca_marcador(navegador, apoio.verificar_cod_erros(2))

            return apoio.verificar_cod_erros(2)

    def inclui_comprov(self, navegador, arquiv):
        navegador.implicitly_wait(5)
        navegador.switch_to.default_content()
        navegador.switch_to.frame('ifrVisualizacao')
        navegador.find_element(By.XPATH, '//*[@id="divArvoreAcoes"]/a[1]/img').click()
        sleep(self.tempo_aleatorio())
        navegador.find_element(By.XPATH, '//*[@id="tblSeries"]/tbody/tr[1]/td/a[2]').click()
        sleep(self.tempo_aleatorio())
        navegador.find_element(By.XPATH, '//*[@id="selSerie"]').send_keys('Cadastro')

        navegador.find_element(By.XPATH, '//*[@id="txtDataElaboracao"]').send_keys(datetime.now().strftime('%d/%m/%Y'))

        navegador.find_element(By.XPATH, '//*[@id="txtNomeArvore"]').send_keys(
            ' - Dados do Benefício')

        navegador.find_element(By.XPATH, '//*[@id="divOptNato"]/div/label').click()
        sleep(self.tempo_aleatorio())
        navegador.find_element(By.XPATH, '//*[@id="divOptRestrito"]/div/label').click()
        sleep(self.tempo_aleatorio())
        drop = Select(navegador.find_element(By.XPATH, '//*[@id="selHipoteseLegal"]'))

        drop.select_by_visible_text("Informação Pessoal (Art. 31 da Lei nº 12.527/2011)")

        navegador.find_element(By.XPATH, '//*[@id="lblArquivo"]').click()
        sleep(self.tempo_aleatorio())

        arquivo = arquiv
        escolhe_arquivo = eSIAPEGeral()
        salva_arquivo = escolhe_arquivo.insere_comprovante(arquivo)
        sleep(self.tempo_aleatorio())
        navegador.find_element(By.XPATH, '//*[@id="btnSalvar"]').click()
        sleep(self.tempo_aleatorio())

        return True

    def inclui_nota_tecnica(self, navegador, dados_nottec):
        navegador.implicitly_wait(5)
        navegador.switch_to.default_content()
        navegador.switch_to.frame('ifrArvore')
        protoc_comp = navegador.find_element(By.PARTIAL_LINK_TEXT, "Comprovante de lançamento em módulo").text.strip()
        convert = Util_suport()
        protocol = convert.extrair_numerais(protoc_comp)

        #navegador.find_element(By.XPATH, '//*[@id="span39713917"]').click()
        sleep(self.tempo_aleatorio())
        navegador.switch_to.default_content()
        navegador.switch_to.frame('ifrVisualizacao')
        # navegador.switch_to.frame('ifrArvoreHtml')
        navegador.find_element(By.XPATH, '/html/body/div[1]/div/div/div[2]/div/a[1]/img').click()
        sleep(self.tempo_aleatorio())
        navegador.find_element(By.XPATH, '//*[@id="txtFiltro"]').send_keys('Nota Técnica', Keys.TAB)
        sleep(self.tempo_aleatorio())
        navegador.find_element(By.XPATH, '//*[@id="tblSeries"]/tbody/tr[12]/td/a[2]/span').click()
        sleep(self.tempo_aleatorio())
        navegador.find_element(By.XPATH, '//*[@id="divOptProtocoloDocumentoTextoBase"]/div/label').click()
        sleep(self.tempo_aleatorio())
        if dados_nottec['total'] < 30000:
            navegador.find_element(By.XPATH, '//*[@id="txtProtocoloDocumentoTextoBase"]').send_keys("35550049")
        elif dados_nottec['total'] >= 30000:
            navegador.find_element(By.XPATH, '//*[@id="txtProtocoloDocumentoTextoBase"]').send_keys("35550639")
        sleep(self.tempo_aleatorio())
        navegador.find_element(By.XPATH, '//*[@id="divOptRestrito"]/div/label').click()
        sleep(self.tempo_aleatorio())
        drop = Select(navegador.find_element(By.XPATH, '//*[@id="selHipoteseLegal"]'))

        drop.select_by_visible_text("Informação Pessoal (Art. 31 da Lei nº 12.527/2011)")

        processo_Sei = dados_nottec['numSei']
        proc_Siape = dados_nottec['numSiape']
        objeto = dados_nottec['objeto']
        objetotxt = dados_nottec['objetotxt']
        interessado = dados_nottec['benefs']
        orgao = dados_nottec['orgao']
        mat_int = dados_nottec['mat_int']
        meses_completos = {
            "JAN": "Janeiro", "FEV": "Fevereiro", "MAR": "Março", "ABR": "Abril",
            "MAI": "Maio", "JUN": "Junho", "JUL": "Julho", "AGO": "Agosto",
            "SET": "Setembro", "OUT": "Outubro", "NOV": "Novembro", "DEZ": "Dezembro"
        }
        mes = dados_nottec['meses']
        ano = dados_nottec['anos']
        valor = dados_nottec['total']
        mes = [meses_completos[m] for m in mes]
        if len(mes) == 1 and len(ano) == 1:
            data_texto = f"{mes[0]} de {ano[0]}"
        else:
            data_texto = f"{mes[0]} de {ano[0]} a {mes[-1]} de {ano[-1]}"
        locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
        valor_formatado = locale.currency(valor, grouping=True, symbol=True)
        valor_extenso = num2words(valor, lang='pt_BR', to='currency')
        # Pega o menor tamanho entre as duas listas
        min_tamanho = min(len(interessado), len(mat_int))

        # Usa o 'zip' e o 'join' apenas nos elementos que têm um par correspondente
        interessados_formatados = ', '.join(
            f'{nome} - SIAPE : {matricula}' for nome, matricula in
            zip(interessado[:min_tamanho], mat_int[:min_tamanho]))

        texto_padrao = f"Nos termos do presente expediente e em face do que consta dos autos, reconheço a dívida e autorizo o " \
                       f"pagamento do valor de {valor_formatado} ({valor_extenso}), inscrito no Módulo de Exercícios Anteriores do Sistema SIAPE, em " \
                       f"favor do(a) senhor(a) {interessados_formatados}, mediante o desbloqueio sistêmico do " \
                       f"presente Processo Administrativo no Módulo de Exercícios Anteriores do Sistema SIAPE."

        navegador.find_element(By.XPATH, '//*[@id="btnSalvar"]').click()
        sleep(self.tempo_aleatorio())
        janela_original = navegador.current_window_handle
        navegador.implicitly_wait(10)
        for window_handle in navegador.window_handles:
            if window_handle != janela_original:
                navegador.switch_to.window(window_handle)
                navegador.maximize_window()
                frame = navegador.find_elements(By.CLASS_NAME, 'cke_wysiwyg_frame')
                navegador.switch_to.frame(frame[7])
                sleep(self.tempo_aleatorio())
                navegador.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[1]/td[2]').send_keys(processo_Sei,
                                                                                                    Keys.TAB, Keys.TAB)

                navegador.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[2]/td[2]').send_keys(" ", proc_Siape,
                                                                                                    Keys.TAB, Keys.TAB)

                navegador.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[3]/td[2]').send_keys(" ", objeto, " ",
                                                                                        objetotxt, Keys.TAB, Keys.TAB)


                navegador.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[4]/td[2]').send_keys(" ", interessado,
                                                                                                    Keys.TAB, Keys.TAB)

                navegador.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[5]/td[2]').send_keys(" ", orgao,
                                                                                                    Keys.TAB, Keys.TAB)

                navegador.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[6]/td[2]').send_keys(" ", mat_int,
                                                                                                    Keys.TAB, Keys.TAB)
                # navegador.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[7]/td[2]').clear()
                navegador.find_element(By.XPATH, '/html/body/table[1]/tbody/tr[7]/td[2]').send_keys(' PENSIONISTA')

                # navegador.find_element(By.XPATH, '/html/body/table[3]/tbody/tr/td[1]').clear()
                navegador.find_element(By.XPATH, '/html/body/table[3]/tbody/tr/td[1]').click()
                navegador.find_element(By.XPATH, '/html/body/table[3]/tbody/tr/td[1]').send_keys(" ", data_texto, Keys.TAB)
                # navegador.find_element(By.XPATH, '/html/body/table[3]/tbody/tr/td[2]').clear()
                navegador.find_element(By.XPATH, '/html/body/table[3]/tbody/tr/td[1]').send_keys(" ", valor_formatado, "(", valor_extenso, ")")

                if valor < 30000:
                    navegador.find_element(By.XPATH, '/html/body/p[19]').clear()
                    paragraph = navegador.find_element(By.XPATH, '/html/body/p[19]')
                    navegador.execute_script('arguments[0].innerText = arguments[1]', paragraph, texto_padrao)

                if valor >= 30000:
                    navegador.find_element(By.XPATH, '/html/body/p[27]').clear()
                    paragraph = navegador.find_element(By.XPATH, '/html/body/p[27]')
                    navegador.execute_script('arguments[0].innerText = arguments[1]', paragraph, texto_padrao)
                sleep(1)
                navegador.find_element(By.XPATH, '/html/body/table[7]/tbody/tr[7]/td[2]/p').click()
                # sleep(100)
                navegador.switch_to.default_content()
                navegador.find_element(By.XPATH, '//*[@id="cke_491"]/span[1]').click()
                sleep(self.tempo_aleatorio())
                wait = WebDriverWait(navegador, 10)
                input_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[contains(@id, "cke_")]')))
                input_field.click()
                input_field.send_keys(protocol)

                ok_button = wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//span[contains(@id, "cke_") and contains(@class, "cke_dialog_ui_button")]')))
                ok_button.click()
                navegador.find_element(By.XPATH, '//*[@id="cke_455_label"]').click()
                sleep(2)
                navegador.close()
                navegador.switch_to.window(janela_original)

    from selenium.webdriver.common.action_chains import ActionChains

    def troca_marcador(self, navegador, message):
        wait = WebDriverWait(navegador, 10)

        # Navegando aos iframes
        apoio = Util_suport()
        primeiro_plano = apoio.primeiro_plano(navegador)
        navegador.switch_to.default_content()
        wait.until(EC.frame_to_be_available_and_switch_to_it('ifrArvore'))

        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.infraArvoreNoSelecionado, .infraArvoreNo, .noVisitado'))).click()

        navegador.switch_to.default_content()
        wait.until(EC.frame_to_be_available_and_switch_to_it('ifrVisualizacao'))

        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="divArvoreAcoes"]/a[23]/img'))).click()
        sleep(self.tempo_aleatorio())
        table = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'table')))

        rows = table.find_elements(By.TAG_NAME, "tr")

        for row in rows[1:]:
            if row.find_element(By.XPATH, "td[2]").text.strip() == "CGPAG INTEGRA":
                target_link = row.find_element(By.XPATH, "td[6]//a[img[@src='/infra_css/svg/remover.svg']]")
                ActionChains(navegador).move_to_element(target_link).click(target_link).perform()
                break

        alert = wait.until(EC.alert_is_present())
        alert.accept()

        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="btnAdicionar"]'))).click()
        sleep(self.tempo_aleatorio())
        dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".dd-select")))
        dropdown.click()

        items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".dd-option-text")))
        sleep(0.6)
        for item in items:
            if item.text == "INTEGRA - RETORNO":
                sleep(0.6)
                item.click()
                break
        sleep(self.tempo_aleatorio())
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="txaTexto"]'))).send_keys(message)

        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="sbmSalvar"]'))).click()

        navegador.switch_to.default_content()
        sleep(self.tempo_aleatorio())
        wait.until(EC.frame_to_be_available_and_switch_to_it('ifrArvore'))
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '.infraArvoreNoSelecionado, .infraArvoreNo, .noVisitado'))).click()

        navegador.switch_to.default_content()
        wait.until(EC.frame_to_be_available_and_switch_to_it('ifrVisualizacao'))
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="divArvoreAcoes"]/a[25]/img'))).click()

        navegador.switch_to.default_content()

        return True

class SeleniumSetup:

    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.chromedriver_path = os.path.join(self.base_path, "bin", "chromedriver", "chromedriver.exe")
        self.chrome_binary_path = os.path.join(self.base_path, "bin", "chrome", "App", "Chrome-bin", "chrome.exe")
        self.log_path = os.path.join(self.base_path, "bin", "chromedriver", "chromedriver.log")
        self.download_folder = os.path.join(self.base_path, 'downloads')

        # Criar o diretório 'downloads' se não existir
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)

        # Limpar a pasta de downloads
        self.limpar_downloads(self.download_folder)

    @property
    def get_download_folder(self):
        return self.download_folder

    def limpar_downloads(self, pasta):
        """Remove arquivos com padrão hodcivws*.jsp da pasta especificada"""
        for arquivo in glob.glob(os.path.join(pasta, 'hodcivws*.jsp')):
            os.remove(arquivo)

    def setup_driver(self):
        options = Options()
        prefs = {
            "download.default_directory": self.download_folder,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "credentials_enable_service": False,
            "password_manager_enabled": False
        }
        options.binary_location = self.chrome_binary_path
        options.add_experimental_option("detach", True)
        options.add_experimental_option("prefs", prefs)
        options.add_experimental_option("useAutomationExtension", False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_argument('disable-infobars')

        service = Service(self.chromedriver_path, log_output=self.log_path)
        navegador = webdriver.Chrome(service=service, options=options)
        navegador.maximize_window()
        return navegador
