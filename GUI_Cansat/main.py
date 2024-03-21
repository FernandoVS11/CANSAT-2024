# @autor: Magno Efren
# Youtube: https://www.youtube.com/c/MagnoEfren
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi

from imagenes import logo

from grafica_Aceleracion import *
from grafica_Altura import *
from grafica_Angulo import *
from grafica_Distancia import *
from grafica_Presion import *
from grafica_Temperatura import *

class VentanaPrincipal(QMainWindow):
	def __init__(self):
		super(VentanaPrincipal,self).__init__()
		loadUi('Diseño.ui',self)

		self.bt_menu.clicked.connect(self.mover_menu)

		self.bt_restaurar.hide()

		#control barra de titulos
		self.bt_minimizar.clicked.connect(self.control_bt_minimizar)		
		self.bt_restaurar.clicked.connect(self.control_bt_normal)
		self.bt_maximizar.clicked.connect(self.control_bt_maximizar)
		self.bt_cerrar.clicked.connect(lambda: self.close())

		#eliminar barra y de titulo - opacidad
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setWindowOpacity(1)
		
		#SizeGrip
		self.gripSize = 10
		self.grip = QtWidgets.QSizeGrip(self)
		self.grip.resize(self.gripSize, self.gripSize)
		
		# mover ventana
		self.frame_superior.mouseMoveEvent = self.mover_ventana

		#acceder a las paginas
		self.bt_GraficasA.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pagina1))			
		self.bt_GraficasB.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pagina2))
		self.bt_GraficasC.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pagina3))	
		self.bt_GraficasD.clicked.connect(lambda: self.stackedWidget.setCurrentWidget(self.pagina4))

		self.presionC = GraficaPresion()
		self.alturaC = GraficaAltura()
		self.temperaturaC = GraficaTemperatura()
		self.aceleracionC = GraficaAceleracion()
		self.anguloC = GraficaAngulo()
		self.distanciaC = GraficaDistancia()
		

		self.presion.addWidget(self.presionC)
		self.altura.addWidget(self.alturaC)	
		self.temperatura.addWidget(self.temperaturaC)
		self.aceleracion.addWidget(self.aceleracionC)
		self.angulo.addWidget(self.anguloC)
		self.distancia.addWidget(self.distanciaC)
		
	def control_bt_minimizar(self):
		self.showMinimized()		

	def  control_bt_normal(self): 
		self.showNormal()		
		self.bt_restaurar.hide()
		self.bt_maximizar.show()

	def  control_bt_maximizar(self): 
		self.showMaximized()
		self.bt_maximizar.hide()
		self.bt_restaurar.show()

	def mover_menu(self):
		width = self.frame_control.width()
		normal = 0
		if width==0:
			extender = 200
		else:
			extender = normal
		self.animacion = QPropertyAnimation(self.frame_control, b'minimumWidth')
		self.animacion.setDuration(300)
		self.animacion.setStartValue(width)
		self.animacion.setEndValue(extender)
		self.animacion.setEasingCurve(QtCore.QEasingCurve.InOutQuart)
		self.animacion.start()
	## SizeGrip
	def resizeEvent(self, event):
		rect = self.rect()
		self.grip.move(rect.right() - self.gripSize, rect.bottom() - self.gripSize)

	## mover ventana
	def mousePressEvent(self, event):
		self.clickPosition = event.globalPos()

	def mover_ventana(self, event):
		if self.isMaximized() == False:			
			if event.buttons() == QtCore.Qt.LeftButton:
				self.move(self.pos() + event.globalPos() - self.clickPosition)
				self.clickPosition = event.globalPos()
				event.accept()
		if event.globalPos().y() <=10:
			self.showMaximized()
			self.bt_maximizar.hide()
			self.bt_restaurar.show()
		else:
			self.showNormal()
			self.bt_restaurar.hide()
			self.bt_maximizar.show()

if __name__ == "__main__":
     app = QApplication(sys.argv)
     mi_app = VentanaPrincipal()
     mi_app.show()
     sys.exit(app.exec_())	