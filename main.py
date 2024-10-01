from PyQt5.QtWidgets import QApplication
from model.model import Model
from view.view import View
import sys


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
        if not self.model.navegador.verificar_tela_inicio(esperar_conectar=False):
            print("é preciso está conectado")
        self.model.carregar_dados()
        for values in self.model.dados:
            self.view.adicionar_item(text=f'{values['Nome']} | {values['Numero']}', type='Unchecked')
        if self.model.dados:
            self.view.tela2_bt_enviar.setEnabled(True)
            
    def enviar(self):
        if not self.model.navegador.verificar_tela_inicio(esperar_conectar=False):
            print("é preciso está conectado")
        for values in self.model.dados:
            try:
                self.model.navegador.enviar_mensagem(numero=values['Numero'], mensagem=values['Mensagem'], arquivo=values['Anexo'])
            except Exception as err:
                print(err)
            
        
        



if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = Model()
    view = View(version="v3.0")
    controller = Controller(model=model, view=view)
    view.show()
    sys.exit(app.exec_())
