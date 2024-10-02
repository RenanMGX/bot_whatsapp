from .Entities.navegador import Navegador
from .Entities.dados import Dados, Dict, List
from tkinter.filedialog import askopenfilename
import os

class Model:
    def __init__(self) -> None:
        self.navegador = Navegador()
        
    def carregar_dados(self):
        file_path :str = askopenfilename()
        if not file_path:
            raise FileNotFoundError(f"arquivo invalido {file_path=}")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"arquivo invalido {file_path=}")
        
        try:
            del self.dados
        except:
            pass
        self.dados = Dados(file_path=file_path).extrair_dados(nacionalidade='Brasil')
        
        return self