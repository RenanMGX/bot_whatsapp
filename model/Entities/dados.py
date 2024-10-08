import pandas as pd
import os
from typing import List, Dict, Literal
import re

class Dados:
    @property
    def df(self) -> pd.DataFrame:
        try:
            return self.__df
        except:
            return pd.DataFrame()
        
    @property
    def file_path(self) -> str:
        return self.__file_path
        
    def __init__(self, file_path:str, *, skiprows:int=7, sheet:str="WhatsApp") -> None:
        if not os.path.exists(file_path):
            raise FileExistsError("Arquivo não encontrado!")
        if (not file_path.endswith(".xlsx")) and ((not file_path.endswith(".xlsm"))) and ((not file_path.endswith(".xls"))) :
            raise TypeError("apenas arquivos excel que terminam com .xlsx")
        
        try:
            del self.__df
        except:
            pass
        
        self.__df:pd.DataFrame = pd.read_excel(file_path, dtype=str, skiprows=skiprows, sheet_name=sheet)        
        
        self.__file_path:str = file_path
        
    def extrair_dados(self, *, nacionalidade:Literal['', 'Brasil']='') -> List[Dict[str,str]]:
        result:List[Dict[str,str]] = []
        for row,value in self.df.iterrows():
            dict_infor = dict = {}
            
            dict_infor['Mensagem'] = str(value['Mensagem - Final'])
            
            
            if value['Anexo']:
                anexo_temp = os.path.join(os.path.dirname(self.file_path), str(value['Anexo']))
                if os.path.exists(anexo_temp):
                    dict_infor['Anexo'] = str(anexo_temp)
                else:
                    dict_infor['Anexo'] = str(value['Anexo'])
            else:
                dict_infor['Anexo'] = ''
                
            dict_infor['Nome'] = str(value['Nome'])
                
            numero:str = str(value['Numero'])
            numero = numero.replace('(', '').replace(')', '').replace('-', '').replace(' ', '').replace('+', '')
            
            if nacionalidade == 'Brasil':
                if len(numero) == 13:
                    dict_infor['Numero'] = numero
                elif len(numero) == 11:
                    dict_infor['Numero'] = "55" + numero
                elif len(numero) == 10:
                    dict_infor['Numero'] = numero[0:2] + "9" + numero[2:]
                else:
                    dict_infor['Numero'] = numero
            else:
                dict_infor['Numero'] = numero
                
            result.append(dict_infor)
                
        return result
            
        
if __name__ == "__main__":
    bot = Dados(r'C:\Users\renan.oliveira\Downloads\## NÃO ENCONTRADOS ##\Envio WhatsApp V.2.xlsm', skiprows=8)
    print(bot.df)
    print(bot.extrair_dados(nacionalidade='Brasil'))

    