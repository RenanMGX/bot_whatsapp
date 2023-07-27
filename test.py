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

class Interface(QDialog,QMainWindow):
    def __init__(self, parent=None):
        super(Interface, self).__init__(parent)

 
        disableWidgetsCheckBox = QCheckBox("&Disable widgets")
        
        self.setWindowTitle("Bot Whatsapp")
        
        self.createTopRightGroupBox()

        disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        self.setLayout(mainLayout)

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("")

        bt_with = 150
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
        self.__bt_iniciar_bot.clicked.connect(self.test)
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

    ##### metodos para teste
    def test(self):
        print(self.__dados[0])
        self.__dados[0][0] = "ENVIADO!!!"
        print(self.__dados[0])
        self.exibir_status(self.__dados)
        

    ############################################

    def iniciar(self):
        self.__bt_iniciar.setVisible(False)
        self.__bt_carregar.setVisible(True)
        self.__navegador = self.iniciar_whats()
        
    def carregar(self):
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
        colunas = "A,B,C,D"
        quantidade_colunas = len(colunas.replace(",",""))
        df = pd.read_excel(planilha, sheet_name='WhatsApp', usecols=colunas, skiprows=7).values.tolist()
        for x in df:
            x.insert(0,"PRONTO PARA ENVIAR!!!")
        return df
        
        
 
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
