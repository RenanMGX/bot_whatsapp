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
from typing import Literal
try:
    from .utils import *
except:
    from utils import enviar_arquivo_abrir

class Nav(Chrome):
    def __delete__(self):
        try:
            self.close()
        except:
            pass
    
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
        #import pdb;pdb.set_trace() # <-------------------------------- Debug
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
            
            sleep(1)
            #import pdb;pdb.set_trace() # <-------------------------------- Debug
            
            xpath_area_texto = self._procurar_element_per_attribute(By.TAG_NAME, 'div', attribute="aria-placeholder", value_attribute="Digite uma mensagem", _element=self.nav.find_element(By.ID, 'main'))
                                                               #'selectable-text copyable-text x15bjb6t x1n2onr6'
            if len(xpath_area_texto.text) > 0:
                xpath_area_texto.send_keys(Keys.RETURN)
            
            
            for msg in _mensagem:
                #while self.nav.find_element(By.XPATH, xpath_enviar).get_attribute('data-icon') != 'send':
                try:
                    xpath_area_texto.send_keys(msg)
                    xpath_area_texto.send_keys(Keys.ALT + Keys.ENTER)
                except:
                    pass
                sleep(.5)
                
                    
            #import pdb;pdb.set_trace() # <-------------------------------- Debug
                                                           
            #xpath_enviar = self.nav.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div[2]/button/span', verificar_tela_login=False)
            #import pdb;pdb.set_trace() # <-------------------------------- Debug
            sleep(1)

            try:
                self._procurar_element_per_attribute(By.TAG_NAME, 'button', attribute="aria-label", value_attribute="Enviar", _element=self.nav.find_element(By.ID, 'main')).click()
            except:
                try:
                    self._procurar_element_per_attribute(By.TAG_NAME, 'div', attribute="aria-label", value_attribute="Enviar", _element=self.nav.find_element(By.ID, 'main')).click()
                except:
                    self._procurar_element_per_attribute(By.TAG_NAME, 'span', attribute="aria-label", value_attribute="Enviar", _element=self.nav.find_element(By.ID, 'main')).click()
            sleep(1)
            
                                                                                                                                                          
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
        
        
        #import pdb;pdb.set_trace() # <-------------------------------- Debug
        #self.nav.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[1]/div/button/span').click() #mais 
                                        #''
        #self.nav.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span/div/div[2]/div/div[1]/button/span').click() #mais            
        try:
            self._procurar_element_per_attribute(By.TAG_NAME, 'button', attribute="aria-label", value_attribute="Anexar", _element=self.nav.find_element(By.ID, 'main')).click()
        except:
            self._procurar_element_per_attribute(By.TAG_NAME, 'div', attribute="aria-label", value_attribute="Anexar", _element=self.nav.find_element(By.ID, 'main')).click()
        sleep(1)
        


        
        if arquivo.endswith(('.jpg', '.gif', '.png', '.svg', '.psd')):
            try:
                self._procurar_element_per_text(by=By.TAG_NAME, value='span', text='Fotos e vídeos', _type='equal').click()
                enviar_arquivo_abrir(arquivo)
            except:
                self._procurar_element_per_attribute(By.TAG_NAME, 'input', attribute="accept", value_attribute="image/*,video/mp4,video/3gpp,video/quicktime").send_keys(arquivo)
            
        elif arquivo.endswith(('.mp3', '.wav', '.ogg', '.aac', '.mpeg', '.flac')):
            try:
                self._procurar_element_per_text(by=By.TAG_NAME, value='span', text='Áudio', _type='equal').click()
                enviar_arquivo_abrir(arquivo)
            except:
                self._procurar_element_per_attribute(By.TAG_NAME, 'input', attribute="accept", value_attribute="audio/wav,audio/mp3,audio/ogg,audio/aac,audio/mpeg").send_keys(arquivo)
            
        else:
            try:                      
                self._procurar_element_per_text(by=By.TAG_NAME, value='span', text='Documento', _type='equal').click()
                enviar_arquivo_abrir(arquivo)
            except:
                self._procurar_element_per_attribute(By.TAG_NAME, 'input', attribute="accept", value_attribute="*").send_keys(arquivo)
        
        sleep(1)
        try:
            self._procurar_element_per_attribute(By.TAG_NAME, 'div', attribute="aria-label", value_attribute="Enviar").click()
            sleep(1)
            return True
        except:
            pass        

        print("não foi possivel anexar o arquivo")
        return False
        
    def _procurar_element_per_attribute(self, by:str, value:str, *, attribute:str, value_attribute:str, _element:WebElement|None=None, _type:Literal['equal', 'in']='equal'):
        if _element is None:
            element = self.nav
        else:
            element = _element
        
        for target in element.find_elements(by, value):
            if _type == 'equal':
                if value_attribute == str(target.get_attribute(attribute)):
                    return target
            elif _type == 'in':
                if value_attribute in str(target.get_attribute(attribute)):
                    return target
            
            
            
            if target.get_attribute(attribute) == value_attribute:
                return target
        raise Exception(f"Elemento não encontrado {by}={value} com {attribute}={value_attribute}")
    
    def _procurar_element_per_text(self, by:str, value:str, *, text:str, _element:WebElement|None=None, _type:Literal['equal', 'in']='equal'):
        if _element is None:
            element = self.nav
        else:
            element = _element
        
        for target in element.find_elements(by, value):
            if _type == 'equal':
                if text == target.text:
                    return target
            elif _type == 'in':
                if text in target.text:
                    return target    
            
        raise Exception(f"Elemento não encontrado {by}={value} com {text=}")
    

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
    #input()
    bot.verificar_tela_inicio()
    
    bot.enviar_mensagem(numero='31994773182', mensagem=datetime.now().strftime("Teste do Renan -> %d/%m/%Y %H:%M:%S.%f"), arquivo=r"C:\Users\renan.oliveira\OneDrive - PATRIMAR ENGENHARIA S A\Documentos\Screenshot_1.png")
    bot.enviar_mensagem(numero='31994773182', mensagem=datetime.now().strftime("Teste do Renan -> %d/%m/%Y %H:%M:%S.%f"), arquivo='C:\\Users\\renan.oliveira\\Downloads\\log da IA\\Campanha (online-audio-converter.com).mp3')
    bot.enviar_mensagem(numero='31994773182', mensagem=datetime.now().strftime("Teste do Renan -> %d/%m/%Y %H:%M:%S.%f"), arquivo='C:\\Users\\renan.oliveira\\Downloads\\log da IA\\campanhanovolar.png')

    print("Concluido")
    # import pdb;pdb.set_trace()
    #bot.enviar_mensagem(numero='9999999999999', mensagem="renan\nteste1\n", arquivo=r"C:\Users\renan.oliveira\Downloads\y\Designer.png")
    #bot.enviar_mensagem(numero='9999999999999', mensagem="renan\nteste1\n", arquivo=r"C:\Users\renan.oliveira\Downloads\y\Designer.png")
    