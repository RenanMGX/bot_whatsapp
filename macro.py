#import os
import sys
import math
# import openpyxl
# import shutil
import getpass
import time
import pandas as pd
import datetime
#import selenium
import urllib
#import requests
#import webbrowser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import logging
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox


# import win32com.client as win32
# import psutil
#função para procurar a planilha
def procurar_arquivo():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    return file_path

data_atual = datetime.datetime.now()

#desativar log do selenium
logging.basicConfig(level=logging.CRITICAL)
########### CLASS #########
class Usuarios:
    def __init__(self, nome, numero, arquivo, texto, texto2):
        # instancia do Nome
        self.__texto = []
        try:
            numero_tratado = self.remover_formatacao_telefone(str(numero))
        except:
            pass

        try:
            if math.isnan(nome):
                self.__nome = None
            else:
                self.__nome = nome
        except:
            self.__nome = nome
        # instancia do Numero
        try:
            if math.isnan(numero_tratado):
                self.__numero = None
            else:
                self.__numero = int(numero_tratado)
        except:
            self.__numero = 9999999999999
        # instancia do Arquivo
        try:
            if math.isnan(arquivo):
                self.__arquivo = None
            else:
                self.__arquivo = arquivo
        except:
            self.__arquivo = arquivo
        # instancia do Texto
        try:
            if math.isnan(texto):
                self.__texto.append(None)
            else:
                self.__texto.append(str(texto))
        except:
            self.__texto.append(str(texto))
        try:
            if math.isnan(texto2):
                self.__texto.append(None)
            else:
                self.__texto.append(str(texto2))
        except:
            self.__texto.append(str(texto2))

    def remover_formatacao_telefone(self, telefone):
        telefone = telefone.replace("(", "").replace(")", "").replace(" ", "")
        return int(telefone)

    def enviar(self, navegador):
                # verifica se o numero e o texto estão vazios se estiverem vazios ele encerra a função forçando a proxima execução e tbm informar no final do programa o motivo do error
        if (self.__numero == None):
            if self.__nome != None:
                result = "A mensagem não foi enviada para ''" + str(self.__nome) + "'' porque o numero ou o texto são invalidos \n"
                errors.append(result)
            return True
        # print(self.__nome)
        # formata o texto para acessar o link
        self.__anexo_verifi = False
        for texto_base in self.__texto:
            if (texto_base == None) or texto_base == "nan":
                continue
            texto = texto_base.encode('utf-8')
            texto = urllib.parse.quote(texto)
            link = f"https://web.whatsapp.com/send?phone=55{self.__numero}&text={texto}"
            # print(link)
            time.sleep(1)
            navegador.get(link)
            time.sleep(1)
            cont = 0
            while True:
            # print("veri 2")
                cont += 1
                try:
                    # print("veri 3")
                    # tentar encontrar o botão Enviar
                    enviar = navegador.find_element(By.XPATH, "//button[@data-testid='compose-btn-send']")
                    break
                except:
                    try:
                        # print("veri 4")
                        # caso não ache o botão enviar tenta achar o botão continuar
                        enviar = navegador.find_element(By.XPATH, '//*[@id="app"]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/button/div/div')
                        enviar.click()
                        cont = 999
                        break
                    except:
                        # print("veri 5")
                        #caso demore muito para achar um dos botões encerra a procura
                        time.sleep(2)
                        if cont >= 25:
                            break
            if cont == 999:
                result = "A mensagem não foi enviada para ''" + str(self.__nome) + "'' porque o numero informado é invalido \n"
                errors.append(result)
                return False
            elif cont >= 25:
                result = "A mensagem não foi enviada para ''" + str(self.__nome) + "'' porque aconteceu algum error ao enviar \n"
                errors.append(result)
                return False
            #clicar no botão encontrado
            enviar.click()
            time.sleep(1)
            if self.__anexo_verifi == False:
                self.anexo(navegador)
            time.sleep(1)
        # input()
        return False
    def anexo(self, navegador):
        if self.__arquivo != None:
        # Anexo de Arquivo
            time.sleep(1)
            try:
                # Clica no botão adicionar
                arquivo = navegador.find_element(By.CSS_SELECTOR, "span[data-icon='clip']")
                arquivo.click()
                # Seleciona input
                time.sleep(1)
                attach = navegador.find_element(By.CSS_SELECTOR, "input[type='file']")
                # Adiciona arquivo
                attach.send_keys(self.__arquivo)
                time.sleep(1)
                # Seleciona botão enviar
                send = navegador.find_element(By.XPATH, '//*[@id="app"]/div/div/div[3]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span')
                # Clica no botão enviar
                send.click()
                confirmou = False
                while True:
                    if confirmou == True:
                        break
                    else:
                        try:
                            navegador.find_element(By.XPATH, '//span[@data-testid="msg-time"]')
                            confirmou = False
                        except:
                            confirmou = True
            except:
                result = "Não foi possivel enviar o anexo para ''" + str(self.__nome) + "'' porque o arquivo não foi encontrado \n"
                errors.append(result)
                return "voltou"
        self.__anexo_verifi = True
##########################
#função do pop up
def popup_completed(mensagem, e=" "):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(e, mensagem)

# Lê a planilha usando o pandas
planilha_excel = procurar_arquivo()
try:
    df = pd.read_excel(planilha_excel, sheet_name='WhatsApp', usecols='A:D,F', skiprows=7)
except FileNotFoundError:
    mens = "Arquivo ''" + planilha_excel + "'' não encontrado"
    popup_completed(mens,"Error")
    sys.exit()
except:
    popup_completed("Feche a Planilha antes de executar o Script","Error")
    sys.exit() 
# Remove as linhas com valores ausentes
# df.dropna(inplace=True)
# Armazena o conteúdo das colunas A, B, C e F em uma lista
lista_bruta = df.values.tolist()
lista_tratada = []
# cria uma lista para cada usaurio na Classe Usuario
for users in lista_bruta:
    lista_tratada.append(Usuarios(users[0],users[1],users[2],users[3],users[4]))
lista_bruta = None

# acessar o navegador do usuario pelo perfil
username = getpass.getuser()
options = webdriver.ChromeOptions()
options.add_argument(f"--user-data-dir=C:\\Users\\{username}\\AppData\\Local\\Google\\Chrome")
# Inicialize o na vegador e chama a função da class Usuarios
finalizador = 0
errors = []
with webdriver.Chrome(options=options)as navegador:
    # a condicional conta quantas linhas da coluna nome estão vazias em sequencia se 5 ou mais estiverem vazias finaliza o loop
    for dados in lista_tratada:
        condicional = dados.enviar(navegador)
        if condicional == True:
            finalizador += 1
        else:
            finalizador = 0
        if finalizador >= 5:
            break
        time.sleep(2)
# final do programa ele conta erros que ocorreram durante a execução e coloca no popup no final do programa
errors_final = ""
for x in errors:
    errors_final = errors_final + x
if errors_final != "":
    popup_completed("o script foi concluido porem com alguns erros, os dados foram salvo no arquivo ''erros.txt''", "Script Concluido")
else:
    popup_completed("Script Concluido sem erros!","Script Concluido")
sys.exit()
