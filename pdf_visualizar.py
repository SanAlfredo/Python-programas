
from PyQt5.QtGui import QIcon, QTextDocument
from PyQt5.QtCore import Qt, QTextCodec, QByteArray
from PyQt5.QtWidgets import (QDialog,QFileDialog,QMessageBox, QToolBar)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog

# =============== CLASE visualizarImprimirExportar =================

class Visualizador_pdf(QDialog):
    def __init__(self,texto,html, nombre_doc,parent=None):
        super(Visualizador_pdf, self).__init__()

        self.setWindowTitle("Ver en pdf")
        self.setWindowIcon(QIcon("logotipo.png"))
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
        self.setFixedSize(450, 250)
        self.texto=texto
        self.html=html
        self.nombre_doc=nombre_doc
        self.initUI()

    def initUI(self):
        self.documento = QTextDocument()

    # *****************************************************************************************
    # METODOS
    # *****************************************************************************************
    def Buscar(self,caso):
        self.documento.clear()
        dat=self.texto
        datos = ""
        if caso==1:
            for dato in dat:
                datos += "<tr><td>%s</td><td>%s</td></tr>" % dato
            reporteHtml = self.html.replace("[DATOS]", datos)
        if caso==2:
            datos = ""
            for dato in dat[0]:
                datos += "<tr><td colspan='2'>%s</td></tr>" % dato
            self.html = self.html.replace("[DATOS9]", datos)
            datos=""
            for dato in dat[1]:
                datos += "<tr><td width='300'>%s</td><td>%s</td></tr>" % dato
            self.html = self.html.replace("[DATOS10]", datos)
            datos = ""
            for dato in dat[2]:
                datos += "<tr><td colspan='2'>%s</td></tr>" % dato
            reporteHtml = self.html.replace("[DATOS11]", datos)
        datos = QByteArray()
        datos.append(str(reporteHtml))
        codec = QTextCodec.codecForHtml(datos)
        unistr = codec.toUnicode(datos)

        if Qt.mightBeRichText(unistr):
            self.documento.setHtml(unistr)
        else:
            self.documento.setPlainText(unistr)

    #region Vista previa
    def vistaPrevia(self):
        if not self.documento.isEmpty():
            impresion = QPrinter(QPrinter.HighResolution)

            vista = QPrintPreviewDialog(impresion, self)
            vista.setWindowTitle("Vista previa")
            vista.setWindowFlags(Qt.Window)
            vista.resize(600, 400)


            exportarPDF = vista.findChildren(QToolBar)
            exportarPDF[0].addAction(QIcon("exportarPDF.png"),"Exportar a PDF", self.exportarPDF)

            vista.paintRequested.connect(self.vistaPreviaImpresion)
            vista.exec_()
        else:
            QMessageBox.critical(self, "Vista previa", "No hay datos para visualizar.   ",
                                 QMessageBox.Ok)
    #endregion
    #region Vista previa de impresion
    def vistaPreviaImpresion(self, impresion):
        self.documento.print_(impresion)
    #endregion
    #region Imprimir el documento mostrado
    def Imprimir(self):
        if not self.documento.isEmpty():
            impresion = QPrinter(QPrinter.HighResolution)

            dlg = QPrintDialog(impresion, self)
            dlg.setWindowTitle("Imprimir documento")

            if dlg.exec_() == QPrintDialog.Accepted:
                self.documento.print_(impresion)

            del dlg
        else:
            QMessageBox.critical(self, "Imprimir", "No hay datos para imprimir.   ",
                                 QMessageBox.Ok)
    #endregion
    #region Exportar a PDF el documento
    def exportarPDF(self):
        if not self.documento.isEmpty():
            nombreArchivo, _ = QFileDialog.getSaveFileName(self, "Exportar a PDF", self.nombre_doc,
                                                           "Archivos PDF (*.pdf);;All Files (*)",
                                                           options=QFileDialog.Options())

            if nombreArchivo:
                impresion = QPrinter(QPrinter.HighResolution)
                impresion.setOutputFormat(QPrinter.PdfFormat)
                impresion.setOutputFileName(nombreArchivo)
                self.documento.print_(impresion)

                QMessageBox.information(self, "Exportar a PDF", "Datos exportados con éxito.   ",
                                        QMessageBox.Ok)
        else:
            QMessageBox.critical(self, "Exportar a PDF", "No hay datos para exportar.   ",
                                 QMessageBox.Ok)
    #endregion