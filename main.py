import sys
from PyQt5.QtWidgets import QApplication
from model.model import Model
from view.view import View
from time import sleep
import traceback

# On Windows, try to initialize COM apartment as STA before Qt calls OleInitialize.
# This avoids: "OleInitialize() failed: COM error ... RPC_E_CHANGED_MODE"
if sys.platform.startswith("win"):
    try:
        # Prefer pywin32 if available
        import pythoncom

        try:
            pythoncom.CoInitialize()
        except Exception as _err:
            # If COM was already initialized with a different mode this may raise
            # RPC_E_CHANGED_MODE; ignore that specific case and continue.
            try:
                hr = getattr(_err, 'hresult', None)
                if hr is not None and (hr & 0xffffffff) == 0x80010106:
                    pass
                else:
                    print('Warning: pythoncom.CoInitialize() raised:', _err)
            except Exception:
                pass
    except Exception:
        # Fallback: use ctypes to call CoInitializeEx and tolerate RPC_E_CHANGED_MODE
        try:
            from ctypes import windll

            COINIT_APARTMENTTHREADED = 0x2
            hr = windll.ole32.CoInitializeEx(None, COINIT_APARTMENTTHREADED)
            if (hr & 0xffffffff) not in (0, 1, 0x80010106):
                print(f"Warning: CoInitializeEx returned 0x{hr & 0xffffffff:08x}")
        except Exception as _e:
            print('Warning: could not initialize COM:', _e)

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
                self.view.adicionar_item(text=f"{values['Nome']} | {values['Numero']}", type='Unchecked')
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
    view = View(version="v4.40", nav=model.navegador) # <------------------ Lembrar de alterar a versão
    ###################################################################################################
    controller = Controller(model=model, view=view)
    view.show()
    sys.exit(app.exec_())
 