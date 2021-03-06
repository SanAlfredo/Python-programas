# libreria para comparar el correo
import datetime
import re
import requests

from PyQt5.QtCore import (QDate, QTime, QTimer, Qt, QRegExp,QDateTime)
from PyQt5.QtGui import (QRegExpValidator)
from PyQt5.QtWidgets import *

# importar las Clases
import Clases
# importar la ventana
from Ventana3_1 import Ui_MainWindow
# imrpotar libreria postgress
import psycopg2
from psycopg2 import sql
#importar la ventana de visualizacion de pdf
import pdf_visualizar
#region variables globales
# variable global usuario para controlar al usuario
usuario = ""
contra=""
codigo=""
matricula_user=""
# para controlar el color de fondo
tema = 0
# variable global para controlar el registro de paciente
reg_pac = 0
x = 0
# variabla global para controlar el registro de usuario
reg_us = 0
#variable global para controlar registro de usuario dentro admin
reg_us_admin=0
#tabla persona
persona=[]
#tabla medico
medico=[]
#es el resultado de la busqueda del usuario en la bbdd
resultado_bbdd_usuario=[]
bbdd_paciente=[]
bbdd_carnet_pac=[]
bbdd_antec_pac=[]
bbdd_padre=[]
bbdd_madre=[]
bbdd_carnet_padre=[]
bbdd_carnet_madre=[]
bbdd_tel1=""
bbdd_tel2=""
#endregion
class Principal(QMainWindow):
    """
    Ventana principal
    """
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()
        # iniciar los stack widget en 0 para no tener sorpresas
        self.Iniciar_cero()
        # --------------------------------------------------------------------------------------------------
        # un validador de datos introducidos por teclado
        self.Validar_valores_intro()
        # --------------------------------------------------------------------------------------------------
        # eventos para obtener hora y fecha
        timer = QTimer(self)
        timer.timeout.connect(self.MostrarHora_fecha)
        timer.start(1000)
        # --------------------------------------------------------------------------------------------------
        # MODULO DE LOGEO
        # --------------------------------------------------------------------------------------------------
        self.ui.btn_inicio.clicked.connect(self.Ventana_login)
        self.ui.btn_log_iniciar.clicked.connect(self.Verifica)
        self.ui.btn_log_close.clicked.connect(self.Cerrar_ventana1)
        # --------------------------------------------------------------------------------------------------
        # MODULO DE REGISTRO USUARIO NUEVO
        # --------------------------------------------------------------------------------------------------
        self.ui.btn_reg_nuevo_user.clicked.connect(self.Verifica_new_user)
        self.ui.btn_reg_limpia.clicked.connect(self.Limpia_reg_user)
        self.ui.btn_reg_close.clicked.connect(self.Cerrar_registro)
        # --------------------------------------------------------------------------------------------------
        # MODULO DE RECUPERACION DE CONTRASE??A
        # --------------------------------------------------------------------------------------------------
        self.ui.btn_recu.clicked.connect(self.Ventana_recu)
        self.ui.btn_recu_limpia.clicked.connect(self.Limpia_recu)
        self.ui.btn_recu_close.clicked.connect(self.Iniciar_cero)
        self.ui.btn_recu_codigo.clicked.connect(self.Verifica_recu)
        self.ui.btn_recu_codigo2.clicked.connect(self.Verifica_codigo)
        self.ui.btn_recu_guarda.clicked.connect(self.Verifica_pass)
        # --------------------------------------------------------------------------------------------------
        # MODULO DE REGISTRO NUEVO USUARIO
        # --------------------------------------------------------------------------------------------------
        self.ui.btn_nuevo.clicked.connect(lambda event: self.Ventana_admi_reg(1))
        self.ui.btn_reg_user_limpia.clicked.connect(self.Limpia_admin_reg)
        self.ui.btn_reg_user_volver.clicked.connect(lambda event: self.ui.Stacked_admin.setCurrentIndex(0))
        self.ui.btn_admin_reg_user.clicked.connect(self.Registra_nuevo_user)
        self.ui.btn_admin_reset.clicked.connect(lambda event:self.Ventana_admi_reg(2))
        # --------------------------------------------------------------------------------------------------
        # MODULO DE ADMINISTRACION DE USUARIOS
        # --------------------------------------------------------------------------------------------------
        self.ui.btn_admin_usuarios.clicked.connect(self.Entrar_control_user)
        self.ui.btn_admi_user_volver.clicked.connect(lambda event: self.ui.Stacked_admin.setCurrentIndex(0))
        self.ui.btn_admin_buscar_user.clicked.connect(lambda event: self.Verifica_amdin(1))
        self.ui.btn_admin_limpiar.clicked.connect(self.Limpia_admin1)
        self.ui.btn_admin_habil.clicked.connect(lambda event: self.Seleccionar_item_tabla(1))
        self.ui.btn_admin_inhabil.clicked.connect(lambda event: self.Seleccionar_item_tabla(2))
        # --------------------------------------------------------------------------------------------------
        # MODULO DE HISTORIALES DE LOGEO
        # --------------------------------------------------------------------------------------------------
        self.ui.btn_admin_historial.clicked.connect(self.Busca_historial)
        self.ui.btn_admin_historial_buscar.clicked.connect(self.Busca_por_fecha)
        self.ui.cb_admin_historial.currentIndexChanged.connect(self.Combo_cambio1)
        self.ui.cb_admin_med.currentIndexChanged.connect(self.Combo_cambio2)
        self.ui.cb_admin_med2.currentIndexChanged.connect(self.Combo_cambio3)
        self.ui.btn_admin_historial_volver.clicked.connect(self.Salir_admin)
        self.ui.btn_admin_historial_limpiar.clicked.connect(self.Limpia_admin2)
        # --------------------------------------------------------------------------------------------------
        # MODULO DE REGISTRO NUEVO PACIENTE
        # --------------------------------------------------------------------------------------------------
        self.ui.btn_reg_pac.clicked.connect(lambda event: self.Ventana_reg_pac(1))
        self.ui.btn_reg_pac_limpiar.clicked.connect(self.Limpia_reg_pac)
        self.ui.btn_reg_pac_save.clicked.connect(self.Ventana_nueva_hist)
        self.ui.btn_reg_pac_close.clicked.connect(self.Cerrar_ventanas_usuario)
        # --------------------------------------------------------------------------------------------------
        # MODULO DE BUSQUEDA DE HISTORIALES Y CONSULTAS
        # --------------------------------------------------------------------------------------------------
        self.ui.btn_busc_pac.clicked.connect(self.Ventana_info_pac)
        self.ui.btn_info_pac_selec.clicked.connect(lambda event: self.Seleccionar_item_tabla(4))
        self.ui.btn_info_pac_ver.clicked.connect(lambda event: self.Seleccionar_item_tabla(5))
        self.ui.btn_info_pac_clean.clicked.connect(self.Limpia_info_busc)
        self.ui.btn_info_pac_close.clicked.connect(self.Cerrar_ventanas_usuario)
        self.ui.btn_info_pac_buscar.clicked.connect(lambda event: self.Verifica_amdin(3))
        # --------------------------------------------------------------------------------------------------
        # MODULO DE BUSQUEDA DE PACIENTE PARA NUEVA CONSULTA O MODIFICACION DE DATOS
        # --------------------------------------------------------------------------------------------------
        self.ui.btn_hist_pac.clicked.connect(lambda event: self.Ventana_reg_hist(1))
        self.ui.btn_hist_pac_buscar.clicked.connect(lambda event: self.Verifica_amdin(2))
        self.ui.btn_hist_pac_close.clicked.connect(self.Cerrar_ventanas_usuario)
        self.ui.btn_hist_pac_selec.clicked.connect(lambda event:self.Seleccionar_item_tabla(3))
        self.ui.btn_hist_pac_clean.clicked.connect(self.Limpia_hist_busc)
        # --------------------------------------------------------------------------------------------------
        # MODULO DE REGISTRO NUEVA CONSULTA
        # --------------------------------------------------------------------------------------------------
        self.ui.btn_hist_pac_clean2.clicked.connect(self.Limpia_hist_pac)
        self.ui.btn_hist_pac_save.clicked.connect(self.Guardar_consulta)
        self.ui.txt_hist_pac_temp.editingFinished.connect(self.Poner_valor)
        self.ui.btn_hist_pac_IMC.clicked.connect(self.Verifica_IMC)
        self.ui.btn_hist_pac_edad.clicked.connect(self.Verifica_edad)
        # --------------------------------------------------------------------------------------------------
        # MODULO MODIFICAR DATOS DE PACIENTE
        # --------------------------------------------------------------------------------------------------
        self.ui.btn_modificar_pac.clicked.connect(lambda event: self.Ventana_reg_hist(2))
        # --------------------------------------------------------------------------------------------------
        # MODULO MODIFICAR DATOS DE USUARIO
        # --------------------------------------------------------------------------------------------------
        self.ui.btn_modificar_user.clicked.connect(self.Ventana_modifica)
        # boton de configuraci??n de tema
        self.ui.btn_config.clicked.connect(self.Ventana_tema)
        self.ui.btn_config_probar.clicked.connect(self.Prueba_tema)
        self.ui.btn_config_save.clicked.connect(self.Elegir_tema)
        self.ui.btn_config_close.clicked.connect(self.Salir_tema)
        # cierre de sesi??n no importa quien este logeado
        self.ui.btn_salir.clicked.connect(self.Salir_al_inicio)

    #region M??dulo inicial, poner las varibles en 0.
    def Iniciar_cero(self):
        """
        M??todo para inciar de cero las variables globales y los campos
        """
        global usuario
        global contra
        global codigo
        global tema
        global x
        global reg_pac
        global reg_us
        global reg_us_admin
        global persona
        global medico
        global resultado_bbdd_usuario
        global bbdd_paciente
        global bbdd_carnet_pac
        global bbdd_antec_pac
        global bbdd_padre
        global bbdd_madre
        global bbdd_carnet_padre
        global bbdd_carnet_madre
        global bbdd_tel1
        global bbdd_tel2
        bbdd_paciente=[]
        bbdd_carnet_pac=[]
        bbdd_antec_pac=[]
        bbdd_padre=[]
        bbdd_madre=[]
        bbdd_carnet_padre=[]
        bbdd_carnet_madre=[]
        bbdd_tel1=""
        bbdd_tel2=""
        # resultado de la busqueda de usuario en la bbdd
        resultado_bbdd_usuario=[]
        # tabla persona
        persona=[]
        # tabla medico
        medico=[]
        reg_us_admin=0
        reg_pac = 0
        reg_us = 0
        x = 0
        usuario = ""
        contra = ""
        codigo=""
        tema = 0
        self.Poner_tema(tema)
        # esconder botones de configuracion y cerrar sesion
        self.ui.btn_config.setVisible(False)
        self.ui.btn_salir.setVisible(False)
        self.ui.txt_reg_user_mat.setReadOnly(False)
        self.ui.lbl_hist_pac_IMC.setVisible(False)
        self.ui.lbl_hist_pac_edad.setVisible(False)
        self.ui.lbl_hist_pac_temp.setText("??C")
        self.ui.lbl_reg_user.setVisible(False)
        self.ui.cb_reg_user.setVisible(False)
        # *************************************************
        # poner los combobox en 0
        # *************************************************
        # administrador
        self.ui.cb_admin_historial.setCurrentIndex(0)
        self.ui.cb_admin_med.setCurrentIndex(0)
        self.ui.cb_admin_med2.setCurrentIndex(0)
        self.ui.cb_admin_med2.setVisible(False)
        self.ui.cb_reg_user.setCurrentIndex(0)
        # paciente nuevo
        self.ui.cb_reg_pac_sex.setCurrentIndex(0)
        self.ui.cb_reg_pac_gsf.setCurrentIndex(0)
        self.ui.cb_reg_pac_gs.setCurrentIndex(0)
        # registro consulta
        self.ui.cb_hist_pac_consul.setCurrentIndex(0)
        # *************************************************
        # poner los stacked menu en 0
        # *************************************************
        self.ui.Stacked_main.setCurrentIndex(0)
        self.ui.Stacked_tareas.setCurrentIndex(0)
        self.ui.Stacked_recu.setCurrentIndex(0)
        self.ui.Stacked_admin.setCurrentIndex(0)
        self.ui.Stacked_admin_log.setCurrentIndex(0)
    #endregion
    #region registro en la tabla historial
    def Registro_tabla_historial(self,datos):
        global matricula_user
        fecha_actual = datetime.datetime.today()
        tabla = "fecha"
        columnas = "id_fecha,fechayhora,tipo_fecha"
        id_fecha1 = self.Conseguir_id_tabla(1, "id_fecha", tabla)
        valores = [id_fecha1, fecha_actual, datos[0]]
        hist = self.Insertar_bbdd(tabla, columnas, valores)
        if hist == 1:
            tabla = "historial"
            columnas = "id_historial,medico,fecha,id_tabla,descripciones,tabla"
            id_historial = self.Conseguir_id_tabla(1, "id_historial", tabla)
            historial_log = [id_historial, matricula_user, id_fecha1, datos[1], datos[2], datos[3]]
            hist1 = self.Insertar_bbdd(tabla, columnas, historial_log)
            if hist1 == 1:
                pass
     #endregion
    #region Cierre de sesion, para usuarios y administrador
    def Salir_al_inicio(self):
        """
        Permite cerrar sesi??n ya sea para el usuario o administrador
        con esto iniciamos de cero
        """
        global usuario
        usuario1=Clases.Metodos.Obtener_datos('USER')
        resp = QMessageBox.question(self, "Cierre de sesi??n", "??Est?? seguro de cerrar la sesi??n?", QMessageBox.Yes
                                    | QMessageBox.No, QMessageBox.No)
        if resp == QMessageBox.Yes:
            if usuario != usuario1:
                # region registro en la tabla historial
                enviar_datos = 6, "Cierre de sesi??n", 5, "Salir del sistema"
                self.Registro_tabla_historial(enviar_datos)
                # endregion
            self.Iniciar_cero()
    #endregion
    #region Sobre escritura al metodo close
    def closeEvent(self,event):
        global usuario
        usuario1 = Clases.Metodos.Obtener_datos('USER')
        cerrar=QMessageBox.question(self,"Cerrar programa","??Est?? seguro de cerrar el programa?",QMessageBox.Yes
                                        | QMessageBox.No, QMessageBox.No)
        if cerrar==QMessageBox.Yes:
            if usuario:
                if usuario != usuario1:
                    # region registro en la tabla historial
                    enviar_datos = 6, "Cierre de sesi??n", 5, "Salir del sistema"
                    self.Registro_tabla_historial(enviar_datos)
                    # endregion
                    event.accept()
                else:
                    event.accept()
            else:
                event.accept()
        else:
            event.ignore()
    #endregion
    # -----------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------
    # entrando a las ventanas
    #region abrir ventana de logeo
    def Ventana_login(self):
        """
        entrar a la ventana de logeo
        se debe limpiar antes de entrar
        """
        self.Limpia_login()
        self.ui.Stacked_main.setCurrentIndex(1)
        self.ui.txt_log_user.setFocus()
        self.les = [self.ui.txt_log_user, self.ui.txt_log_pass, self.ui.btn_log_iniciar]
    #endregion
    #region Ventana de registro
    def Ventana_registro(self):
        """
        Entrar a la ventana de registro de nuevo usuario
        donde debe ingresar sus datos, todos los campos son obligatorios
        """
        global reg_us
        global resultado_bbdd_usuario
        if reg_us == 1:
            self.Limpia_reg_user()
        if reg_us == 2:
            resultado_bbdd_usuario=self.Datos_del_usuario()
            self.ui.txt_reg_user_mat.setText(resultado_bbdd_usuario[0])
            self.ui.txt_reg_user_mat.setReadOnly(True)
            self.ui.txt_reg_user_CI.setText(resultado_bbdd_usuario[7])
            self.ui.cb_reg_user_CI.setCurrentIndex(resultado_bbdd_usuario[8])
            self.ui.txt_reg_nom_user.setText(resultado_bbdd_usuario[9])
            self.ui.txt_reg_apell1_user.setText(resultado_bbdd_usuario[10])
            self.ui.txt_reg_apell2_user.setText(resultado_bbdd_usuario[11])
            texto=resultado_bbdd_usuario[4],resultado_bbdd_usuario[5]
            password=Clases.Metodos.Desencriptador(2,texto)
            self.ui.txt_reg_pass.setText(password)
            self.ui.txt_reg_pass1.setText(password)
            self.ui.txt_reg_correo_user.setText(resultado_bbdd_usuario[6])
            self.ui.comboBox.setCurrentIndex(resultado_bbdd_usuario[12])
        self.ui.Stacked_main.setCurrentIndex(2)
        self.ui.txt_reg_user_CI.setFocus()
        self.les = [self.ui.txt_reg_user_CI, self.ui.cb_reg_user_CI, self.ui.txt_reg_user_mat, self.ui.txt_reg_nom_user,
                        self.ui.txt_reg_apell1_user, self.ui.txt_reg_apell2_user, self.ui.txt_reg_pass, self.ui.txt_reg_pass1,
                        self.ui.txt_reg_correo_user, self.ui.comboBox, self.ui.btn_reg_nuevo_user]
    #endregion
    #region Ventana de recuperaci??n de contrase??a
    def Ventana_recu(self):
        self.Limpia_recu()
        self.ui.Stacked_main.setCurrentIndex(3)
        self.ui.txt_recu_user.setFocus()
        self.les = [self.ui.txt_recu_user, self.ui.txt_recu_correo, self.ui.btn_recu_codigo]
    #endregion
    #region Ventana de registro de paciente
    def Ventana_reg_pac(self, num):
        global tema
        global reg_pac
        self.Poner_tema(tema)
        self.ui.txt_reg_pac_nom.setFocus()
        if num == 1:
            reg_pac = 1
            self.ui.lbl_reg_mod_pac.setText("Registro de nuevo historial de paciente")
            self.Limpia_reg_pac()
        if num == 2:
            reg_pac = 2
            self.ui.lbl_reg_mod_pac.setText("Edici??n del registro de historial de paciente")
        self.les = [self.ui.txt_reg_pac_nom,self.ui.txt_reg_pac_app1,self.ui.txt_reg_pac_app2,self.ui.txt_reg_pac_CI,
                    self.ui.cb_reg_pac_CI,self.ui.date_reg_pac_nac,self.ui.cb_reg_pac_gs,self.ui.cb_reg_pac_gsf,
                    self.ui.cb_reg_pac_sex,self.ui.txt_reg_pac_pes,self.ui.txt_reg_pac_tall,self.ui.pt_reg_pac_ap,
                    self.ui.pt_reg_pac_alerg,self.ui.txt_reg_pac_pro1,self.ui.txt_reg_pac_res1,self.ui.txt_reg_pac_dir,
                    self.ui.txt_reg_pac_barr,self.ui.txt_reg_pac_padre,self.ui.txt_reg_pac_padre1,self.ui.txt_reg_pac_padre2,
                    self.ui.txt_reg_pac_CI_padre,self.ui.cb_reg_pac_CI_padre,self.ui.txt_reg_pac_tel1,self.ui.txt_reg_pac_madre,
                    self.ui.txt_reg_pac_madre1, self.ui.txt_reg_pac_madre2,self.ui.txt_reg_pac_CI_madre,self.ui.cb_reg_pac_CI_madre,
                    self.ui.txt_reg_pac_tel2,self.ui.btn_reg_pac_save]
        self.ui.Stacked_main.setCurrentIndex(6)
    #endregion
    #region modificar datos de usuario
    def Ventana_modifica(self):
        global tema
        self.Poner_tema(tema)
        global reg_us
        reg_us = 2
        self.Ventana_registro()
    #endregion
    #region Ventana para registro de historias, buscar su historia primero
    def Ventana_reg_hist(self, num):
        '''
        Esta parte del c??digo se encuentra dentro del Stackmain 7 que es un cuadro
        de b??squeda de nombres para encontrar historias, sirve para modificar al
        paciente o para registrar una nueva consulta seleccionando el nombre en la tabla
        '''
        global tema
        self.Poner_tema(tema)
        global x
        if num == 1:
            x = 1
        if num == 2:
            x = 2
        self.Limpia_hist_busc()
        self.ui.Stacked_main.setCurrentIndex(7)
        self.ui.txt_hist_pac_nom.setFocus()
        self.les = [self.ui.txt_hist_pac_nom, self.ui.txt_hist_pac_app1, self.ui.txt_hist_pac_app2,
                    self.ui.btn_hist_pac_buscar]
    #endregion
    #region ventana para registro de historias despues de buscar o registrar, se puede ingresar por 2 caminos
    def Ventana_reg_hist2(self, datos):
        global tema
        self.Poner_tema(tema)
        self.Limpia_hist_pac()
        self.ui.lbl_hist_pac_nombre.setText(datos[0])
        self.ui.lbl_hist_pac_codigo.setText(datos[1])
        self.ui.lbl_hist_pac_antecedentes.setPlainText(datos[2])
        self.ui.lbl_hist_pac_alergias.setPlainText(datos[3])
        self.ui.cb_hist_pac_consul.setFocus()
        self.les = [self.ui.cb_hist_pac_consul, self.ui.txt_hist_pac_fc, self.ui.txt_hist_pac_fr,
                    self.ui.txt_hist_pac_temp,
                    self.ui.txt_hist_pac_SO, self.ui.txt_hist_pac_pa1, self.ui.txt_hist_pac_pa2,
                    self.ui.txt_hist_pac_percef,
                    self.ui.tab_fecha_hora, self.ui.btn_hist_pac_edad, self.ui.txt_hist_pac_pes,
                    self.ui.txt_hist_pac_tall,
                    self.ui.btn_hist_pac_IMC, self.ui.pt_hist_pac_con, self.ui.btn_hist_pac_save]
    #endregion
    #region modulo que controla el registro de historias clinicas
    def Ventana_nueva_hist(self):
        global reg_pac
        global persona
        nom_pac=self.ui.txt_reg_pac_nom.text()
        ap1_pac=self.ui.txt_reg_pac_app1.text()
        ap2_pac=self.ui.txt_reg_pac_app2.text()
        ci_pac=self.ui.txt_reg_pac_CI.text()
        ex_ci_pac=self.ui.cb_reg_pac_CI.currentIndex()
        fecha_pac=self.ui.date_reg_pac_nac.date()
        fecha_pac=fecha_pac.toPyDate()
        fecha_pac=fecha_pac.strftime('%Y-%m-%d')
        fecha_pac1=fecha_pac
        fecha_pac=datetime.datetime.strptime(fecha_pac,'%Y-%m-%d')
        sexo_pac=self.ui.cb_reg_pac_sex.currentIndex()
        factor_pac=self.ui.cb_reg_pac_gsf.currentIndex()
        grupo_pac=self.ui.cb_reg_pac_gs.currentIndex()
        peso_pac=self.ui.txt_reg_pac_pes.text()
        talla_pac=self.ui.txt_reg_pac_tall.text()
        antecedentes = self.ui.pt_reg_pac_ap.toPlainText()
        alergias = self.ui.pt_reg_pac_alerg.toPlainText()
        procedencia=self.ui.txt_reg_pac_pro1.text()
        residencia=self.ui.txt_reg_pac_res1.text()
        direccion=self.ui.txt_reg_pac_dir.text()
        barrio=self.ui.txt_reg_pac_barr.text()
        nom_padre=self.ui.txt_reg_pac_padre.text()
        ap1_padre=self.ui.txt_reg_pac_padre1.text()
        ap2_padre=self.ui.txt_reg_pac_padre2.text()
        ci_padre=self.ui.txt_reg_pac_CI_padre.text()
        ex_ci_padre=self.ui.cb_reg_pac_CI_padre.currentIndex()
        tel_padre=self.ui.txt_reg_pac_tel1.text()
        nom_madre = self.ui.txt_reg_pac_madre.text()
        ap1_madre = self.ui.txt_reg_pac_madre1.text()
        ap2_madre = self.ui.txt_reg_pac_madre2.text()
        ci_madre = self.ui.txt_reg_pac_CI_madre.text()
        ex_ci_madre = self.ui.cb_reg_pac_CI_madre.currentIndex()
        tel_madre = self.ui.txt_reg_pac_tel2.text()
        r=0
        t=0
        if not nom_pac or grupo_pac==0 or factor_pac==0 or sexo_pac==0 or not procedencia or not residencia or not direccion or not barrio:
            QMessageBox.critical(self,"Mensaje de error","Los campos de:\n\t\tnombre del paciente\n\t\tfactor sanguineo\n\t\tgrupo sanguineo\n"
                                                         "\t\tsexo\n\t\tprocedencia\n\t\tresidencia\n\t\tdirecci??n\n\t\tbarrio\n"
                                                         "Son campos obligatorios\n")
        elif (ci_pac and ex_ci_pac==0) or (ci_padre and ex_ci_padre==0) or (ci_madre and ex_ci_madre==0):
            QMessageBox.critical(self,"Mensaje de error","No se olvide elegir una extensi??n para el n??mero de carnet")
        elif (not ci_pac and ex_ci_pac!=0) or (not ci_padre and ex_ci_padre!=0) or (not ci_madre and ex_ci_madre!=0):
            QMessageBox.critical(self,"Mensaje de error","No es posible guardar una extensi??n de carnet sin el n??mero")
        elif not nom_padre and not nom_madre and not ap1_padre and not ap2_padre and not ap1_madre and not ap2_madre:
            QMessageBox.critical(self,"Mensaje de error","Al menos uno de los padres debe ser registrado")
        elif (nom_padre and not ap1_padre and not ap2_padre) or (nom_madre and not ap1_madre and not ap2_madre) or (not ap1_pac and not ap2_pac):
            QMessageBox.critical(self,"Mensaje de error","Al menos uno de los apellidos debe ser llenado")
        elif (not nom_padre and ap1_padre and not ap2_padre) or (not nom_padre and not ap1_padre and ap2_padre) or (not nom_madre and ap1_madre and not ap2_madre) \
                or (not nom_madre and not ap1_madre and ap2_madre):
            QMessageBox.critical(self,"Mensaje de error","No se guardan s??lo apellidos, debe tener un nombre")
        else:
            if not ap1_pac and ap2_pac:
                ap1_pac="sin apellido"
                nom_pac=nom_pac.lower().strip()
                ap2_pac=ap2_pac.lower().strip()
            if not ap2_pac and ap1_pac:
                ap2_pac="sin apellido"
                nom_pac=nom_pac.lower().strip()
                ap1_pac=ap1_pac.lower().strip()
            if nom_pac and ap1_pac and ap2_pac:
                nom_pac = nom_pac.lower().strip()
                ap1_pac = ap1_pac.lower().strip()
                ap2_pac = ap2_pac.lower().strip()
            if nom_padre:
                nom_padre=nom_padre.lower().strip()
                if not ap1_padre and ap2_padre:
                    ap1_padre="sin apellido"
                    ap2_padre=ap2_padre.lower().strip()
                if not ap2_padre and ap1_padre:
                    ap2_padre="sin apellido"
                    ap1_padre=ap1_padre.lower().strip()
                if ap1_padre and ap2_padre:
                    ap1_padre = ap1_padre.lower().strip()
                    ap2_padre = ap2_padre.lower().strip()
            if nom_madre:
                nom_madre=nom_madre.lower().strip()
                if not ap1_madre and ap2_madre:
                    ap1_madre="sin apellido"
                    ap2_madre=ap2_madre.lower().strip()
                if not ap2_madre and ap1_madre:
                    ap2_madre="sin apellido"
                    ap1_madre=ap1_madre.lower().strip()
                if ap1_madre and ap2_madre:
                    ap1_madre = ap1_madre.lower().strip()
                    ap2_madre = ap2_madre.lower().strip()
            if not antecedentes and not alergias:
                r=0
            if not antecedentes and alergias:
                antecedentes="no hay antecedentes"
                alergias=alergias.lower().strip()
                r=1
            if antecedentes and not alergias:
                alergias="no hay alergias"
                antecedentes=antecedentes.lower().strip()
                r=1
            if antecedentes and alergias:
                antecedentes = antecedentes.lower().strip()
                alergias = alergias.lower().strip()
                r=1
            if not peso_pac and not talla_pac:
                peso_pac=0.000
                talla_pac=0.00
            if not peso_pac and talla_pac:
                peso_pac=0.000
            if not talla_pac and peso_pac:
                talla_pac=0.00
            peso_pac=round(float(peso_pac),3)
            talla_pac=round(float(talla_pac),2)
            procedencia = str(procedencia).lower().strip()
            residencia = str(residencia).lower().strip()
            direccion = str(direccion).lower().strip()
            barrio = str(barrio).lower().strip()
            t=1
        if t==1:
            if reg_pac==1:
                tabla = "fecha"
                columnas = "id_fecha,fechayhora,tipo_fecha"
                id_fecha = self.Conseguir_id_tabla(1, "id_fecha", tabla)
                valores = [id_fecha, fecha_pac, 1]
                resp = self.Insertar_bbdd(tabla, columnas, valores)
                if resp==1:
                    #region registro en la tabla historial
                    enviar_datos = 7, str(id_fecha), 1, "fecha"
                    self.Registro_tabla_historial(enviar_datos)
                    #endregion
                    id_persona=""
                    persona = [id_persona, nom_pac, ap1_pac, ap2_pac, id_fecha, sexo_pac]
                    id_persona = self.Creador_id()
                    resp1 = self.Verifica_id_crea_id(1,id_persona)
                    if resp1[0] == 1:
                        id_persona = resp1[1]
                        persona = [id_persona, nom_pac, ap1_pac, ap2_pac, id_fecha, sexo_pac]
                        tabla = "persona"
                        columnas = "id_persona, nombre, apellido1, apellido2, fecha, tipo_sexo"
                        resp2 = self.Insertar_bbdd(tabla, columnas, persona)
                        if resp2==1:
                            # region registro en la tabla historial
                            enviar_datos = 7, str(id_persona), 1, "persona"
                            self.Registro_tabla_historial(enviar_datos)
                            # endregion
                            if ci_pac:
                                enviar=ci_pac,ex_ci_pac,id_persona
                                self.Registrar_carnet(3,enviar)
                            tabla = "dato_general"
                            columnas = "id_dato,peso,talla"
                            id_dato = self.Conseguir_id_tabla(1, "id_dato", tabla)
                            valores = [id_dato, peso_pac,talla_pac]
                            resp4 = self.Insertar_bbdd(tabla, columnas, valores)
                            if resp4==1:
                                # region registro en la tabla historial
                                enviar_datos = 7, str(id_dato), 1, "dato_general"
                                self.Registro_tabla_historial(enviar_datos)
                                # endregion
                                id_paciente="PAC"
                                resp5=self.Verifica_id_crea_id(2,id_paciente)
                                if resp5[0]==1:
                                    id_paciente=resp5[1]
                                    paciente=[id_paciente,id_persona,grupo_pac,factor_pac,procedencia,residencia,direccion,barrio,id_dato]
                                    tabla = "paciente"
                                    columnas = "id_paciente,id_persona, grupo_sanguineo, factor_sanguineo, procedencia, residencia, direccion, barrio, dato_general"
                                    resp6 = self.Insertar_bbdd(tabla, columnas, paciente)
                                    if resp6==1:
                                        # region registro en la tabla historial
                                        enviar_datos = 7, str(id_paciente), 1, "paciente"
                                        self.Registro_tabla_historial(enviar_datos)
                                        # endregion
                                        if r==1:
                                            enviar=antecedentes,alergias,id_paciente
                                            self.Registrar_ante_pac(2,enviar)
                                        if nom_padre:
                                            enviar = nom_padre, ap1_padre, ap2_padre, ci_padre, ex_ci_padre, tel_padre, id_paciente, 1
                                            self.Registrar_Progenitor(3,enviar)
                                        if nom_madre:
                                            enviar = nom_madre, ap1_madre, ap2_madre, ci_madre, ex_ci_madre, tel_madre, id_paciente, 2
                                            self.Registrar_Progenitor(3, enviar)
                                        paciente1 = "{} {} {}".format(self.ui.txt_reg_pac_nom.text(), self.ui.txt_reg_pac_app1.text(),
                                                                     self.ui.txt_reg_pac_app2.text())
                                        codigo = id_paciente
                                        datos = (paciente1, codigo, antecedentes, alergias)
                                        reg_pac = 0
                                        self.ui.Stacked_main.setCurrentIndex(8)
                                        self.Ventana_reg_hist2(datos)
                                    else:
                                        QMessageBox.critical(self,"Mensaje de error","No se pudo guardar los datos de paciente")
                                else:
                                    QMessageBox.critical(self,"Mensaje de error","No se pudo verificar el c??digo de paciente")
                            else:
                                QMessageBox.critical(self,"Mensaje de error","No se pudo ingresar los datos de peso y talla de nacimiento")
                        else:
                            QMessageBox.critical(self,"Mensaje de error","No se pudo ingresar los datos:\n"
                                                                         "nombre, apellidos, fecha de nacimiento del paciente")
                    else:
                        QMessageBox.critical(self,"Mensaje de error","Ocurri?? un error y no se pudo verificar el id del paciente")
                else:
                    QMessageBox.critical(self,"Mensaje de error","No se pudo ingresar la fecha de nacimiento del paciente")
            if reg_pac == 2:
                datos_a_mandar = nom_pac, ap1_pac, ap2_pac, ci_pac, ex_ci_pac, fecha_pac, \
                                 fecha_pac1, sexo_pac, factor_pac, grupo_pac, peso_pac, \
                                 talla_pac, antecedentes, alergias, procedencia, residencia, \
                                 direccion, barrio, nom_padre, ap1_padre, ap2_padre, \
                                 ci_padre, ex_ci_padre, tel_padre, nom_madre, ap1_madre, \
                                 ap2_madre, ci_madre, ex_ci_madre, tel_madre
                self.Verificar5(datos_a_mandar)
    #endregion
    # ****************************************************************************************************************************
    #region *********************     REGISTRO Y ACTUALIZACION DE DATOS
    def Registrar_carnet(self, caso, datos):
        global bbdd_paciente
        if caso==1:
            ci=datos[3]
            ex_ci=datos[4]
            cod_per=bbdd_paciente[14]
        if caso==2 or caso==3:
            ci=datos[0]
            ex_ci=datos[1]
            cod_per=datos[2]
        tabla = "carnet"
        columnas = "id_carnet, numero, extension, persona"
        id_ci = self.Conseguir_id_tabla(1, "id_carnet", tabla)
        valores = [id_ci, str(ci).strip(), ex_ci, cod_per]
        resp4 = self.Insertar_bbdd(tabla, columnas, valores)
        if resp4 == 1:
            # region registro en la tabla historial
            enviar_datos = 7, str(id_ci), 1, "carnet"
            self.Registro_tabla_historial(enviar_datos)
            # endregion
        else:
            if caso==1 or caso==3:
                QMessageBox.critical(self, "Mensaje de error", "No se pudo registrar el carnet\ndel paciente en la bbdd")
            else:
                QMessageBox.critical(self, "Mensaje de error", "No se pudo registrar el carnet\ndel padre o madre en la bbdd")

    def Registrar_ante_pac(self,caso,datos):
        global bbdd_paciente
        if caso==1:
            antecedentes=datos[12]
            alergias =datos[13]
            cod_pac=bbdd_paciente[13]
        if caso==2:
            antecedentes=datos[0]
            alergias=datos[1]
            cod_pac=datos[2]
        tabla = "antecedentes"
        columnas = "id_antecedentes, patologicos, alergias, paciente"
        id_antecedentes = self.Conseguir_id_tabla(1, "id_antecedentes", tabla)
        valores = [id_antecedentes, antecedentes, alergias, cod_pac]
        resp6 = self.Insertar_bbdd(tabla, columnas, valores)
        if resp6 == 1:
            # region registro en la tabla historial
            enviar_datos = 7, str(id_antecedentes), 1, "antecedentes"
            self.Registro_tabla_historial(enviar_datos)
            # endregion
        else:
            QMessageBox.critical(self, "Mensaje de error", "No se pudo guardar la tabla antecedentes")

    def Actualiza_carnet(self,caso,datos):
        global bbdd_carnet_pac
        global bbdd_carnet_padre
        global bbdd_carnet_madre
        if caso==1:
            cod_ci=bbdd_carnet_pac[0]
            ci_bd=bbdd_carnet_pac[1]
            ex_bd=bbdd_carnet_pac[2]
            ci=datos[3]
            ex_ci=datos[4]
        if caso==2:
            cod_ci = bbdd_carnet_padre[2]
            ci_bd = bbdd_carnet_padre[0]
            ex_bd = bbdd_carnet_padre[1]
            ci=datos[0]
            ex_ci=datos[1]
        if caso==3:
            cod_ci = bbdd_carnet_madre[2]
            ex_bd = bbdd_carnet_madre[1]
            ci_bd = bbdd_carnet_madre[0]
            ci=datos[0]
            ex_ci=datos[1]
        if ci != ci_bd or ex_ci != ex_bd:
            tabla = "carnet"
            columnas = "numero", "extension"
            id_tabla = "id_carnet"
            valores = ci, ex_ci, cod_ci
            resp5 = self.Update_bbdd(2, tabla, columnas, id_tabla, valores)
            if resp5 == 1:
                # region registro en la tabla historial
                enviar_datos = 8, str(cod_ci), 2, "carnet"
                self.Registro_tabla_historial(enviar_datos)
                # endregion
            else:
                if caso==1:
                    QMessageBox.critical(self, "Mensaje de error", "No se pudo actualizar el carnet del paciente")
                if caso==2:
                    QMessageBox.critical(self, "Mensaje de error", "No se pudo actualizar el carnet del padre")
                if caso==3:
                    QMessageBox.critical(self, "Mensaje de error", "No se pudo actualizar el carnet de la madre")

    def Actualiza_ante_pac(self,datos):
        global bbdd_antec_pac
        antecedentes = datos[12]
        alergias = datos[13]
        cod_ant_pac = bbdd_antec_pac[0]
        antecedentes_bd = bbdd_antec_pac[1]
        alergias_bd = bbdd_antec_pac[2]
        if antecedentes != antecedentes_bd or alergias != alergias_bd:
            tabla = "antecedentes"
            columnas = "patologicos", "alergias"
            id_tabla = "id_antecedentes"
            valores = antecedentes, alergias, cod_ant_pac
            resp7 = self.Update_bbdd(2, tabla, columnas, id_tabla, valores)
            if resp7 == 1:
                # region registro en la tabla historial
                enviar_datos = 8, str(cod_ant_pac), 2, "antecedentes"
                self.Registro_tabla_historial(enviar_datos)
                # endregion
            else:
                QMessageBox.critical(self, "Mensaje de error", "No se pudo actualizar los antecedentes del paciente")

    def Actualiza_tel(self,datos):
        tel=datos[0]
        cod_fam=datos[1]
        tabla = "telefono"
        columnas = "numero",
        id_tabla = "familiar"
        valores = tel, cod_fam
        resp = self.Update_bbdd(2, tabla, columnas, id_tabla, valores)
        if resp == 1:
            # region registro en la tabla historial
            enviar_datos = 8, str(cod_fam), 2, "telefono"
            self.Registro_tabla_historial(enviar_datos)
            # endregion
        else:
            if datos[2]==1:
                QMessageBox.critical(self, "Mensaje de error", "No se pudo actualizar el tel??fono del padre")
            else:
                QMessageBox.critical(self, "Mensaje de error", "No se pudo actualizar el tel??fono de la madre")

    def Registrar_tel(self,datos):
        tel=datos[0]
        id_familiar=datos[1]
        tabla = "telefono"
        columnas = "id_telefono,numero,familiar"
        id_tel = self.Conseguir_id_tabla(1, "id_telefono", tabla)
        valores = [id_tel, tel, id_familiar]
        resp14 = self.Insertar_bbdd(tabla, columnas, valores)
        if resp14 == 1:
            # region registro en la tabla historial
            enviar_datos = 7, str(id_tel), 1, "telefono"
            self.Registro_tabla_historial(enviar_datos)
            # endregion
        else:
            if datos[2]==1:
                QMessageBox.critical(self, "Mensaje de error", "No se pudo guardar el tel??fono del padre")
            else:
                QMessageBox.critical(self, "Mensaje de error", "No se pudo guardar el tel??fono de la madre")

    def Registrar_Progenitor(self,caso,datos):
        global bbdd_paciente
        global persona
        fecha_actual = datetime.datetime.today()
        if caso==1:
            nom=datos[18]
            ap1=datos[19]
            ap2=datos[20]
            ci=datos[21]
            tel=datos[23]
            cod_pac = bbdd_paciente[13]
            sexo_progenitor=1
        if caso==2:
            nom = datos[24]
            ap1 = datos[25]
            ap2 = datos[26]
            ci = datos[27]
            tel = datos[29]
            cod_pac = bbdd_paciente[13]
            sexo_progenitor = 2
        if caso==3:
            nom = datos[0]
            ap1 = datos[1]
            ap2 = datos[2]
            ci = datos[3]
            tel = datos[5]
            cod_pac = datos[6]
            if datos[7]==1:
                sexo_progenitor = 1
            else:
                sexo_progenitor = 2
        tabla = "fecha"
        columnas = "id_fecha,fechayhora,tipo_fecha"
        id_fecha = self.Conseguir_id_tabla(1, "id_fecha", tabla)
        valores = [id_fecha, fecha_actual, 7]
        resp8 = self.Insertar_bbdd(tabla, columnas, valores)
        if resp8 == 1:
            # region registro en la tabla historial
            enviar_datos = 7, str(id_fecha), 1, "fecha"
            self.Registro_tabla_historial(enviar_datos)
            # endregion
            id_persona = ""
            persona = [id_persona, nom, ap1, ap2, id_fecha, sexo_progenitor]
            id_persona = self.Creador_id()
            resp9 = self.Verifica_id_crea_id(1, id_persona)
            if resp9[0] == 1:
                id_persona = resp9[1]
                persona = [id_persona, nom, ap1, ap2, id_fecha, sexo_progenitor]
                tabla = "persona"
                columnas = "id_persona, nombre, apellido1, apellido2, fecha, tipo_sexo"
                resp10 = self.Insertar_bbdd(tabla, columnas, persona)
                if resp10 == 1:
                    # region registro en la tabla historial
                    enviar_datos = 7, str(id_persona), 1, "persona"
                    self.Registro_tabla_historial(enviar_datos)
                    # endregion
                    if ci:
                        if caso==1:
                            enviar=datos[21],datos[22],id_persona
                        if caso==2:
                            enviar=datos[27],datos[28],id_persona
                        if caso==3:
                            enviar=datos[3],datos[4],id_persona
                        self.Registrar_carnet(2,enviar)
                    id_familiar = "FAM"
                    resp12 = self.Verifica_id_crea_id(3, id_familiar)
                    if resp12[0] == 1:
                        id_familiar = resp12[1]
                        familiar = [id_familiar, id_persona, sexo_progenitor, cod_pac]
                        tabla = "familiar"
                        columnas = "id_familiar, id_persona, tipo_familiar, paciente"
                        resp13 = self.Insertar_bbdd(tabla, columnas, familiar)
                        if resp13 == 1:
                            # region registro en la tabla historial
                            enviar_datos = 7, str(id_familiar), 1, "familiar"
                            self.Registro_tabla_historial(enviar_datos)
                            # endregion
                            if tel:
                                if caso==1:
                                    enviar=datos[23],id_familiar,1
                                if caso==2:
                                    enviar=datos[29],id_familiar,2
                                if caso==3:
                                    enviar=datos[5],id_familiar,sexo_progenitor
                                self.Registrar_tel(enviar)
                        else:
                            QMessageBox.critical(self, "Mensaje de error", "No se pudo registrar al familiar")
                    else:
                        QMessageBox.critical(self, "Mensaje de error", "No se pudo encontrar el id de familiar")
                else:
                    if sexo_progenitor==1:
                        QMessageBox.critical(self, "Mensaje de error", "No se pudo guardar los datos personales del padre")
                    if sexo_progenitor==2:
                        QMessageBox.critical(self, "Mensaje de error", "No se pudo guardar los datos personales de la madre")
            else:
                if sexo_progenitor==1:
                    QMessageBox.critical(self, "Mensaje de error", "No se encontr?? un id para el padre")
                if sexo_progenitor==2:
                    QMessageBox.critical(self, "Mensaje de error", "No se encontr?? un id para la madre")
        else:
            if sexo_progenitor==1:
                QMessageBox.critical(self, "Mensaje de error", "No se pudo ingresar la fecha del padre")
            if sexo_progenitor==2:
                QMessageBox.critical(self, "Mensaje de error", "No se pudo ingresar la fecha de la madre")

    def Verifica_ci_tel_Progenitor(self,datos):
        global bbdd_carnet_padre
        global bbdd_carnet_madre
        global bbdd_tel1
        global bbdd_tel2
        ci=datos[0]
        tel=datos[2]
        if datos[5]==1:
            if not bbdd_carnet_padre:
                e = 0
            else:
                e = 1
            if not bbdd_tel1:
                f=0
            else:
                tel1=bbdd_tel1
                f=1
        else:
            if not bbdd_carnet_madre:
                e = 0
            else:
                e = 1
            if not bbdd_tel2:
                f=0
            else:
                tel1=bbdd_tel2
                f=1
        if ci:
            if e == 0:
                enviar=datos[0],datos[1],datos[4]
                self.Registrar_carnet(2,enviar)
            else:
                enviar=datos[0],datos[1]
                if datos[5]==1:
                    self.Actualiza_carnet(2,enviar)
                else:
                    self.Actualiza_carnet(3, enviar)
        if tel:
            if datos[5] == 1:
                enviar = datos[2], datos[3], 1
            else:
                enviar = datos[2], datos[3], 2
            if f==0:
                self.Registrar_tel(enviar)
            else:
                if tel != tel1:
                    self.Actualiza_tel(enviar)

    def Verificar_Progenitor(self,caso,datos):
        global bbdd_padre
        global bbdd_madre
        if caso==1:
            nom=datos[18]
            ap1=datos[19]
            ap2=datos[20]
            nom_bd = bbdd_padre[1]
            ap1_bd = bbdd_padre[2]
            ap2_bd = bbdd_padre[3]
            cod_per_fam = bbdd_padre[4]
            cod_fam = bbdd_padre[0]
            enviar = datos[21], datos[22], datos[23], cod_fam, cod_per_fam,1
        if caso==2:
            nom=datos[24]
            ap1=datos[25]
            ap2=datos[26]
            nom_bd = bbdd_madre[1]
            ap1_bd = bbdd_madre[2]
            ap2_bd = bbdd_madre[3]
            cod_per_fam = bbdd_madre[4]
            cod_fam = bbdd_madre[0]
            enviar = datos[27], datos[28], datos[29], cod_fam, cod_per_fam,2
        if nom != nom_bd or ap1 != ap1_bd or ap2 != ap2_bd:
            tabla = "persona"
            columnas = "nombre", "apellido1", "apellido2"
            id_tabla = "id_persona"
            valores = nom, ap1, ap2, cod_per_fam
            resp = self.Update_bbdd(2, tabla, columnas, id_tabla, valores)
            if resp == 1:
                # region registro en la tabla historial
                enviar_datos = 8, str(cod_per_fam), 2, "persona"
                self.Registro_tabla_historial(enviar_datos)
                # endregion
                self.Verifica_ci_tel_Progenitor(enviar)
        else:
            self.Verifica_ci_tel_Progenitor(enviar)
    #endregion
    #region ******************* CONTIENE TODAS LAS VERIFICACIONES DE PACIENTE
    def Verificar1(self,datos):
        global bbdd_paciente
        global bbdd_carnet_pac
        global bbdd_antec_pac
        global bbdd_padre
        global bbdd_madre
        global bbdd_carnet_padre
        global bbdd_carnet_madre
        global bbdd_tel1
        global bbdd_tel2
        global reg_pac
        ci_pac=datos[3]
        nom_padre=datos[18]
        nom_madre=datos[24]
        if not bbdd_carnet_pac:
            a = 0
        else:
            a = 1
        if not datos[12] and not datos[13]:
            r=0
        else:
            r=1
        if not bbdd_antec_pac:
            b = 0
        else:
            b = 1
        if not bbdd_padre:
            c = 0
        else:
            c = 1
        if not bbdd_madre:
            d = 0
        else:
            d = 1
        if ci_pac:
            if a == 0:
                self.Registrar_carnet(1,datos)
            else:
                self.Actualiza_carnet(1,datos)
        if r == 1:
            if b == 0:
                self.Registrar_ante_pac(1,datos)
            else:
                self.Actualiza_ante_pac(datos)
        if nom_padre:
            if c == 0:
                self.Registrar_Progenitor(1,datos)
            else:
                self.Verificar_Progenitor(1,datos)
        if nom_madre:
            if d == 0:
                self.Registrar_Progenitor(2,datos)
            else:
                self.Verificar_Progenitor(2,datos)
        bbdd_paciente = []
        bbdd_carnet_pac = []
        bbdd_antec_pac = []
        bbdd_padre = []
        bbdd_madre = []
        bbdd_carnet_padre = []
        bbdd_carnet_madre = []
        bbdd_tel1 = ""
        bbdd_tel2 = ""
        QMessageBox.information(self, "Guardado", "Se ha modificado con ??xito los datos mencionados")
        self.ui.Stacked_main.setCurrentIndex(5)
        reg_pac = 0

    def Verificar2(self,datos):
        global bbdd_paciente
        fecha_pac1=datos[6]
        fecha_pac_bd = bbdd_paciente[3]
        fecha_pac_bd = fecha_pac_bd.strftime('%Y-%m-%d')
        cod_fecha_pac = bbdd_paciente[16]
        if fecha_pac1 != fecha_pac_bd:
            tabla = "fecha"
            columnas = "fechayhora",
            id_tabla = "id_fecha"
            valores = fecha_pac1, cod_fecha_pac
            resp3 = self.Update_bbdd(2, tabla, columnas, id_tabla, valores)
            if resp3 == 1:
                # region registro en la tabla historial
                enviar_datos = 8, str(cod_fecha_pac), 2, "fecha"
                self.Registro_tabla_historial(enviar_datos)
                # endregion
            else:
                QMessageBox.critical(self, "Mensaje de error", "No se pudo actualizar su fecha de nacimiento")
            self.Verificar1(datos)
        else:
            self.Verificar1(datos)

    def Verificar3(self,datos):
        global bbdd_paciente
        peso_pac=datos[10]
        talla_pac=datos[11]
        peso_pac_bd = float(bbdd_paciente[11])
        talla_pac_bd = float(bbdd_paciente[12])
        cod_dat_pac = bbdd_paciente[15]
        if peso_pac != peso_pac_bd or talla_pac != talla_pac_bd:
            tabla = "dato_general"
            columnas = "peso", "talla"
            id_tabla = "id_dato"
            valores = peso_pac, talla_pac, cod_dat_pac
            resp2 = self.Update_bbdd(2, tabla, columnas, id_tabla, valores)
            if resp2 == 1:
                # region registro en la tabla historial
                enviar_datos = 8, str(cod_dat_pac), 2, "dato_general"
                self.Registro_tabla_historial(enviar_datos)
                # endregion
            else:
                QMessageBox.critical(self, "Mensaje de error", "No se pudo actualizar los cambios\n "
                                                               "en el peso y la talla del paciente")
            self.Verificar2(datos)
        else:
            self.Verificar2(datos)

    def Verificar4(self,datos):
        global bbdd_paciente
        grupo_pac=datos[9]
        factor_pac=datos[8]
        procedencia=datos[14]
        residencia=datos[15]
        direccion=datos[16]
        barrio=datos[17]
        grupo_pac_bd = bbdd_paciente[5]
        factor_pac_bd = bbdd_paciente[6]
        procedencia_bd = bbdd_paciente[7]
        residencia_bd = bbdd_paciente[8]
        direccion_bd = bbdd_paciente[9]
        barrio_bd = bbdd_paciente[10]
        cod_pac = bbdd_paciente[13]
        if grupo_pac != grupo_pac_bd or factor_pac != factor_pac_bd or procedencia != procedencia_bd or residencia != residencia_bd or direccion != direccion_bd \
                or barrio != barrio_bd:
            tabla = "paciente"
            columnas = "grupo_sanguineo", "factor_sanguineo", "procedencia", "residencia", "direccion", "barrio"
            id_tabla = "id_paciente"
            valores = grupo_pac, factor_pac, procedencia, residencia, direccion, barrio, cod_pac
            resp1 = self.Update_bbdd(2, tabla, columnas, id_tabla, valores)
            if resp1 == 1:
                # region registro en la tabla historial
                enviar_datos = 8, str(cod_pac), 2, "paciente"
                self.Registro_tabla_historial(enviar_datos)
                # endregion
            else:
                QMessageBox.critical(self, "Mensaje de error","No se pudo actualizar:\n"
                                                              "\t\tgrupo sanguineo\n"
                                                              "\t\tfactor sanguineo\n"
                                                              "\t\tprocedencia\n"
                                                              "\t\tresidencia\n"
                                                              "\t\tdireccion\n"
                                                              "\t\tbarrio\n")
            self.Verificar3(datos)
        else:
            self.Verificar3(datos)

    def Verificar5(self, datos):
        global bbdd_paciente
        nom_pac_bd = bbdd_paciente[0]
        ap1_pac_bd = bbdd_paciente[1]
        ap2_pac_bd = bbdd_paciente[2]
        sexo_pac_bd = bbdd_paciente[4]
        nom_pac=datos[0]
        ap1_pac=datos[1]
        ap2_pac=datos[2]
        sexo_pac=datos[7]
        cod_per_pac=bbdd_paciente[14]
        if nom_pac != nom_pac_bd or ap1_pac != ap1_pac_bd or ap2_pac != ap2_pac_bd or sexo_pac != sexo_pac_bd:
            tabla = "persona"
            columnas = "nombre", "apellido1", "apellido2", "tipo_sexo"
            id_tabla = "id_persona"
            valores = nom_pac, ap1_pac, ap2_pac, sexo_pac, cod_per_pac
            resp = self.Update_bbdd(2, tabla, columnas, id_tabla, valores)
            if resp == 1:
                # region registro en la tabla historial
                enviar_datos = 8, str(cod_per_pac), 2, "persona"
                self.Registro_tabla_historial(enviar_datos)
                # endregion
            else:
                QMessageBox.critical(self, "Mensaje de error", "No se pudo actualizar los datos:\n"
                                                               "nombre, apellidos y sexo del paciente")
            self.Verificar4(datos)
        else:
            self.Verificar4(datos)
    #endregion
    #region Guardar el formulario de la consulta en la bbdd
    def Guardar_consulta(self):
        global matricula_user
        id_paciente=str(self.ui.lbl_hist_pac_codigo.text())
        if self.ui.tab_fecha_hora.currentIndex() == 0:
            fecha = datetime.datetime.today()
        if self.ui.tab_fecha_hora.currentIndex() == 1:
            fecha = self.ui.spin_hist_pac_date.dateTime()
            fecha=fecha.toPyDateTime()
            fecha=fecha.strftime('%Y-%m-%d %H:%M')
            fecha=datetime.datetime.strptime(fecha,'%Y-%m-%d %H:%M')
        combo=self.ui.cb_hist_pac_consul.currentIndex()
        peso=self.ui.txt_hist_pac_pes.text()
        tall=self.ui.txt_hist_pac_tall.text()
        frec_card=self.ui.txt_hist_pac_fc.text()
        frec_resp=self.ui.txt_hist_pac_fr.text()
        temp=self.ui.txt_hist_pac_temp.text()
        sat=self.ui.txt_hist_pac_SO.text()
        presion1=self.ui.txt_hist_pac_pa1.text()
        presion2=self.ui.txt_hist_pac_pa2.text()
        per_cef=self.ui.txt_hist_pac_percef.text()
        motivo=self.ui.pt_hist_pac_con.toPlainText()
        examen = self.ui.pt_hist_pac_ex.toPlainText()
        diagnos = self.ui.pt_hist_pac_diag.toPlainText()
        trat = self.ui.pt_hist_pac_trat.toPlainText()
        obs = self.ui.pt_hist_pac_obs.toPlainText()
        prox=self.ui.spin_hist_pac_dat.date()
        if combo==0:
            QMessageBox.critical(self,"Mensaje de error","Debe registrar por lo menos el tipo de consulta")
        else:
            prox = prox.toPyDate()
            prox1 = str(prox)
            if prox1 == '2000-01-01':
                prox = fecha + datetime.timedelta(days=4)
            else:
                prox = prox.strftime('%Y-%m-%d')
                prox = datetime.datetime.strptime(prox, '%Y-%m-%d')
            if combo==1:
                id_consulta="CON"
                tipo=2
            if combo==2:
                id_consulta="REC"
                tipo=3
            if combo==3:
                id_consulta="EME"
                tipo=4
            if not frec_card:
                frec_card=0
            if not frec_resp:
                frec_resp=0
            if not temp:
                temp=0.0
            if not sat:
                sat=0
            if not presion1 and not presion2:
                presion="0 - 0"
            if not presion1 and presion2:
                presion="0 - "+str(presion2)
            if not presion2 and presion1:
                presion=str(presion1)+" - 0"
            if presion1 and presion2:
                presion=str(presion1)+" - "+str(presion2)
            if not per_cef:
                per_cef=0.0
            if not motivo:
                motivo="no se registr?? el motivo"
            if not examen:
                examen="no se realiz?? el ex??men f??sico"
            if not diagnos:
                diagnos="no se tiene un diagn??stico para registrar"
            if not trat:
                trat="no se tiene un tratamiento para registrar"
            if not obs:
                obs="no se tiene ningua observaci??n para registrar"
            if not peso and not tall:
                peso=0.0
                tall=0.0
            if not peso and tall:
                peso=0.0
            if not tall and peso:
                tall=0.0
            peso=float(peso)
            tall=float(tall)
            tabla = "fecha"
            columnas = "id_fecha,fechayhora,tipo_fecha"
            id_fecha = self.Conseguir_id_tabla(1, "id_fecha", tabla)
            valores = [id_fecha, fecha, tipo]
            resp = self.Insertar_bbdd(tabla, columnas, valores)
            if resp == 1:
                # region registro en la tabla historial
                enviar_datos = 7, str(id_fecha), 1, "fecha"
                self.Registro_tabla_historial(enviar_datos)
                # endregion
                tabla = "dato_general"
                columnas = "id_dato,peso,talla"
                id_dato = self.Conseguir_id_tabla(1, "id_dato", tabla)
                valores = [id_dato, peso, tall]
                resp2 = self.Insertar_bbdd(tabla, columnas, valores)
                if resp2 == 1:
                    # region registro en la tabla historial
                    enviar_datos = 7, str(id_dato), 1, "dato_general"
                    self.Registro_tabla_historial(enviar_datos)
                    # endregion
                    resp3 = self.Verifica_id_crea_id(4, id_consulta)
                    if resp3[0] == 1:
                        id_consulta = resp3[1]
                        consulta = [id_consulta, id_paciente, matricula_user, id_fecha,frec_card,frec_resp,temp,sat,presion,per_cef,motivo,examen,diagnos,trat,obs,prox,id_dato]
                        tabla = "consulta"
                        columnas = "id_consulta,codigo_paciente,id_medico,fecha,frecuencia_cardiaca,frecuencia_respiratoria,temperatura,saturacion,presion,perimetro_cefalico," \
                                   "motivo,examen,diagnostico,tratamiento,observaciones,proxima_revision,dato_general"
                        resp4 = self.Insertar_bbdd(tabla, columnas, consulta)
                        if resp4==1:
                            # region registro en la tabla historial
                            enviar_datos = 7, str(id_consulta), 1, "consulta"
                            self.Registro_tabla_historial(enviar_datos)
                            # endregion
                            QMessageBox.information(self,"Mensaje de ??xito","La consulta fue guardada con ??xito en la Base de datos")
                            self.ui.Stacked_main.setCurrentIndex(5)
                        else:
                            QMessageBox.critical(self,"Mensaje de error","No se pudo guardar los datos de consulta del paciente")
                    else:
                        QMessageBox.critical(self,"Mensaje de error","No se pudo verificar el c??digo de la consulta")
                else:
                    QMessageBox.critical(self,"Mensaje de error","No se pudo guardar los datos generales del paciente")
            else:
                QMessageBox.critical(self,"Mensaje de error","No se pudo guardar la fecha de consulta")
    #endregion
    # ventana de informacion de historiales
    def Ventana_info_pac(self):
        global tema
        self.Poner_tema(tema)
        self.Limpia_info_busc()
        self.ui.Stacked_main.setCurrentIndex(9)
        self.ui.txt_info_pac_nom.setFocus()
        self.les = [self.ui.txt_info_pac_nom, self.ui.txt_info_pac_app1, self.ui.txt_info_pac_app2,
                    self.ui.btn_info_pac_buscar]
    def Salir_admin(self):
        self.Limpia_admin2()
        self.ui.Stacked_admin.setCurrentIndex(0)
    # --------------------------------------------------------------------------------------------------
    # --------------------------------------------------------------------------------------------------
    #region Evento ventana de logeo para la entrada
    def Verifica(self):
        usuario = self.ui.txt_log_user.text()
        contra = self.ui.txt_log_pass.text()
        global reg_us
        if not usuario or not contra:
            QMessageBox.critical(self, "Mensaje de advertencia", "Debe llenar todos los campos")
        else:
            resp=self.Logeo_postgres(usuario,contra)
            if resp==0:
                QMessageBox.critical(self, "Mensaje de advertencia", "El Usuario y/o contrase??a no son correctos\n"
                                                                     "o la cuenta ha sido suspendida\nPor favor verifique sus datos")
            else:
                #comprobar si es usuario y a donde va
                columna="grupo"
                tabla="grupo_sanguineo"
                valor="id_grupo",1
                resp1=self.Select_bbdd(columna,tabla,valor)
                if resp1[0]==1:
                    self.Entrar_con_usuario(1)
                else:
                    columna = "cuenta_user"
                    tabla = "usuario"
                    valor = "cuenta_user", usuario
                    resp2=self.Select_bbdd(columna,tabla,valor)
                    if resp2[0]==0:
                        reg_us = 1
                        self.Ventana_registro()
                    else:
                        columna = "validaciones"
                        tabla = "medico"
                        valor = "usuario", usuario
                        resp3=self.Select_bbdd(columna,tabla,valor)
                        columna = "validacion"
                        tabla = "validaciones"
                        valor = "id_validaciones", resp3[1]
                        resultado=self.Select_bbdd(columna,tabla,valor)
                        if resultado[1]==False:
                            codigo=QInputDialog.getText(self,"Ventana para introducir su c??digo","Ingrese el c??digo enviado a su correo")
                            columna = "codigo"
                            tabla = "validaciones"
                            valor = "id_validaciones", resp3[1]
                            resp4=self.Select_bbdd(columna,tabla,valor)
                            if resp4[0]==1:
                                codigo1=resp4[1]
                                if codigo[0]!=codigo1:
                                    QMessageBox.critical(self,"Mensaje de error","El c??digo ingresado no corresponde al enviado al correo, verifique nuevamente")
                                else:
                                    tabla="validaciones"
                                    columnas="validacion",
                                    id_tabla="id_validaciones"
                                    valores='True',resp3[1]
                                    resp5=self.Update_bbdd(2,tabla,columnas,id_tabla,valores)
                                    if resp5==1:
                                        self.Entrar_con_usuario(2)
                                    else:
                                        QMessageBox.critical(self,"Mensaje de error","Algo salio mal, intente nuevamente")
                        else:
                            self.Entrar_con_usuario(2)
    #endregion
    # ------------------------------------------------------------------------------------------
    #region Dirige al m??dulo de entrada medico o admi
    def Entrar_con_usuario(self, num):
        global tema
        global usuario
        global matricula_user
        columna = "tema"
        tabla = "usuario"
        valor = "cuenta_user", usuario
        resp=self.Select_bbdd(columna,tabla,valor)
        if resp[0]==1:
            tema=resp[1]
            self.Poner_tema(tema)
        else:
            tema=0
            self.Poner_tema(tema)
        self.ui.btn_config.setVisible(True)
        self.ui.btn_salir.setVisible(True)
        if num == 1:
            #se entra al modulo de administracion
            self.ui.Stacked_tareas.setCurrentIndex(1)
            self.ui.Stacked_main.setCurrentIndex(4)
        else:
            #se entra al modulo de usuario
            valor = "usuario", usuario
            resultado = self.Select_bbdd("matricula", "medico", valor)
            if resultado[0] == 1:
                matricula_user = resultado[1]
                # region registro en la tabla historial
                enviar_datos = 5, "Inicio de sesi??n", 4, "Entra al sistema"
                self.Registro_tabla_historial(enviar_datos)
                # endregion
                self.ui.Stacked_tareas.setCurrentIndex(2)
                self.ui.Stacked_main.setCurrentIndex(5)
    #endregion
    #region Verifica campos vacios y guarda en la bbdd el reg de un usuario
    def Verifica_new_user(self):
        global usuario
        global reg_us
        global carnet
        global persona
        global usuario1
        global medico
        fecha2 = datetime.datetime.today()
        #tabla carnet debe ir llena, todos los campos son obligatorios
        carnet=[self.ui.txt_reg_user_CI.text(),self.ui.cb_reg_user_CI.currentIndex()]
        id_persona=""
        id_ci=0
        id_fecha=0
        #Tabla persona
        persona= [id_persona, self.ui.txt_reg_nom_user.text(), self.ui.txt_reg_apell1_user.text(), self.ui.txt_reg_apell2_user.text(), id_fecha, self.ui.comboBox.currentIndex()]
        sal=""
        id_validaciones=0
        contra1=self.ui.txt_reg_pass1.text()
        usuario1=[usuario,self.ui.txt_reg_pass.text(),sal,0]
        medico=[self.ui.txt_reg_user_mat.text(),id_persona,usuario,self.ui.txt_reg_correo_user.text(),id_validaciones]
        r=0
        if not carnet[0] or carnet[1]==0 or not medico[0] or not persona[1] or not usuario1[1] or not contra1 or not medico[3] or persona[5]==0:
            QMessageBox.critical(self,"Mensaje de error","Debe llenar todos los campos\n menos 1 apellido si no lo hubiera\n"
                                                         "todos los dem??s campos son obligatorios")
        elif usuario1[1] != contra1:
            QMessageBox.critical(self, "Mensaje de error", "Las contrase??as deben ser iguales")
        elif self.Verifica_email(medico[3]) == 1:
            QMessageBox.critical(self, "Mensaje de advertencia", "Introduzca una direcci??n de correo v??lida\n"
                                                                 "Las direcciones v??lidas son:\n\t\t\tGmail\n\t\t\tHotmail\n\t\t\tOutlook\n\t\t\tYahoo")
        elif not persona[2] and not persona[3]:
            QMessageBox.critical(self,"Mensaje de error","Al menos un campo de apellido debe ser llenado")
        else:
            if not persona[2] and persona[3]:
                persona[2]="Sin apellido"
            if not persona[3] and persona[2]:
                persona[3]="Sin apellido"
            r=1
        if r==1:
            if reg_us==1:
                medico[0]=str(self.ui.txt_reg_user_mat.text()).strip()
                resp9=self.Verificar_matricula()
                if resp9==1:
                    codigo = Clases.Metodos.Generador_clave()
                    resp10=self.Probar_conexion()
                    if resp10==1:
                        Clases.Metodos.Enviar_codigo(codigo, medico[3])
                        tabla="fecha"
                        columnas="id_fecha,fechayhora,tipo_fecha"
                        id_fecha=self.Conseguir_id_tabla(1,"id_fecha",tabla)
                        valores = [id_fecha,fecha2, 7]
                        resp=self.Insertar_bbdd(tabla,columnas,valores)
                        if resp==1:
                            persona[1] = str(persona[1]).lower().strip()
                            persona[2] = str(persona[2]).lower().strip()
                            persona[3] = str(persona[3]).lower().strip()
                            id_persona=self.Creador_id()
                            resp1=self.Verifica_id_crea_id(1,id_persona)
                            if resp1[0]==1:
                                id_persona=resp1[1]
                                persona[0]=id_persona
                                persona[4] = id_fecha
                                tabla = "persona"
                                columnas = "id_persona, nombre, apellido1, apellido2, fecha, tipo_sexo"
                                resp5 = self.Insertar_bbdd(tabla, columnas, persona)
                                if resp5==1:
                                    tabla="validaciones"
                                    columnas="id_validaciones,codigo,validacion,habilitacion"
                                    id_validaciones=self.Conseguir_id_tabla(1,"id_validaciones",tabla)
                                    valores=[id_validaciones,codigo,False,True]
                                    resp3=self.Insertar_bbdd(tabla,columnas,valores)
                                    if resp3==1:
                                        medico[0]=str(medico[0])
                                        medico[1]=id_persona
                                        medico[2]=usuario
                                        medico[3]=str(medico[3]).lower().strip()
                                        medico[4]=id_validaciones
                                        encriptado=Clases.Metodos.Encriptador2(2,usuario1[1])
                                        usuario1[1]=encriptado[1]
                                        usuario1[2]=encriptado[0]
                                        tabla="usuario"
                                        columnas="cuenta_user,pass,sal,tema"
                                        resp4=self.Insertar_bbdd(tabla,columnas,usuario1)
                                        if resp4==1:
                                            tabla = "carnet"
                                            columnas = "id_carnet,numero,extension,persona"
                                            id_ci = self.Conseguir_id_tabla(1, "id_carnet", tabla)
                                            valores = [id_ci, str(carnet[0]).strip(), carnet[1], id_persona]
                                            resp2 = self.Insertar_bbdd(tabla, columnas, valores)
                                            if resp2==1:
                                                tabla="medico"
                                                columnas="matricula, id_persona, usuario, correo, validaciones"
                                                resp6=self.Insertar_bbdd(tabla,columnas,medico)
                                                if resp6==1:
                                                    resp7=self.Reset_pass(2,usuario,contra1)
                                                    if resp7==1:
                                                        QMessageBox.information(self,"Mensaje de ??xito","Se ha registrado con ??xito al sistema.\n"
                                                                                                "Revise su correo electr??nico para revisar la clave que se le envi??")
                                                        self.Iniciar_cero()
                                                    else:
                                                        QMessageBox.critical(self,"Mensaje de error","Ha ocurrido un error y no se pudo guardar su nueva contrase??a")
                                                else:
                                                    QMessageBox.critical(self,"Mensaje de error","Ha ocurrido un error y no se pudo guardar los datos de m??dico")
                                            else:
                                                QMessageBox.critical(self, "Mensaje de error", "Ha ocurrido un error y no se pudo guardar el carnet de identidad")
                                        else:
                                            QMessageBox.critical(self,"Mensaje de error","Ha ocurrido un error y no se pudo guardar los datos de usuario")
                                    else:
                                        QMessageBox.critical(self,"Mensaje de error","Ha ocurrido un error y no se pudo guardar los datos de validaci??n")
                                else:
                                    QMessageBox.critical(self, "Mensaje de error", "Ha ocurrido un error y no se pudo guardar los datos personales")
                            else:
                                QMessageBox.critical(self,"Mensaje de error","Ha ocurrido un error y no se pudo verificar el ID de la persona")
                        else:
                            QMessageBox.critical(self,"Mensaje de error","Ha ocurrido un error y no se pudo guardar la fecha")
                    else:
                        QMessageBox.critical(self, "Mensaje de error", "No se pudo conectar a internet o ocurri?? alg??n error, verifique su conexi??n a internet")
                else:
                    QMessageBox.critical(self,"Mensaje de error","La matricula de m??dico ya se encuentra registrada\n"
                                                                 "Verifique con el administrador para obtener una nueva contrase??a")
            if reg_us==2:
                self.Verificar_user_5(carnet)
                carnet = []
                usuario1 = []
    #endregion
    #region Modificaci??n de datos de usuario
    def Verificar_user_1(self):
        global persona
        global medico
        global reg_us
        persona = []
        medico = []
        self.Limpia_reg_user()
        reg_us = 0
        self.ui.Stacked_main.setCurrentIndex(5)

    def Verificar_user_2(self):
        global usuario
        global resultado_bbdd_usuario
        sal = resultado_bbdd_usuario[4]
        password = resultado_bbdd_usuario[5]
        texto = sal, password
        password_desencriptada = Clases.Metodos.Desencriptador(2, texto)
        contra1 = self.ui.txt_reg_pass1.text()
        if contra1 != password_desencriptada:
            encriptado = Clases.Metodos.Encriptador2(2, contra1)
            tabla = "usuario"
            columnas = "pass", "sal"
            id_tabla = "cuenta_user"
            valores = encriptado[1], encriptado[0], usuario
            resp = self.Update_bbdd(2, tabla, columnas, id_tabla, valores)
            if resp == 1:
                # region registro en la tabla historial
                enviar_datos = 8, str(usuario), 2, "usuario"
                self.Registro_tabla_historial(enviar_datos)
                # endregion
                resp1 = self.Reset_pass(2, usuario, contra1)
                if resp1 == 1:
                    QMessageBox.information(self, "Se ha cambiado con exito", "La contrase??a ha sido cambiada")
                    QMessageBox.information(self, "Cambio de pantalla","Se ha cambiado la contrase??a por favor vuelva a iniciar sesi??n")
                    self.Iniciar_cero()
        else:
            self.Verificar_user_1()

    def Verificar_user_3(self):
        global resultado_bbdd_usuario
        global medico
        correo = resultado_bbdd_usuario[6]
        medico[3] = str(medico[3]).lower().strip()
        codigo = Clases.Metodos.Generador_clave()
        if medico[3] != correo:
            resp10 = self.Probar_conexion()
            if resp10 == 1:
                Clases.Metodos.Enviar_codigo(codigo, medico[3])
                tabla = "medico"
                columnas = "correo",
                id_tabla = "matricula"
                valores = medico[3], resultado_bbdd_usuario[0]
                resp2 = self.Update_bbdd(2, tabla, columnas, id_tabla, valores)
                if resp2 == 1:
                    # region registro en la tabla historial
                    enviar_datos = 8, str(resultado_bbdd_usuario[0]), 2, "medico"
                    self.Registro_tabla_historial(enviar_datos)
                    # endregion
                    tabla = "validaciones"
                    columnas = "codigo", "validacion"
                    id_tabla = "id_validaciones"
                    valores = codigo, 'False', resultado_bbdd_usuario[3]
                    resp3 = self.Update_bbdd(2, tabla, columnas, id_tabla, valores)
                    if resp3 == 1:
                        # region registro en la tabla historial
                        enviar_datos = 8, str(resultado_bbdd_usuario[3]), 2, "validaciones"
                        self.Registro_tabla_historial(enviar_datos)
                        # endregion
                        QMessageBox.information(self, "Mensaje de ??xito", "Se ha actualizado con ??xito el correo\n"
                                                                          "Se le ha enviado un nuevo c??digo de confirmaci??n\n"
                                                                          "a su nueva direcci??n de correo electr??nico")
            else:
                QMessageBox.critical(self, "Mensaje de error","No hay conexi??n a internet, verifique su conexi??n antes de continuar")
            self.Verificar_user_2()
        else:
            self.Verificar_user_2()

    def Verificar_user_4(self):
        global persona
        global resultado_bbdd_usuario
        nombre = resultado_bbdd_usuario[9]
        apellido_p = resultado_bbdd_usuario[10]
        apellido_m = resultado_bbdd_usuario[11]
        sexo = resultado_bbdd_usuario[12]
        persona[1] = str(persona[1]).lower().strip()
        persona[2] = str(persona[2]).lower().strip()
        persona[3] = str(persona[3]).lower().strip()
        if nombre != persona[1] or apellido_p != persona[2] or apellido_m != persona[3] or sexo != persona[5]:
            tabla = "persona"
            columnas = "nombre", "apellido1", "apellido2", "tipo_sexo"
            id_tabla = "id_persona"
            valores = persona[1], persona[2], persona[3], persona[5], resultado_bbdd_usuario[1]
            resp1 = self.Update_bbdd(2, tabla, columnas, id_tabla, valores)
            if resp1 == 1:
                # region registro en la tabla historial
                enviar_datos = 8, str(resultado_bbdd_usuario[1]), 2, "persona"
                self.Registro_tabla_historial(enviar_datos)
                # endregion
            else:
                QMessageBox.critical(self, "Mensaje de error", "No se pudo actualizar los datos personales")
            self.Verificar_user_3()
        else:
            self.Verificar_user_3()

    def Verificar_user_5(self,carnet):
        global resultado_bbdd_usuario
        numero = resultado_bbdd_usuario[7]
        extension = resultado_bbdd_usuario[8]
        carnet[0] = str(carnet[0]).strip()
        if carnet[0] != numero or carnet[1] != extension:
            tabla = "carnet"
            columnas = "numero", "extension"
            id_tabla = "id_carnet"
            valores = carnet[0], carnet[1], resultado_bbdd_usuario[2]
            resp = self.Update_bbdd(2, tabla, columnas, id_tabla, valores)
            if resp == 1:
                # region registro en la tabla historial
                enviar_datos = 8, str(resultado_bbdd_usuario[2]), 2, "carnet"
                self.Registro_tabla_historial(enviar_datos)
                # endregion
            else:
                QMessageBox.critical(self, "Mensaje de error", "No se pudo actualizar el carnet")
            self.Verificar_user_4()
        else:
            self.Verificar_user_4()
    #endregion
    #region como su nombre indica la siguiente funcion pretende comprobar direcion de mail v??lida
    def Verifica_email(self,mail):
        #formato_email1 = re.compile(r"[a-zA-Z0-9!#$%&'*\/=?^_`{|}~+-]([\.]?[a-zA-Z0-9!#$%&'*\/=?^_`{|}~+-])+@[a-zA-Z0-9]([^@&%$/()=???!.,:;]|\d)+[a-zA-Z0-9][\.][a-zA-Z]{2,4}([\.][a-zA-Z]{2})?")
        formato_email1 = re.compile(r"^[A-Za-z0-9\.\+]+@gmail.com")
        formato_email2 = re.compile(r"^[(A-Za-z0-9\_\-\)]+@hotmail.com")
        formato_email3 = re.compile(r"^[(A-Za-z0-9\_\-\)]+@outlook.com")
        formato_email4 = re.compile(r"^[(A-Za-z0-9\_\-\.)]+@yahoo.com")
        formato_email5 = re.compile(r"^[(A-Za-z0-9\_\-\.)]+@udabol.edu.bo")
        # formato_email = re.compile(r"^[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$")
        r = 0
        if formato_email1.match(mail) or formato_email2.match(mail) or formato_email3.match(mail) or formato_email4.match(mail) or formato_email5.match(mail):
            r = 0
        else:
            r = 1
        return r
    #endregion
    #region metodo para verificar espacios en blanco para recuperar la contrase??a
    def Verifica_recu(self):
        global usuario
        global codigo
        usuario = self.ui.txt_recu_user.text()
        mail = self.ui.txt_recu_correo.text()
        if not usuario or not mail:
            QMessageBox.critical(self, "Campos vacios", "Debe llenar todos los espacios\n"
                                                        "Introduzca su Usuario y correo con el que se registr??")
        else:
            usuario=str(usuario)
            mail=str(mail)
            if self.Verifica_email(mail)== 1:
                QMessageBox.critical(self, "Mensaje de advertencia", "Introduzca una direcci??n de correo v??lida\n"
                                                                     "Las direcciones v??lidas son:\n\t\t\tGmail\n\t\t\tHotmail\n\t\t\tOutlook\n\t\t\tYahoo")
            else:
                resp=self.Obtener_correo()
                if resp[0]!=1 or mail != resp[1]:
                    QMessageBox.critical(self, "Error de usuario","El usuario y/o correo no coinciden con los de registro\n"
                                                                  "Por favor ingresar un usuario y correo registrados")
                else:
                    codigo = Clases.Metodos.Generador_clave()
                    resp10 = self.Probar_conexion()
                    if resp10 == 1:
                        Clases.Metodos.Enviar_codigo(codigo, mail)
                        QMessageBox.information(self, "C??digo enviado", "C??digo enviado exitosamente, revisar su correo")
                        self.ui.txt_recu_user.clear()
                        self.ui.txt_recu_correo.clear()
                        self.ui.Stacked_recu.setCurrentIndex(1)
                        self.ui.txt_recu_codigo.setFocus()
                    else:
                        QMessageBox.critical(self,"Mensaje de error de env??o","Ocurrio un error y no se pudo enviar el c??digo\n"
                                                                              "de validaci??n a su correo")
    #endregion
    #region verificar el codigo enviado al correo
    def Verifica_codigo(self):
        global codigo
        codigo1 = self.ui.txt_recu_codigo.text()
        if not codigo1:
            QMessageBox.critical(self, "Campos vacios", "debe asegurarse de llenar el codigo")
        else:
            if codigo1 != codigo:
                QMessageBox.critical(self, "Mensaje de error", "El c??digo introducido no es correcto\n"
                                                               "Revise su correo")
            else:
                self.ui.Stacked_recu.setCurrentIndex(2)
                self.ui.txt_recu_contra1.setFocus()
    #endregion
    #region verifica espacios vacios y contrase??a
    def Verifica_pass(self):
        global usuario
        contra1 = self.ui.txt_recu_contra1.text()
        contra2 = self.ui.txt_recu_contra2.text()
        if not contra1 or not contra2:
            QMessageBox.critical(self, "Campos vac??os", "Debe llenar los espacios en blanco")
        else:
            if contra1 != contra2:
                QMessageBox.critical(self, "Error de datos", "Verifique que sus contrase??as sean iguales")
            else:
                contra1=str(contra1)
                encriptado = Clases.Metodos.Encriptador2(2,contra1)
                tabla="usuario"
                columnas="pass","sal"
                id_tabla="cuenta_user"
                valores=encriptado[1],encriptado[0],usuario
                resp=self.Update_bbdd(1,tabla,columnas,id_tabla,valores)
                if resp==1:
                    resp1=self.Reset_pass(2,usuario,contra1)
                    if resp1==1:
                        QMessageBox.information(self, "Se ha cambiado con exito", "La contrase??a ha sido cambiada")
                        self.Iniciar_cero()
                    else:
                        QMessageBox.critical(self,"Mensaje de error","Ha ocurrido un error y no se pudo guardar la nueva contrase??a")
                else:
                    QMessageBox.critical(self,"Mensaje de error","Ha ocurrido alg??n error y no se pudo cambiar la contrase??a")
    #endregion
    # -----------------------------------------------------------------------------------------
    # metodos dentro del admin
    #region verificar para la busqueda de usuarios para habilitar y deshabilitar
    def Verifica_amdin(self, caso):
        '''
        verifica si los datos introducidos son correctos en la base de datos
        :param caso:
        si el caso es 1: nos manda a la busqueda de usuarios de la ventana de administracion
        :return:
        '''
        global nom
        global ape1
        global ape2
        if caso == 1:
            nom = self.ui.txt_admin_nombre.text()
            ape1 = self.ui.txt_admin_app1.text()
            ape2 = self.ui.txt_admin_app2.text()
        if caso == 2:
            nom = self.ui.txt_hist_pac_nom.text()
            ape1 = self.ui.txt_hist_pac_app1.text()
            ape2 = self.ui.txt_hist_pac_app2.text()
        if caso == 3:
            nom = self.ui.txt_info_pac_nom.text()
            ape1 = self.ui.txt_info_pac_app1.text()
            ape2 = self.ui.txt_info_pac_app2.text()
        if not nom and not ape1 and not ape2:
            QMessageBox.critical(self, "Campos vac??os", "Al menos uno de los campos debe ser llenado")
        else:
            if nom and not ape1 and not ape2:
                nom = str(nom).lower()
                if caso==1:
                    resultado = self.Busqueda_user(1, nom,ape1,ape2)
                if caso==2 or caso==3:
                    resultado=self.Busqueda_paciente(1,nom,ape1,ape2)
                if not resultado:
                    mensaje = "No existe una persona con el nombre: {}".format(nom)
                    QMessageBox.critical(self, "Mensaje de error", mensaje)
                else:
                    if caso==2 or caso==3:
                        # region registro en la tabla historial
                        razon = "busqueda paciente: {}".format(nom)
                        enviar_datos = 9, razon, 3, "persona, consulta, fecha"
                        self.Registro_tabla_historial(enviar_datos)
                        # endregion
                    if caso==1:
                        self.Datos_tabla(1, resultado)
                    if caso==2:
                        self.Datos_tabla(2, resultado)
                    if caso==3:
                        self.Datos_tabla(3, resultado)
            if ape1 and not nom and not ape2:
                ape1 = str(ape1).lower()
                if caso==1:
                    resultado = self.Busqueda_user(2, nom, ape1, ape2)
                if caso==2 or caso==3:
                    resultado=self.Busqueda_paciente(2,nom,ape1,ape2)
                if not resultado:
                    mensaje = "No existe una persona con apellido paterno: {}".format(ape1)
                    QMessageBox.critical(self, "Mensaje de error", mensaje)
                else:
                    if caso==2 or caso ==3:
                        # region registro en la tabla historial
                        razon = "busqueda paciente: {}".format(ape1)
                        enviar_datos = 9, razon, 3, "persona, consulta, fecha"
                        self.Registro_tabla_historial(enviar_datos)
                        # endregion
                    if caso==1:
                        self.Datos_tabla(1, resultado)
                    if caso==2:
                        self.Datos_tabla(2, resultado)
                    if caso==3:
                        self.Datos_tabla(3, resultado)
            if ape2 and not nom and not ape1:
                ape2 = str(ape2).lower()
                if caso==1:
                    resultado = self.Busqueda_user(3, nom, ape1, ape2)
                if caso==2 or caso==3:
                    resultado=self.Busqueda_paciente(3,nom,ape1,ape2)
                if not resultado:
                    mensaje = "No existe una persona con apellido materno: {}".format(ape2)
                    QMessageBox.critical(self, "Mensaje de error", mensaje)
                else:
                    if caso==2 or caso==3:
                        # region registro en la tabla historial
                        razon = "busqueda paciente: {}".format(ape2)
                        enviar_datos = 9, razon, 3, "persona, consulta, fecha"
                        self.Registro_tabla_historial(enviar_datos)
                        # endregion
                    if caso==1:
                        self.Datos_tabla(1, resultado)
                    if caso==2:
                        self.Datos_tabla(2, resultado)
                    if caso==3:
                        self.Datos_tabla(3, resultado)
            if nom and ape1 and not ape2:
                nom = str(nom).lower()
                ape1 = str(ape1).lower()
                if caso==1:
                    resultado = self.Busqueda_user(4, nom, ape1, ape2)
                if caso==2 or caso==3:
                    resultado=self.Busqueda_paciente(4,nom,ape1,ape2)
                if not resultado:
                    mensaje = "No existe una persona con nombre {} y apellido paterno {}".format(nom, ape1)
                    QMessageBox.critical(self, "Mensaje de error", mensaje)
                else:
                    if caso==2 or caso==3:
                        # region registro en la tabla historial
                        razon = "busqueda paciente: {} {}".format(nom, ape1)
                        enviar_datos = 9, razon, 3, "persona, consulta, fecha"
                        self.Registro_tabla_historial(enviar_datos)
                        # endregion
                    if caso==1:
                        self.Datos_tabla(1, resultado)
                    if caso==2:
                        self.Datos_tabla(2, resultado)
                    if caso==3:
                        self.Datos_tabla(3, resultado)
            if nom and ape2 and not ape1:
                nom = str(nom).lower()
                ape2 = str(ape2).lower()
                if caso==1:
                    resultado = self.Busqueda_user(5, nom, ape1, ape2)
                if caso==2 or caso==3:
                    resultado=self.Busqueda_paciente(5,nom,ape1,ape2)
                if not resultado:
                    mensaje = "No existe una persona con nombre {} y apellido materno {}".format(nom, ape2)
                    QMessageBox.critical(self, "Mensaje de error", mensaje)
                else:
                    if caso==2 or caso==3:
                        # region registro en la tabla historial
                        razon = "busqueda paciente: {} {}".format(nom, ape2)
                        enviar_datos = 9, razon, 3, "persona, consulta, fecha"
                        self.Registro_tabla_historial(enviar_datos)
                        # endregion
                    if caso==1:
                        self.Datos_tabla(1, resultado)
                    if caso==2:
                        self.Datos_tabla(2, resultado)
                    if caso==3:
                        self.Datos_tabla(3, resultado)
            if ape1 and ape2 and not nom:
                ape1 = str(ape1).lower()
                ape2 = str(ape2).lower()
                if caso==1:
                    resultado = self.Busqueda_user(6, nom, ape1, ape2)
                if caso==2 or caso==3:
                    resultado=self.Busqueda_paciente(6,nom,ape1,ape2)
                if not resultado:
                    mensaje = "No existe una persona con apellido paterno {} y apellido materno {}".format(ape1, ape2)
                    QMessageBox.critical(self, "Mensaje de error", mensaje)
                else:
                    if caso==2 or caso==3:
                        # region registro en la tabla historial
                        razon = "busqueda paciente: {} {}".format(ape1, ape2)
                        enviar_datos = 9, razon, 3, "persona, consulta, fecha"
                        self.Registro_tabla_historial(enviar_datos)
                        # endregion
                    if caso==1:
                        self.Datos_tabla(1, resultado)
                    if caso==2:
                        self.Datos_tabla(2, resultado)
                    if caso==3:
                        self.Datos_tabla(3, resultado)
            if nom and ape1 and ape2:
                nom = str(nom).lower()
                ape1 = str(ape1).lower()
                ape2 = str(ape2).lower()
                if caso==1:
                    resultado = self.Busqueda_user(7, nom, ape1, ape2)
                if caso==2 or caso==3:
                    resultado=self.Busqueda_paciente(7,nom,ape1,ape2)
                if not resultado:
                    mensaje = "No existe una persona con nombre {} {} {}".format(nom, ape1, ape2)
                    QMessageBox.critical(self, "Mensaje de error", mensaje)
                else:
                    if caso==2 or caso==3:
                        # region registro en la tabla historial
                        razon = "busqueda paciente: {} {} {}".format(nom, ape1, ape2)
                        enviar_datos = 9, razon, 3, "persona, consulta, fecha"
                        self.Registro_tabla_historial(enviar_datos)
                        # endregion
                    if caso==1:
                        self.Datos_tabla(1, resultado)
                    if caso==2:
                        self.Datos_tabla(2, resultado)
                    if caso == 3:
                        self.Datos_tabla(3, resultado)
    #endregion
    #region metodo de registro de nuevo usuario
    def Registra_nuevo_user(self):
        user1=self.ui.txt_reg_user.text()
        global reg_us_admin
        if not user1:
            QMessageBox.critical(self,"Mensaje de error","Debe llenar el campo con un usuario")
        else:
            user2=str(user1)
            resp=self.Comprobar_usuario(user2)
            if resp==1:
                if reg_us_admin==1:
                    QMessageBox.critical(self, "Mensaje de error", "El usuario ya se encuentra registrado\n"
                                                                   "Elija otro nombre de usuario")
                if reg_us_admin==2:
                    password1 = Clases.Metodos.Generador_clave()
                    resp2 = self.Reset_pass(1, user2, password1)
                    if resp2 == 1:
                        QMessageBox.information(self, "Mensaje de ??xito", "Se ha cambiado la contrase??a con ??xito\n"
                                                                          "Seleccione guardar o imprimir despu??s de cerrar este d??alogo")
                        texto1 = (("Usuario: ", user1), ("Contrase??a: ", password1))
                        nombre1 = "Cambio de contrase??a"
                        self.Enviar_datos(1, texto1, nombre1)
                        self.ui.txt_reg_user.clear()
                    else:
                        QMessageBox.critical(self, "Mensaje de error", "Algo sali?? mal, por favor intente nuevamente")
                        self.ui.txt_reg_user.clear()

            else:
                if reg_us_admin==1:
                    password = Clases.Metodos.Generador_clave()
                    resp1 = self.Crear_usuario(user2, password)
                    if resp1 == 1:
                        QMessageBox.information(self, "Mensaje de ??xito", "Usuario creado con ??xito\n"
                                                                          "seleccione guardar o imprimir despu??s de cerrar este d??alogo")
                        texto = (("Usuario: ", user1), ("Contrase??a: ", password))
                        nombre = "Nuevo usuario"
                        self.Enviar_datos(1, texto, nombre)
                        self.ui.txt_reg_user.clear()
                    else:
                        QMessageBox.critical(self, "Mensaje de error", "Algo sali?? mal, por favor intente nuevamente")
                        self.ui.txt_reg_user.clear()
                if reg_us_admin==2:
                    QMessageBox.critical(self, "Mensaje de error", "Verifique que su cuenta de usuario sea la correcta\n"
                                                                   "No se encontr?? a nadie con ese nombre")
    #endregion
    #region Calculo de la edad
    def Verifica_edad(self):
        id_tabla = str(self.ui.lbl_hist_pac_codigo.text())
        columna = "id_persona"
        tabla = "paciente"
        valor = "id_paciente", id_tabla
        resp = self.Select_bbdd(columna,tabla,valor)
        if resp[0]==1:
            # region registro en la tabla historial
            enviar_datos = 9, str(id_tabla), 3, "paciente"
            self.Registro_tabla_historial(enviar_datos)
            # endregion
            id_tabla =resp[1]
            columna = "fecha"
            tabla = "persona"
            valor = "id_persona", id_tabla
            resp1 = self.Select_bbdd(columna, tabla, valor)
            if resp1[0]==1:
                # region registro en la tabla historial
                enviar_datos = 9, str(id_tabla), 3, "persona"
                self.Registro_tabla_historial(enviar_datos)
                # endregion
                id_tabla = resp1[1]
                columna = "fechayhora"
                tabla = "fecha"
                valor = "id_fecha", id_tabla
                resp2 = self.Select_bbdd(columna, tabla, valor)
                if resp2[0]==1:
                    # region registro en la tabla historial
                    enviar_datos = 9, str(id_tabla), 3, "fecha"
                    self.Registro_tabla_historial(enviar_datos)
                    # endregion
                    fecha1=resp2[1]
        if self.ui.tab_fecha_hora.currentIndex() == 0:
            fecha = QDate.currentDate()
        if self.ui.tab_fecha_hora.currentIndex() == 1:
            fecha = self.ui.spin_hist_pac_date.date()
        mensaje=self.Calcular_fecha(fecha1, fecha)
        self.ui.lbl_hist_pac_edad.setText(mensaje)
        self.ui.lbl_hist_pac_edad.setVisible(True)
    #endregion
    #region Calcular la edad
    def Calcular_fecha(self, fecha1, fecha):
        #print(fecha1.day, fecha1.month, fecha1.year, fecha.day(), fecha.month(), fecha.year())
        # fecha_nac=float(fecha1.day)+(int(fecha1.month)*m)+(int(fecha1.year)*a)
        # fecha_act = float(fecha.day()) + (int(fecha.month()) * m) + (int(fecha.year()) * a)
        anio = fecha.year() - fecha1.year
        anio -= ((fecha.month(), fecha.day()) < (fecha1.month, fecha1.day))
        if fecha.month() > fecha1.month:
            mes = fecha.month() - fecha1.month
        else:
            mes = 12 - abs(fecha1.month - fecha.month())
        mes -= (fecha.day() < fecha1.day)
        if mes == 12:
            mes = 0
        c = 0
        a = 2000
        #global y
        var = True
        #dentro del while se genera un bucle que permite contrar los a??os normales y
        #los a??os bisiestos, con esto podemos saber los dias exactos que tiene
        while c < 17 and var == True:
            if fecha.year() == a:
                y = 31, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
                var = False
            else:
                a += 4
                c += 1
                y = 31, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31
        if fecha.day() < fecha1.day:
            dia = y[fecha.month() - 1] - fecha1.day + fecha.day()
        if fecha.day() >= fecha1.day:
            dia = fecha.day() - fecha1.day
        mensaje = "{} a??os {} meses {} d??as".format(anio, mes, dia)
        return mensaje
    #endregion
    #region Verificar campos vac??os antes de hacer el c??lculo IMC
    def Verifica_IMC(self):
        global w1
        w1 = self.ui.txt_hist_pac_pes.text()
        altura = self.ui.txt_hist_pac_tall.text()
        if not w1 and not altura:
            QMessageBox.critical(self, "Error entrada de datos", "Debe llenar los campos de peso y talla")
        elif not altura or altura == "0":
            QMessageBox.critical(self, "Advertencia error", "No se puede realizar divisi??n entre cero\n"
                                                            "Introduzca un valor para la talla")
        else:
            if not w1 and altura:
                w = 0.0
                altura = float(altura)
                h = round(altura / 100, 2)
                mensaje=self.Calcu_IMC(w, h)
            if w1 and altura:
                w1 = float(w1)
                altura = float(altura)
                w = round(w1, 3)
                h = round(altura / 100, 2)
                mensaje=self.Calcu_IMC(w, h)
            self.ui.lbl_hist_pac_IMC.setText(mensaje)
            self.ui.lbl_hist_pac_IMC.setVisible(True)
    #endregion
    #region Aqui hacemos la l??gica para el IMC
    def Calcu_IMC(self, peso, talla):
        resp = Clases.Metodos.Calcula_IMC(peso, talla)
        global mensaje
        if resp < 18.5:
            mensaje = "{}{}{}".format(resp, " ", "Bajo peso")
        if resp >= 18.5 and resp <= 24.9:
            mensaje = "{}{}{}".format(resp, " ", "Peso normal")
        if resp > 24.9 and resp <= 29.9:
            mensaje = "{}{}{}".format(resp, " ", "Sobrepeso")
        if resp > 29.9 and resp <= 34.9:
            mensaje = "{}{}{}".format(resp, " ", "Obesidad I")
        if resp > 34.9 and resp <= 39.9:
            mensaje = "{}{}{}".format(resp, " ", "Obesidad II")
        if resp > 39.9 and resp <= 49.9:
            mensaje = "{}{}{}".format(resp, " ", "Obesidad III")
        if resp > 49.9:
            mensaje = "{}{}{}".format(resp, " ", "Obesidad IV")
        return mensaje
    #endregion
    #region ver los historiales de logeo
    def Busca_historial(self):
        global tema
        self.Limpia_admin2()
        self.Poner_tema(tema)
        self.ui.Stacked_main.setCurrentIndex(4)
        self.ui.Stacked_admin.setCurrentIndex(2)
    #endregion
    #region controla el cambio del combobox de historial de usuario
    def Combo_cambio1(self):
        global medico
        d=QDate(2000,1,1)
        dato=""
        a=self.ui.cb_admin_historial.currentIndex()
        if a==0:
            self.Limpia_admin2()
        if a==1:
            medico=[]
            self.ui.Stacked_admin_log.setCurrentIndex(0)
            self.ui.cb_admin_med.setCurrentIndex(0)
            self.ui.cb_admin_med2.setCurrentIndex(0)
            self.ui.cb_admin_med2.setVisible(False)
            self.ui.Tabla_admin_historial.clearContents()
            self.ui.Tabla_admin_historial.setRowCount(0)
            self.ui.date_admin_historial.setDate(d)
            resultado = self.Busqueda_historial(1,dato)
            if not resultado:
                QMessageBox.critical(self, "Mensaje de error", "No se pudo acceder a la base de datos")
            else:
                self.Datos_tabla(5, resultado)
        if a==2:
            medico=[]
            self.ui.cb_admin_med.setCurrentIndex(0)
            self.ui.cb_admin_med2.setCurrentIndex(0)
            self.ui.cb_admin_med2.setVisible(False)
            self.ui.Tabla_admin_historial.clearContents()
            self.ui.Tabla_admin_historial.setRowCount(0)
            self.ui.date_admin_historial.setDate(d)
            self.ui.Stacked_admin_log.setCurrentIndex(1)
        if a==3:
            dato = '7 day'
        if a==4:
            dato = '14 day'
        if a==5:
            dato = '1 month'
        if a==6:
            dato = '3 month'
        if a==7:
            dato = '6 month'
        if a==8:
            dato = '9 month'
        if a==9:
            dato = '1 year'
        if a==10:
            dato = '5 year'
        if a==11:
            dato = '10 year'
        if a==3 or a==4 or a==5 or a==6 or a==7 or a==8 or a==9 or a ==10 or a==11:
            medico=[]
            self.ui.Stacked_admin_log.setCurrentIndex(0)
            self.ui.cb_admin_med.setCurrentIndex(0)
            self.ui.cb_admin_med2.setCurrentIndex(0)
            self.ui.cb_admin_med2.setVisible(False)
            self.ui.Tabla_admin_historial.clearContents()
            self.ui.Tabla_admin_historial.setRowCount(0)
            self.ui.date_admin_historial.setDate(d)
            resultado = self.Busqueda_historial(3,dato)
            if not resultado:
                QMessageBox.critical(self, "Mensaje de error", "No se pudo acceder a la base de datos")
            else:
                self.Datos_tabla(5, resultado)
        if a==12:
            resultado = self.Busqueda_historial(4,dato)
            medico=[]
            self.ui.cb_admin_med.clear()
            self.ui.cb_admin_med.addItem("M??dicos")
            if not resultado:
                QMessageBox.critical(self,"Mensaje de error","No hay m??dicos registrados o no se pudo ingresar al a base de datos")
            else:
                c = 0
                for i in resultado:
                    medico.insert(c,i[0])
                    nombre="{} {} {}".format(i[1],i[2],i[3])
                    self.ui.cb_admin_med.addItem(nombre)
                    c+=1
                self.ui.Stacked_admin_log.setCurrentIndex(2)
                self.ui.cb_admin_med2.setCurrentIndex(0)
                self.ui.cb_admin_med2.setVisible(False)
                self.ui.Tabla_admin_historial.clearContents()
                self.ui.Tabla_admin_historial.setRowCount(0)
                self.ui.date_admin_historial.setDate(d)
    #endregion
    #region Controla el cambio en el combobox general
    def Combo_cambio2(self):
        d=QDate(2000,1,1)
        a=self.ui.cb_admin_med.currentIndex()
        if a==0:
            self.ui.cb_admin_med2.setCurrentIndex(0)
            self.ui.cb_admin_med2.setVisible(False)
            self.ui.Tabla_admin_historial.clearContents()
            self.ui.Tabla_admin_historial.setRowCount(0)
            self.ui.date_admin_historial.setDate(d)
        else:
            self.ui.cb_admin_med2.setVisible(True)
    #endregion
    #region Controla el cambio en el combobox de medicos
    def Combo_cambio3(self):
        global medico
        a=self.ui.cb_admin_med.currentIndex()
        b=self.ui.cb_admin_med2.currentIndex()
        if a!=0:
            dato1=medico[a-1]
            if b==1:
                self.ui.Tabla_admin_historial.clearContents()
                self.ui.Tabla_admin_historial.setRowCount(0)
                resultado = self.Busqueda_historial(5, dato1)
                if not resultado:
                    QMessageBox.critical(self, "Mensaje de error", "No se pudo acceder a la base de datos")
                else:
                    self.Datos_tabla(5, resultado)
            if b==2:
                dato=dato1,'7 day'
            if b==3:
                dato = dato1, '14 day'
            if b==4:
                dato = dato1, '1 month'
            if b==5:
                dato = dato1, '3 month'
            if b==6:
                dato = dato1, '6 month'
            if b==7:
                dato = dato1, '9 month'
            if b==8:
                dato = dato1, '1 year'
            if b==9:
                dato = dato1, '5 year'
            if b==10:
                dato = dato1, '10 year'
            if b==2 or b==3 or b==4 or b==5 or b==6 or b==7 or b==8 or b==9 or b==10:
                self.ui.Tabla_admin_historial.clearContents()
                self.ui.Tabla_admin_historial.setRowCount(0)
                resultado = self.Busqueda_historial(6, dato)
                if not resultado:
                    QMessageBox.critical(self, "Mensaje de error", "No se pudo acceder a la base de datos")
                else:
                    self.Datos_tabla(5, resultado)
    #endregion
    #region Busca por fecha en el historial de administracion
    def Busca_por_fecha(self):
        fecha = self.ui.date_admin_historial.date()
        fecha = fecha.toPyDate()
        fecha = fecha.strftime('%Y-%m-%d')
        fecha = fecha.split("-")
        anio = int(fecha[0])
        mes = int(fecha[1])
        dia = int(fecha[2])
        dato=anio,mes,dia
        resultado = self.Busqueda_historial(2, dato)
        if not resultado:
            mensaje="No se encontraron registros de la fecha: {}-{}-{}".format(dia,mes,anio)
            QMessageBox.critical(self, "Mensaje de error", mensaje)
        else:
            self.Datos_tabla(5, resultado)
    #endregion
    #region cerrar la ventana de registro de usuario
    def Cerrar_registro(self):
        global reg_us
        if reg_us == 1:
            self.ui.Stacked_main.setCurrentIndex(0)
            reg_us = 0
        if reg_us == 2:
            self.ui.Stacked_main.setCurrentIndex(5)
            reg_us = 0
    #endregion
    #region entra a la ventana de administracion
    def Entrar_control_user(self):
        global tema
        self.Limpia_admin1()
        self.Limpia_admin2()
        self.Poner_tema(tema)
        self.ui.Stacked_admin.setCurrentIndex(1)
        self.ui.txt_admin_nombre.setFocus()
        self.les = [self.ui.txt_admin_nombre, self.ui.txt_admin_app1, self.ui.txt_admin_app2,
                    self.ui.btn_admin_buscar_user]
    #endregion
    #region entrar a la ventana para cambiar el tema
    def Ventana_tema(self):
        global usuario
        global tema
        self.Poner_tema(tema)
        self.Limpia_tema()
        self.Limpia_admin2()
        self.ui.Stacked_main.setCurrentIndex(10)
    #endregion
    #region entrar a la ventana de registro de nuevo usuario desde el administrador
    def Ventana_admi_reg(self,caso):
        global tema
        global reg_us_admin
        self.Poner_tema(tema)
        self.Limpia_admin2()
        self.Limpia_admin_reg()
        self.ui.Stacked_main.setCurrentIndex(4)
        self.ui.Stacked_admin.setCurrentIndex(3)
        self.ui.txt_reg_user.setFocus()
        self.les = [self.ui.txt_reg_user, self.ui.btn_admin_reg_user]
        if caso==1:
            self.ui.lbl_admin_reg_titulo.setText("Registrar un nuevo usuario")
            reg_us_admin=1
        if caso==2:
            self.ui.lbl_admin_reg_titulo.setText("Resetear la contrase??a de usuario")
            reg_us_admin=2
    #endregion
    # ------------------------------------------------------------------------------------------
    # region metodos de limpieza de campos
    # limpiar el Loggin
    def Limpia_login(self):
        self.ui.txt_log_user.clear()
        self.ui.txt_log_pass.clear()

    # Limpiar el registro de usuario
    def Limpia_reg_user(self):
        self.ui.txt_reg_user_CI.clear()
        self.ui.cb_reg_user_CI.setCurrentIndex(0)
        self.ui.txt_reg_user_mat.clear()
        self.ui.txt_reg_nom_user.clear()
        self.ui.txt_reg_apell1_user.clear()
        self.ui.txt_reg_apell2_user.clear()
        self.ui.txt_reg_pass.clear()
        self.ui.txt_reg_pass1.clear()
        self.ui.txt_reg_correo_user.clear()
        self.ui.comboBox.setCurrentIndex(0)

    # Limpia ventana de recuperacion de contrase??a
    def Limpia_recu(self):
        self.ui.txt_recu_user.clear()
        self.ui.txt_recu_correo.clear()
        self.ui.txt_recu_codigo.clear()
        self.ui.txt_recu_contra1.clear()
        self.ui.txt_recu_contra2.clear()
        self.ui.Stacked_recu.setCurrentIndex(0)

    # Limpia la ventana de admin 1
    def Limpia_admin1(self):
        self.ui.txt_admin_nombre.clear()
        self.ui.txt_admin_app1.clear()
        self.ui.txt_admin_app2.clear()
        self.ui.Tabla_admin_user.clearContents()
        self.ui.Tabla_admin_user.setRowCount(0)

        # Limpia la ventana de admin 2

    # limpia los contenidos dentro de la busqueda de logeo
    def Limpia_admin2(self):
        global medico
        d=QDate(2000,1,1)
        self.ui.cb_admin_historial.setCurrentIndex(0)
        self.ui.Stacked_admin_log.setCurrentIndex(0)
        self.ui.cb_admin_med.setCurrentIndex(0)
        self.ui.cb_admin_med2.setCurrentIndex(0)
        self.ui.date_admin_historial.setDate(d)
        self.ui.cb_admin_med2.setVisible(False)
        self.ui.Tabla_admin_historial.clearContents()
        self.ui.Tabla_admin_historial.setRowCount(0)
        medico=[]

    # limpia la ventana de seleccion de tema
    def Limpia_tema(self):
        self.ui.cb_config_tema.setCurrentIndex(0)

    # Limpia los campos de registro de paciente
    def Limpia_reg_pac(self):
        d=QDate(2000,1,1)
        self.ui.txt_reg_pac_nom.clear()
        self.ui.txt_reg_pac_app1.clear()
        self.ui.txt_reg_pac_app2.clear()
        self.ui.txt_reg_pac_CI.clear()
        self.ui.txt_reg_pac_tall.clear()
        self.ui.txt_reg_pac_pes.clear()
        self.ui.txt_reg_pac_tel1.clear()
        self.ui.txt_reg_pac_tel2.clear()
        self.ui.txt_reg_pac_pro1.clear()
        self.ui.txt_reg_pac_res1.clear()
        self.ui.txt_reg_pac_dir.clear()
        self.ui.txt_reg_pac_barr.clear()
        self.ui.txt_reg_pac_padre.clear()
        self.ui.txt_reg_pac_padre1.clear()
        self.ui.txt_reg_pac_padre2.clear()
        self.ui.txt_reg_pac_CI_padre.clear()
        self.ui.txt_reg_pac_CI_madre.clear()
        self.ui.txt_reg_pac_madre.clear()
        self.ui.txt_reg_pac_madre1.clear()
        self.ui.txt_reg_pac_madre2.clear()
        self.ui.pt_reg_pac_ap.clear()
        self.ui.pt_reg_pac_alerg.clear()
        self.ui.cb_reg_pac_sex.setCurrentIndex(0)
        self.ui.cb_reg_pac_gs.setCurrentIndex(0)
        self.ui.cb_reg_pac_gsf.setCurrentIndex(0)
        self.ui.cb_reg_pac_CI.setCurrentIndex(0)
        self.ui.cb_reg_pac_CI_padre.setCurrentIndex(0)
        self.ui.cb_reg_pac_CI_madre.setCurrentIndex(0)
        self.ui.date_reg_pac_nac.setDate(d)

    # limpia busqueda
    def Limpia_hist_busc(self):
        self.ui.txt_hist_pac_nom.clear()
        self.ui.txt_hist_pac_app1.clear()
        self.ui.txt_hist_pac_app2.clear()
        self.ui.Tabla_hist_pac.clearContents()
        self.ui.Tabla_hist_pac.setRowCount(0)

    # limpia historia
    def Limpia_hist_pac(self):
        d=QDateTime(2000,1,1,00,00)
        e=QDate(2000,1,1)
        self.ui.cb_hist_pac_consul.setCurrentIndex(0)
        self.ui.txt_hist_pac_fc.clear()
        self.ui.txt_hist_pac_fr.clear()
        self.ui.txt_hist_pac_temp.clear()
        self.ui.txt_hist_pac_SO.clear()
        self.ui.txt_hist_pac_pa1.clear()
        self.ui.txt_hist_pac_pa2.clear()
        self.ui.txt_hist_pac_percef.clear()
        self.ui.tab_fecha_hora.setCurrentIndex(0)
        self.ui.lbl_hist_pac_edad.clear()
        self.ui.lbl_hist_pac_edad.setVisible(False)
        self.ui.lbl_hist_pac_IMC.clear()
        self.ui.lbl_hist_pac_IMC.setVisible(False)
        self.ui.lbl_hist_pac_temp.setText("??C")
        self.ui.txt_hist_pac_pes.clear()
        self.ui.txt_hist_pac_tall.clear()
        self.ui.pt_hist_pac_con.clear()
        self.ui.pt_hist_pac_ex.clear()
        self.ui.pt_hist_pac_diag.clear()
        self.ui.pt_hist_pac_trat.clear()
        self.ui.pt_hist_pac_obs.clear()
        self.ui.spin_hist_pac_date.setDateTime(d)
        self.ui.spin_hist_pac_dat.setDate(e)

    # limpia la busqueda y tablas en modulo de informacion de historias
    def Limpia_info_busc(self):
        self.ui.txt_info_pac_nom.clear()
        self.ui.txt_info_pac_app1.clear()
        self.ui.txt_info_pac_app2.clear()
        self.ui.Tabla_info_pac1.clearContents()
        self.ui.Tabla_info_pac2.clearContents()
        self.ui.Tabla_info_pac1.setRowCount(0)
        self.ui.Tabla_info_pac2.setRowCount(0)

    def Limpia_admin_reg(self):
        self.ui.txt_reg_user.clear()
        self.ui.cb_reg_user.setCurrentIndex(0)
    # endregion
    # ------------------------------------------------------------------------------------------
    # m??todos que ocurren al cerrar las ventanas
    # Cerrar la ventana 1 de logeo implica borrar los line edit
    def Cerrar_ventana1(self):
        global usuario
        usuario = ""
        self.ui.Stacked_main.setCurrentIndex(0)
    # region Metodo para salir del modulo de configuracion de tema
    def Salir_tema(self):
        global usuario
        global tema
        global reg_pac
        global reg_us
        reg_pac = 0
        reg_us = 0
        self.Poner_tema(tema)
        usuario1 = Clases.Metodos.Obtener_datos('USER')
        if usuario == usuario1:
            self.ui.Stacked_main.setCurrentIndex(4)
            self.ui.Stacked_admin.setCurrentIndex(0)
        else:
            self.ui.Stacked_main.setCurrentIndex(5)
    # endregion
    # region Metodo para Cerrar algunas ventanas de usuario medico
    def Cerrar_ventanas_usuario(self):
        global reg_pac
        global reg_us
        global x
        reg_pac = 0
        reg_us = 0
        x = 0
        self.ui.Stacked_main.setCurrentIndex(5)
    # endregion
    # ----------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------
    # m??todos que mejoran el funcionamiento
    # region Metodo rango de enfermedad por temperatura
    def Poner_valor(self):
        valor = float(self.ui.txt_hist_pac_temp.text())
        if valor:
            resp = Clases.Metodos.Temp_verf(valor)
            if resp == 1:
                self.ui.lbl_hist_pac_temp.setText("??C Hipotermia")
            elif resp == 2:
                self.ui.lbl_hist_pac_temp.setText("??C Normal")
            elif resp == 3:
                self.ui.lbl_hist_pac_temp.setText("??C Febr??cula")
            elif resp == 4:
                self.ui.lbl_hist_pac_temp.setText("??C Fiebre")
    # endregion
    # region metodo Elegir el tema
    def Elegir_tema(self):
        tema1 = self.ui.cb_config_tema.currentIndex()
        global tema
        global usuario
        if tema1 == 0:
            QMessageBox.critical(self, "Mensaje de error", "Debe seleccionar al menos una opcion para tener el tema")
        else:
            self.Poner_tema(tema1)
            tabla="usuario"
            columnas="tema",
            id_tabla="cuenta_user"
            valores=tema1,usuario
            resp=self.Update_bbdd(2,tabla,columnas,id_tabla,valores)
            tema = tema1
            if resp==1:
                # region registro en la tabla historial
                enviar_datos = 8, str(usuario), 2, "usuario"
                self.Registro_tabla_historial(enviar_datos)
                # endregion
            else:
                QMessageBox.critical(self,"Mensaje de error","Algo sali?? mal, no se pudo guardar el tema que eligi??\n"
                                                             "Intente nuevamete dentro de un momento")
    # endregion
    # region metodo probar cambios en el tema de fondo y letra
    def Prueba_tema(self):
        tema1 = self.ui.cb_config_tema.currentIndex()
        if tema1 == 0:
            QMessageBox.critical(self, "Mensaje de error", "Debe seleccionar al menos una opcion para probar el tema")
        else:
            self.Poner_tema(tema1)
    # endregion
    # region m??todo para el cambio de tema o implementaci??n
    def Poner_tema(self, tema1):
        # ************************************************************************************************
        # FONDO negro CON LETRAS BLANCAS
        # ************************************************************************************************
        if tema1 == 1:
            self.ui.Frame_main.setStyleSheet("*{\n"
                                             # "    font: 75 italic 12pt \"Times New Roman\";\n"
                                             "	  color: rgb(255, 255, 255);\n"
                                             "}\n"
                                             "QFrame{\n"
                                             "	background-color: rgb(0, 0, 0);\n"
                                             "}\n"
                                             "QLineEdit{\n"
                                             "	background:transparent;\n"
                                             "	border-radius:20px;\n"
                                             "	border:1px solid #ffffff;\n"
                                             "}\n"
                                             "QLineEdit:focus,QPlainTextEdit:hover,QComboBox:hover{\n"
                                             "	background:#5b004d;\n"
                                             "}\n"
                                             "QPlainTextEdit{\n"
                                             "	border:1px solid #ffffff;\n"
                                             "}\n"
                                             "QCalendarWidget QWidget{\n"
                                             "	background-color: rgb(0, 0, 0);\n"
                                             "	selection-color: rgb(255, 255, 255);\n"
                                             "	alternate-background-color:rgb(0,0,0);\n"
                                             "	selection-background-color: rgb(91, 0, 77);\n"
                                             "}\n"
                                             "QSpinBox{\n"
                                             "	background-color: rgb(0, 0, 0);\n"
                                             "	border:1px solid #ffffff;\n"
                                             "	selection-color: rgb(255, 255, 255);\n"
                                             "	border-radius:12px;\n"
                                             "	selection-background-color: rgb(91, 0, 77);\n"
                                             "}\n"
                                             "QAbstractItemView{\n"
                                             "	background-color: rgb(0, 0, 0);\n"
                                             "	selection-color: rgb(255, 255, 255);\n"
                                             "	selection-background-color: rgb(91, 0, 77);\n"
                                             "}\n"
                                             "QComboBox{\n"
                                             "	border:1px solid #ffffff;\n"
                                             "	border-radius:20px;\n"
                                             "	background:transparent;\n"
                                             "	selection-background-color: rgb(91, 0, 77);\n"
                                             "}\n"
                                             "QHeaderView::section{\n"
                                             "	background-color: rgb(0, 0, 0);\n"
                                             "	border:1px solid #ffffff;\n"
                                             "}\n"
                                             "QDateEdit,QTimeEdit,QDateTimeEdit{\n"
                                             "	background-color: rgb(0, 0, 0);\n"
                                             "	border-radius:8px;\n"
                                             "	border:1px solid #ffffff;\n"
                                             "}\n"
                                             "QDateEdit:hover,QTimeEdit:hover,QDateTimeEdit:hover{\n"
                                             "	background:#5b004d;\n"
                                             "	border-radius:8px;\n"
                                             "}\n"
                                             "QToolTip {\n"
                                             "  border: 1px solid #ffffff;\n"
                                             "  padding: 5px;\n"
                                             "  border-radius: 5px;\n"
                                             "  opacity: 200;\n"
                                             "	background:transparent;\n"
                                             "  }\n"
                                             "QTabWidget::pane{\n"
                                             "  border: 1px solid #ffffff;\n"
                                             "  top:-1px;\n"
                                             "	background:transparent;\n"
                                             "}\n"
                                             "QTabBar::tab{\n"
                                             "  border: 1px #ffffff;\n"
                                             "  padding: 10px;\n"
                                             "	background:transparent;\n"
                                             "}\n"
                                             "QTabBar::tab:selected{\n"
                                             "	margin-bottom: -1px;\n"
                                             "  border: 1px solid #ffffff;\n"
                                             "	border-radius:10px;\n"
                                             "}\n"

                                             "QTabBar::tab:hover{\n"
                                             "	background:#5b004d;\n"
                                             "	border-radius:10px;\n"
                                             "}\n"
                                             "QScrollBar:vertical{\n"
                                             "border: 1px solid #ffffff;\n"
                                             "background:transparent;\n"
                                             "width:10px;\n"
                                             "border-radius:5px;\n"
                                             "margin: 0px 0px 0px 0px;\n"
                                             "}\n"
                                             "QScrollBar:horizontal{\n"
                                             "border: 1px solid #ffffff;\n"
                                             "background:transparent;\n"
                                             "height:10px;\n"
                                             "border-radius:5px;\n"
                                             "margin: 0px 0px 0px 0px;\n"
                                             "}\n"
                                             "QScrollBar::handle:vertical{\n"
                                             "	border:1px solid #ffffff;\n"
                                             "	border-radius:5px;\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(0, 0,0), stop: 0.5 rgb(0, 0, 0), stop:1 rgb(0, 0, 0));\n"
                                             "min-height: 0px;\n"
                                             "}\n"
                                             "QScrollBar::handle:vertical{\n"
                                             "	border:1px solid #ffffff;\n"
                                             "	border-radius:5px;\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(0, 0,0), stop: 0.5 rgb(0, 0, 0), stop:1 rgb(0, 0, 0));\n"
                                             "min-width: 0px;\n"
                                             "}\n"
                                             "QScrollBar::add-line:vertical {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(0, 0, 0), stop: 0.5 rgb(0, 0, 0),  stop:1 rgb(0, 0, 0));\n"
                                             "height: 0px;\n"
                                             "subcontrol-position: bottom;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::sub-line:vertical {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0  rgb(0, 0, 0), stop: 0.5 rgb(0, 0, 0),  stop:1 rgb(0, 0, 0));\n"
                                             "height: 0 px;\n"
                                             "subcontrol-position: top;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::add-line:horizontal {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(0, 0, 0), stop: 0.5 rgb(0, 0, 0),  stop:1 rgb(0, 0, 0));\n"
                                             "width: 0px;\n"
                                             "subcontrol-position: right;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::sub-line:horizontal {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0  rgb(0, 0, 0), stop: 0.5 rgb(0, 0, 0),  stop:1 rgb(0, 0, 0));\n"
                                             "width: 0 px;\n"
                                             "subcontrol-position: left;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::handle:vertical:hover,QScrollBar::handle:horizontal:hover{\n"
                                             "border-radius:5px;\n"
                                             "background:#5b004d;\n"
                                             "}\n"
                                             "QPushButton{\n"
                                             "	padding: 5px;\n"
                                             "	border:1px solid #ffffff;\n"
                                             "	border-radius:15px;\n"
                                             "}\n"
                                             "QPushButton#btn_config,#btn_salir,#btn_log_close,#btn_reg_close,"
                                             "#btn_recu_close,#btn_admi_user_volver,#btn_admin_historial_volver,"
                                             "#btn_admin_historial_buscar,#btn_reg_user_volver,#btn_mod_close,"
                                             "#btn_mod_nom_volver,#btn_mod_pass_volver,#btn_mod_correo_volver,"
                                             "#btn_reg_pac_close,#btn_hist_pac_close,#btn_hist_pac_IMC,"
                                             "#btn_hist_pac_clean2,#btn_hist_pac_save,#btn_info_pac_buscar,"
                                             "#btn_info_pac_selec,#btn_info_pac_close,#btn_mod_pac_buscar,"
                                             "#btn_mod_pac_close,#btn_config_close{\n"
                                             "	border:1px solid #ffffff;\n"
                                             "	border-radius:8px;\n"
                                             "}\n"
                                             "QPushButton:hover,QPushButton:focus{\n"
                                             "	background:#5b004d;\n"
                                             "	border-radius:15px;\n"
                                             "}")

            # ************************************************************************************************
            # FONDO NEGRO CON LETRAS VERDES
            # ************************************************************************************************
        if tema1 == 2:
            self.ui.Frame_main.setStyleSheet("*{\n"
                                             # "    font: 75 italic 12pt \"Times New Roman\";\n"
                                             "	  color: rgb(85, 255, 0);\n"
                                             "}\n"
                                             "QFrame{\n"
                                             "	background-color: rgb(0, 0, 0);\n"
                                             "}\n"
                                             "QLineEdit{\n"
                                             "	background:transparent;\n"
                                             "	border-radius:20px;\n"
                                             "	border:1px solid #55ff00;\n"
                                             "}\n"
                                             "QLineEdit:focus,QPlainTextEdit:hover,QComboBox:hover{\n"
                                             "	background:#131071;\n"
                                             "}\n"
                                             "QPlainTextEdit{\n"
                                             "	border:1px solid #55ff00;\n"
                                             "}\n"
                                             "QCalendarWidget QWidget{\n"
                                             "  background-color: rgb(0, 0, 0);\n"
                                             "	selection-color: rgb(85, 255, 0);\n"
                                             "	alternate-background-color: rgb(0, 0, 0);\n"
                                             "	selection-background-color: rgb(19, 16, 113);\n"
                                             "}\n"
                                             "QSpinBox{\n"
                                             "  background-color:rgb(0,0,0);\n"
                                             "	border:1px solid #55ff00;\n"
                                             "	selection-color: rgb(85, 255, 0);\n"
                                             "	border-radius:12px;\n"
                                             "	selection-background-color: rgb(19, 16, 113);\n"
                                             "}\n"
                                             "QAbstractItemView{\n"
                                             "	background-color: rgb(0, 0, 0);\n"
                                             "	selection-color: rgb(85, 255, 0);\n"
                                             "	selection-background-color: rgb(19, 16, 113);\n"
                                             "}\n"
                                             "QComboBox{\n"
                                             "	border:1px solid #55ff00;\n"
                                             "	border-radius:20px;\n"
                                             "	background:transparent;\n"
                                             "	selection-background-color: rgb(19, 16, 113);\n"
                                             "}\n"
                                             "QHeaderView::section{\n"
                                             "	background-color: rgb(0, 0, 0);\n"
                                             "	border:1px solid #55ff00;\n"
                                             "}\n"
                                             "QDateEdit,QTimeEdit{\n"
                                             "  background-color:rgb(0,0,0);\n"
                                             "	border-radius:8px;\n"
                                             "	border:1px solid #55ff00;\n"
                                             "}\n"
                                             "QDateEdit:hover,QTimeEdit:hover{\n"
                                             "	background:#131071;\n"
                                             "	border-radius:8px;\n"
                                             "}\n"
                                             "QToolTip {\n"
                                             "  border: 1px solid #55ff00;\n"
                                             "  padding: 5px;\n"
                                             "  border-radius: 5px;\n"
                                             "  opacity: 200;\n"
                                             "	background:transparent;\n"
                                             "  }\n"
                                             "QTabWidget::pane{\n"
                                             "  border: 1px solid #55ff00;\n"
                                             "  top:-1px;\n"
                                             "	background:transparent;\n"
                                             "}\n"
                                             "QTabBar::tab{\n"
                                             "  border: 1px #55ff00;\n"
                                             "  padding: 10px;\n"
                                             "	background:transparent;\n"
                                             "}\n"
                                             "QTabBar::tab:selected{\n"
                                             "	margin-bottom: -1px;\n"
                                             "  border: 1px solid #55ff00;\n"
                                             "	border-radius:10px;\n"
                                             "}\n"
                                             "QTabBar::tab:hover{\n"
                                             "	background:#131071;\n"
                                             "	border-radius:10px;\n"
                                             "}\n"
                                             "QScrollBar:vertical{\n"
                                             "border: 1px solid #55ff00;\n"
                                             "background:transparent;\n"
                                             "width:10px;\n"
                                             "border-radius:5px;\n"
                                             "margin: 0px 0px 0px 0px;\n"
                                             "}\n"
                                             "QScrollBar:horizontal{\n"
                                             "border: 1px solid #55ff00;\n"
                                             "background:transparent;\n"
                                             "height:10px;\n"
                                             "border-radius:5px;\n"
                                             "margin: 0px 0px 0px 0px;\n"
                                             "}\n"
                                             "QScrollBar::handle:vertical {\n"
                                             "	border:1px solid #55ff00;\n"
                                             "	border-radius:5px;\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(0, 0,0), stop: 0.5 rgb(0, 0, 0), stop:1 rgb(0, 0, 0));\n"
                                             "min-height: 0px;\n"
                                             "}\n"
                                             "QScrollBar::handle:horizontal {\n"
                                             "	border:1px solid #55ff00;\n"
                                             "	border-radius:5px;\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(0, 0,0), stop: 0.5 rgb(0, 0, 0), stop:1 rgb(0, 0, 0));\n"
                                             "min-width: 0px;\n"
                                             "}\n"
                                             "QScrollBar::add-line:vertical {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(0, 0, 0), stop: 0.5 rgb(0, 0, 0),  stop:1 rgb(0, 0, 0));\n"
                                             "height: 0px;\n"
                                             "subcontrol-position: bottom;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::add-line:horizontal {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(0, 0, 0), stop: 0.5 rgb(0, 0, 0),  stop:1 rgb(0, 0, 0));\n"
                                             "width: 0px;\n"
                                             "subcontrol-position: right;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::sub-line:vertical {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0  rgb(0, 0, 0), stop: 0.5 rgb(0, 0, 0),  stop:1 rgb(0, 0, 0));\n"
                                             "height: 0 px;\n"
                                             "subcontrol-position: top;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::sub-line:horizontal {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0  rgb(0, 0, 0), stop: 0.5 rgb(0, 0, 0),  stop:1 rgb(0, 0, 0));\n"
                                             "width: 0 px;\n"
                                             "subcontrol-position: left;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::handle:vertical:hover,QScrollbar::handle:horizontal:hover{\n"
                                             "border-radius:5px;\n"
                                             "background:#131071;\n"
                                             "}\n"
                                             "QPushButton{\n"
                                             "	padding: 5px;\n"
                                             "	border:1px solid #55ff00;\n"
                                             "	border-radius:15px;\n"
                                             "}\n"
                                             "QPushButton#btn_config,#btn_salir,#btn_log_close,#btn_reg_close,"
                                             "#btn_recu_close,#btn_admi_user_volver,#btn_admin_historial_volver,"
                                             "#btn_admin_historial_buscar,#btn_reg_user_volver,#btn_mod_close,"
                                             "#btn_mod_nom_volver,#btn_mod_pass_volver,#btn_mod_correo_volver,"
                                             "#btn_reg_pac_close,#btn_hist_pac_close,#btn_hist_pac_IMC,"
                                             "#btn_hist_pac_clean2,#btn_hist_pac_save,#btn_info_pac_buscar,"
                                             "#btn_info_pac_selec,#btn_info_pac_close,#btn_mod_pac_buscar,"
                                             "#btn_mod_pac_close,#btn_config_close{\n"
                                             "	border:1px solid #55ff00;\n"
                                             "	border-radius:8px;\n"
                                             "}\n"
                                             "QPushButton:hover,QPushButton:focus{\n"
                                             "	background:#131071;\n"
                                             "	border-radius:15px;\n"
                                             "}")
            # ************************************************************************************************
            # FONDO NEGRO CON LETRAS AMARILLAS
            # ************************************************************************************************
        if tema1 == 3:
            self.ui.Frame_main.setStyleSheet("*{\n"
                                             # "    font: 75 italic 12pt \"Times New Roman\";\n"
                                             "	  color: rgb(255, 255, 0);\n"
                                             "}\n"
                                             "QFrame{\n"
                                             "	background-color: rgb(0, 0, 0);\n"
                                             "}\n"
                                             "QLineEdit{\n"
                                             "	background:transparent;\n"
                                             "	border-radius:20px;\n"
                                             "	border:1px solid #ffff00;\n"
                                             "}\n"
                                             "QLineEdit:focus,QPlainTextEdit:hover,QComboBox:hover{\n"
                                             "	background:#862d00;\n"
                                             "}\n"
                                             "QPlainTextEdit{\n"
                                             "	border:1px solid #ffff00;\n"
                                             "}\n"
                                             "QCalendarWidget QWidget{\n"
                                             "  background-color: rgb(0, 0, 0);\n"
                                             "	selection-color: rgb(255, 255, 0);\n"
                                             "	alternate-background-color: rgb(0, 0, 0);\n"
                                             "	selection-background-color: rgb(134, 45, 0);\n"
                                             "}\n"
                                             "QSpinBox{\n"
                                             "  background-color:rgb(0,0,0);\n"
                                             "	border:1px solid #ffff00;\n"
                                             "	selection-color: rgb(255, 255, 0);\n"
                                             "	border-radius:12px;\n"
                                             "	selection-background-color: rgb(134, 45, 0);\n"
                                             "}\n"
                                             "QAbstractItemView{\n"
                                             "	background-color: rgb(0, 0, 0);\n"
                                             "	selection-color: rgb(255, 255, 0);\n"
                                             "	selection-background-color: rgb(134, 45, 0);\n"
                                             "}\n"
                                             "QComboBox{\n"
                                             "	border:1px solid #ffff00;\n"
                                             "	border-radius:20px;\n"
                                             "	background:transparent;\n"
                                             "	selection-background-color: rgb(134, 45, 0);\n"
                                             "}\n"
                                             "QHeaderView::section{\n"
                                             "	background-color: rgb(0, 0, 0);\n"
                                             "	border:1px solid #ffff00;\n"
                                             "}\n"
                                             "QDateEdit,QTimeEdit{\n"
                                             "  background-color:rgb(0,0,0);\n"
                                             "	border-radius:8px;\n"
                                             "	border:1px solid #ffff00;\n"
                                             "}\n"
                                             "QDateEdit:hover,QTimeEdit:hover{\n"
                                             "	background:#862d00;\n"
                                             "	border-radius:8px;\n"
                                             "}\n"
                                             "QToolTip {\n"
                                             "  border: 1px solid #ffff00;\n"
                                             "  padding: 5px;\n"
                                             "  border-radius: 5px;\n"
                                             "  opacity: 200;\n"
                                             "	background:transparent;\n"
                                             "  }\n"
                                             "QTabWidget::pane{\n"
                                             "  border: 1px solid #ffff00;\n"
                                             "  top:-1px;\n"
                                             "	background:transparent;\n"
                                             "}\n"
                                             "QTabBar::tab{\n"
                                             "  border: 1px #ffff00;\n"
                                             "  padding: 10px;\n"
                                             "	background:transparent;\n"
                                             "}\n"
                                             "QTabBar::tab:selected{\n"
                                             "	margin-bottom: -1px;\n"
                                             "  border: 1px solid #ffff00;\n"
                                             "	border-radius:10px;\n"
                                             "}\n"
                                             "QTabBar::tab:hover{\n"
                                             "	background:#862d00;\n"
                                             "	border-radius:10px;\n"
                                             "}\n"
                                             "QScrollBar:vertical{\n"
                                             "border: 1px solid #ffff00;\n"
                                             "background:transparent;\n"
                                             "width:10px;\n"
                                             "border-radius:5px;\n"
                                             "margin: 0px 0px 0px 0px;\n"
                                             "}\n"
                                             "QScrollBar:horizontal{\n"
                                             "border: 1px solid #ffff00;\n"
                                             "background:transparent;\n"
                                             "height:10px;\n"
                                             "border-radius:5px;\n"
                                             "margin: 0px 0px 0px 0px;\n"
                                             "}\n"
                                             "QScrollBar::handle:vertical {\n"
                                             "	border:1px solid #ffff00;\n"
                                             "	border-radius:5px;\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(0, 0,0), stop: 0.5 rgb(0, 0, 0), stop:1 rgb(0, 0, 0));\n"
                                             "min-height: 0px;\n"
                                             "}\n"
                                             "QScrollBar::handle:horizontal {\n"
                                             "	border:1px solid #ffff00;\n"
                                             "	border-radius:5px;\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(0, 0,0), stop: 0.5 rgb(0, 0, 0), stop:1 rgb(0, 0, 0));\n"
                                             "min-width: 0px;\n"
                                             "}\n"
                                             "QScrollBar::add-line:vertical {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(0, 0, 0), stop: 0.5 rgb(0, 0, 0),  stop:1 rgb(0, 0, 0));\n"
                                             "height: 0px;\n"
                                             "subcontrol-position: bottom;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::add-line:horizontal {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(0, 0, 0), stop: 0.5 rgb(0, 0, 0),  stop:1 rgb(0, 0, 0));\n"
                                             "width: 0px;\n"
                                             "subcontrol-position: right;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::sub-line:vertical {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0  rgb(0, 0, 0), stop: 0.5 rgb(0, 0, 0),  stop:1 rgb(0, 0, 0));\n"
                                             "height: 0 px;\n"
                                             "subcontrol-position: top;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::sub-line:horizontal {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0  rgb(0, 0, 0), stop: 0.5 rgb(0, 0, 0),  stop:1 rgb(0, 0, 0));\n"
                                             "width: 0 px;\n"
                                             "subcontrol-position: left;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::handle:vertical:hover,QScrollBar::handle:horizontal:hover{\n"
                                             "border-radius:5px;\n"
                                             "background:#862d00;\n"
                                             "}\n"
                                             "QPushButton{\n"
                                             "	padding: 5px;\n"
                                             "	border:1px solid #ffff00;\n"
                                             "	border-radius:15px;\n"
                                             "}\n"
                                             "QPushButton#btn_config,#btn_salir,#btn_log_close,#btn_reg_close,"
                                             "#btn_recu_close,#btn_admi_user_volver,#btn_admin_historial_volver,"
                                             "#btn_admin_historial_buscar,#btn_reg_user_volver,#btn_mod_close,"
                                             "#btn_mod_nom_volver,#btn_mod_pass_volver,#btn_mod_correo_volver,"
                                             "#btn_reg_pac_close,#btn_hist_pac_close,#btn_hist_pac_IMC,"
                                             "#btn_hist_pac_clean2,#btn_hist_pac_save,#btn_info_pac_buscar,"
                                             "#btn_info_pac_selec,#btn_info_pac_close,#btn_mod_pac_buscar,"
                                             "#btn_mod_pac_close,#btn_config_close{\n"
                                             "	border:1px solid #ffff00;\n"
                                             "	border-radius:8px;\n"
                                             "}\n"
                                             "QPushButton:hover,QPushButton:focus{\n"
                                             "	background:#862d00;\n"
                                             "	border-radius:15px;\n"
                                             "}")
            # ************************************************************************************************
            # FONDO BEIS CON LETRAS NEGRAS
            # ************************************************************************************************
        if tema1 == 4:
            self.ui.Frame_main.setStyleSheet("*{\n"
                                             # "    font: 75 italic 12pt \"Times New Roman\";\n"
                                             "	  color: rgb(0, 0, 0);\n"
                                             "}\n"
                                             "QFrame{\n"
                                             "	background-color: rgb(236, 201, 173);\n"
                                             "}\n"
                                             "QLineEdit{\n"
                                             "	background:transparent;\n"
                                             "	border-radius:20px;\n"
                                             "	border:1px solid #000000;\n"
                                             "}\n"
                                             "QLineEdit:focus,QPlainTextEdit:hover,QComboBox:hover{\n"
                                             "	background:#ff9500;\n"
                                             "}\n"
                                             "QPlainTextEdit{\n"
                                             "	border:1px solid #000000;\n"
                                             "}\n"
                                             "QCalendarWidget QWidget{\n"
                                             "	selection-color: rgb(0, 0, 0);\n"
                                             "  background-color: rgb(236, 201, 173);\n"
                                             "	alternate-background-color: rgb(236, 201, 173);\n"
                                             "	selection-background-color: rgb(255, 149, 0);\n"
                                             "}\n"
                                             "QSpinBox{\n"
                                             "  background-color:rgb(236, 201, 173);\n"
                                             "	border:1px solid #000000;\n"
                                             "	selection-color: rgb(0, 0, 0);\n"
                                             "	border-radius:12px;\n"
                                             "	selection-background-color: rgb(255, 149, 0);\n"
                                             "}\n"
                                             "QAbstractItemView{\n"
                                             "	background-color: rgb(236, 201, 173);\n"
                                             "	selection-color: rgb(0, 0, 0);\n"
                                             "	selection-background-color: rgb(255, 149, 0);\n"
                                             "}\n"
                                             "QComboBox{\n"
                                             "	border:1px solid #000000;\n"
                                             "	border-radius:20px;\n"
                                             "	background:transparent;\n"
                                             "	selection-background-color: rgb(255, 149, 0);\n"
                                             "}\n"
                                             "QHeaderView::section{\n"
                                             "	background-color: rgb(236, 201, 173);\n"
                                             "	border:1px solid #000000;\n"
                                             "}\n"
                                             "QDateEdit,QTimeEdit{\n"
                                             "  background-color:rgb(236, 201, 173);\n"
                                             "	border-radius:8px;\n"
                                             "	border:1px solid #000000;\n"
                                             "}\n"
                                             "QDateEdit:hover,QTimeEdit:hover{\n"
                                             "	background:#ff9500;\n"
                                             "	border-radius:8px;\n"
                                             "}\n"
                                             "QToolTip {\n"
                                             "  border: 1px solid #000000;\n"
                                             "  padding: 5px;\n"
                                             "  border-radius: 5px;\n"
                                             "  opacity: 200;\n"
                                             "	background-color: rgb(236, 201, 173);\n"
                                             "  }\n"
                                             "QTabWidget::pane{\n"
                                             "  border: 1px solid #000000;\n"
                                             "  top:-1px;\n"
                                             "	background:transparent;\n"
                                             "}\n"
                                             "QTabBar::tab{\n"
                                             "  border: 1px #000000;\n"
                                             "  padding: 10px;\n"
                                             "	background:transparent;\n"
                                             "}\n"
                                             "QTabBar::tab:selected{\n"
                                             "	margin-bottom: -1px;\n"
                                             "  border: 1px solid #000000;\n"
                                             "	border-radius:10px;\n"
                                             "}\n"
                                             "QTabBar::tab:hover{\n"
                                             "	background:#ff9500;\n"
                                             "	border-radius:10px;\n"
                                             "}\n"
                                             "QScrollBar:vertical{\n"
                                             "border: 1px solid #000000;\n"
                                             "background:transparent;\n"
                                             "width:10px;\n"
                                             "border-radius:5px;\n"
                                             "margin: 0px 0px 0px 0px;\n"
                                             "}\n"
                                             "QScrollBar:horizontal{\n"
                                             "border: 1px solid #000000;\n"
                                             "background:transparent;\n"
                                             "height:10px;\n"
                                             "border-radius:5px;\n"
                                             "margin: 0px 0px 0px 0px;\n"
                                             "}\n"
                                             "QScrollBar::handle:vertical {\n"
                                             "border: 1px solid #000000;\n"
                                             "border-radius:5px;\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(236, 201, 173), stop: 0.5 rgb(236, 201, 173), stop:1 rgb(236, 201, 173));\n"
                                             "min-height: 0px;\n"
                                             "}\n"
                                             "QScrollBar::handle:horizontal {\n"
                                             "border: 1px solid #000000;\n"
                                             "border-radius:5px;\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(236, 201, 173), stop: 0.5 rgb(236, 201, 173), stop:1 rgb(236, 201, 173));\n"
                                             "min-width: 0px;\n"
                                             "}\n"
                                             "QScrollBar::add-line:vertical {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(236, 201, 173), stop: 0.5 rgb(236, 201, 173),  stop:1 rgb(236, 201, 173));\n"
                                             "height: 0px;\n"
                                             "subcontrol-position: bottom;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::add-line:horizontal {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(236, 201, 173), stop: 0.5 rgb(236, 201, 173),  stop:1 rgb(236, 201, 173));\n"
                                             "width: 0px;\n"
                                             "subcontrol-position: right;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::sub-line:vertical {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0  rgb(236, 201, 173), stop: 0.5 rgb(236, 201, 173),  stop:1 rgb(236, 201, 173));\n"
                                             "height: 0 px;\n"
                                             "subcontrol-position: top;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::sub-line:horizontal {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0  rgb(236, 201, 173), stop: 0.5 rgb(236, 201, 173),  stop:1 rgb(236, 201, 173));\n"
                                             "width: 0 px;\n"
                                             "subcontrol-position: left;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::handle:vertical:hover,QScrollBar::handle:horizontal:hover{\n"
                                             "border-radius:5px;\n"
                                             "background:#ff9500;\n"
                                             "}\n"
                                             "QPushButton{\n"
                                             "	padding: 5px;\n"
                                             "	border:1px solid #000000;\n"
                                             "	border-radius:15px;\n"
                                             "}\n"
                                             "QPushButton#btn_config,#btn_salir,#btn_log_close,#btn_reg_close,"
                                             "#btn_recu_close,#btn_admi_user_volver,#btn_admin_historial_volver,"
                                             "#btn_admin_historial_buscar,#btn_reg_user_volver,#btn_mod_close,"
                                             "#btn_mod_nom_volver,#btn_mod_pass_volver,#btn_mod_correo_volver,"
                                             "#btn_reg_pac_close,#btn_hist_pac_close,#btn_hist_pac_IMC,"
                                             "#btn_hist_pac_clean2,#btn_hist_pac_save,#btn_info_pac_buscar,"
                                             "#btn_info_pac_selec,#btn_info_pac_close,#btn_mod_pac_buscar,"
                                             "#btn_mod_pac_close,#btn_config_close{\n"
                                             "	border:1px solid #000000;\n"
                                             "	border-radius:8px;\n"
                                             "}\n"
                                             "QPushButton:hover,QPushButton:focus{\n"
                                             "	background:#ff9500;\n"
                                             "	border-radius:15px;\n"
                                             "}")
            # ************************************************************************************************
            # FONDO CELESTE CON LETRAS NEGRAS
            # ************************************************************************************************
        if tema1 == 5:
            self.ui.Frame_main.setStyleSheet("*{\n"
                                             # "    font: 75 italic 12pt \"Times New Roman\";\n"
                                             "	  color: rgb(0, 0, 0);\n"
                                             "}\n"
                                             "QFrame{\n"
                                             "	background-color: rgb(170, 255, 255);\n"
                                             "}\n"
                                             "QLineEdit{\n"
                                             "	background:transparent;\n"
                                             "	border-radius:20px;\n"
                                             "	border:1px solid #000000;\n"
                                             "}\n"
                                             "QLineEdit:focus,QPlainTextEdit:hover,QComboBox:hover{\n"
                                             "	background:#e7e7e7;\n"
                                             "}\n"
                                             "QPlainTextEdit{\n"
                                             "	border:1px solid #000000;\n"
                                             "}\n"
                                             "QCalendarWidget QWidget{\n"
                                             "  background-color: rgb(170, 255, 255);\n"
                                             "	selection-color: rgb(0,0,0);\n"
                                             "	alternate-background-color: rgb(170, 255, 255);\n"
                                             "	selection-background-color: rgb(231, 231, 231);\n"
                                             "}\n"
                                             "QSpinBox{\n"
                                             "  background-color:rgb(170, 255, 255);\n"
                                             "	border:1px solid #000000;\n"
                                             "	selection-color: rgb(0,0,0);\n"
                                             "	border-radius:12px;\n"
                                             "	selection-background-color: rgb(231, 231, 231);\n"
                                             "}\n"
                                             "QAbstractItemView{\n"
                                             "	selection-color: rgb(0,0,0);\n"
                                             "	background-color: rgb(170, 255, 255);\n"
                                             "	selection-background-color: rgb(231, 231, 231);\n"
                                             "}\n"
                                             "QComboBox{\n"
                                             "	border:1px solid #000000;\n"
                                             "	border-radius:20px;\n"
                                             "	background:transparent;\n"
                                             "	selection-background-color: rgb(231, 231, 231);\n"
                                             "}\n"
                                             "QHeaderView::section{\n"
                                             "	background-color: rgb(170, 255, 255);\n"
                                             "	border:1px solid #000000;\n"
                                             "}\n"
                                             "QDateEdit,QTimeEdit{\n"
                                             "  background-color:rgb(170, 255, 255);\n"
                                             "	border-radius:8px;\n"
                                             "	border:1px solid #000000;\n"
                                             "}\n"
                                             "QDateEdit:hover,QTimeEdit:hover{\n"
                                             "	background:#e7e7e7;\n"
                                             "	border-radius:8px;\n"
                                             "}\n"
                                             "QToolTip {\n"
                                             "  border: 1px solid #000000;\n"
                                             "  padding: 5px;\n"
                                             "  border-radius: 5px;\n"
                                             "  opacity: 200;\n"
                                             "	background-color: rgb(170, 255, 255);\n"
                                             "  }\n"
                                             "QTabWidget::pane{\n"
                                             "  border: 1px solid #000000;\n"
                                             "  top:-1px;\n"
                                             "	background:transparent;\n"
                                             "}\n"
                                             "QTabBar::tab{\n"
                                             "  border: 1px #000000;\n"
                                             "  padding: 10px;\n"
                                             "	background:transparent;\n"
                                             "}\n"
                                             "QTabBar::tab:selected{\n"
                                             "	margin-bottom: -1px;\n"
                                             "  border: 1px solid #000000;\n"
                                             "	border-radius:10px;\n"
                                             "}\n"
                                             "QTabBar::tab:hover{\n"
                                             "	background:#e7e7e7;\n"
                                             "	border-radius:10px;\n"
                                             "}\n"
                                             "QScrollBar:vertical{\n"
                                             "border: 1px solid #000000;\n"
                                             "background:transparent;\n"
                                             "width:10px;\n"
                                             "border-radius:5px;\n"
                                             "margin: 0px 0px 0px 0px;\n"
                                             "}\n"
                                             "QScrollBar:horizontal{\n"
                                             "border: 1px solid #000000;\n"
                                             "background:transparent;\n"
                                             "height:10px;\n"
                                             "border-radius:5px;\n"
                                             "margin: 0px 0px 0px 0px;\n"
                                             "}\n"
                                             "QScrollBar::handle:vertical {\n"
                                             "	border:1px solid #000000;\n"
                                             "	border-radius:5px;\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(170, 255, 255), stop: 0.5 rgb(170, 255, 255), stop:1 rgb(170, 255, 255));\n"
                                             "min-height: 0px;\n"
                                             "}\n"
                                             "QScrollBar::handle:horizontal {\n"
                                             "	border:1px solid #000000;\n"
                                             "	border-radius:5px;\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(170, 255, 255), stop: 0.5 rgb(170, 255, 255), stop:1 rgb(170, 255, 255));\n"
                                             "min-width: 0px;\n"
                                             "}\n"
                                             "QScrollBar::add-line:vertical {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(170, 255, 255), stop: 0.5 rgb(170, 255, 255),  stop:1 rgb(170, 255, 255));\n"
                                             "height: 0px;\n"
                                             "subcontrol-position: bottom;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::add-line:horizontal {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0 rgb(170, 255, 255), stop: 0.5 rgb(170, 255, 255),  stop:1 rgb(170, 255, 255));\n"
                                             "width: 0px;\n"
                                             "subcontrol-position: right;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::sub-line:vertical {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0  rgb(170, 255, 255), stop: 0.5 rgb(170, 255, 255),  stop:1 rgb(170, 255, 255));\n"
                                             "height: 0 px;\n"
                                             "subcontrol-position: top;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::sub-line:horizontal {\n"
                                             "background: qlineargradient(x1:0, y1:0, x2:1, y2:0,stop: 0  rgb(170, 255, 255), stop: 0.5 rgb(170, 255, 255),  stop:1 rgb(170, 255, 255));\n"
                                             "width: 0 px;\n"
                                             "subcontrol-position: left;\n"
                                             "subcontrol-origin: margin;\n"
                                             "}\n"
                                             "QScrollBar::handle:vertical:hover,QScrollBar::handle:horizontal:hover{\n"
                                             "border-radius:5px;\n"
                                             "background:#e7e7e7;\n"
                                             "}\n"
                                             "QPushButton{\n"
                                             "	padding: 5px;\n"
                                             "	border:1px solid #000000;\n"
                                             "	border-radius:15px;\n"
                                             "}\n"
                                             "QPushButton#btn_config,#btn_salir,#btn_log_close,#btn_reg_close,"
                                             "#btn_recu_close,#btn_admi_user_volver,#btn_admin_historial_volver,"
                                             "#btn_admin_historial_buscar,#btn_reg_user_volver,#btn_mod_close,"
                                             "#btn_mod_nom_volver,#btn_mod_pass_volver,#btn_mod_correo_volver,"
                                             "#btn_reg_pac_close,#btn_hist_pac_close,#btn_hist_pac_IMC,"
                                             "#btn_hist_pac_clean2,#btn_hist_pac_save,#btn_info_pac_buscar,"
                                             "#btn_info_pac_selec,#btn_info_pac_close,#btn_mod_pac_buscar,"
                                             "#btn_mod_pac_close,#btn_config_close{\n"
                                             "	border:1px solid #000000;\n"
                                             "	border-radius:8px;\n"
                                             "}\n"
                                             "QPushButton:hover,QPushButton:focus{\n"
                                             "	background:#e7e7e7;\n"
                                             "	border-radius:15px;\n"
                                             "}")
            # ************************************************************************************************
            # FONDO POR DEFECTO
            # ************************************************************************************************
        if tema1 == 6 or tema1 == 0:
            self.ui.Frame_main.setStyleSheet("*{\n"
                                             "    font: 75 12pt \"Times New Roman\";\n"
                                             "}")
    # endregion
    # region m??todo uestra la hora y la fecha
    def MostrarHora_fecha(self):
        tiempoactual = QTime.currentTime()
        fechaactual = QDate.currentDate()
        tiempo = tiempoactual.toString('hh:mm')
        fecha = fechaactual.toString(Qt.DefaultLocaleLongDate)
        self.ui.lbl_fecha.setText(fecha)
        self.ui.lcdNumber.display(tiempo)
        fecha1 = fechaactual.toString('dd/MM/yyyy')
        fecha2 = '{} {}'.format(fecha1, tiempo)
        self.ui.lbl_hist_pac_date1.setText(fecha2)
    # endregion
    # region sobreescribir evento de presionar enter
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
            wfocus = QApplication.focusWidget()  # obtenemos el widget que tiene el focus
            if wfocus in self.les:  # verificamos que se encuentre en la lista
                ix = self.les.index(wfocus)  # obtenemos el indice del QLineEdit
                if ix != len(self.les) - 1:  # cambiamos el focus si no es el ultimo
                    self.les[ix + 1].setFocus()
            if wfocus ==self.ui.btn_log_iniciar:
                self.Verifica()
        QMainWindow.keyPressEvent(self, event)
    # endregion
    # region Validacion de entradas con expresiones regulares
    def Validar_valores_intro(self):
        # validar sin espacios
        reg = QRegExp('[a-zA-Z0-9????????????????????????????]+$')
        # Crea un validador
        valida = QRegExpValidator(self)
        valida.setRegExp(reg)
        # validar letras y espacios
        reg1 = QRegExp('[a-zA-Z???????????????????????????? ]+$')
        valida1 = QRegExpValidator(self)
        valida1.setRegExp(reg1)
        # Crea segundo validador para el correo
        reg2 = QRegExp('[A-Za-z0-9\.\+_-]+@[A-Za-z0-9\._-]+\.[a-zA-Z]*$')
        valida2 = QRegExpValidator(self)
        valida2.setRegExp(reg2)
        # Validar letras y numeros sin espacios
        reg3 = QRegExp('[a-zA-Z0-9]+$')
        valida3 = QRegExpValidator(self)
        valida3.setRegExp(reg3)
        # Validar solo numeros
        reg4 = QRegExp('[0-9]{6,8}$')
        valida4 = QRegExpValidator(self)
        valida4.setRegExp(reg4)
        # validar numeros decimales
        reg5 = QRegExp('^(([0-9]+\.[0-9]*[1-9][0-9]*)|([0-9]*[1-9][0-9]*\.[0-9]+)|([0-9]*[1-9][0-9]*))$')
        valida5 = QRegExpValidator(self)
        valida5.setRegExp(reg5)
        reg6=QRegExp('[A-Z0-9]+-[A-Z0-9]+$')
        valida6 = QRegExpValidator(self)
        valida6.setRegExp(reg6)
        # --------------------------------------------------------------------------------------------------
        # aplicando las validaciones
        self.Validar_entrada(valida, valida1, valida2, valida3, valida4, valida5,valida6)
    # endregion
    # region Validar entrada de datos
    def Validar_entrada(self, valida, valida1, valida2, valida3, valida4, valida5,valida6):
        """
        Los valores de entrada vienen del m??todo de expresiones regulares
        :param valida: letras + num + caracteres especiales sin espacios
        :param valida1: letras + caracteres especiales con espacios
        :param valida2: correos
        :param valida3: letras + num sin espacios
        :param valida4: numeros sin espacios
        :param valida5: numeros decimales
        :param valida6: numeros mas guion y letras mayusculas
        """
        # *************************************************
        # modulo de inicio de sesi??n
        self.ui.txt_log_user.setValidator(valida)
        self.ui.txt_log_pass.setValidator(valida)
        # modulo de registro nuevo usuario
        self.ui.txt_reg_user_CI.setValidator(valida6)
        self.ui.txt_reg_user_mat.setValidator(valida6)
        self.ui.txt_reg_nom_user.setValidator(valida1)
        self.ui.txt_reg_apell1_user.setValidator(valida1)
        self.ui.txt_reg_apell2_user.setValidator(valida1)
        self.ui.txt_reg_pass.setValidator(valida)
        self.ui.txt_reg_pass1.setValidator(valida)
        self.ui.txt_reg_correo_user.setValidator(valida2)
        # modulo de recuperacion de contrase??a
        self.ui.txt_recu_user.setValidator(valida)
        self.ui.txt_recu_correo.setValidator(valida2)
        self.ui.txt_recu_codigo.setValidator(valida3)
        self.ui.txt_recu_contra1.setValidator(valida)
        self.ui.txt_recu_contra2.setValidator(valida)
        # modulo de habilitacion o deshabilitacion de usuario
        self.ui.txt_admin_nombre.setValidator(valida1)
        self.ui.txt_admin_app1.setValidator(valida1)
        self.ui.txt_admin_app2.setValidator(valida1)
        # modulo de registro nuevo usuario
        self.ui.txt_reg_user.setValidator(valida)
        # modulo registro nuevo paciente
        self.ui.txt_reg_pac_CI.setValidator(valida6)
        self.ui.txt_reg_pac_CI_padre.setValidator(valida6)
        self.ui.txt_reg_pac_CI_madre.setValidator(valida6)
        self.ui.txt_reg_pac_nom.setValidator(valida1)
        self.ui.txt_reg_pac_app1.setValidator(valida1)
        self.ui.txt_reg_pac_app2.setValidator(valida1)
        self.ui.txt_reg_pac_tall.setValidator(valida5)
        self.ui.txt_reg_pac_pes.setValidator(valida5)
        self.ui.txt_reg_pac_padre.setValidator(valida1)
        self.ui.txt_reg_pac_padre1.setValidator(valida1)
        self.ui.txt_reg_pac_padre2.setValidator(valida1)
        self.ui.txt_reg_pac_tel1.setValidator(valida4)
        self.ui.txt_reg_pac_madre.setValidator(valida1)
        self.ui.txt_reg_pac_madre1.setValidator(valida1)
        self.ui.txt_reg_pac_madre2.setValidator(valida1)
        self.ui.txt_reg_pac_tel2.setValidator(valida4)
        # modulo de busqueda de paciente
        self.ui.txt_hist_pac_nom.setValidator(valida1)
        self.ui.txt_hist_pac_app1.setValidator(valida1)
        self.ui.txt_hist_pac_app2.setValidator(valida1)
        # modulo de registro nueva consulta
        self.ui.txt_hist_pac_fc.setValidator(valida4)
        self.ui.txt_hist_pac_fr.setValidator(valida4)
        self.ui.txt_hist_pac_temp.setValidator(valida5)
        self.ui.txt_hist_pac_SO.setValidator(valida4)
        self.ui.txt_hist_pac_pa1.setValidator(valida4)
        self.ui.txt_hist_pac_pa2.setValidator(valida4)
        self.ui.txt_hist_pac_percef.setValidator(valida5)
        self.ui.txt_hist_pac_pes.setValidator(valida5)
        self.ui.txt_hist_pac_tall.setValidator(valida5)
        # modulo de consulta de historias
        self.ui.txt_info_pac_nom.setValidator(valida1)
        self.ui.txt_info_pac_app1.setValidator(valida1)
        self.ui.txt_info_pac_app2.setValidator(valida1)
    # endregion
    # ----------------------------------------------------------------------------------------
    # METODOS PARA MOSTRAR PDF y para mostrar en tablas
    # ----------------------------------------------------------------------------------------
    #region Enviar los datos a la ventana de vista de pdf
    def Enviar_datos(self,caso,texto,nombre):
        if caso==1:
            html = """
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="UTF-8">
            <style>
            h3 {
                font-family: Times New Roman;
                text-align: center;
               }
            h2 {
                font-family: Times New Roman;
                text-align: center;
               }
            h1 {
                font-family: Times New Roman;
                text-align: center;
               }
            table {
                   font-family: Times New Roman;
                   border-collapse: collapse;
                   width: 100%;
                  }
            td {
                font-size:12pt;
                text-align: left;
                padding-top: 4px;
                padding-right: 6px;
                padding-bottom: 2px;
                padding-left: 6px;
               }
            th {
                text-align: left;
                padding: 4px;
                background-color: black;
                color: white;
               }
            tr:nth-child(even) {
                                background-color: #dddddd;
                               }
            </style>
            </head>
            <body>
            <h1>Sistema de Informaci??n de historiales Cl??nicos Ped??atricos<br/></h1>
            <h1>"Consultorio Ped??atrico Divino Ni??o Jes??s"<br/></h1>
            <h2>Creaci??n de Cuenta de Usuario<br/></h2>
              [DATOS]
            </body>
            </html>
            """
            self.main=pdf_visualizar.Visualizador_pdf(texto,html,nombre)
            self.main.Buscar(1)
            self.main.vistaPrevia()
    #endregion
    #region Crear el formato en html para el pdf de reporte de consulta
    def Crear_html(self,entrada):
        html = """
                    <!DOCTYPE html>
                    <html>
                    <head>
                    <meta charset="UTF-8">
                    <style>
                    h3 {
                        font-family: Times New Roman;
                        text-align: center;
                       }
                    h2 {
                        font-family: Times New Roman;
                        text-align: center;
                       }
                    h1 {
                        font-family: Times New Roman;
                        text-align: center;
                       }
                    table {
                           font-family: Times New Roman;
                           border-collapse: collapse;
                           width: 100%;
                          }
                    td {
                        font-size:12pt;
                        text-align: left;
                        padding-top: 4px;
                        padding-right: 6px;
                        padding-bottom: 2px;
                        padding-left: 6px;
                       }
                    th {
                        text-align: left;
                        padding: 4px;
                        background-color: black;
                        color: white;
                       }
                    tr:nth-child(even) {
                                        background-color: #dddddd;
                                       }
                    </style>
                    </head>
                    <body>
                    <h1>Sistema de Informaci??n de historiales Cl??nicos Ped??atricos</h1>
                    <h1>"Consultorio Pedi??trico Divino Ni??o Jes??s"</h1>
                    <h2>Historial Cl??nico del paciente<br/></h2>
                    <table border="1" align="left" width="100%" cellspacing="0">
                      [DATOS1]
                      [DATOS2]
                      [DATOS3]
                      [DATOS4]
                      [DATOS5]
                      [DATOS6]
                      [DATOS7]
                      [DATOS8]
                    </table>
                    <hr>
                    <h2>Consulta detallada<br/></h2>
                      <table border="1" align="left" width="100%" cellspacing="0">
                      [DATOS9]
                      [DATOS10]
                      [DATOS11]
                    </table>
                    </body>
                    </html>
                    """
        datos = ""
        for dato in entrada[0]:
            datos += "<tr><td width='300'>%s</td><td>%s</td></tr>" % dato
        html = html.replace("[DATOS1]", datos)
        datos=""
        for dato in entrada[1]:
            datos += "<tr><td colspan='2'>%s</td></tr>" % dato
        html = html.replace("[DATOS2]", datos)
        datos = ""
        for dato in entrada[2]:
            datos += "<tr><td>%s</td><td>%s</td></tr>" % dato
        html = html.replace("[DATOS3]", datos)
        datos = ""
        for dato in entrada[3]:
            datos += "<tr><td colspan='2'>%s</td></tr>" % dato
        html = html.replace("[DATOS4]", datos)
        datos = ""
        for dato in entrada[4]:
            datos += "<tr><td>%s</td><td>%s</td></tr>" % dato
        html = html.replace("[DATOS5]", datos)
        datos = ""
        for dato in entrada[5]:
            datos += "<tr><td colspan='2'>%s</td></tr>" % dato
        html = html.replace("[DATOS6]", datos)
        datos = ""
        for dato in entrada[6]:
            datos += "<tr><td>%s</td><td>%s</td></tr>" % dato
        html = html.replace("[DATOS7]", datos)
        datos = ""
        for dato in entrada[7]:
            datos += "<tr><td colspan='2'>%s</td></tr>" % dato
        html1 = html.replace("[DATOS8]", datos)
        return html1
    #endregion
    #region Mostrar los datos de la tabla
    def Datos_tabla(self,caso,respuesta):
        if caso==1:
            Tabla=self.ui.Tabla_admin_user
        if caso==2:
            Tabla=self.ui.Tabla_hist_pac
        if caso==3:
            Tabla=self.ui.Tabla_info_pac1
        if caso==4:
            Tabla=self.ui.Tabla_info_pac2
        if caso==5:
            Tabla=self.ui.Tabla_admin_historial
        Tabla.clearContents()
        Tabla.setRowCount(0)
        if caso==1:
            fila = 0
            for datos in respuesta:
                Tabla.setRowCount(fila + 1)
                dato = str(fila + 1)
                id_dato = QTableWidgetItem(dato)
                Tabla.setItem(fila, 0, id_dato)
                c = 1
                for i in datos:
                    if i == True:
                        i = "Habilitado"
                    elif i == False:
                        i = "Inhabilitado"
                    Tabla.setItem(fila, c, QTableWidgetItem(i))
                    c += 1
                fila += 1
        if caso==2:
            fila = 0
            for datos in respuesta:
                Tabla.setRowCount(fila + 1)
                Tabla.setItem(fila, 0, QTableWidgetItem(datos[0]))
                Tabla.setItem(fila, 1, QTableWidgetItem(datos[1].strftime('%Y-%m-%d')))
                Tabla.setItem(fila, 2, QTableWidgetItem(datos[2]))
                Tabla.setItem(fila, 3, QTableWidgetItem(datos[3]))
                Tabla.setItem(fila, 4, QTableWidgetItem(datos[4]))
                Tabla.setItem(fila, 5, QTableWidgetItem(datos[5].strftime('%Y-%m-%d')))
                fila+=1
        if caso==3:
            fila = 0
            for datos in respuesta:
                Tabla.setRowCount(fila + 1)
                Tabla.setItem(fila, 0, QTableWidgetItem(datos[0]))
                Tabla.setItem(fila, 1, QTableWidgetItem(datos[1].strftime('%Y-%m-%d')))
                Tabla.setItem(fila, 2, QTableWidgetItem(datos[2]))
                Tabla.setItem(fila, 3, QTableWidgetItem(datos[3]))
                Tabla.setItem(fila, 4, QTableWidgetItem(datos[4]))
                fila+=1
        if caso==4:
            fila = 0
            for datos in respuesta:
                Tabla.setRowCount(fila + 1)
                Tabla.setItem(fila, 0, QTableWidgetItem(datos[0].strftime('%Y-%m-%d')))
                dato=datos[1].split("-")
                if dato[0]=='CON':
                    Tabla.setItem(fila, 1, QTableWidgetItem("Consulta"))
                if dato[0]=='REC':
                    Tabla.setItem(fila, 1, QTableWidgetItem("Reconsulta"))
                if dato[0]=='EME':
                    Tabla.setItem(fila, 1, QTableWidgetItem("Emergencia"))
                fila+=1
        if caso==5:
            fila = 0
            for datos in respuesta:
                Tabla.setRowCount(fila + 1)
                dato=datos[0].strftime('%Y-%m-%d %H:%M')
                dato=dato.split(" ")
                fecha=dato[0]
                hora=dato[1]
                nombre="{} {} {}".format(datos[1],datos[2],datos[3])
                Tabla.setItem(fila, 0, QTableWidgetItem(fecha))
                Tabla.setItem(fila, 1, QTableWidgetItem(hora))
                Tabla.setItem(fila, 2, QTableWidgetItem(nombre))
                Tabla.setItem(fila, 3, QTableWidgetItem(datos[4]))
                Tabla.setItem(fila, 4, QTableWidgetItem(datos[5]))
                Tabla.setItem(fila, 5, QTableWidgetItem(datos[6]))
                fila+=1

    #endregion
    #region Metodo para seleccionar los items recuperados y ponerlos en la tabla
    def Seleccionar_item_tabla(self,caso):
        global x
        global reg_pac
        global datos_paciente
        global html
        global fecha_nac1
        global bbdd_paciente
        global bbdd_carnet_pac
        global bbdd_antec_pac
        global bbdd_padre
        global bbdd_madre
        global bbdd_carnet_padre
        global bbdd_carnet_madre
        global bbdd_tel1
        global bbdd_tel2
        if caso ==1:
            elegida = self.ui.Tabla_admin_user.selectedItems()
            if elegida:
                seleccionada = [dato.text() for dato in elegida]
                seleccionada = tuple(seleccionada)
                if seleccionada[5]=="Habilitado":
                    mensaje="El usuario {} {} {} ya se encuentra habilitado".format(seleccionada[1].upper(),
                                                                                    seleccionada[2].upper(),
                                                                                    seleccionada[3].upper())
                    QMessageBox.critical(self,"Mensaje de error",mensaje)
                else:
                    resp=self.Habilitacion(caso,seleccionada)
                    if resp==1:
                        mensaje = "Se ha Habilitado al usuario: {} {} {}".format(seleccionada[1].upper(),
                                                                                          seleccionada[2].upper(),
                                                                                          seleccionada[3].upper())
                        QMessageBox.information(self,"Informaci??n de resultado",mensaje)
                    else:
                        QMessageBox.critical(self,"Mensaje de error","Ha ocurrido alg??n error y no se pudo realizar los cambios")

            else:
                QMessageBox.critical(self,"Mensaje de error","Debe selecionar un nombre de la tabla para habilitar")
        if caso == 2:
            elegida = self.ui.Tabla_admin_user.selectedItems()
            if elegida:
                seleccionada = [dato.text() for dato in elegida]
                seleccionada = tuple(seleccionada)
                if seleccionada[5] == "Inhabilitado":
                    mensaje = "El usuario {} {} {} ya se encuentra inhabilitado".format(seleccionada[1].upper(),
                                                                                      seleccionada[2].upper(),
                                                                                      seleccionada[3].upper())
                    QMessageBox.critical(self, "Mensaje de error", mensaje)
                else:
                    resp = self.Habilitacion(caso, seleccionada)
                    if resp == 1:
                        mensaje = "Se ha inhabilitado al usuario: {} {} {}".format(seleccionada[1].upper(),
                                                                                 seleccionada[2].upper(),
                                                                                 seleccionada[3].upper())
                        QMessageBox.information(self, "Informaci??n de resultado", mensaje)
                    else:
                        QMessageBox.critical(self, "Mensaje de error", "Ha ocurrido alg??n error y no se pudo realizar los cambios")

            else:
                QMessageBox.critical(self, "Mensaje de error", "Debe selecionar un nombre de la tabla para inhabilitar")
        if caso==3:
            elegida=self.ui.Tabla_hist_pac.selectedItems()
            if elegida:
                seleccionada=[dato.text() for dato in elegida]
                seleccionada=tuple(seleccionada)
                if x==1:
                    nombre="{} {} {}".format(seleccionada[2].capitalize(),seleccionada[3].capitalize(),seleccionada[4].capitalize())
                    codigo=seleccionada[0]
                    valor = "paciente", codigo
                    resp1 = self.Select_bbdd("patologicos", "antecedentes", valor)
                    if resp1[0] == 1:
                        # region registro en la tabla historial
                        enviar_datos = 9, str(codigo), 3, "antecedentes"
                        self.Registro_tabla_historial(enviar_datos)
                        # endregion
                        patologicos = resp1[1]
                        resp2=self.Select_bbdd("alergias", "antecedentes", valor)
                        if resp2[0]==1:
                            # region registro en la tabla historial
                            enviar_datos = 9, str(codigo), 3, "antecedentes"
                            self.Registro_tabla_historial(enviar_datos)
                            # endregion
                            alergias=resp2[1]
                            datos = (nombre, codigo, patologicos, alergias)
                            x=0
                            self.ui.Stacked_main.setCurrentIndex(8)
                            self.Ventana_reg_hist2(datos)
                    else:
                        patologicos="No se encontr?? nada en la base de datos"
                        alergias = "No se encontr?? nada en la base de datos"
                        datos = (nombre, codigo, patologicos, alergias)
                        x = 0
                        self.ui.Stacked_main.setCurrentIndex(8)
                        self.Ventana_reg_hist2(datos)
                if x==2:
                    codigo_paciente = seleccionada[0]
                    resp = self.Buscar_datos_paciente(1, codigo_paciente)
                    if resp[0] == 1:
                        datos = resp[1]
                        bbdd_paciente=datos
                        # region registro en la tabla historial
                        enviar_datos = 9, str(codigo_paciente), 3, "paciente, persona"
                        self.Registro_tabla_historial(enviar_datos)
                        # endregion
                        self.ui.txt_reg_pac_nom.setText(datos[0])
                        self.ui.txt_reg_pac_app1.setText(datos[1])
                        self.ui.txt_reg_pac_app2.setText(datos[2])
                        fecha_nac = datos[3].strftime('%Y-%m-%d')
                        temporal = fecha_nac.split('-')
                        fecha_nac = QDate(int(temporal[0]), int(temporal[1]), int(temporal[2]))
                        self.ui.date_reg_pac_nac.setDate(fecha_nac)
                        self.ui.cb_reg_pac_sex.setCurrentIndex(datos[4])
                        self.ui.cb_reg_pac_gs.setCurrentIndex(datos[5])
                        self.ui.cb_reg_pac_gsf.setCurrentIndex(datos[6])
                        self.ui.txt_reg_pac_pes.setText(str(datos[11]))
                        self.ui.txt_reg_pac_tall.setText(str(datos[12]))
                        self.ui.txt_reg_pac_pro1.setText(datos[7])
                        self.ui.txt_reg_pac_res1.setText(datos[8])
                        self.ui.txt_reg_pac_dir.setText(datos[9])
                        self.ui.txt_reg_pac_barr.setText(datos[10])
                        resp1 = self.Buscar_datos_paciente(2, codigo_paciente)
                        if resp1[0] == 1:
                            # region registro en la tabla historial
                            enviar_datos = 9, str(codigo_paciente), 3, "antecedentes"
                            self.Registro_tabla_historial(enviar_datos)
                            # endregion
                            if resp1[1]!=None:
                                datos = resp1[1]
                                bbdd_antec_pac=datos
                                self.ui.pt_reg_pac_ap.setPlainText(datos[1])
                                self.ui.pt_reg_pac_alerg.setPlainText(datos[2])
                            else:
                                bbdd_antec_pac = []
                        else:
                            bbdd_antec_pac=[]
                        resp2 = self.Buscar_datos_paciente(3, codigo_paciente)
                        if resp2[0] == 1:
                            if resp2[1] != None:
                                # region registro en la tabla historial
                                enviar_datos = 9, str(codigo_paciente), 3, "carnet"
                                self.Registro_tabla_historial(enviar_datos)
                                # endregion
                                datos = resp2[1]
                                bbdd_carnet_pac=datos
                                self.ui.txt_reg_pac_CI.setText(datos[1])
                                self.ui.cb_reg_pac_CI.setCurrentIndex(datos[2])
                            else:
                                bbdd_carnet_pac=[]
                        else:
                            bbdd_carnet_pac=[]
                        resp3 = self.Buscar_datos_paciente(4, codigo_paciente)
                        if resp3[0] == 1:
                            # region registro en la tabla historial
                            enviar_datos = 9, str(codigo_paciente), 3, "familiar"
                            self.Registro_tabla_historial(enviar_datos)
                            # endregion
                            datos = resp3[1]
                            if len(datos) > 1:
                                dato1 = datos[0]
                                id_fam1 = dato1[0]
                                nom_fam1 = dato1[1]
                                app1_fam1 = dato1[2]
                                app2_fam1 = dato1[3]
                                tipo_fam1 = dato1[4]
                                dato2 = datos[1]
                                id_fam2 = dato2[0]
                                nom_fam2 = dato2[1]
                                app1_fam2 = dato2[2]
                                app2_fam2 = dato2[3]
                                tipo_fam2 = dato2[4]
                                if tipo_fam1 == 1:
                                    bbdd_padre=dato1
                                    bbdd_madre=dato2
                                    self.ui.txt_reg_pac_padre.setText(nom_fam1)
                                    self.ui.txt_reg_pac_padre1.setText(app1_fam1)
                                    self.ui.txt_reg_pac_padre2.setText(app2_fam1)
                                    self.ui.txt_reg_pac_madre.setText(nom_fam2)
                                    self.ui.txt_reg_pac_madre1.setText(app1_fam2)
                                    self.ui.txt_reg_pac_madre2.setText(app2_fam2)
                                    resp4 = self.Buscar_datos_paciente(5, id_fam1)
                                    if resp4[0] == 1:
                                        if resp4[1] != None:
                                            # region registro en la tabla historial
                                            enviar_datos = 9, str(id_fam1), 3, "carnet"
                                            self.Registro_tabla_historial(enviar_datos)
                                            # endregion
                                            datos = resp4[1]
                                            bbdd_carnet_padre=datos
                                            self.ui.txt_reg_pac_CI_padre.setText(datos[0])
                                            self.ui.cb_reg_pac_CI_padre.setCurrentIndex(datos[1])
                                        else:
                                            bbdd_carnet_padre=[]
                                    else:
                                        bbdd_carnet_padre=[]
                                    resp5 = self.Buscar_datos_paciente(5, id_fam2)
                                    if resp5[0] == 1:
                                        if resp5[1] != None:
                                            # region registro en la tabla historial
                                            enviar_datos = 9, str(id_fam2), 3, "carnet"
                                            self.Registro_tabla_historial(enviar_datos)
                                            # endregion
                                            datos = resp5[1]
                                            bbdd_carnet_madre=datos
                                            self.ui.txt_reg_pac_CI_madre.setText(datos[0])
                                            self.ui.cb_reg_pac_CI_madre.setCurrentIndex(datos[1])
                                        else:
                                            bbdd_carnet_madre=[]
                                    else:
                                        bbdd_carnet_madre=[]
                                    columna = "numero"
                                    tabla = "telefono"
                                    valor = "familiar", id_fam1
                                    resp6 = self.Select_bbdd(columna, tabla, valor)
                                    if resp6[0] == 1:
                                        # region registro en la tabla historial
                                        enviar_datos = 9, str(id_fam1), 3, "telefono"
                                        self.Registro_tabla_historial(enviar_datos)
                                        # endregion
                                        bbdd_tel1=resp6[1]
                                        print(bbdd_tel1)
                                        self.ui.txt_reg_pac_tel1.setText(str(resp6[1]))
                                    else:
                                        bbdd_tel1=""
                                    valor = "familiar", id_fam2
                                    resp7 = self.Select_bbdd(columna, tabla, valor)
                                    if resp7[0] == 1:
                                        # region registro en la tabla historial
                                        enviar_datos = 9, str(id_fam2), 3, "telefono"
                                        self.Registro_tabla_historial(enviar_datos)
                                        # endregion
                                        bbdd_tel2=resp7[1]
                                        self.ui.txt_reg_pac_tel2.setText(str(resp7[1]))
                                    else:
                                        bbdd_tel2=""
                                else:
                                    bbdd_padre = dato2
                                    bbdd_madre = dato1
                                    self.ui.txt_reg_pac_padre.setText(nom_fam2)
                                    self.ui.txt_reg_pac_padre1.setText(app1_fam2)
                                    self.ui.txt_reg_pac_padre2.setText(app2_fam2)
                                    self.ui.txt_reg_pac_madre.setText(nom_fam1)
                                    self.ui.txt_reg_pac_madre1.setText(app1_fam1)
                                    self.ui.txt_reg_pac_madre2.setText(app2_fam1)
                                    resp4 = self.Buscar_datos_paciente(5, id_fam1)
                                    if resp4[0] == 1:
                                        if resp4[1] != None:
                                            # region registro en la tabla historial
                                            enviar_datos = 9, str(id_fam1), 3, "carnet"
                                            self.Registro_tabla_historial(enviar_datos)
                                            # endregion
                                            datos = resp4[1]
                                            bbdd_carnet_madre=datos
                                            self.ui.txt_reg_pac_CI_madre.setText(datos[0])
                                            self.ui.cb_reg_pac_CI_madre.setCurrentIndex(datos[1])
                                        else:
                                            bbdd_carnet_madre=[]
                                    else:
                                        bbdd_carnet_madre=[]
                                    resp5 = self.Buscar_datos_paciente(5, id_fam2)
                                    if resp5[0] == 1:
                                        if resp5[1] != None:
                                            # region registro en la tabla historial
                                            enviar_datos = 9, str(id_fam2), 3, "carnet"
                                            self.Registro_tabla_historial(enviar_datos)
                                            # endregion
                                            datos = resp5[1]
                                            bbdd_carnet_padre=datos
                                            self.ui.txt_reg_pac_CI_padre.setText(datos[0])
                                            self.ui.cb_reg_pac_CI_padre.setCurrentIndex(datos[1])
                                        else:
                                            bbdd_carnet_padre=[]
                                    else:
                                        bbdd_carnet_padre=[]
                                    columna = "numero"
                                    tabla = "telefono"
                                    valor = "familiar", id_fam1
                                    resp6 = self.Select_bbdd(columna, tabla, valor)
                                    if resp6[0] == 1:
                                        # region registro en la tabla historial
                                        enviar_datos = 9, str(id_fam1), 3, "telefono"
                                        self.Registro_tabla_historial(enviar_datos)
                                        # endregion
                                        bbdd_tel2=resp6[1]
                                        self.ui.txt_reg_pac_tel2.setText(str(resp6[1]))
                                    else:
                                        bbdd_tel2=""
                                    valor = "familiar", id_fam2
                                    resp7 = self.Select_bbdd(columna, tabla, valor)
                                    if resp7[0] == 1:
                                        # region registro en la tabla historial
                                        enviar_datos = 9, str(id_fam2), 3, "telefono"
                                        self.Registro_tabla_historial(enviar_datos)
                                        # endregion
                                        bbdd_tel1=resp7[1]
                                        self.ui.txt_reg_pac_tel1.setText(str(resp7[1]))
                                    else:
                                        bbdd_tel1=""
                            else:
                                dato1 = datos[0]
                                id_fam1 = dato1[0]
                                nom_fam1 = dato1[1]
                                app1_fam1 = dato1[2]
                                app2_fam1 = dato1[3]
                                tipo_fam1 = dato1[4]
                                if tipo_fam1 == 1:
                                    bbdd_padre = dato1
                                    bbdd_madre = []
                                    self.ui.txt_reg_pac_padre.setText(nom_fam1)
                                    self.ui.txt_reg_pac_padre1.setText(app1_fam1)
                                    self.ui.txt_reg_pac_padre2.setText(app2_fam1)
                                    resp4 = self.Buscar_datos_paciente(5, id_fam1)
                                    if resp4[0] == 1:
                                        if resp4[1] != None:
                                            # region registro en la tabla historial
                                            enviar_datos = 9, str(id_fam1), 3, "carnet"
                                            self.Registro_tabla_historial(enviar_datos)
                                            # endregion
                                            datos = resp4[1]
                                            bbdd_carnet_padre=datos
                                            bbdd_carnet_madre=[]
                                            self.ui.txt_reg_pac_CI_padre.setText(datos[0])
                                            self.ui.cb_reg_pac_CI_padre.setCurrentIndex(datos[1])
                                        else:
                                            bbdd_carnet_padre=[]
                                            bbdd_carnet_madre=[]
                                    else:
                                        bbdd_carnet_padre = []
                                        bbdd_carnet_madre = []
                                    columna = "numero"
                                    tabla = "telefono"
                                    valor = "familiar", id_fam1
                                    resp6 = self.Select_bbdd(columna, tabla, valor)
                                    if resp6[0] == 1:
                                        # region registro en la tabla historial
                                        enviar_datos = 9, str(id_fam1), 3, "telefono"
                                        self.Registro_tabla_historial(enviar_datos)
                                        # endregion
                                        bbdd_tel1=resp6[1]
                                        bbdd_tel2=""
                                        self.ui.txt_reg_pac_tel1.setText(str(resp6[1]))
                                    else:
                                        bbdd_tel1=""
                                        bbdd_tel2=""
                                else:
                                    bbdd_padre = []
                                    bbdd_madre = dato1
                                    self.ui.txt_reg_pac_madre.setText(nom_fam1)
                                    self.ui.txt_reg_pac_madre1.setText(app1_fam1)
                                    self.ui.txt_reg_pac_madre2.setText(app2_fam1)
                                    resp4 = self.Buscar_datos_paciente(5, id_fam1)
                                    if resp4[0] == 1:
                                        if resp4[1] != None:
                                            # region registro en la tabla historial
                                            enviar_datos = 9, str(id_fam1), 3, "carnet"
                                            self.Registro_tabla_historial(enviar_datos)
                                            # endregion
                                            datos = resp4[1]
                                            bbdd_carnet_madre=datos
                                            bbdd_carnet_padre=[]
                                            self.ui.txt_reg_pac_CI_madre.setText(datos[0])
                                            self.ui.cb_reg_pac_CI_madre.setCurrentIndex(datos[1])
                                        else:
                                            bbdd_carnet_madre=[]
                                            bbdd_carnet_padre=[]
                                    else:
                                        bbdd_carnet_madre = []
                                        bbdd_carnet_padre = []
                                    columna = "numero"
                                    tabla = "telefono"
                                    valor = "familiar", id_fam1
                                    resp6 = self.Select_bbdd(columna, tabla, valor)
                                    if resp6[0] == 1:
                                        # region registro en la tabla historial
                                        enviar_datos = 9, str(id_fam1), 3, "telefono"
                                        self.Registro_tabla_historial(enviar_datos)
                                        # endregion
                                        bbdd_tel2=resp6[1]
                                        bbdd_tel1=""
                                        self.ui.txt_reg_pac_tel2.setText(str(resp6[1]))
                                    else:
                                        bbdd_tel2=""
                                        bbdd_tel1=""
                    x=0
                    self.Ventana_reg_pac(2)
            else:
                QMessageBox.critical(self,"Mensaje de error","Debe seleccionar un nombre de la tabla para continuar")
        if caso==4:
            sex = ['Masculino', 'Femenino']
            grup = ['A', 'B', 'AB', '0', 'No sabe']
            fac = ['Positivo', 'Negativo', 'No sabe']
            ex = ['CH', 'LP', 'CB', 'OR', 'PT', 'TJ', 'SC', 'BE', 'PD', 'Otro pa??s']
            elegida =self.ui.Tabla_info_pac1.selectedItems()
            if elegida:
                seleccionada=[dato.text() for dato in elegida]
                seleccionada=tuple(seleccionada)
                datos_paciente=self.Busqueda_paciente(8,seleccionada[0],seleccionada[0],seleccionada[0])
                codigo_paciente1=seleccionada[0]
                if datos_paciente:
                    # region registro en la tabla historial
                    enviar_datos = 9, str(codigo_paciente1), 3, "consultas, fecha"
                    self.Registro_tabla_historial(enviar_datos)
                    # endregion
                    resp = self.Buscar_datos_paciente(1, codigo_paciente1)
                    if resp[0] == 1:
                        # region registro en la tabla historial
                        enviar_datos = 9, str(codigo_paciente1), 3, "persona, paciente, dato_general"
                        self.Registro_tabla_historial(enviar_datos)
                        # endregion
                        datos = resp[1]
                        nombre = '{} {} {}'.format(datos[0], datos[1], datos[2])
                        fecha_nac1 = datos[3]
                        fecha_nac = datos[3].strftime('%Y-%m-%d')
                        sexo = sex[datos[4] - 1]
                        grupo = grup[datos[5] - 1]
                        factor = fac[datos[6] - 1]
                        proce = datos[7]
                        resi = datos[8]
                        direc = datos[9]
                        barr = datos[10]
                        peso1 = datos[11]
                        talla1 = datos[12]
                        if peso1 == 0.000 or talla1 == 0.00:
                            IMC1 = "Talla fuera de rango"
                        else:
                            talla1 = round(talla1 / 100, 2)
                            IMC1 = self.Calcu_IMC(peso1, talla1)
                        resp1 = self.Buscar_datos_paciente(2, codigo_paciente1)
                        if resp1[0] == 1:
                            # region registro en la tabla historial
                            enviar_datos = 9, str(codigo_paciente1), 3, "antecedentes"
                            self.Registro_tabla_historial(enviar_datos)
                            # endregion
                            if resp1[1]!=None:
                                datos = resp1[1]
                                antecedentes = datos[1]
                                alergias = datos[2]
                            else:
                                antecedentes = "No tiene antecedentes patol??gicos"
                                alergias = "No posee alergias"
                        else:
                            antecedentes = "No tiene antecedentes patol??gicos"
                            alergias = "No posee alergias"
                        resp2 = self.Buscar_datos_paciente(3, codigo_paciente1)
                        if resp2[0] == 1:
                            if resp2[1]!=None:
                                # region registro en la tabla historial
                                enviar_datos = 9, str(codigo_paciente1), 3, "carnet"
                                self.Registro_tabla_historial(enviar_datos)
                                # endregion
                                datos = resp2[1]
                                carnet = datos[1]
                                extension = ex[datos[2] - 1]
                            else:
                                carnet = "No tiene registro"
                                extension = "--"
                        else:
                            carnet = "No tiene registro"
                            extension = "--"
                        resp3 = self.Buscar_datos_paciente(4, codigo_paciente1)
                        if resp3[0] == 1:
                            # region registro en la tabla historial
                            enviar_datos = 9, str(codigo_paciente1), 3, "familiar"
                            self.Registro_tabla_historial(enviar_datos)
                            # endregion
                            datos = resp3[1]
                            if len(datos) > 1:
                                dato1 = datos[0]
                                id_fam1 = dato1[0]
                                nom_fam1 = dato1[1]
                                app1_fam1 = dato1[2]
                                app2_fam1 = dato1[3]
                                tipo_fam1 = dato1[4]
                                dato2 = datos[1]
                                id_fam2 = dato2[0]
                                nom_fam2 = dato2[1]
                                app1_fam2 = dato2[2]
                                app2_fam2 = dato2[3]
                                tipo_fam2 = dato2[4]
                                if tipo_fam1 == 1:
                                    nom_padre = '{} {} {}'.format(nom_fam1, app1_fam1, app2_fam1)
                                    nom_madre = '{} {} {}'.format(nom_fam2, app1_fam2, app2_fam2)
                                    resp4 = self.Buscar_datos_paciente(5, id_fam1)
                                    if resp4[0] == 1:
                                        if resp4[1] != None:
                                            # region registro en la tabla historial
                                            enviar_datos = 9, str(id_fam1), 3, "carnet"
                                            self.Registro_tabla_historial(enviar_datos)
                                            # endregion
                                            datos = resp4[1]
                                            carnet1 = datos[0]
                                            extension1 = ex[datos[1] - 1]
                                        else:
                                            carnet1 = "No tiene registro"
                                            extension1 = "--"
                                    else:
                                        carnet1 = "No tiene registro"
                                        extension1 = "--"
                                    resp5 = self.Buscar_datos_paciente(5, id_fam2)
                                    if resp5[0] == 1:
                                        if resp5[1] != None:
                                            # region registro en la tabla historial
                                            enviar_datos = 9, str(id_fam2), 3, "carnet"
                                            self.Registro_tabla_historial(enviar_datos)
                                            # endregion
                                            datos = resp5[1]
                                            carnet2 = datos[0]
                                            extension2 = ex[datos[1] - 1]
                                        else:
                                            carnet2 = "No tiene registro"
                                            extension2 = "--"
                                    else:
                                        carnet2 = "No tiene registro"
                                        extension2 = "--"
                                    columna = "numero"
                                    tabla = "telefono"
                                    valor = "familiar", id_fam1
                                    resp6 = self.Select_bbdd(columna, tabla, valor)
                                    if resp6[0] == 1:
                                        # region registro en la tabla historial
                                        enviar_datos = 9, str(id_fam1), 3, "telefono"
                                        self.Registro_tabla_historial(enviar_datos)
                                        # endregion
                                        tel1 = resp6[1]
                                    else:
                                        tel1 = "No tiene n??mero registrado"
                                    columna = "numero"
                                    tabla = "telefono"
                                    valor = "familiar", id_fam2
                                    resp7 = self.Select_bbdd(columna, tabla, valor)
                                    if resp7[0] == 1:
                                        # region registro en la tabla historial
                                        enviar_datos = 9, str(id_fam2), 3, "telefono"
                                        self.Registro_tabla_historial(enviar_datos)
                                        # endregion
                                        tel2 = resp7[1]
                                    else:
                                        tel2 = "No tiene n??mero registrado"
                                else:
                                    nom_madre = '{} {} {}'.format(nom_fam1, app1_fam1, app2_fam1)
                                    nom_padre = '{} {} {}'.format(nom_fam2, app1_fam2, app2_fam2)
                                    resp4 = self.Buscar_datos_paciente(5, id_fam2)
                                    if resp4[0] == 1:
                                        if resp4[1] != None:
                                            # region registro en la tabla historial
                                            enviar_datos = 9, str(id_fam1), 3, "carnet"
                                            self.Registro_tabla_historial(enviar_datos)
                                            # endregion
                                            datos = resp4[1]
                                            carnet1 = datos[0]
                                            extension1 = ex[datos[1] - 1]
                                        else:
                                            carnet1 = "No tiene registro"
                                            extension1 = "--"
                                    else:
                                        carnet1 = "No tiene registro"
                                        extension1 = "--"
                                    resp5 = self.Buscar_datos_paciente(5, id_fam1)
                                    if resp5[0] == 1:
                                        if resp5[1] != None:
                                            # region registro en la tabla historial
                                            enviar_datos = 9, str(id_fam2), 3, "carnet"
                                            self.Registro_tabla_historial(enviar_datos)
                                            # endregion
                                            datos = resp5[1]
                                            carnet2 = datos[0]
                                            extension2 = ex[datos[1] - 1]
                                        else:
                                            carnet2 = "No tiene registro"
                                            extension2 = "--"
                                    else:
                                        carnet2 = "No tiene registro"
                                        extension2 = "--"
                                    columna = "numero"
                                    tabla = "telefono"
                                    valor = "familiar", id_fam2
                                    resp6 = self.Select_bbdd(columna, tabla, valor)
                                    if resp6[0] == 1:
                                        # region registro en la tabla historial
                                        enviar_datos = 9, str(id_fam1), 3, "telefono"
                                        self.Registro_tabla_historial(enviar_datos)
                                        # endregion
                                        tel1 = resp6[1]
                                    else:
                                        tel1 = "No tiene n??mero registrado"
                                    columna = "numero"
                                    tabla = "telefono"
                                    valor = "familiar", id_fam1
                                    resp7 = self.Select_bbdd(columna, tabla, valor)
                                    if resp7[0] == 1:
                                        # region registro en la tabla historial
                                        enviar_datos = 9, str(id_fam2), 3, "telefono"
                                        self.Registro_tabla_historial(enviar_datos)
                                        # endregion
                                        tel2 = resp7[1]
                                    else:
                                        tel2 = "No tiene n??mero registrado"
                            else:
                                dato1 = datos[0]
                                id_fam1 = dato1[0]
                                nom_fam1 = dato1[1]
                                app1_fam1 = dato1[2]
                                app2_fam1 = dato1[3]
                                tipo_fam1 = dato1[4]
                                if tipo_fam1 == 1:
                                    nom_padre = '{} {} {}'.format(nom_fam1, app1_fam1, app2_fam1)
                                    nom_madre = 'No tiene registro'
                                    resp4 = self.Buscar_datos_paciente(5, id_fam1)
                                    if resp4[0] == 1:
                                        if resp4[1] != None:
                                            # region registro en la tabla historial
                                            enviar_datos = 9, str(id_fam1), 3, "carnet"
                                            self.Registro_tabla_historial(enviar_datos)
                                            # endregion
                                            datos = resp4[1]
                                            carnet1 = datos[0]
                                            extension1 = ex[datos[1] - 1]
                                        else:
                                            carnet1 = "No tiene registro"
                                            extension1 = "--"
                                    else:
                                        carnet1 = "No tiene registro"
                                        extension1 = "--"
                                    carnet2 = "No tiene registro"
                                    extension2 = "--"
                                    columna = "numero"
                                    tabla = "telefono"
                                    valor = "familiar", id_fam1
                                    resp6 = self.Select_bbdd(columna, tabla, valor)
                                    if resp6[0] == 1:
                                        # region registro en la tabla historial
                                        enviar_datos = 9, str(id_fam1), 3, "telefono"
                                        self.Registro_tabla_historial(enviar_datos)
                                        # endregion
                                        tel1 = resp6[1]
                                    else:
                                        tel1 = "No tiene n??mero"
                                    tel2 = "No tiene n??mero registrado"
                                else:
                                    nom_padre = 'No tiene registro'
                                    nom_madre = '{} {} {}'.format(nom_fam1, app1_fam1, app2_fam1)
                                    resp4 = self.Buscar_datos_paciente(5, id_fam1)
                                    if resp4[0] == 1:
                                        if resp4[1] != None:
                                            # region registro en la tabla historial
                                            enviar_datos = 9, str(id_fam1), 3, "carnet"
                                            self.Registro_tabla_historial(enviar_datos)
                                            # endregion
                                            datos = resp4[1]
                                            carnet2 = datos[0]
                                            extension2 = ex[datos[1] - 1]
                                        else:
                                            carnet2 = "No tiene registro"
                                            extension2 = "--"
                                    else:
                                        carnet2 = "No tiene registro"
                                        extension2 = "--"
                                    carnet1 = "No tiene registro"
                                    extension1 = "--"
                                    columna = "numero"
                                    tabla = "telefono"
                                    valor = "familiar", id_fam1
                                    resp6 = self.Select_bbdd(columna, tabla, valor)
                                    if resp6[0] == 1:
                                        # region registro en la tabla historial
                                        enviar_datos = 9, str(id_fam1), 3, "telefono"
                                        self.Registro_tabla_historial(enviar_datos)
                                        # endregion
                                        tel2 = resp6[1]
                                    else:
                                        tel2 = "No tiene n??mero"
                                    tel1 = "No tiene n??mero registrado"
                    enviar1 = "C??digo de paciente: {} ".format(codigo_paciente1)
                    enviar2 = "Fecha de nacimiento: {}".format(fecha_nac)
                    enviar3="Nombre del paciente: {}".format(nombre)
                    enviar4="Sexo: {}".format(sexo)
                    enviar5="CI: {} {}".format(carnet,extension)
                    enviar6="Grupo y Factor sanguineo: {} {}".format(grupo,factor)
                    enviar7="Procedencia: {}".format(proce)
                    enviar8="Residencia: {}".format(resi)
                    enviar9="Direcci??n: {}".format(direc)
                    enviar10="Barrio: {}".format(barr)
                    enviar11="Peso de Nacimiento: {} [Kg]".format(peso1)
                    enviar12="Talla de nacimiento: {} [m]".format(talla1)
                    enviar13="IMC: {}".format(IMC1)
                    enviar14="Nombre del padre: {}".format(nom_padre)
                    enviar15="CI: {} {}".format(carnet1,extension1)
                    enviar16="Tel??fono o celular: {}".format(tel1)
                    enviar17 = "Nombre de la madre: {}".format(nom_madre)
                    enviar18 = "CI: {} {}".format(carnet2,extension2)
                    enviar19="Tel??fono o celular: {}".format(tel2)
                    enviar20="Antecedentes patol??gicos: {}".format(antecedentes)
                    enviar21="Alergias: {}".format(alergias)
                    texto1=((enviar1,enviar2),(enviar3,enviar4),(enviar5,enviar6))
                    texto2=(enviar7,enviar8,enviar9,enviar10)
                    texto3=((enviar11,enviar12),)
                    texto4=(enviar13,enviar14)
                    texto5=((enviar15,enviar16),)
                    texto6=(enviar17,)
                    texto7=((enviar18,enviar19),)
                    texto8=(enviar20,enviar21)
                    texto=(texto1,texto2,texto3,texto4,texto5,texto6,texto7,texto8)
                    html=self.Crear_html(texto)
                    self.Datos_tabla(4, datos_paciente)
            else:
                QMessageBox.critical(self,"Mensaje de error","Debe elegir a un paciente para ver sus consultas")
        if caso==5:
            elegida=self.ui.Tabla_info_pac2.selectedItems()
            if elegida:
                seleccionada=[dato.text() for dato in elegida]
                seleccionada=tuple(seleccionada)
                for i in datos_paciente:
                    if i[0].strftime('%Y-%m-%d') == seleccionada[0]:
                        codigo_consulta=i[1]
                resp8=self.Buscar_datos_paciente(6,codigo_consulta)
                if resp8[0]==1:
                    # region registro en la tabla historial
                    enviar_datos = 9, str(codigo_consulta), 3, "consulta, fecha"
                    self.Registro_tabla_historial(enviar_datos)
                    # endregion
                    datos=resp8[1]
                    dr='Dr. {} {} {}'.format(datos[0],datos[1],datos[2])
                    fecha_ate1=datos[3].strftime('%Y-%m-%d')
                    temporal=fecha_ate1.split('-')
                    fecha_ate1=QDate(int(temporal[0]),int(temporal[1]),int(temporal[2]))
                    fecha_ate=datos[3].strftime('%Y-%m-%d %H:%M')
                    frec_car=datos[4]
                    frec_resp=datos[5]
                    temp=datos[6]
                    resp = Clases.Metodos.Temp_verf(temp)
                    if resp == 1:
                        temp="{} ??C Hipotermia".format(temp)
                    elif resp == 2:
                        temp = "{} ??C Normal".format(temp)
                    elif resp == 3:
                        temp = "{} ??C Febr??cula".format(temp)
                    elif resp == 4:
                        temp = "{} ??C Fiebre".format(temp)
                    sat=datos[7]
                    presion=datos[8]
                    per_cef=datos[9]
                    edad=self.Calcular_fecha(fecha_nac1, fecha_ate1)
                    peso2 = datos[10]
                    talla2 = datos[11]
                    if peso2 == 0.000 or talla2 == 0.00:
                        IMC2 = "No se puede calcular con una altura igual a 0"
                    else:
                        talla2 = round(talla2 / 100, 2)
                        IMC2 = self.Calcu_IMC(peso2, talla2)
                    motivo=datos[12]
                    examen=datos[13]
                    diag=datos[14]
                    trat=datos[15]
                    obs=datos[16]
                    prox=datos[17].strftime('%Y-%m-%d')
                    enviar1="M??dico encargado de la atenci??n: {}".format(dr)
                    enviar2="Fecha y hora de atenci??n: {}".format(fecha_ate)
                    enviar3="Frecuencia cardiaca: {} ".format(frec_car)
                    enviar4="Frecuencia respiratoria: {}".format(frec_resp)
                    enviar5="Temperatura: {}".format(temp)
                    enviar6="Per??metro cef??lico: {}[cm]".format(per_cef)
                    enviar7="Saturaci??n de ox??geno: {}%".format(sat)
                    enviar8="Presi??n arterial: {}".format(presion)
                    enviar9 = "Peso: {} [Kg]".format(peso2)
                    enviar10="Talla: {} [m]".format(talla2)
                    enviar11 = "IMC: {}".format(IMC2)
                    enviar12="Edad: {}".format(edad)
                    enviar13="Motivo de la consulta (SUBJETIVO): {}".format(motivo)
                    enviar14="Examen f??sico (OBJETIVO): {}".format(examen)
                    enviar15="Diagn??stico (AN??LISIS): {}".format(diag)
                    enviar16="Tratamiento (PLAN): {}".format(trat)
                    enviar17="Observaciones: {}".format(obs)
                    enviar18="Pr??xima revisi??n: {}".format(prox)
                    texto1=(enviar1,enviar2)
                    texto2=((enviar3,enviar4),(enviar5,enviar6),(enviar7,enviar8),(enviar9,enviar10),(enviar11,enviar12))
                    texto3=(enviar13,enviar14,enviar15,enviar16,enviar17,enviar18)
                    texto=(texto1,texto2,texto3)
                    self.main = pdf_visualizar.Visualizador_pdf(texto, html, "Historial de consulta")
                    self.main.Buscar(2)
                    self.main.vistaPrevia()
                else:
                    QMessageBox.critical(self,"Mensaje de error","No se pudo encontrar la Consulta solicitada")
            else:
                QMessageBox.critical(self,"Mensaje de error","Debe elegir una consulta para verla, imprimirla o guardarla")
    #endregion
    #region metodo que toma la letra inicial del nombre, app, app y crea una clave
    def Creador_id(self):
        global persona
        tupla=persona[1],persona[2],persona[3]
        e = 0
        k = ""
        for i in tupla:
            e = 0
            for j in i:
                if e == 0:
                    k = k + j
                e += 1
        return k.upper()
    #endregion
    #region Crea un nuevo codigo para enviar a las tablas
    def Nuevo_codigo(self,resultado):
        nombre = resultado.split("-")
        valor = int(nombre[1]) + 1
        id_nuevo = nombre[0] + "-{}".format(valor)
        return id_nuevo
    #endregion
    # region Probar la conexion a internet
    def Probar_conexion(self):
        try:
            requests.get('http://www.google.com/', timeout=5)
            resp = 1
        except:
            resp = 0
        return resp
    #endregion
    # ----------------------------------------------------------------------------------------
    #METODOS PARA POSTGRES
    # ----------------------------------------------------------------------------------------
    #region Logeo a la bbdd
    def Logeo_postgres(self,user,con):
        global usuario
        global contra
        conn=""
        try:
            conn = psycopg2.connect(
                host=Clases.Metodos.Obtener_datos('HOST'),
                database=Clases.Metodos.Obtener_datos('DATABASE'),
                port=Clases.Metodos.Obtener_datos('PORT'),
                user=user,
                password=con
            )
            resp=1
        except:
            resp=0
        finally:
            if conn!="":
                conn.close()

        if resp==1:
            usuario=user
            contra=con
        return resp
    #endregion
    #region Comprobar si el usuario esta en la bbdd
    def Comprobar_usuario(self,user):
        global usuario
        global contra
        conn=""
        try:
            conn = psycopg2.connect(
                host=Clases.Metodos.Obtener_datos('HOST'),
                database=Clases.Metodos.Obtener_datos('DATABASE'),
                port=Clases.Metodos.Obtener_datos('PORT'),
                user=usuario,
                password=contra
            )
            cursor=conn.cursor()
            cursor.execute('SELECT 1 FROM pg_user WHERE usename=%s',(user,))
            resultado=cursor.fetchall()
            if not resultado:
                resp=0
            else:
                for i in resultado:
                    for j in i:
                        resp=int(j)
        except:
            resp=0
        finally:
            if conn!="":
                cursor.close()
                conn.close()
        return resp
    #endregion
    #region Creacion de nuevo usuario medico
    def Crear_usuario(self,user,password):
        global usuario
        global contra
        conn=""
        try:
            conn = psycopg2.connect(
                host=Clases.Metodos.Obtener_datos('HOST'),
                database=Clases.Metodos.Obtener_datos('DATABASE'),
                port=Clases.Metodos.Obtener_datos('PORT'),
                user=usuario,
                password=contra
            )
            cursor=conn.cursor()
            query = sql.SQL("CREATE USER {username} WITH LOGIN PASSWORD {password}").format(
                username=sql.Identifier(user),
                password=sql.Placeholder()
            )
            cursor.execute(query, (password,))
            query = sql.SQL("GRANT grupo_medico TO {username}").format(
                username=sql.Identifier(user)
            )
            cursor.execute(query)
            conn.commit()
            resp=1
        except:
            resp=0
        finally:
            if conn!="":
                cursor.close()
                conn.close()
        return resp
    #endregion
    #region Reset de contrase??a:
    def Reset_pass(self,caso,user,contras):
        global usuario
        global contra
        conn=""
        try:
            if caso==1:
                conn = psycopg2.connect(
                    host=Clases.Metodos.Obtener_datos('HOST'),
                    database=Clases.Metodos.Obtener_datos('DATABASE'),
                    port=Clases.Metodos.Obtener_datos('PORT'),
                    user=usuario,
                    password=contra
                )
                cursor=conn.cursor()
                query = sql.SQL("ALTER USER {username} PASSWORD {password}").format(
                    username=sql.Identifier(user),
                    password=sql.Placeholder()
                )
                cursor.execute(query,(contras,))
                conn.commit()
                resp=1
            if caso==2:
                conn = psycopg2.connect(
                    host=Clases.Metodos.Obtener_datos('HOST'),
                    database=Clases.Metodos.Obtener_datos('DATABASE'),
                    port=Clases.Metodos.Obtener_datos('PORT'),
                    user=Clases.Metodos.Obtener_datos('USER'),
                    password=Clases.Metodos.Obtener_datos('PASSWORD')
                )
                cursor=conn.cursor()
                query = sql.SQL("ALTER USER {username} PASSWORD {password}").format(
                    username=sql.Identifier(user),
                    password=sql.Placeholder()
                )
                cursor.execute(query,(contras,))
                conn.commit()
                resp=1
        except:
            resp=0
        finally:
            if conn!="":
                cursor.close()
                conn.close()
        return resp
    #endregion
    #region Busqueda de usuario
    def Busqueda_user(self,caso,nom,app1,app2):
        global usuario
        global contra
        conn=""
        try:
            conn = psycopg2.connect(
                host=Clases.Metodos.Obtener_datos('HOST'),
                database=Clases.Metodos.Obtener_datos('DATABASE'),
                port=Clases.Metodos.Obtener_datos('PORT'),
                user=usuario,
                password=contra
            )
            cursor=conn.cursor()
            if caso==1:
                cursor.execute('SELECT * FROM busqueda_user1(%s)', (nom,))
            if caso==2:
                cursor.execute('SELECT * FROM busqueda_user2(%s)', (app1,))
            if caso==3:
                cursor.execute('SELECT * FROM busqueda_user3(%s)', (app2,))
            if caso==4:
                cursor.execute('SELECT * FROM busqueda_user4(%s,%s)', (nom,app1,))
            if caso==5:
                cursor.execute('SELECT * FROM busqueda_user5(%s,%s)', (nom,app2,))
            if caso==6:
                cursor.execute('SELECT * FROM busqueda_user6(%s,%s)', (app1,app2,))
            if caso==7:
                cursor.execute('SELECT * FROM busqueda_user7(%s,%s,%s)', (nom,app1,app2,))
            resultado=cursor.fetchall()
        except:
            resultado=[]
        finally:
            if conn!="":
                cursor.close()
                conn.close()
        return resultado
    #endregion
    #region Busqueda de datos del paciente para ver en el reporte de historial
    def Buscar_datos_paciente(self,caso,busqueda):
        global usuario
        global contra
        conn = ""
        try:
            conn = psycopg2.connect(
                host=Clases.Metodos.Obtener_datos('HOST'),
                database=Clases.Metodos.Obtener_datos('DATABASE'),
                port=Clases.Metodos.Obtener_datos('PORT'),
                user=usuario,
                password=contra
            )
            cursor = conn.cursor()
            if caso==1:
                cursor.execute('select * from busq_datos_pac(%s)',(busqueda,))
                resp=cursor.fetchone()
            if caso==2:
                cursor.execute('select * from busq_ante_pac(%s)',(busqueda,))
                resp = cursor.fetchone()
            if caso==3:
                cursor.execute('select * from busq_carnet_pac(%s)',(busqueda,))
                resp = cursor.fetchone()
            if caso==4:
                cursor.execute('select * from busq_fam_pac(%s)',(busqueda,))
                resp = cursor.fetchall()
            if caso==5:
                cursor.execute('select * from busq_carnet_fam(%s)',(busqueda,))
                resp = cursor.fetchone()
            if caso==6:
                cursor.execute('select * from busq_consul_pac(%s)',(busqueda,))
                resp = cursor.fetchone()
            resp1=1
        except:
            resp=None
            resp1=0
        finally:
            if conn!="":
                cursor.close()
                conn.close()
        return resp1,resp
    #endregion
    #region Busqueda de paciente
    def Busqueda_paciente(self,caso,nom,app1,app2):
        global usuario
        global contra
        conn = ""
        try:
            conn = psycopg2.connect(
                host=Clases.Metodos.Obtener_datos('HOST'),
                database=Clases.Metodos.Obtener_datos('DATABASE'),
                port=Clases.Metodos.Obtener_datos('PORT'),
                user=usuario,
                password=contra
            )
            cursor = conn.cursor()
            if caso == 1:
                cursor.execute('SELECT * FROM busqueda_paciente1(%s)', (nom,))
            if caso == 2:
                cursor.execute('SELECT * FROM busqueda_paciente2(%s)', (app1,))
            if caso == 3:
                cursor.execute('SELECT * FROM busqueda_paciente3(%s)', (app2,))
            if caso == 4:
                cursor.execute('SELECT * FROM busqueda_paciente4(%s,%s)', (nom, app1,))
            if caso == 5:
                cursor.execute('SELECT * FROM busqueda_paciente5(%s,%s)', (nom, app2,))
            if caso == 6:
                cursor.execute('SELECT * FROM busqueda_paciente6(%s,%s)', (app1, app2,))
            if caso == 7:
                cursor.execute('SELECT * FROM busqueda_paciente7(%s,%s,%s)', (nom, app1, app2,))
            if caso==8:
                cursor.execute('SELECT * FROM busqueda_consulta(%s)',(nom,))
            resultado = cursor.fetchall()
        except:
            resultado = []
        finally:
            if conn != "":
                cursor.close()
                conn.close()
        return resultado
    #endregion
    #region Habilitacion e inhabilitacion de usuario
    def Habilitacion(self,caso,tupla):
        global usuario
        global contra
        conn = ""
        try:
            conn = psycopg2.connect(
                host=Clases.Metodos.Obtener_datos('HOST'),
                database=Clases.Metodos.Obtener_datos('DATABASE'),
                port=Clases.Metodos.Obtener_datos('PORT'),
                user=usuario,
                password=contra
            )
            cursor = conn.cursor()
            query='select usuario, validaciones from medico inner join persona p on p.id_persona = medico.id_persona where p.nombre=%s and p.apellido1=%s and p.apellido2=%s'
            cursor.execute(query,(tupla[1],tupla[2],tupla[3]))
            resultado=cursor.fetchone()
            if resultado:
                user=resultado[0]
                valid=resultado[1]
            else:
                user=""
                valid=0
            if caso==1:
                cursor.execute('SELECT * FROM habil(%s)',(valid,))
                query = sql.SQL("ALTER USER {username} LOGIN").format(
                    username=sql.Identifier(user)
                )
                cursor.execute(query)
                conn.commit()
                resp=1
            if caso==2:
                print("AQUI")
                cursor.execute('SELECT * FROM inhabil(%s)',(valid,))
                query = sql.SQL("ALTER USER {username} NOLOGIN").format(
                    username=sql.Identifier(user)
                )
                cursor.execute(query)
                conn.commit()
                resp = 1
        except:
            resp=0
        finally:
            if conn!="":
                cursor.close()
                conn.close()
        return resp
    #endregion
    #region Inserta en cualquier tabla de la base de datos
    def Insertar_bbdd(self,tabla,columnas,valores):
        '''
        ESTE MODULO INSERTA DATOS EN A BBDD
        :param tabla: debe ser un string que ingresa el nombre de la tabla a la cual se desea insertar los datos
        :param columnas: debe ser un string con los datos en tabla ejem: "Nombre,Apellido,correo"
        :param valores: los valores correspondientes a esas colummnas
        :return: devuelve un booleano para saber si fue o no correcta la entrada de datos
        '''
        global usuario
        global contra
        conn=""
        c = 0
        val = ""
        while c < len(valores) - 1:
            val = val + '%s' + ","
            c += 1
        val = val + '%s'
        query = 'INSERT INTO ' + tabla + '(' + columnas + ') VALUES (' + val + ')'
        try:
            conn = psycopg2.connect(
                host=Clases.Metodos.Obtener_datos('HOST'),
                database=Clases.Metodos.Obtener_datos('DATABASE'),
                port=Clases.Metodos.Obtener_datos('PORT'),
                user=usuario,
                password=contra
            )
            cursor=conn.cursor()
            cursor.execute(query,valores)
            conn.commit()
            resp=1
        except:
            resp=0
        finally:
            if conn!="":
                cursor.close()
                conn.close()
        return resp
    #endregion
    # region Puede actualizar cualquier tabla en la bbdd
    def Update_bbdd(self,caso, tabla, columnas, id_tabla, valores):
        '''
        ESTE MODULO ACTUALIZA DATOS EN LA BBDD
        :param caso: si es con usuario o admi
        :param tabla: es un string que contiene el nombre de la tabla a la cual se desea hacer la actualizacion
        :param columnas: es un vector de string ejmp: "columna1","columna2" que se desea actualizar
        :param id_tabla: es el valor que identifica al id es decir el nombre de esa columna
        :param valores: todos los valores de las colummnas a ser modificadas y el identificador al ultimo para saber a cual
        :return: retorna un booleano 1 para correcto 0 incorrecto
        '''
        global usuario
        global contra
        c = len(columnas)
        a = 0
        val = ""
        if c > 1:
            while a < c - 1:
                val = val + columnas[a] + '=%s,'
                a += 1
            val = val + columnas[c - 1] + '=%s'
        else:
            val = val + columnas[0] + '=%s'
        conn = ""
        try:
            if caso==1:
                conn = psycopg2.connect(
                    host=Clases.Metodos.Obtener_datos('HOST'),
                    database=Clases.Metodos.Obtener_datos('DATABASE'),
                    port=Clases.Metodos.Obtener_datos('PORT'),
                    user=Clases.Metodos.Obtener_datos('USER'),
                    password=Clases.Metodos.Obtener_datos('PASSWORD')
                )
            if caso==2:
                conn = psycopg2.connect(
                    host=Clases.Metodos.Obtener_datos('HOST'),
                    database=Clases.Metodos.Obtener_datos('DATABASE'),
                    port=Clases.Metodos.Obtener_datos('PORT'),
                    user=usuario,
                    password=contra
                )
            cursor = conn.cursor()
            query = 'UPDATE ' + tabla + ' set ' + val + ' where ' + id_tabla + '=%s'
            cursor.execute(query, valores)
            conn.commit()
            resp = 1
        except:
            resp = 0
        finally:
            if conn != "":
                cursor.close()
                conn.close()
        return resp
    # endregion
    #region Puede hacer un select al campo deseado en cualquier tabla de la bbdd
    def Select_bbdd(self,columna,tabla,valor):
        '''
        ESTE MODULO PERMITE BUSCAR UNA COLUMNA EN CUALQUIER TABLA
        :param columna: es la columna que se desea encontrar su valor
        :param tabla: es la tabla a la cual pertenece esa columna
        :param valor: un vector del nombre la columna llave y la llave
        :return: retorna un booleano y el valor buscado
        '''
        global usuario
        global contra
        tipo = valor[0]
        buscado = valor[1]
        conn = ""
        try:
            conn = psycopg2.connect(
                host=Clases.Metodos.Obtener_datos('HOST'),
                database=Clases.Metodos.Obtener_datos('DATABASE'),
                port=Clases.Metodos.Obtener_datos('PORT'),
                user=usuario,
                password=contra
            )
            cursor = conn.cursor()
            query = 'SELECT ' + columna + ' FROM ' + tabla + ' WHERE ' + tipo + '=%s'
            cursor.execute(query, (buscado,))
            resp = cursor.fetchone()[0]
            if resp == None:
                resp1 = 0
            else:
                resp1 = 1
        except:
            resp1 = 0
            resp = 0
        finally:
            if conn != "":
                cursor.close()
                conn.close()
        return resp1, resp
    #endregion
    #region Consigue el id de las tablas seriales
    def Conseguir_id_tabla(self,caso,id_querido,tabla):
        global usuario
        global contra
        conn = ""
        query='SELECT max('+id_querido+') FROM '+tabla
        try:
            conn = psycopg2.connect(
                host=Clases.Metodos.Obtener_datos('HOST'),
                database=Clases.Metodos.Obtener_datos('DATABASE'),
                port=Clases.Metodos.Obtener_datos('PORT'),
                user=usuario,
                password=contra
            )
            cursor = conn.cursor()
            cursor.execute(query)
            if caso==1:
                resp = cursor.fetchone()[0]
                if resp == None:
                    resp = 1
                else:
                    resp = int(resp) + 1
        except:
            resp=0
        finally:
            if conn!="":
                cursor.close()
                conn.close()
        return resp
    #endregion
    #region Verifica que el id sea unico y si no lo es aumenta en 1 el valor
    def Verifica_id_crea_id(self,caso,id_persona):
        global usuario
        global contra
        conn = ""
        try:
            conn = psycopg2.connect(
                host=Clases.Metodos.Obtener_datos('HOST'),
                database=Clases.Metodos.Obtener_datos('DATABASE'),
                port=Clases.Metodos.Obtener_datos('PORT'),
                user=usuario,
                password=contra
            )
            cursor=conn.cursor()
            buscado = id_persona + "%"
            if caso == 1:
                query = sql.SQL("select all id_persona from persona where id_persona like {buscado1}").format(
                    buscado1=sql.Placeholder()
                )
            if caso == 2:
                query = sql.SQL("select all id_paciente from paciente where id_paciente like {buscado1}").format(
                    buscado1=sql.Placeholder()
                )
            if caso == 3:
                query = sql.SQL("select all id_familiar from familiar where id_familiar like {buscado1}").format(
                    buscado1=sql.Placeholder()
                )
            if caso == 4:
                query = sql.SQL("select all id_consulta from consulta where id_consulta like {buscado1}").format(
                    buscado1=sql.Placeholder()
                )
            cursor.execute(query, (buscado,))
            resultado = cursor.fetchall()
            if not resultado:
                id_nuevo = id_persona + "-1"
            else:
                n = len(resultado)
                id_nuevo = resultado[n - 1]
                id_nuevo = id_nuevo[0]
                id_nuevo=self.Nuevo_codigo(id_nuevo)
            resp=1
        except:
            resp=0
            id_nuevo=id_persona
        finally:
            if conn!="":
                cursor.close()
                conn.close()
        return resp,id_nuevo
    #endregion
    #region Verifica si la matricula ya se encuentra registrada
    def Verificar_matricula(self):
        global usuario
        global contra
        global medico
        conn = ""
        try:
            conn = psycopg2.connect(
                host=Clases.Metodos.Obtener_datos('HOST'),
                database=Clases.Metodos.Obtener_datos('DATABASE'),
                port=Clases.Metodos.Obtener_datos('PORT'),
                user=usuario,
                password=contra
            )
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM medico where matricula=%s',(medico[0],))
            resultado=cursor.fetchone()
            if resultado ==None:
                resp=1
            else:
                resp = 0
        except:
            resp = 0
        finally:
            if conn != "":
                cursor.close()
                conn.close()
        return resp
    #endregion
    #region Obtenemos el correo electronico de la base de datos del usuario
    def Obtener_correo(self):
        global usuario
        conn = ""
        try:
            conn = psycopg2.connect(
                host=Clases.Metodos.Obtener_datos('HOST'),
                database=Clases.Metodos.Obtener_datos('DATABASE'),
                port=Clases.Metodos.Obtener_datos('PORT'),
                user=Clases.Metodos.Obtener_datos('USER'),
                password=Clases.Metodos.Obtener_datos('PASSWORD')
            )
            cursor=conn.cursor()
            cursor.execute('SELECT correo FROM medico where usuario=%s',(usuario,))
            respuesta=cursor.fetchone()
            if respuesta==None:
                resp=0
                resp1="No hay correo"
            else:
                for i in respuesta:
                    resp1=i
                resp=1
        except:
            resp=0
            resp1="No hay correo"
        finally:
            if conn!="":
                cursor.close()
                conn.close()
        return resp,resp1
    #endregion
    #region Devuelve todos los datos del usuario que pueden ser modificados
    def Datos_del_usuario(self):
        global usuario
        global contra
        conn = ""
        try:
            conn = psycopg2.connect(
                host=Clases.Metodos.Obtener_datos('HOST'),
                database=Clases.Metodos.Obtener_datos('DATABASE'),
                port=Clases.Metodos.Obtener_datos('PORT'),
                user=usuario,
                password=contra
            )
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM datos_usuario(%s)', (usuario,))
            resultado = cursor.fetchone()
        except:
            resultado = []
        finally:
            if conn != "":
                cursor.close()
                conn.close()
        return resultado
    #endregion
    #region Busqueda de historial de uso de medicos por admin
    def Busqueda_historial(self,caso,dato):
        global usuario
        global contra
        conn=""
        try:
            conn = psycopg2.connect(
                host=Clases.Metodos.Obtener_datos('HOST'),
                database=Clases.Metodos.Obtener_datos('DATABASE'),
                port=Clases.Metodos.Obtener_datos('PORT'),
                user=usuario,
                password=contra
            )
            cursor=conn.cursor()
            if caso==1:
                cursor.execute('SELECT * FROM busq_hist1()')
            if caso==2:
                cursor.execute('SELECT * FROM busq_hist2(%s,%s,%s)',dato)
            if caso==3:
                query = sql.SQL("select  f.fechayhora,p.nombre,p.apellido1,p.apellido2,historial.id_tabla,historial.tabla,"
                                "d.descripcion,m.matricula from historial inner join fecha f on f.id_fecha = historial.fecha "
                                "inner join medico m on m.matricula = historial.medico inner join descripciones d on d.id_descripcion = historial.descripciones "
                                "inner join persona p on p.id_persona = m.id_persona where fechayhora> now()- interval {buscado} order by "
                                "f.fechayhora desc").format(
                    buscado=sql.Placeholder()
                )
                cursor.execute(query, (dato,))
            if caso==4:
                cursor.execute('select medico.matricula, p.nombre, p.apellido1, p.apellido2 from medico inner join persona p on p.id_persona = medico.id_persona')
            if caso==5:
                cursor.execute('SELECT * FROM busq_hist1_1(%s)',(dato,))
            if caso==6:
                query = sql.SQL("select  f.fechayhora,p.nombre,p.apellido1,p.apellido2,historial.id_tabla,historial.tabla,"
                                "d.descripcion,m.matricula from historial inner join fecha f on f.id_fecha = historial.fecha "
                                "inner join medico m on m.matricula = historial.medico inner join descripciones d on d.id_descripcion = historial.descripciones "
                                "inner join persona p on p.id_persona = m.id_persona where m.matricula= {matri} and fechayhora> now()- interval {buscado} "
                                "order by f.fechayhora desc").format(
                    matri=sql.Placeholder(),
                    buscado=sql.Placeholder()
                )
                cursor.execute(query, dato)
            resultado=cursor.fetchall()
        except:
            resultado=[]
        finally:
            if conn!="":
                cursor.close()
                conn.close()
        return resultado
    #endregion