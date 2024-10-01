from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver.remote.webelement import WebElement
import exceptions as ModelExecptions
from time import sleep
from getpass import getuser
import os

class Nav(Chrome):
    def __init__(self) -> None:
        options = Options()
        options.add_argument(f"--user-data-dir=C:\\Users\\{getuser()}\\AppData\\Local\\Google\\Chrome")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super().__init__(options=options)
        
    def find_element(self, by=By.ID, value: str | None = None) -> WebElement:
        try:
            while super().find_element(By.ID, 'app').text == 'WhatsApp\n Protegida com a criptografia de ponta a ponta':
                sleep(1)
        except:
            pass
        element = super().find_element(by, value)
        
        return  element


class Navegador():
    @property
    def url(self) -> str:
        url_temp:str = self.__url
        if not url_temp.endswith('/'):
            url_temp += '/'
        return url_temp
    
    @property
    def nav(self) -> Nav:
        try:
            return self.__nav
        except Exception as err:
            print("Navegador não foi iniciado")
            raise err
                
    def iniciar_navegador(self, url):
        for _ in range(60):
            try:
                self.__nav = Nav()
                self.__nav.get(url)
                sleep(5)
                self.__url:str = url
                return self
            except:
                try:
                    del self.__nav
                except:
                    pass
                sleep(1)
        raise Exception("não foi possivel iniciar o Navegador")
    
    def verificar_tela_inicio(self, *, esperar_conectar:bool=True) -> bool:
        while True:
            try:
                self.nav.find_element(By.ID, 'link-device-phone-number-code-screen-instructions')
                print("ainda não fez login")
                sleep(1)
            except exceptions.NoSuchElementException:
                if not esperar_conectar:
                    return False
                try:
                    self.nav.find_element(By.ID, 'side')
                    sleep(1)
                    if len(janelas:=self.nav.window_handles):
                        for janela in janelas:
                            if janela == janelas[0]:
                                continue
                            self.nav.switch_to.window(janela)
                            self.nav.close()
                            self.nav.switch_to.window(janelas[0])
                    print("Está conectado!")
                    return True
                except exceptions.NoSuchElementException:
                    print("conectando")
                sleep(1)
    
    
    def enviar_mensagem(self, *, numero:str, mensagem:str, arquivo:str=""):
        for _ in range(3):
            url = f'{self.url}send?phone={numero}'
            print(url)
            self.nav.get(url)
            
            self.__verificar_numero()
            
            if arquivo:
                self.__anexar_arquivo(arquivo)
            
            xpath_area_texto = '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p'
            while len(self.nav.find_element(By.XPATH, xpath_area_texto).text) > 0:
                self.nav.find_element(By.XPATH, xpath_area_texto).send_keys(Keys.BACKSPACE)
            self.nav.find_element(By.XPATH, xpath_area_texto).send_keys(mensagem)
            

            
            xpath_enviar:str = '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[2]/button/span'
            if self.nav.find_element(By.XPATH, xpath_enviar).get_attribute('data-icon') == 'send':
                self.nav.find_element(By.XPATH, xpath_enviar).click()
                return True
    
    def __anexar_arquivo(self, arquivo:str) -> None:
        if not os.path.exists(arquivo):
            return
        if not os.path.isfile(arquivo):
            return
        
        self.nav.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[1]/div[2]/div/div/div/span').click() #mais
        
        if (arquivo.endswith('.jpg')) or (arquivo.endswith('.gif')) or (arquivo.endswith('.png')) or (arquivo.endswith('.svg')) or (arquivo.endswith('.psd')):
            self.nav.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[1]/div[2]/div/span/div/ul/div/div[2]/li/div/input').send_keys(arquivo)
        else:
            self.nav.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[1]/div[2]/div/span/div/ul/div/div[1]/li/div/input').send_keys(arquivo)
        
        self.nav.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]/div/div/span').click()


    def __verificar_numero(self):
        try:
            self.nav.find_element(By.ID , 'side')
            try:
                err = self.nav.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[1]')
                self.nav.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button/div/div').click()
                raise ModelExecptions.NumeroInvalido(err.text)
            except ModelExecptions.NumeroInvalido as err:
                raise err
            except Exception:
                pass
        except exceptions.NoSuchElementException:
            print("telefone não encontrado")
            self.nav.get(self.url)
            raise ModelExecptions.NumeroInvalido("telefone não encontrado")
        except Exception as err:
            raise err
        
        print("numero liberado sem problemas")
        
if __name__ == "__main__":
    pass    
    