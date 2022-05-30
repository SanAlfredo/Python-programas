#libreria que genera randoms
import random
# importar libreria que permite el envio de correos
import smtplib
import ssl
#libreria que permite abrir archivos
import os

#importa la libreria que permite encriptar
from cryptography.fernet import Fernet
# para el generador
import string
# importar la libreria time para poner un tiempo de espera hasta cerrar la sesion
import time
# importar libreria para enviar el texto en multiparte
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Metodos():
    #region Encriptador
    def Encriptador2(caso,texto):
        texto1 = texto.encode()
        if caso==1:
            path = os.getcwdb()
            path = path.decode()
            path = path + '\dato.kydat'
            try:
                file = open(path, 'rb')
                key = file.read()
                file.close()
            except:
                print("no se pudo abrir el documento")
            f = Fernet(key)
            encriptado = f.encrypt(texto1)
            encriptado = encriptado.decode()
        if caso==2:
            key=Fernet.generate_key()
            f=Fernet(key)
            encrip=f.encrypt(texto1)
            encrip=encrip.decode()
            key=key.decode()
            encriptado=key,encrip
        return encriptado
    #endregion
    #region Desencriptador
    def Desencriptador(caso,texto):
        if caso==1:
            #key="6lMvivMhpNEkS2mexhDHNlgpSR5zyDMJPk0Vn7dZDWw="
            path = os.getcwdb()
            path = path.decode()
            path = path + '\dato.kydat'
            try:
                file = open(path, 'rb')
                key = file.read()
                file.close()
            except:
                print("no se pudo abrir el documento")
            f = Fernet(key)
            texto1 = texto.encode()
        if caso==2:
            f=Fernet(texto[0])
            texto1=texto[1].encode()
        desencriptado = f.decrypt(texto1)
        desencriptado = desencriptado.decode()
        return desencriptado
    #endregion
    #region Calcular verificar temperatura:
    def Temp_verf(valor):
        resp=0
        if valor < 36.5:
            resp=1
        elif valor >= 36.5 and valor <= 37.2:
            resp=2
        elif valor > 37.2 and valor <= 37.9:
            resp=3
        elif valor > 37.9:
            resp=4
        return resp
    #endregion
    #region Calcular IMC : Indice de Masa corporal
    def Calcula_IMC(peso,talla):
        icm=peso/talla**2
        icm=round(icm,1)
        return icm
    #endregion
    #region Obtener los valores de un diccionario
    def Obtener_datos(seccion) -> str:
        '''
        Contenedor de llaves o claves
        :return: retorna un valor string que pertenece al valor del diccionario
        '''
        diccionario={"MAIL":"gAAAAABhZbTRQfzc5FLvzwqgSWuzh2_A5N_lAPeuyH89bVc0bXiVlwRqQCOwwhNAjAOCph_swU6PC6_wBrPSRvI8_uJR8YZ3nI3rMkQh2YnlBLg03c7LKTZ6BV1F-adZzPnXqSLOCZbD",
                     "MAIL_PASS":"gAAAAABhZ1QfT0YfPODX428LEFwLZULT9wDBAx7sFVfgZVYJGy7xzXJlTdyu153ESMv612X9rWwJthcMmfOz8ieJnq2hMdQB5_goSI4l_QMPgP-VD-X5MNY=",
                     "HOST":"gAAAAABhZbWPeJe1PKJMiwCF37DGUA6xp-5Ux_ZE7bl6YdMtSFHdU2pmHJNiiCdRegH8-0CSH36x9j9txzSw3byT0WABCqiQeQ==",
                     "HOST2":"gAAAAABhpMXplU9X5hqAoBRbnpm1srygBiOy172bibRBWejbSvHYhh33hOScVSPVHkJNKh1bIehEi5yb_z3zgz-IvE9qwowGCQ==",
                     "DATABASE":"gAAAAABhZbWuTaUjm3R-xyTLkD1nN4yCChpJHF-hop45vmxLzqEEvUsoM5AsFE2CcgJ4IuKwd5o2xTSNgQ0-c0sCoopFqPOzew==",
                     "DATABASE2":"gAAAAABhpMYFbLCJw2WGRTpEAWm62Mcg6Jq4495H1zj4p2POou0vK5QLrqcSc9lN52caPMjORqaSmgAf2yLvdlT_w2Ehm223JQ==",
                     "PORT":"gAAAAABhZbXRW37jr0Lbh6uy8uSNL2OY9tbmmLCt49ouJMGc_2UJA2qK7zx1DOYoxF-k3KGOXkiGgmXIJHPshqZZQO9VGDSJ2A==",
                     "USER":"gAAAAABhZbYQINDcn_cQi1WgBgKD6D0ZZFINwO2EJA982RkFa1vt2QbzkHIHD-kqYXWUdu8y48ibjpsqZXJbCzba77UsXeGcZw==",
                     "PASSWORD":"gAAAAABhZbYxvgfaX3avSJqHVa1Jtlh_Opccl8JRoXJgYlQKPypeB2dQsysOD6cOMzqVbft7pQ4pd_UzQT0q_DYRDsXFjRMKXw==",
                     "USER1":"gAAAAABhpMUO9KyZ1Wl9E-SqXUKptT2ihYlF-PxAZRYbxUF4-f7d_AHGhLp8OmJeSb1zWcD09UsAtXHsvc_MyPL_LAoPLCJTrA==",
                     "PASSWORD2":"gAAAAABhpMUoRhRduihu2niaH-PUhNv46I02jglBarJUT1CngQ6-vIAwk01pmF8xR2V7R9oFiSmdmCPvHZSm8ji3Ih_bLDldHw=="}
        dato1=diccionario[seccion]
        dato=Metodos.Desencriptador(1,dato1)
        return dato
    #endregion
    #region generador de numeros y letras aleatorio
    def Generador_clave(caracteres=string.ascii_letters + string.digits):
        return ''.join(random.choice(caracteres) for _ in range(5))
    #endregion
    #region enviar correo
    def Enviar_codigo(codigo,correo):
        usuario = Metodos.Obtener_datos('MAIL')
        #config.get('conexionescorreo','MAIL')
        contra = Metodos.Obtener_datos('MAIL_PASS')
        #config.get('conexionescorreo','MAIL_PASS')
        destino = str(correo)
        subject = 'Código de validación'
        codigo1 = str(codigo)
        # crear el mensaje
        mensaje = MIMEMultipart("alternative")  # que es la estandar
        mensaje["Subject"] = subject
        mensaje["From"] = usuario
        mensaje["To"] = destino
        #crear un formato html para el mensaje
        html = f"""
        <html>
        <body>
            Hola <i>{destino}</i><br>
            Tu código de verificacion es: <b>{codigo1}</b>
        </body>
        </html>
        """
        # el contenido del mensaje como HTML
        parte_html = MIMEText(html, "html")
        # agregar contenido
        mensaje.attach(parte_html)

        # enviar el mensaje
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(usuario, contra)
            server.sendmail(usuario, destino, mensaje.as_string())
            print("ENVIADO CORRECTAMENTE EL CORREO")
            time.sleep(5)
            server.quit()
    #endregion