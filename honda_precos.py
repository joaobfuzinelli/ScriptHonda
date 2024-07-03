from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from openpyxl import Workbook

def obter_preco_veiculo(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless") #sem interface gráfica (Caso queira que mude é só falar)

    # Caminho do executável do ChromeWebDriver
    chromedriver_path = r"C:\Users\joaob\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"
    service = Service(executable_path=chromedriver_path)

    # Configurar o webdriver do Chrome
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(url)
        
        # Aguardar o carregamento completo da página
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'andes-money-amount__fraction'))) #Essa Classe que está sendo mencionanda faz referência ao campo de preço do Mercado Livre
    
        # Extrair nome, fabricante e preço do veículo
        nome_element = driver.find_element(By.XPATH, '//h1[@class="ui-pdp-title"]') #Título do anúncio
        fabricante_element = driver.find_element(By.XPATH, '//span[@class="ui-pdp-subtitle"]') #Condição do anúncio (Novo, usado etc)
        preco_element = driver.find_element(By.CLASS_NAME, 'andes-money-amount__fraction') #Preço do veículo
        
        nome = nome_element.text.strip()
        fabricante = fabricante_element.text.strip()
        preco = preco_element.text.strip()
        
        return nome, fabricante, preco
    
    except Exception as e:
        print(f'Ocorreu um erro durante a execução: {e}')
        return None, None, None
    
    finally:
        driver.quit()  # Fechar o navegador ao finalizar

def gerar_planilha_excel(dados_veiculo):
    # Criar um novo Workbook (arquivo Excel)
    wb = Workbook()
    ws = wb.active
    ws.title = "Veículos"
    
    # Definir cabeçalhos
    ws.append(["Nome do Veículo", "Fabricante", "Preço"])
    
    # Adicionar dados do veículo
    ws.append(dados_veiculo)
    
    # Salvar o arquivo Excel
    wb.save("dados_veiculo.xlsx")
    print("Arquivo Excel gerado com sucesso!")

if __name__ == '__main__':
    url = 'https://carro.mercadolivre.com.br/MLB-3757344557-volkswagen-gol-16-mi-8v-flex-4p-manual-_JM#position=1&search_layout=grid&type=item&tracking_id=23f32f31-c37e-49b5-9f08-f86bb86fe6da'
    print(f'Obtendo dados do veículo de {url}')
    nome, fabricante, preco = obter_preco_veiculo(url)
    
    if nome and fabricante and preco:
        dados_veiculo = [nome, fabricante, preco]
        gerar_planilha_excel(dados_veiculo)
    else:
        print(f'Não foi possível obter os dados do veículo de {url}')

#Docstrings abaixo

"""
Por enquanto decidi deixar apenas um veículo apenas para fazer o teste do script, mas em breve será adicionado mais carros porém de uma forma mais dinâmica. Vale lembrar que o código pode não funcionar em todos os computadores, pois é necessário inserir no código o caminho do Webdriver do Google, mas isso será mudado.
"""