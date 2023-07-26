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
from PyQt6.QtWidgets import (QApplication, QCheckBox, QDialog, QPushButton, 
QStyleFactory, QVBoxLayout, QMainWindow, QLabel, QGroupBox, QGridLayout)
from PyQt6.QtGui import QFont, QFontDatabase
from PyQt6.QtCore import Qt

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

    def test(self):
        print("funciou")

        

    def createTopRightGroupBox(self):
        self.topRightGroupBox = QGroupBox("")

        self.__bt_iniciar = QPushButton("Iniciar")
        self.__bt_iniciar.setDefault(True)
        self.__bt_iniciar.clicked.connect(self.iniciar)
        self.__bt_iniciar.setFixedSize(150,50)
        

        self.setGeometry(300,300,600,150)

        self.__title_infor_text = QLabel()
        font = QFont("Arial", 12, QFont.Weight.Bold)
        self.__title_infor_text.setFont(font)
        
        self.__infor_text = QLabel()


        layout = QVBoxLayout()
        layout.addWidget(self.__bt_iniciar)
        layout.addWidget(self.__title_infor_text)
        layout.addWidget(self.__infor_text)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)


    def iniciar(self):
        caminho = self.procurar_arquivo()
        if caminho != "":
            if self.is_excel_file(caminho):
                self.infor(reset=True)
                self.__bt_iniciar.setVisible(False)
                self.excel_load(caminho)
            else:
                self.infor("selecione apenas arquivos do excel",title="Erro")
        else:
            self.infor("nenhum arquivo selecionado tente novamente",title="Erro")

    def excel_load(self,planilha):
        colunas = "A,B,C,D"
        quantidade_colunas = len(colunas.replace(",",""))
        df = pd.read_excel(planilha, sheet_name='WhatsApp', usecols=colunas, skiprows=7).values.tolist()
        
        
 
    def infor(self, mensagem="", title="", reset=False):
        if reset == False:
            self.__title_infor_text.setText(title)
            self.__infor_text.setText(mensagem)
        else:
            self.__title_infor_text.setText("")
            self.__infor_text.setText("")


    


        ######## metodos apenas do bot do whats
    def iniciar_whats(self):
        username = getpass.getuser()
        options = webdriver.ChromeOptions()
        options.add_argument(f"--user-data-dir=C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome")
        self.__navegador = webdriver.Chrome(options=options)
        link = f"https://web.whatsapp.com/"
        self.__navegador.get(link)
    
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
