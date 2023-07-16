import os
import math
# import openpyxl
# import shutil
import getpass
import time
import pandas as pd
import selenium
import urllib
import requests
import webbrowser
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
# import win32com.client as win32
# import psutil
import tkinter as tk
from tkinter import messagebox
########### CLASS #########
class Usuarios:
    def __init__(self, nome, numero, arquivo, texto):
        # instancia do Nome
        try:
            if math.isnan(nome):
                self.__nome = None
            else:
                self.__nome = nome
        except:
            self.__nome = nome
        # instancia do Numero
        try:
            if math.isnan(numero):
                self.__numero = None
            else:
                self.__numero = int(numero)
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
                self.__texto = None
            else:
                self.__texto = str(texto)
        except:
            self.__texto = str(texto)
    
    def enviar(self, navegador):
        # verifica se o numero e o texto estão vazios se estiverem vazios ele encerra a função forçando a proxima execução e tbm informar no final do programa o motivo do error
        if (self.__numero == None) or (self.__texto == None):
            if self.__nome != None:
                result = "\n A mensagem não foi enviada para ''" + str(self.__nome) + "'' porque o numero ou o texto são invalidos \n"
                errors.append(result)
            return True
        # print(self.__nome)
        # formata o texto para acessar o link
        texto = self.__texto.encode('utf-8')
        texto = urllib.parse.quote(texto)
        link = f"https://web.whatsapp.com/send?phone=55{self.__numero}&text={texto}"
        # print(link)
        time.sleep(1)
        navegador.get(link)
        time.sleep(1)
        try:
            alert = navegador.switch_to.alert
            alert.accept()
            # print("aceitou")
        except:
            pass
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
                    enviar = navegador.find_element(By.XPATH, "/html/body/div[1]/div/span[2]/div/span/div/div/div/div/div/div[2]/div/div")
                    enviar.click()
                    cont = 999
                    break
                except:
                    # print("veri 5")
                    #caso demore muito para achar um dos botões encerra a procura
                    time.sleep(3)
                    if cont >= 25:
                        break
        if cont >= 25:
            result = "\nA mensagem não foi enviada para ''" + str(self.__nome) + "'' porque aconteceu algum error ao enviar \n"
            errors.append(result)
            return False
        #clicar no botão encontrado
        enviar.click()
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
                send = navegador.find_element(By.XPATH,"/html/body/div[1]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div")
                # Clica no botão enviar
                send.click()
            except:
                result = "\nNão foi possivel enviar o anexo para ''" + str(self.__nome) + "'' porque o arquivo não foi encontrado \n"
                errors.append(result)
                return
                time.sleep(10)  
        return False
##########################
#função do pop up
def popup_completed(mensagem, e=" "):
        root = tk.Tk()
        root.withdraw()
        messagebox.showinfo(e, mensagem)

# Lê a planilha usando o pandas
planilha_excel = "Envio WhatsApp V.2.xlsm"
try:
    df = pd.read_excel(planilha_excel, sheet_name='WhatsApp', usecols='A:D', skiprows=7)
except FileNotFoundError:
    mens = "Arquivo ''" + planilha_excel + "'' não encontrado"
    popup_completed(mens,"Error")
    exit()
except:
    popup_completed("Feche a Planilha antes de executar o Script","Error")
    exit() 
# Remove as linhas com valores ausentes
# df.dropna(inplace=True)
# Armazena o conteúdo das colunas A, B, C e F em uma lista
lista_bruta = df.values.tolist()
lista_tratada = []
for users in lista_bruta:
    lista_tratada.append(Usuarios(users[0],users[1],users[2],users[3]))
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
        # print(finalizador)
        if condicional == True:
            finalizador += 1
        else:
            finalizador = 0
        if finalizador >= 5:
            # print("Finalizado")
            break
        time.sleep(2)
# final do programa ele conta erros que ocorreram durante a execução e coloca no popup no final do programa
errors_final = ""
for x in errors:
    errors_final = errors_final + x
if errors_final != "":
    popup_completed("Os seguintes erros aconteceram: \n" + errors_final, "Script Concluido")
else:
    popup_completed("Script Concluido sem erros!","Script Concluido")
