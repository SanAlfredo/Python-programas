'''
    Importaciones de librerías necesarias
'''
#region Librerias
#libreria tiempo
import time
#libreria para postgres
import psycopg2
#importar el módulo clases
import Clases
#endregion
from PyQt5.QtWidgets import QMessageBox
class Posgress():
    #region Crear tablas en la BBDD postgres
    def Crear_tabla(self):
        try:
            conn = psycopg2.connect(
                host=Clases.Metodos.Obtener_datos('HOST'),
                database=Clases.Metodos.Obtener_datos('DATABASE'),
                port=Clases.Metodos.Obtener_datos('PORT'),
                user=Clases.Metodos.Obtener_datos('USER'),
                password=Clases.Metodos.Obtener_datos('PASSWORD')
            )
            cursor=conn.cursor()
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS GRUPO_SANGUINEO(
            ID_GRUPO SERIAL NOT NULL,
            GRUPO VARCHAR NOT NULL,
            PRIMARY KEY (ID_GRUPO));
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS DATO_GENERAL(
            ID_DATO serial NOT NULL,
            PESO DECIMAL(10,3),
            TALLA DECIMAL(10,2),
            PRIMARY KEY (ID_DATO));
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS FACTOR_SANGUINEO(
            ID_FACTOR SERIAL NOT NULL,
            FACTOR VARCHAR,
            PRIMARY KEY (ID_FACTOR));
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS USUARIO(
            CUENTA_USER VARCHAR NOT NULL,
            PASS VARCHAR,
            SAL VARCHAR,
            TEMA INT,
            PRIMARY KEY (CUENTA_USER));
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS VALIDACIONES(
            ID_VALIDACIONES SERIAL NOT NULL,
            CODIGO VARCHAR,
            VALIDACION BOOLEAN,
            HABILITACION BOOLEAN,
            PRIMARY KEY (ID_VALIDACIONES));
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS EXTENSION(
            ID_EXTENSION SERIAL NOT NULL,
            TIPO VARCHAR,
            DESCRIPCION VARCHAR,
            PRIMARY KEY (ID_EXTENSION));
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS DESCRIPCIONES(
            ID_DESCRIPCION SERIAL NOT NULL,
            DESCRIPCION VARCHAR,
            PRIMARY KEY (ID_DESCRIPCION));
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS TIPO_DATO(
            ID_TIPO SERIAL NOT NULL,
            TIPO_DATO VARCHAR,
            PRIMARY KEY (ID_TIPO));
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS TIPO_SEXO(
            ID_TIPO SERIAL NOT NULL,
            TIPO_DATO VARCHAR,
            PRIMARY KEY (ID_TIPO));
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS TIPO_FAMILIAR(
            ID_TIPO SERIAL NOT NULL,
            TIPO_DATO VARCHAR,
            PRIMARY KEY (ID_TIPO));
            ''')

            cursor.execute('''
            CREATE TABLE IF NOT EXISTS FECHA(
            ID_FECHA SERIAL NOT NULL,
            FECHAYHORA timestamp,
            TIPO_FECHA INT,
            PRIMARY KEY (ID_FECHA),
            FOREIGN KEY (TIPO_FECHA) REFERENCES TIPO_DATO(ID_TIPO));
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS PERSONA(
            ID_PERSONA VARCHAR NOT NULL,
            NOMBRE VARCHAR,
            APELLIDO1 VARCHAR,
            APELLIDO2 VARCHAR,
            FECHA INT,
            TIPO_SEXO INT,
            PRIMARY KEY (ID_PERSONA),
            FOREIGN KEY (FECHA) REFERENCES FECHA(ID_FECHA),
            FOREIGN KEY (TIPO_SEXO) REFERENCES TIPO_SEXO(ID_TIPO));
            ''')
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS CARNET(
                        ID_CARNET SERIAL NOT NULL,
                        NUMERO VARCHAR,
                        EXTENSION INT,
                        PERSONA VARCHAR UNIQUE,
                        PRIMARY KEY (ID_CARNET),
                        FOREIGN KEY (PERSONA) REFERENCES persona(id_persona),
                        FOREIGN KEY (EXTENSION) REFERENCES EXTENSION(ID_EXTENSION));
                        ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS MEDICO(
            MATRICULA VARCHAR NOT NULL,
            ID_PERSONA VARCHAR,
            USUARIO VARCHAR,
            CORREO VARCHAR,
            VALIDACIONES INT,
            PRIMARY KEY (MATRICULA),
            FOREIGN KEY (ID_PERSONA) REFERENCES PERSONA(ID_PERSONA),
            FOREIGN KEY (USUARIO) REFERENCES USUARIO(CUENTA_USER),
            FOREIGN KEY (VALIDACIONES) REFERENCES VALIDACIONES(ID_VALIDACIONES));
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS PACIENTE(
            ID_PACIENTE VARCHAR NOT NULL,
            ID_PERSONA VARCHAR,
            GRUPO_SANGUINEO INT,
            FACTOR_SANGUINEO INT,
            PROCEDENCIA VARCHAR,
            RESIDENCIA VARCHAR,
            DIRECCION VARCHAR,
            BARRIO VARCHAR,
            DATO_GENERAL INT,
            PRIMARY KEY (ID_PACIENTE),
            FOREIGN KEY (ID_PERSONA) REFERENCES PERSONA(ID_PERSONA),
            FOREIGN KEY (GRUPO_SANGUINEO) REFERENCES GRUPO_SANGUINEO(ID_GRUPO),
            FOREIGN KEY (FACTOR_SANGUINEO) REFERENCES FACTOR_SANGUINEO(ID_FACTOR),
            FOREIGN KEY (DATO_GENERAL) REFERENCES DATO_GENERAL(ID_DATO));
            ''')
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS ANTECEDENTES(
                        ID_ANTECEDENTES SERIAL NOT NULL,
                        PATOLOGICOS VARCHAR,
                        ALERGIAS VARCHAR,
                        PACIENTE VARCHAR unique,
                        PRIMARY KEY (ID_ANTECEDENTES),
                        FOREIGN KEY (PACIENTE) REFERENCES PACIENTE(id_paciente));
                        ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS FAMILIAR(
            ID_FAMILIAR VARCHAR NOT NULL,
            ID_PERSONA VARCHAR,
            TIPO_FAMILIAR INT,
            PACIENTE VARCHAR,
            PRIMARY KEY (ID_FAMILIAR),
            FOREIGN KEY (ID_PERSONA) REFERENCES PERSONA(ID_PERSONA),
            FOREIGN KEY (TIPO_FAMILIAR) REFERENCES TIPO_FAMILIAR(ID_TIPO),
            FOREIGN KEY (PACIENTE) REFERENCES PACIENTE(ID_PACIENTE));
            ''')
            cursor.execute('''
                        CREATE TABLE IF NOT EXISTS TELEFONO(
                        ID_TELEFONO serial NOT NULL,
                        NUMERO INT,
                        FAMILIAR VARCHAR UNIQUE,
                        FOREIGN KEY (FAMILIAR) REFERENCES familiar(id_familiar),
                        PRIMARY KEY (ID_TELEFONO));
                        ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS CONSULTA(
            ID_CONSULTA VARCHAR NOT NULL,
            CODIGO_PACIENTE VARCHAR,
            ID_MEDICO VARCHAR,
            FECHA INT,
            FRECUENCIA_CARDIACA INT,
            FRECUENCIA_RESPIRATORIA INT,
            TEMPERATURA DECIMAL(10,2),
            SATURACION INT,
            PRESION VARCHAR,
            PERIMETRO_CEFALICO DECIMAL(10,2),
            MOTIVO VARCHAR,
            EXAMEN VARCHAR,
            DIAGNOSTICO VARCHAR,
            TRATAMIENTO VARCHAR,
            OBSERVACIONES VARCHAR,
            PROXIMA_REVISION DATE,
            DATO_GENERAL INT,
            PRIMARY KEY (ID_CONSULTA),
            FOREIGN KEY (CODIGO_PACIENTE) REFERENCES PACIENTE(ID_PACIENTE),
            FOREIGN KEY (ID_MEDICO) REFERENCES MEDICO(MATRICULA),
            FOREIGN KEY (FECHA) REFERENCES FECHA(ID_FECHA),
            FOREIGN KEY (DATO_GENERAL) REFERENCES DATO_GENERAL(ID_DATO));
            ''')
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS HISTORIAL(
            ID_HISTORIAL SERIAL NOT NULL,
            MEDICO VARCHAR,
            FECHA INT,
            ID_TABLA VARCHAR,
            DESCRIPCIONES INT,
            TABLA VARCHAR,
            PRIMARY KEY (ID_HISTORIAL),
            FOREIGN KEY (MEDICO) REFERENCES MEDICO(MATRICULA),
            FOREIGN KEY (FECHA) REFERENCES fecha(id_fecha),
            FOREIGN KEY (DESCRIPCIONES) REFERENCES descripciones(id_descripcion));
            ''')
            conn.commit()
        except:
            QMessageBox.critical(self,"Mensaje de error de creación de tablas","Se ha producido un error, las tablas no pudieron crearse")
        finally:
            cursor.close()
            conn.close()
    #endregion