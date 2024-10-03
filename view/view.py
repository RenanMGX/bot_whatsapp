# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\interface.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from typing import Literal
from PyQt5.QtCore import Qt
from model.Entities.navegador import Navegador

class View(QMainWindow):
    
    def __init__(self, *, nav:Navegador|None=None, version:str='Beta'):
        self.__nav:Navegador|None = nav
        self.__version = version
        super().__init__()
        self.setObjectName("BotWhatsApp")
        self.resize(200, 100)
        
        self.Telas = QtWidgets.QStackedWidget(self)
        self.Telas.setGeometry(QtCore.QRect(10, 10, 421, 231))
        self.Telas.setObjectName("Telas")
        
        self.tela1_iniciar = QtWidgets.QWidget()
        self.tela1_iniciar.setObjectName("tela1_iniciar")
        
        self.tela1_bt_iniciar = QtWidgets.QPushButton(self.tela1_iniciar)
        self.tela1_bt_iniciar.setGeometry(QtCore.QRect(50, 25, 91, 31))
        self.tela1_bt_iniciar.setObjectName("tela1_bt_iniciar")
        
        self.Telas.addWidget(self.tela1_iniciar)
        
        self.tela2_dados = QtWidgets.QWidget()
        self.tela2_dados.setObjectName("tela2_dados")
        
        self.tela2_bt_carregar_arquivo = QtWidgets.QPushButton(self.tela2_dados)
        self.tela2_bt_carregar_arquivo.setGeometry(QtCore.QRect(10, 10, 111, 41))
        self.tela2_bt_carregar_arquivo.setObjectName("tela2_bt_carregar_arquivo")
        
        self.tela2_bt_enviar = QtWidgets.QPushButton(self.tela2_dados)
        self.tela2_bt_enviar.setEnabled(False)
        self.tela2_bt_enviar.setGeometry(QtCore.QRect(10, 60, 111, 41))
        self.tela2_bt_enviar.setObjectName("tela2_bt_carregar_arquivo_2")
        
        self.tela2_lista = QtWidgets.QListWidget(self.tela2_dados)
        self.tela2_lista.setGeometry(QtCore.QRect(140, 10, 256, 192))
        self.tela2_lista.setObjectName("tela2_lista")
        
        self.tela2_label = QtWidgets.QLabel(self.tela2_dados)
        self.tela2_label.setGeometry(QtCore.QRect(10, 120, 111, 80))
        #self.tela2_label.setStyleSheet("border: 2px solid black")
        self.tela2_label.setWordWrap(True)
        
        self.Telas.addWidget(self.tela2_dados)

        self.retranslateUi()
        self.Telas.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("BotWhatsApp", f"Automação WhatsAPP {self.__version}"))
        
        self.tela1_bt_iniciar.setText(_translate("BotWhatsApp", "Iniciar"))
        
        self.tela2_bt_carregar_arquivo.setText(_translate("BotWhatsApp", "Carregar Arquivos"))
        
        self.tela2_bt_enviar.setText(_translate("BotWhatsApp", "Enviar"))
        
        __sortingEnabled = self.tela2_lista.isSortingEnabled()
        
        self.tela2_lista.setSortingEnabled(False)
                
        self.tela2_lista.setSortingEnabled(__sortingEnabled)
        
    def paginate(self, index:int):
        if index == 0:
            self.resize(200, 100)
        elif index == 1:
            self.resize(450, 250)
        self.Telas.setCurrentIndex(index)
        
    def adicionar_item(self, *, text:str, type:Literal['Unchecked', 'Checked']):
        item = QtWidgets.QListWidgetItem()
        item.setFlags(item.flags() & ~Qt.ItemIsEnabled)#type:ignore

        if type =='Checked':
            item.setCheckState(QtCore.Qt.Checked) #type:ignore
        elif type == 'Unchecked':
            item.setCheckState(QtCore.Qt.Unchecked) #type:ignore
            
        item.setText(text)
        
        self.tela2_lista.addItem(item)

    def closeEvent(self, event):
        if self.__nav:
            print("fechou")
            try:
                self.__nav.nav.close()
            except:
                pass
            try:
                del self.__nav
            except:
                pass
            
        event.accept()
    

if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    
    app = QApplication(sys.argv)
    view = View()
    view.paginate(1)
    view.adicionar_item(text='text', type='Unchecked')
    view.show()
    sys.exit(app.exec_())
    