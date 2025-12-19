from pywinauto.application import Application
from pywinauto import Desktop
import pygetwindow
from time import sleep   
from pywinauto.application import WindowSpecification
import os
import string
import shutil
        
def enviar_arquivo_abrir(arquivo):
    for i in range(10):
        try:
            
            import pdb;pdb.set_trace() # <-------------------------------- Debug
            app = Application().connect(title_re=f".*Abrir.*")
            
            n_caract = {'~':'', '%':'', '¨':'', '(':'', ')':'', '=':''}
            temp_name = os.path.basename(arquivo)
            for k, v in n_caract.items():
                temp_name = temp_name.replace(k, v)
                
            if temp_name != os.path.basename(arquivo):
                new_arquivo = os.path.join(os.path.dirname(arquivo), temp_name)
                shutil.copy(arquivo, new_arquivo)
                arquivo = new_arquivo
            
            arquivo = os.path.normpath(arquivo)
            
            janela:WindowSpecification = app.window(title_re=f".*Abrir.*")
            # if "(" in arquivo:
            #     import pdb;pdb.set_trace() # <-------------------------------- Debug
                
            janela["&Nome:Edit"].set_edit_text(arquivo)
            janela["&Abrir"].click()
            
            
            sleep(1)
            os.remove(arquivo) if temp_name != os.path.basename(arquivo) else None
                        
            return
        except:
            sleep(1)
