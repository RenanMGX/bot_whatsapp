import os
import subprocess
import sys
import getpass
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchWindowException
from time import sleep
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
from PyQt6.QtCore import QDateTime, Qt, QTimer
from PyQt6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget, QTableWidgetItem, QMainWindow)
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import Qt
import atexit
import math
import urllib

class Interface(QDialog,QMainWindow):
    def __init__(self, parent=None):
        super(Interface, self).__init__(parent)

 
        disableWidgetsCheckBox = QCheckBox("&Disable widgets")
        
        self.setWindowTitle("Bot Whatsapp Relacionamento com o Cliente")
        
        self.createTopRightGroupBox()

        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        self.setLayout(mainLayout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("")

        bt_with = 300
        bt_height = 50
        
        #botão iniciar
        self.__bt_iniciar = QPushButton("Iniciar")
        self.__bt_iniciar.setDefault(True)
        self.__bt_iniciar.clicked.connect(self.iniciar)
        self.__bt_iniciar.setFixedSize(bt_with,bt_height)

        #botão carregar
        self.__bt_carregar = QPushButton("Carregar Planilha")
        self.__bt_carregar.setDefault(True)
        self.__bt_carregar.clicked.connect(self.carregar)
        self.__bt_carregar.setFixedSize(bt_with,bt_height)
        self.__bt_carregar.setVisible(False)

        #botão iniciar o bot
        self.__bt_iniciar_bot = QPushButton("Começar Envio")
        self.__bt_iniciar_bot.setDefault(True)
        self.__bt_iniciar_bot.clicked.connect(self.enviar)
        self.__bt_iniciar_bot.setFixedSize(bt_with,bt_height)
        self.__bt_iniciar_bot.setVisible(False)

        #tabela do status
        self.__tabela = QTextEdit()
        self.__tabela.setReadOnly(True)
        self.__tabela.setVisible(False)

        

        #self.setGeometry(300,300,600,150)
        #self.setMaximumHeight(100)
        #self.setMaximumWidth(300)

        self.__title_infor_text = QLabel()
        font = QFont("Arial", 12, QFont.Weight.Bold)
        self.__title_infor_text.setFont(font)
        self.__title_infor_text.setVisible(False)
        
        self.__infor_text = QLabel()
        self.__infor_text.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.__bt_iniciar)
        layout.addWidget(self.__bt_carregar)
        layout.addWidget(self.__bt_iniciar_bot)
        layout.addWidget(self.__tabela)
        layout.addWidget(self.__title_infor_text)
        layout.addWidget(self.__infor_text)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)

        self.__contador_exec = False

    ##### metodos para teste
    def test(self):
        #print(self.__dados[0])
        #self.__dados[0][0] = "ENVIADO!!!"
        #print(self.__dados[0])
        #self.exibir_status(self.__dados)
        self.enviar()
        

    ############################################

    def iniciar(self):
        self.__bt_iniciar.setVisible(False)
        self.__bt_carregar.setVisible(True)
        self.__navegador = self.iniciar_whats()
        
    def carregar(self):
        if self.is_browser_open() == False:
            self.infor(reset=True)
            self.infor("O navegador foi fechado tente novamente", title="Error:")
            self.__bt_carregar.setVisible(False)
            self.__bt_iniciar.setVisible(True)
            return

        caminho = self.procurar_arquivo()
        if caminho != "":
            if self.is_excel_file(caminho):
                self.infor(reset=True)
                self.__bt_carregar.setVisible(False)
                self.__dados = self.excel_load(caminho)
                self.exibir_status(self.__dados)
                self.__bt_iniciar_bot.setVisible(True)
            else:
                self.infor("selecione apenas arquivos do excel",title="Erro")
        else:
            self.infor("nenhum arquivo selecionado tente novamente",title="Erro")
 
    def exibir_status(self,data,reset=False):
        if reset == True:
            self.__tabela.setVisible(False)
            return
        self.setGeometry(300,300,400,300)
        self.__tabela.setVisible(True)
        datas = ""
        for x in data:
            datas += f"{x[0:3]}\n"
        self.__tabela.setPlainText(str(datas))


    def excel_load(self,planilha):
        colunas = "A,B,C,D,F"
        quantidade_colunas = len(colunas.replace(",",""))
        df = pd.read_excel(planilha, sheet_name='WhatsApp', usecols=colunas, skiprows=7).values.tolist()
        for x in df:
            x.insert(0,"PRONTO PARA ENVIAR!!!")
        return df
    
    def enviar(self):
        if self.is_browser_open() == False:
            self.infor(reset=True)
            self.infor("O navegador foi fechado tente novamente", title="Error:")
            self.__bt_iniciar_bot.setVisible(False)
            self.__bt_iniciar.setVisible(True)
            return
        if self.__contador_exec == False:
            self.__contador_exec = True
            print("foi")
        else:
            self.__contador_exec = False
            return 
        self.infor(reset=True)
        try:
            self.__navegador.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[1]/div/div/div[2]/div')
            self.infor(reset=True)
            self.infor("conecte-se ao whatsapp web antes de prosseguir", title="Error")
            self.__contador_exec = False
            return
        except:
            pass

        try:
            self.__navegador.find_element(By.XPATH, '//*[@id="side"]/div[1]/div/div/div[2]/div/div[1]/p')
        except:
            self.infor("espere o site carregar", title="Espere!")
            self.__contador_exec = False
            return 
        
        self.__bt_iniciar_bot.setVisible(False)
        self.infor(reset=True)

        self.tratar_dados()
        vesualiza_final = []
        for dados in self.__dados_prontos:
            if dados["Numero"] == None:
                dados["Status"] == "Error: numero não encontrado"
                continue
            if (dados["Mensagem"] == None) or (dados["Mensagem"] == "nan"):
                dados["Status"] = "Error: mensagem não encontrada!"
                continue
            if (dados["Nome"] == None) or (dados["Nome"] == "nan"):
                dados["Nome"] = "SEM NOME"
            dados["Mensagem"] = dados["Mensagem"].encode('utf-8')
            dados["Mensagem"] = urllib.parse.quote(dados["Mensagem"])
            link = f'https://web.whatsapp.com/send?phone=55{dados["Numero"]}&text={dados["Mensagem"]}'
            self.__navegador.get(link)
            contator_finalizar = 0
            achou_numero = False
            while True:
                try:
                    enviar = self.__navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')
                    achou_numero = True
                    break
                except:
                    pass
                
                try:
                    enviar = self.__navegador.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button/div/div')
                    break
                except:
                    pass
                if contator_finalizar >= 5*60:
                    enviar = False
                else:
                    contator_finalizar +=1
                    sleep(1)
            if enviar == False:
                dados["Status"] == "Error: não conseguiu clicar"
                continue
            else:
                if achou_numero:
                    enviar.click()
                    dados["Status"] = "Enviado: mensagem"
                else:
                    enviar.click()
                    dados["Status"] = "Error: não achou numero"
                    continue
            
            if (dados["Arquivo"] != None) and (os.path.isfile(dados["Arquivo"])):
                sleep(1)
                # etapa 1
                contator_finalizar = 0
                while True:
                    try:
                        arquivo = self.__navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[1]/div[2]/div/div/div/span')
                        break
                    except:
                        if contator_finalizar <= 5*60:
                            contator_finalizar += 1
                            sleep(1)
                        else:
                            arquivo = False
                            break
                if arquivo == False:
                    continue
                else:
                    arquivo.click()

                #etapa 2
                contator_finalizar = 0
                while True:
                    try:
                        attach = self.__navegador.find_element(By.CSS_SELECTOR, "input[type='file']")
                        break
                    except:
                        if contator_finalizar <= 5*60:
                            contator_finalizar += 1
                            sleep(1)
                        else:
                            arquivo = False
                            break
                if arquivo == False:
                    continue
                else:
                    attach.send_keys(dados["Arquivo"])

                #etapa 3
                contator_finalizar = 0
                while True:
                    try:
                        send = self.__navegador.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span')
                        break
                    except:
                        if contator_finalizar <= 5*60:
                            contator_finalizar += 1
                            sleep(1)
                        else:
                            arquivo = False
                            break
                if arquivo == False:
                    continue
                else:
                    send.click()

                #etapa 4
                confirmou = False
                while True:
                    if confirmou == True:
                        break
                    else:
                        try:
                            self.__navegador.find_element(By.XPATH, '//span[@data-testid="msg-time"]')
                        except:
                            confirmou = True
            print("##")
            print(dados["Mensagem2"] != None)
            print("##")
            if dados["Mensagem2"] != None:
                controle_mensagem2 = True
                while controle_mensagem2:
                    try:
                        texto = self.__navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p')
                        texto.send_keys(dados["Mensagem2"])
                        enviar = self.__navegador.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span')
                        enviar.click()
                        controle_mensagem2 = False
                    except Exception as error:
                        print(error)
                        sleep(1)


                
                #etapa final
                dados["Status"] = "Enviado: mensagem e anexo"



            sleep(1)
        sleep(1)
        for x in self.__dados_prontos:
            vesualiza_final.append(list(x.values()))
        self.exibir_status(vesualiza_final)
        self.__bt_iniciar_bot.setVisible(True)
        print("finalizado")
        sleep(2)
        self.__contador_exec = False
        
    def tratar_dados(self):
        self.__dados_prontos = []
        for dados_brutos in self.__dados:
            dados_temp = {}
            dados_temp["Status"] = dados_brutos[0]
            dados_temp["Nome"] = dados_brutos[1]
            dados_temp["Numero"] = dados_brutos[2]
            dados_temp["Arquivo"] = dados_brutos[3]
            dados_temp["Mensagem"] = dados_brutos[4]
            dados_temp["Mensagem2"] = dados_brutos[5]
            #Tratar Nome
            try:
                if math.isnan(dados_temp["Nome"]):
                    dados_temp["Nome"] = None                    
                else:
                    dados_temp["Nome"] = str(dados_temp["Nome"])
            except:
                dados_temp["Nome"] = str(dados_temp["Nome"])
    
            #Tratar numero
            
            try:
                if math.isnan(dados_temp["Numero"]):
                    dados_temp["Numero"] = None                    
                else:
                    dados_temp["Numero"] = str(int(dados_temp["Numero"]))
                    dados_temp["Numero"] = dados_temp["Numero"].replace("(", "").replace(")", "").replace(" ", "")
                    dados_temp["Numero"] = int(dados_temp["Numero"])
                    
            except:
                dados_temp["Numero"] = 9999999999999999

            #Tratar Arquivo
            try:
                if math.isnan(dados_temp["Arquivo"]):
                    dados_temp["Arquivo"] = None
                else:
                    dados_temp["Arquivo"] = str(dados_temp["Arquivo"])
            except:
                dados_temp["Arquivo"] = str(dados_temp["Arquivo"])

            #Tratar Mensagem
            try:
                if math.isnan(dados_temp["Mensagem"]):
                    dados_temp["Mensagem"] = None
                else:
                    dados_temp["Mensagem"] = str(dados_temp["Mensagem"])
            except:
                dados_temp["Mensagem"] = str(dados_temp["Mensagem"])
            try:
                if math.isnan(dados_temp["Mensagem2"]):
                    dados_temp["Mensagem2"] = None
                else:
                    dados_temp["Mensagem2"] = str(dados_temp["Mensagem2"])
            except:
                dados_temp["Mensagem2"] = str(dados_temp["Mensagem2"])

            self.__dados_prontos.append(dados_temp)




    def infor(self, mensagem="", title="", reset=False):
        if reset == False:
            self.__infor_text.setVisible(True)
            self.__title_infor_text.setVisible(True)
            self.__title_infor_text.setText(title)
            self.__infor_text.setText(mensagem)
        else:
            self.__infor_text.setVisible(False)
            self.__title_infor_text.setVisible(False)
            self.__title_infor_text.setText("")
            self.__infor_text.setText("")


        ######## metodos apenas do bot do whats
    def iniciar_whats(self):
        username = getpass.getuser()
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir=C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome")
        navegador = webdriver.Chrome(options=options)
        link = f"https://web.whatsapp.com/"
        navegador.get(link)
        atexit.register(navegador.quit)
        return navegador
    
    def procurar_arquivo(self):
        root = tk.Tk()
        root.withdraw()
        caminho = filedialog.askopenfilename()
        return caminho

    def is_browser_open(self):
        try:
            self.__navegador.current_url
            return True
        except (NoSuchWindowException, NameError):
            return False
    def is_excel_file(self,file_path):
        return os.path.isfile(file_path) and file_path.lower().endswith(('.xls', '.xlsx', '.xlsm', '.xlsb'))








if __name__ == "__main__":
    app = QApplication(sys.argv)
    gallery = Interface()
    gallery.show()
    gallery.showNormal()
    sys.exit(app.exec())
