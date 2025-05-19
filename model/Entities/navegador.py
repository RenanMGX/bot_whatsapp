from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium.webdriver.remote.webelement import WebElement
try:
    from . import exceptions as ModelExecptions
except:
    pass
from time import sleep
from getpass import getuser
import os

class Nav(Chrome):
    def __init__(self) -> None:
        options = Options()
        options.add_argument(f"--user-data-dir=C:\\Users\\{getuser()}\\AppData\\Local\\Google\\Chrome")
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        super().__init__(options=options)
        
    def find_element(self, by=By.ID, value: str | None = None, verificar_tela_login:bool=True) -> WebElement:
        if verificar_tela_login:
            try:
                while super().find_element(By.ID, 'app').text == 'WhatsApp\n Protegida com a criptografia de ponta a ponta':
                    sleep(.1)
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
                sleep(.1)
            except exceptions.NoSuchElementException:
                if not esperar_conectar:
                    return True
                try:
                    self.nav.find_element(By.ID, 'side')
                    sleep(.1)
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
                sleep(.1)
    
    
    def enviar_mensagem(self, *, numero:str, mensagem:str, arquivo:str=""):
        try:
            url = f'{self.url}send?phone={numero}'
            #print(url)
            self.nav.get(url)
            
            # try:
            #     self.__verificar_numero()
            # except Exception as err:
            #     print(type(err), err)
            #     continue
            
            #sleep(2)
            while self.nav.find_element(By.ID, 'app').text.startswith('Iniciando conversa'):
                print('Iniciando conversa')
                sleep(.1)
            
            _mensagem = mensagem.split('\n')
            #import pdb;pdb.set_trace() # <-------------------------------- Debug
                        
            xpath_area_texto = self.nav.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[1]/div/div[1]/p', verificar_tela_login=False)
            if len(xpath_area_texto.text) > 0:
                xpath_area_texto.send_keys(Keys.RETURN)
            
            for msg in _mensagem:
                #while self.nav.find_element(By.XPATH, xpath_enviar).get_attribute('data-icon') != 'send':
                xpath_area_texto.send_keys(msg)
                xpath_area_texto.send_keys(Keys.ALT + Keys.ENTER)
                
                    
            xpath_enviar = self.nav.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[2]/button/span', verificar_tela_login=False)
            if xpath_enviar.get_attribute('data-icon') == 'send':
                xpath_enviar.click()
                #sleep(.5)
            
            if arquivo:
                try:
                    if self.__anexar_arquivo(arquivo):
                        print("Anexou")
                except Exception as err:
                    print(type(err), str(err))
            
            sleep(1)
            
            return True
        except Exception as err:
            raise err
    
    def __anexar_arquivo(self, arquivo:str) -> bool:
        print("anexando arquivo")
        if not os.path.exists(arquivo):
            print("arquivo não existe")
            return False
        if not os.path.isfile(arquivo):
            print("não é um arquivo")
            return False
        
        self.nav.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[1]/div/button/span').click() #mais 
        #import pdb;pdb.set_trace() # <-------------------------------- Debug

        for num in range(1,15):
            try:
                if (arquivo.endswith('.jpg')) or (arquivo.endswith('.gif')) or (arquivo.endswith('.png')) or (arquivo.endswith('.svg')) or (arquivo.endswith('.psd')):
                    self.nav.find_element(By.XPATH, f'//*[@id="app"]/div/span[{num}]/div/ul/div/div/div[2]/li/div/input').send_keys(arquivo)
                
                else:                               
                    self.nav.find_element(By.XPATH, f'//*[@id="app"]/div/span[{num}]/div/ul/div/div/div[1]/li/div/input').send_keys(arquivo)
                break
            except:
                pass
                #sleep(1)
            if num >= 14:
                print("não foi possivel anexar o arquivo")
                return False
        
        for _ in range(25): 
            try:
                self.nav.find_element(By.XPATH, f'//*[@id="app"]/div/div[3]/div/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]/div/div').click()
                sleep(5)
                return True
            except:
                pass
            sleep(.25)
            
        # for num in range(15):
        #     try:                                 
        #         self.nav.find_element(By.XPATH, f'//*[@id="app"]/div/div[{num}]/div/div[2]/div[2]/span/div/div/div/div[2]/div/div[2]/div[2]/div/div').click()
        #         return
        #     except:
        #         pass
        #     if num >= 14:
        #         raise Exception("Erro ao anexar arquivo")
        print("não foi possivel anexar o arquivo")
        return False
        

    def __verificar_numero(self):
        sleep(2)
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
    from datetime import datetime
    bot = Navegador()  
    bot.iniciar_navegador(f"https://web.whatsapp.com/")  
    
    bot.enviar_mensagem(numero='31994773182', mensagem=datetime.now().strftime("Teste do Renan -> %d/%m/%Y %H:%M:%S.%f"), arquivo=r"C:\Users\renan.oliveira\OneDrive - PATRIMAR ENGENHARIA S A\Documentos\Screenshot_1.png")
    bot.enviar_mensagem(numero='31994773182', mensagem=datetime.now().strftime("Teste do Renan -> %d/%m/%Y %H:%M:%S.%f"), arquivo=r"C:\Users\renan.oliveira\OneDrive - PATRIMAR ENGENHARIA S A\Documentos\planilha oliveira trust final.xlsx")
    bot.enviar_mensagem(numero='31994773182', mensagem=datetime.now().strftime("Teste do Renan -> %d/%m/%Y %H:%M:%S.%f"), arquivo=r"C:\Users\renan.oliveira\OneDrive - PATRIMAR ENGENHARIA S A\Documentos\planilha oliveira trust final.xlsx")

    #import pdb;pdb.set_trace()
    #bot.enviar_mensagem(numero='9999999999999', mensagem="renan\nteste1\n", arquivo=r"C:\Users\renan.oliveira\Downloads\y\Designer.png")
    #bot.enviar_mensagem(numero='9999999999999', mensagem="renan\nteste1\n", arquivo=r"C:\Users\renan.oliveira\Downloads\y\Designer.png")
    