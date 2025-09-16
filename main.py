import sys
from PyQt5.QtWidgets import QApplication
from model.model import Model
from view.view import View
from time import sleep
import traceback

class Controller:
    def __init__(self, *, model: Model, view: View) -> None:
        self.view = view
        self.model = model
        self.initial_config()
        
    def initial_config(self):
        self.view.tela1_bt_iniciar.clicked.connect(self.iniciar)
        self.view.tela2_bt_carregar_arquivo.clicked.connect(self.carregar)
        self.view.tela2_bt_enviar.clicked.connect(self.enviar)
    
    def iniciar(self):
        self.model.navegador.iniciar_navegador(f"https://web.whatsapp.com/")
        self.model.navegador.verificar_tela_inicio()
        self.view.paginate(1)
        
    def carregar(self):
        self.view.tela2_label.setText("")
        try:
            if not self.model.navegador.verificar_tela_inicio(esperar_conectar=False):
                print("é preciso está conectado")
                raise Exception("é preciso está conectado")
            self.model.carregar_dados()
            self.view.tela2_lista.clear()
            for values in self.model.dados:
                self.view.adicionar_item(text=f'{values['Nome']} | {values['Numero']}', type='Unchecked')
            if self.model.dados:
                self.view.tela2_bt_enviar.setEnabled(True)
            self.view.tela2_label.setText("Arquivo carregado!")
        except Exception as err:
            self.view.tela2_label.setText(str(err))
            
    def enviar(self):
        self.view.tela2_label.setText("")
        self.view.hide()
        try:
            if not self.model.navegador.verificar_tela_inicio(esperar_conectar=False):
                print("é preciso está conectado")
                raise Exception("é preciso está conectado")
            for values in self.model.dados:
                try:
                    self.model.navegador.enviar_mensagem(numero=values['Numero'], mensagem=values['Mensagem'], arquivo=values['Anexo'])
                except Exception as err:
                    print(err)
                    print("<--------------")
                    print(traceback.format_exc())
                    print(">--------------")
                sleep(4)
            self.view.tela2_label.setText("Finalizado!")
        except Exception as err:
            self.view.tela2_label.setText(str(err))
        finally:
            self.view.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = Model()
    ##################################################################################################
    view = View(version="v3.2", nav=model.navegador) # <------------------ Lembrar de alterar a versão
    ###################################################################################################
    controller = Controller(model=model, view=view)
    view.show()
    sys.exit(app.exec_())
 