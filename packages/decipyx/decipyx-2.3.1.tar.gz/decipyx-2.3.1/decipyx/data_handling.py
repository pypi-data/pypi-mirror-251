"""Funções para uso no decipex"""
from pandas.core.internals import concat
import pandas as pd
import datetime as dt
import numpy as np
import calendar
import openpyxl

class DataHandling:

    def arquivos_leitura(self, df_list):
        """
        Lê uma lista de arquivos e retorna um dicionário de DataFrames.
        
        Parâmetros:
        - df_list: Lista de caminhos de arquivos para leitura.
        
        Retorna:
        - Um dicionário onde a chave é o nome do DataFrame (derivado do nome do arquivo) 
        e o valor é o próprio DataFrame.
        
        Exceções:
        - ValueError: Se a extensão do arquivo não for suportada.
        """
        
        def read_file(file_path):
            file_extension = file_path.split('.')[-1]
            if file_extension == 'csv':
                return pd.read_csv(file_path, sep=';')
            elif file_extension == 'xlsx' or file_extension == 'xls':
                return pd.read_excel(file_path)
            elif file_extension == 'parquet':
                return pd.read_parquet(file_path)
            else:
                raise ValueError(f"Extensão {file_extension} não suportada.")
            
        dfs = {}
        for file in df_list:
            name = file.split('/')[-1].split('.')[0].replace(' ', '_')
            dfs[name] = read_file(file)
            print(f"Nome do dataframe listado: " + name)    
            
        return dfs

    def filtra_df(coluna,valor,df):
        """
        Função para filtrar um DataFrame baseado em um valor em uma coluna específica.

        Parâmetros:
            coluna (str): O nome da coluna a ser filtrada.
            valor (str, int, etc.): O valor que a coluna deve ter para a linha ser mantida.
            df (pandas.DataFrame): O DataFrame a ser filtrado.

        Retorna:
            pandas.DataFrame: O DataFrame filtrado.
        """
        df = df.copy()
        df = df.loc[df[coluna] == valor]
        return df

    def filtra_cpf_progressao(df):
        """
        Função para filtrar um DataFrame para conter apenas as linhas com o maior valor em 
        'count_classe_padrao_atual' para cada CPF distinto.

        Parâmetros:
            df (pandas.DataFrame): O DataFrame a ser filtrado.

        Retorna:
            pandas.DataFrame: O DataFrame filtrado.
        """
        df = df.copy()
        df['contador_cpf'] = df.groupby('IT-NU-CPF')['count_classe_padrao_atual'].transform('count')
        df = df.loc[df.groupby('IT-NU-CPF')['count_classe_padrao_atual'].idxmax()]
        return df

    def separa_grmatricula_anomes(df):
        """
        Função para separar a coluna 'GR-MATRICULA-ANO-MES' em três novas colunas: 'Orgão', 'Matrícula', 'Ano', e 'Mês'.

        Parâmetros:
            df (pandas.DataFrame): O DataFrame original que contém a coluna 'GR-MATRICULA-ANO-MES'.

        Retorna:
            pandas.DataFrame: O DataFrame com as novas colunas adicionadas.
        """
        df = df.copy()
        df['GR-MATRICULA-ANO-MES'] = df['GR-MATRICULA-ANO-MES'].astype(str)
        df['Orgão'] = df['GR-MATRICULA-ANO-MES'].str.slice(0, 5)
        df['Matrícula'] = df['GR-MATRICULA-ANO-MES'].str.slice(5, 12)
        Ano_Mês = df['GR-MATRICULA-ANO-MES'].str.slice(12, 18)
        df['Ano'] = Ano_Mês.str.slice(0, 4)
        df['Mês'] = Ano_Mês.str.slice(4, 6)
        return df

    def separa_grmatricula_anomes_gr(df):
        """
        Função para separar a coluna 'GR-MATRICULA-ANO-MES' em três novas colunas: 'OrgãoMatrícula'

        Parâmetros:
            df (pandas.DataFrame): O DataFrame original que contém a coluna 'GR-MATRICULA-ANO-MES'.

        Retorna:
            pandas.DataFrame: O DataFrame com as novas colunas adicionadas.
        """
        df = df.copy()
        df['GR-MATRICULA-ANO-MES'] = df['GR-MATRICULA-ANO-MES'].astype(str)
        df['GR-MATRICULA'] = df['GR-MATRICULA-ANO-MES'].str.slice(0, 11)
        return df

    def separa_grmatricula(df):
        """
        Função para separar a coluna 'GR-MATRICULA' em duas novas colunas: 'Orgão' e 'Matrícula'.

        Parâmetros:
            df (pandas.DataFrame): O DataFrame original que contém a coluna 'GR-MATRICULA'.

        Retorna:
            pandas.DataFrame: O DataFrame com as novas colunas adicionadas.
        """
        df = df.copy()
        df['GR-MATRICULA'] = df['GR-MATRICULA'].astype(str).copy()
        df['Orgão'] = df['GR-MATRICULA'].str.slice(0, 5)
        df['Matrícula'] = df['GR-MATRICULA'].str.slice(5, 12)
        return df

    def converte_datetime(df):
        """
        Função para converter todas as colunas que contêm 'DT_' ou 'DATA' no nome para o formato datetime.

        Parâmetros:
            df (pandas.DataFrame): O DataFrame original que contém as colunas.

        Retorna:
            pandas.DataFrame: O DataFrame com as colunas convertidas.
        """
        df = df.copy()
        date_columns = df.filter(regex='DT_|DATA|IT_DA').columns
        for col in date_columns:
            df[col] = pd.to_datetime(df[col], format='%d/%m/%Y %H:%M:%S', errors='coerce')
            df[col] = df[col].dt.strftime('%d/%m/%Y')
        return df

    def verifica_classe_padrao(df):

        """
        Função para verificar e manipular a coluna 'IT-CO-PADRAO'. Converte os números para numerais romanos e combina
        as colunas 'IT-CO-CLASSE', 'IT-CO-PADRAO' e 'IT-CO-NIVEL' em uma nova coluna 'classe_padrao_nivel'.

        Parâmetros:
            df (pandas.DataFrame): O DataFrame original que contém as colunas a serem verificadas e manipuladas.

        Retorna:
            pandas.DataFrame: O DataFrame com a nova coluna 'classe_padrao_nivel' adicionada.
        """
        # Cria uma cópia do 'df' para que as alterações não modifiquem o 'df' original
        df = df.copy()
        # Função para converter um número para número romano
        def converter_real_romano(numero):
            romanos = {
                '1000': 'M', '900': 'CM', '500': 'D', '400': 'CD',
                '100': 'C', '90': 'XC', '50': 'L', '40': 'XL',
                '10': 'X', '9': 'IX', '5': 'V', '4': 'IV', '1': 'I'
            }
            # Verifica se o valor já é um número romano ou uma string equivalente
            if numero in romanos.values() or numero in romanos.keys():
                return numero
            resultado = ''
            try:
                valor_numerico = int(numero)
                for valor, simbolo in romanos.items():
                    while valor_numerico >= int(valor):
                        resultado += simbolo
                        valor_numerico -= int(valor)
            except ValueError:
                resultado = numero
            return resultado

        # Função para converter um número para número romano
        def converter_romano_real(numero):
            romanos = {
                '1': 'I', '2': 'II', '3': 'III', '4': 'IV', '5': 'V',
                '6': 'VI', '7': 'VII', '8': 'VIII', '9': 'IX', '10': 'X',
                '11': 'XI', '12': 'XII', '13': 'XIII', '14': 'XIV', '15': 'XV',
                '16': 'XVI', '17': 'XVII', '18': 'XVIII', '19': 'XIX', '20': 'XX'
            }
            partes = numero.split('-')
            if len(partes) == 2:
                partes[1] = romanos.get(partes[1], partes[1])
                return '-'.join(partes)
            else:
                return numero

        # Aplicando a conversão para números romanos
        df['IT-CO-PADRAO'] = df['IT-CO-PADRAO'].apply(converter_real_romano)

        # Substituindo NaN por 0
        df = df.fillna(0)
        # Concatenação das colunas com hífen
        df['classe_padrao_nivel'] = df.apply(lambda row: '-'.join(filter(lambda x: x != '0', [str(row['IT-CO-CLASSE']), str(row['IT-CO-PADRAO']), str(row['IT-CO-NIVEL'])])), axis=1)
        # Aplicando a conversão para números romanos
        df['classe_padrao_nivel'] = df['classe_padrao_nivel'].apply(converter_romano_real)

        return df

    def verifica_padrao_atual(df):
        """
        Função para verificar a coluna 'classe_padrao_nivel' e atualizar a coluna 'count_classe_padrao_atual' com 
        valores inteiros correspondentes.

        Parâmetros:
            df (pandas.DataFrame): O DataFrame original que contém as colunas a serem verificadas e atualizadas.

        Retorna:
            pandas.DataFrame: O DataFrame com a coluna 'count_classe_padrao_atual' atualizada.
        """
        # Cria uma cópia do 'df' para que as alterações não modifiquem o 'df' original
        df = df.copy()
        # Dicionário com as informações de mudança
        classe_padrao_roma = { 'A-I'   :1,
                        'A-II'  :2,
                        'A-III' :3,
                        'A-IV'  :4,
                        'A-V'   :5,
                        'A-VI'  :6,
                        'B-I'   :7,
                        'B-II'  :8,
                        'B-III' :9,
                        'B-IV'  :10,
                        'B-V'   :11,
                        'B-VI'  :12,
                        'C-I'   :13,
                        'C-II'  :14,
                        'C-III' :15,
                        'C-IV'  :16,
                        'C-V'   :17,
                        'C-VI'  :18,
                        'S-I'   :19,
                        'S-II'  :20,
                        'S-III' :21,

                    }
        #Substituindo
        for valor_antigo, valor_novo in classe_padrao_roma.items():
            if valor_antigo in df['classe_padrao_nivel'].values:
                df.loc[df['classe_padrao_nivel'] == valor_antigo, 'count_classe_padrao_atual'] = int(valor_novo)
            else:
                df.loc[df['classe_padrao_nivel'] == valor_antigo, 'count_classe_padrao_atual'] = 0
        return df

    def verifica_progressao(df):
        """
        Função para verificar a coluna 'count_classe_padrao_progressao' e atualizar a coluna 'count_classe_padrao_cod' 
        com strings correspondentes.

        Parâmetros:
            df (pandas.DataFrame): O DataFrame original que contém as colunas a serem verificadas e atualizadas.

        Retorna:
            pandas.DataFrame: O DataFrame com a coluna 'count_classe_padrao_cod' atualizada.
        """
        # Cria uma cópia do 'df' para que as alterações não modifiquem o 'df' original
        df = df.copy()
        # Dicionário com as informações de mudança
        roma_classe_padrao = {
                        1:'A-I',
                        2:'A-II',
                        3:'A-III',
                        4:'A-IV',
                        5:'A-V' ,
                        6:'A-VI',
                        7:'B-I' ,
                        8:'B-II',
                        9:'B-III',
                        10:'B-IV' ,
                        11:'B-V'  ,
                        12:'B-VI' ,
                        13:'C-I'  ,
                        14:'C-II' ,
                        15:'C-III',
                        16:'C-IV' ,
                        17:'C-V'  ,
                        18:'C-VI' ,
                        19:'S-I'  ,
                        20:'S-II' ,
                        21:'S-III',
                    }

        #Substituindo
        for valor_antigo, valor_novo in roma_classe_padrao.items():
            if valor_antigo in df['count_classe_padrao_progressao'].values:
                df.loc[df['count_classe_padrao_progressao'] == valor_antigo, 'count_classe_padrao_cod'] = valor_novo
            else:
                df.loc[df['count_classe_padrao_progressao'] == valor_antigo, 'count_classe_padrao_cod'] = 'ATINGIU O NÍVEL MÁXIMO'
        return df

    def verifica_tempo_progressao(df):
        """
        Função para verificar o tempo de progressão com base na coluna 'IT-DA-OCOR-INGR-ORGAO-SERV' e atualizar a 
        coluna 'count_classe_padrao_progressao' com os valores correspondentes.

        Parâmetros:
            df (pandas.DataFrame): O DataFrame original que contém as colunas a serem verificadas e atualizadas.

        Retorna:
            pandas.DataFrame: O DataFrame com a coluna 'count_classe_padrao_progressao' atualizada.
        """
        # Cria uma cópia do 'df' para que as alterações não modifiquem o 'df' original
        df1 = df.copy()
        df = df.copy()
        # Data atual
        data_atual = dt.datetime.now()
        # Converter coluna para valores de data
        df1['IT-DA-OCOR-INGR-ORGAO-SERV'] = pd.to_datetime(df1['IT-DA-OCOR-INGR-ORGAO-SERV'], format='%d/%m/%Y')
        # Extrai o mês por extenso da coluna 'Data'
        df['progride_em'] = df1['IT-DA-OCOR-INGR-ORGAO-SERV'].dt.month.map(lambda x: calendar.month_name[x])
        # Cálculo dos meses decorridos e incremento do contador a cada 12 meses
        df['meses_decorridos'] = ((data_atual - df1['IT-DA-OCOR-INGR-ORGAO-SERV']) / np.timedelta64(1, 'M')).astype(int)
        df['contador_12_meses'] = df['meses_decorridos'] // 12
        df.loc[df['contador_12_meses'] == 0, 'count_classe_padrao_progressao'] = df['count_classe_padrao_atual']
        df.loc[df['contador_12_meses'] != 0, 'count_classe_padrao_progressao'] = df['count_classe_padrao_atual'] + 1
        return df

    def le_e_filtra_excel(self, df):
        """
        Lê um arquivo dataframe, retira os valores duplicados e retorna uma lista dos valores contidos nele.

        Parâmetros:
        - filePath (str): O caminho para o arquivo Excel que deve ser lido. O padrão é None.

        Retorna:
        - list: Uma lista dos valores lidos do arquivo Excel, ou None se ocorrer um erro ou se nenhum arquivo for fornecido.

        Exemplo de Uso:
        >>> le_e_filtra_excel('seu_arquivo.xlsx')
        [1, 'algum texto', 3.5, ...]
        """
        try:
            # Lê o arquivo xlsx se o caminho for fornecido
            if not df.empty:
                valores = df.stack().tolist()  # Converte o DataFrame em uma lista de valores
                valores_unicos = list(set(valores))  # Remove valores duplicados
                return valores_unicos
            else:
                print("Erro: DataFrame vazio.")
                return None
        except Exception as e:
            print(f"Erro ao ler o arquivo .xlsx: {e}")
            return None
        
    def completa_caractere(self, df, coluna, num_caracteres):
        """
        Função para completar os valores em uma coluna específica com zeros à esquerda até que tenham um determinado número de caracteres.

        Parâmetros:
            df (pandas.DataFrame): O DataFrame original.
            coluna (str): O nome da coluna para preencher.
            num_caracteres (int): O número total de caracteres que cada valor deve ter.

        Retorna:
            pandas.DataFrame: O DataFrame com a coluna preenchida.
        """
        df = df.copy()
        df[coluna] = df[coluna].astype(str).str.zfill(num_caracteres)
        return df

    def filtrar_colunas(self, df, colunas_manter=[]):
        """
        Função para filtrar um DataFrame, mantendo apenas as colunas desejadas.

        Parâmetros:
            df (pandas.DataFrame): O DataFrame original.
            colunas_manter (list): Lista de colunas para manter. Se a lista estiver vazia, todas as colunas serão mantidas.

        Retorna:
            pandas.DataFrame: O DataFrame filtrado.
        """
        df = df.copy()
        if not colunas_manter:
            # Se a lista de colunas a manter estiver vazia, retorne o DataFrame original
            return df
        else:
            # Crie um novo DataFrame que contém apenas as colunas desejadas
            df_filtrado = df[colunas_manter]
            return df_filtrado
        
    def filtra_cggaf_centralizado(self, df):
        """
        Filtra um DataFrame para manter apenas as linhas onde a coluna 'Centralização' possui o valor 'Centralizado'.

        Parâmetros:
            df (pandas.DataFrame): O DataFrame a ser filtrado.

        Retorna:
            pandas.DataFrame: O DataFrame filtrado.
        """
        # Cria uma cópia do 'df' para que as alterações não modifiquem o 'df' original
        df = df.copy()

        # Aplica as condições de filtro nas colunas 'Centralização'
        df_filtered = df[df['Centralização'].isin(['Centralizado'])]

        return df_filtered

    def retira_valores_duplicados(self, df, coluna):
        # Cria uma cópia do 'df' para que as alterações não modifiquem o 'df' original
        df = df.copy()

        if coluna in df.columns:
            print("A coluna existe em df.")
        else:
            print("A coluna não existe em df.")

        # Filtra as linhas que têm valores repetidos na coluna 'NU_CPF'
        df = df.drop_duplicates(subset=coluna)

        # Contagem dos valores únicos na coluna 'NU_CPF'
        contagem = df[coluna].value_counts().reset_index()
        contagem.columns = [coluna, 'Contagem']

        # Criação do novo DataFrame com todas as colunas do original e a coluna de contagem
        df = pd.merge(df, contagem, on=coluna, how='left')

        return df

    def combina_dataframes(self, coluna,df1,df2,tipo):
        """
        Função para combinar dois dataframes.

        Parâmetros:
            coluna : A coluna que está presente nos dois DataFrames a serem combinados.
            df1 (pandas.DataFrame): O DataFrame a ser filtrado.
            df2 (pandas.DataFrame): O DataFrame a ser filtrado.
            tipo : Tipo de merge que será aplicado, outer, inner, etc.

        Retorna:
            pandas.DataFrame: O DataFrame filtrado.
        """
        # Cria uma cópia do 'df' para que as alterações não modifiquem o 'df' original
        df1 = df1.copy()
        df2 = df2.copy()

        # Combina df1 e df2 em um novo df tendo como chave a coluna informada na declaraçao da função
        df  = df1.merge(
            df2, on=[coluna],
            how= tipo,
            suffixes=['_df1', '_df2'],
            indicator=True
            )
        # Agora, remova a coluna _merge
        df.drop('_merge', axis=1, inplace=True)

        return df

    def filtra_cggaf_status(self, df):
        # Cria uma cópia do 'df' para que as alterações não modifiquem o 'df' original
        df = df.copy()

        # Corrigir erro de digitação da planilha fINALIZADO -> FINALIZADO
        df.loc[df['Status_da_Demanda_CGGAF'].isin(['fINALIZADO']), 'Status_da_Demanda_CGGAF'] = 'FINALIZADO'

        # Atribuir SOLICITAR à Status_da_Demanda_CGGAF
        df.loc[~df['Status_da_Demanda_CGGAF'].isin(['FINALIZADO', 'EM ATENDIMENTO']), 'Status_da_Demanda_CGGAF'] = 'SOLICITAR'

        return df

    def filtra_data_sessao(self, df):
        # Cria uma cópia do 'df' para que as alterações não modifiquem o 'df' original
        df = df.copy()
        sessa_rpps = df['RPPS - Data da Sessão']
        sessa_rgps = df['RGPS - Data da Sessão']
        # Aplica as condições de filtro nas colunas 'Status_da_Demanda_CGGAF' e 'REGIME RGPS'
        df_filtered = df[
            (
            ((sessa_rpps == 'A partir de 06/05/1999') | (sessa_rpps == 'sem_data_de_sessão')) | 
            ((sessa_rgps == 'A partir de 2021')       | (sessa_rgps == 'sem_data_de_sessão')))]

        return df_filtered

    def filtra_rpps_rgps_cols(self, df):
        # Cria uma cópia do 'df' para que as alterações não modifiquem o 'df' original
        df = df.copy()
        sessa_rpps = df['RPPS - Data da Sessão']
        sessa_rgps = df['RGPS - Data da Sessão']

        value_list = [
                    'A partir de 06/05/1999', 
                    'sem_data_de_sessão', 
                    'A partir de 2021', 
                    ]

        df.loc[sessa_rpps.isna(), 'RPPS - Data da Sessão'] = "sem_periodo_tas"
        df.loc[sessa_rgps.isna(), 'RGPS - Data da Sessão'] = "sem_periodo_tas"

        # Atribuir sem_periodo_tas à RPPS - Data da Sessão e/ou RGPS - Data da Sessão que estão com células em branco
        for value in value_list :
            df.loc[sessa_rpps.isin([value]) | sessa_rgps.isin([value]), 'CONTA_SESSAO'] = 'OK'

        return df

    def divide_dataframe(self, df, num_parts):

        size = len(df) // num_parts
        return [df[i*size:(i+1)*size] for i in range(num_parts)]

    # ------------------------------------------------------
    def gafieira_tratamento_arquivos(self, df_list,colunas_rename=None, colunas_manter=None):
        """
        Processa e filtra uma lista de DataFrames conforme critérios específicos 
        relacionados à "gafieira" para CNV INSS.

        Parâmetros:
        - df_list: Lista de DataFrames para processar.

        Retorna:
        DataFrame único após processamento e concatenação.
        """
        
        if not isinstance(df_list, list):
            raise ValueError("O argumento df_list deve ser uma lista de DataFrames.")
        
        if colunas_rename is None:
            colunas_rename = {}
        if colunas_manter is None:
            colunas_manter = []
        
        df_processado = []
        # lista_colunas = colunas_manter = []


        for df in df_list:
            if not isinstance(df, pd.DataFrame):
                raise TypeError("Cada item em df_list deve ser um DataFrame.")
            
            # df_filtered = df.rename(columns = {'IT-NU-CPF':'NU_CPF','IT-SG-UF-UPAG':'UPAG_INSS'}).copy()
            df_filtered = df.rename(columns = colunas_rename).copy()
            # df_filtered = extradados.filtrar_colunas(df_filtered, ['GR-MATRICULA-ANO-MES', 'NU_CPF', 'IT-CO-ORGAO-ATUAL', 'UPAG_INSS']).copy()

            # df_filtered = filtrar_colunas(df_filtered, ['GR-MATRICULA-ANO-MES', 'NU_CPF', 'IT-CO-ORGAO-ATUAL', 'UPAG_INSS']).copy()

            df_filtered = self.filtrar_colunas(df_filtered, colunas_manter).copy()
            df_filtered['NU_CPF'] = df_filtered['NU_CPF'].astype(str)
            df_filtered = df_filtered.fillna(0)
            df_processado.append(df_filtered)

        df_unique = pd.concat(df_processado)
        # df_unique = extradados.retira_valores_duplicados(df_unique, 'NU_CPF')
        df_unique = self.retira_valores_duplicados(df_unique, 'NU_CPF')
        df_unique = df_unique.drop('Contagem', axis=1)

        return df_unique

    def converte_float_para_int(self, num):
        """
        Converte um número de ponto flutuante para um número inteiro.
        
        Parâmetros:
        - num (float): O número de ponto flutuante que deve ser convertido.
        
        Retorna:
        - int: O número convertido para inteiro.
        
        Exemplo de Uso:
        >>> onverte_float_para_int(2150921.0)
        2150921
        """
        try:
            return int(num)
        except (ValueError, TypeError):
            print("Erro: O valor fornecido não pode ser convertido para inteiro.")
            return None
        
    def converte_float_list_para_int_list(self, float_list):
        """
        Converte uma lista de números de ponto flutuante para uma lista de números inteiros.
        
        Parâmetros:
        - float_list (list): A lista de números de ponto flutuante que deve ser convertida.
        
        Retorna:
        - list: A lista de números convertida para inteiros.
        
        Exemplo de Uso:
        >>> converte_float_list_para_int_list([2150921.0, 12345.0, 6789.0])
        [2150921, 12345, 6789]
        """
        try:
            return [int(x) for x in float_list]
        except (ValueError, TypeError):
            print("Erro: Um ou mais valores na lista não podem ser convertidos para inteiros.")
            return None
    
    def gafieira_tratamento_excel(self, df_list,colunas_rename=None, colunas_manter=None):
        """
        Realiza o tratamento dos dados para o TTCC.

        Parâmetros:
        - df_list (list): Lista contendo os DataFrames a serem processados.
        - extradados (module): Módulo contendo funções auxiliares para tratamento de dados.

        Retorna:
        - DataFrame: DataFrame tratado para o TTCC.
        """
        if colunas_rename is None:
            colunas_rename = {}    
        if colunas_manter is None:
            colunas_manter = []

        # Concatena todos os DataFrames da lista
        df_concat = pd.concat(df_list)

        df_filtered = df_concat.rename(columns = colunas_rename).copy()

        # Filtra as colunas desejadas
        colunas_manter = ['CO_ORGAO', 'MAT_SERV', 'NU_CPF', 'NO_SERVIDOR', 'DT_OCOR_INATIVIDADE_SERV', 
                        'RPPS - Data da Sessão', 'RGPS - Data da Sessão', 'Status_da_Demanda_CGGAF']

        # df_ttcc_cols = extradados.filtrar_colunas(df_ttcc_concat, colunas_manter=colunas_manter).copy()
        df_filtered = self.filtrar_colunas(df_filtered, colunas_manter).copy()

        # Converte a coluna NU_CPF para string
        df_filtered['NU_CPF'] = df_filtered['NU_CPF'].astype(str)

        return df_filtered

    def gafieira_resultado(self, df):
        """
        Processa e ajusta um DataFrame para a "gafieira".

        Parâmetros:
        - df: DataFrame para processar.

        Retorna:
        DataFrame processado conforme critérios específicos de "gafieira".
        """
        
        # Certifique-se de que a entrada é um DataFrame
        if not isinstance(df, pd.DataFrame):
            raise TypeError("O argumento df deve ser um pandas DataFrame.")

        # Cópia do DataFrame para evitar modificações no original
        df = df.copy()

        # Processamento sequencial
        df_centralizados        = self.filtra_cggaf_centralizado(df)
        df_filtro_status        = self.filtra_df('Status_da_Demanda_CGGAF', 'SOLICITAR', df_centralizados)
        df_sessao               = self.filtra_rpps_rgps_cols(df_filtro_status)
        df_convert_datetime     = self.converte_datetime(df_sessao)
        df_filtro_conta_sessao  = self.filtra_df('CONTA_SESSAO','OK', df_convert_datetime)
        df_cpf_caracter         = self.completa_caractere(df_filtro_conta_sessao, 'NU_CPF', 11)
        df_mat_caracter         = self.completa_caractere(df_cpf_caracter, 'MAT_SERV', 7)
        df_result               = df_cpf_caracter

        return df_result

if __name__ == '__main__':
    print(openpyxl.__version__)

