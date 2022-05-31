import os.path
import sys
from os import environ

from PyQt5 import QtCore
from PyQt5.QtWidgets import *

## ==> ventana de inicio o splashscreen
from Ventana1_1 import Ui_Dialog
# importar la ventana 2
from Ventana_Principal import Principal
#from cryptography.fernet import Fernet
## ==> variables globales
counter = 0
# ventana de inicio
class SplashScreen(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        #self.Crear_llave()
        ## UI ==> Codigos de la interface
        ########################################################################
        ## quitando barra de titulos
        self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ## Iniciando el Qtimer
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.progress)
        # Tiempo en milisegundos
        self.timer.start(35)
        # Texto inicial
        self.ui.texto.setText("Iniciando el Programa...")
        # Textos cambiantes durante la barra de progreso
        QtCore.QTimer.singleShot(3000, lambda: self.ui.texto.setText("Cargando Archivos..."))
        QtCore.QTimer.singleShot(4500, lambda: self.ui.texto.setText("Carga finalizada..."))
        ## Activando la ventana de inicio
        ########################################################################
        self.show()
        ## ==> END ##
    ## ==> Funciones de la aplicacion
    ########################################################################
    #region funcion para la barra de progreso
    def progress(self):

        global counter

        # poniendo valor a la barra de progreso
        self.ui.barra1.setValue(counter)

        # cerrar la ventana inicial y abrir la ventana de login
        if counter > 100:
            # detener el timer
            self.timer.stop()
            # mostrar la ventana Login
            self.main = Principal()
            self.main.show()
            # Cerrar la ventana de inicio
            self.close()
        # aumentamos el contador
        counter += 1
    #endregion
#definir funcion para evitar errores con qt
def eliminar_Qt_warning():
    environ["QT_DEVICE_PIXEL_RATIO"]="0"
    environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    environ["QT_SCREEN_SCALE_FACTORS"] = "1"
    environ["QT_SCALE_FACTOR"] = "1"
### ::::::::::: damos inicio a la aplicacion
if __name__ == "__main__":
    eliminar_Qt_warning()
    app = QApplication(sys.argv)
    window = SplashScreen()
    sys.exit(app.exec_())