# @autor: Magno Efren
# Youtube: https://www.youtube.com/c/MagnoEfren
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QHeaderView
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi

import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt
from imagenes import logo
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

		self.presionC = Canvas_presion()
		self.alturaC = Canvas_altura()
		self.temperaturaC = Canvas_temperatura()
		self.aceleracionC = Canvas_aceleracion()
		self.anguloC = Canvas_angulo()
		self.distanciaC = Canvas_distancia()
		

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
		if True:			
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

class Canvas_presion(FigureCanvas):    
	def __init__(self, parent=None):
		self.fig , self.ax = plt.subplots(1,dpi=60, figsize=(1, 1), 
										  sharey=True, facecolor='white')
		super().__init__(self.fig) 
		t = np.arange(0., 5., 0.2)
		self.ax.set_title('Presión\n')
		self.ax.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
			


class Canvas_altura(FigureCanvas):
	def __init__(self, parent=None):     
		self.fig , self.ax = plt.subplots(1,dpi=60, figsize=(1, 1), 
										  sharey=True, facecolor='white')
		super().__init__(self.fig) 
		x = np.arange(0.1, 4, 0.5)
		y = np.exp(-x)
		self.ax.set_title('Altura\n')
		self.ax.errorbar(x, y, xerr=0.2, yerr=0.4)


class Canvas_temperatura(FigureCanvas):
	def __init__(self, parent=None): 
		t = np.linspace(0, 2 * np.pi, 1024)
		data2d = np.sin(t)[:, np.newaxis] * np.cos(t)[np.newaxis, :]

		self.fig, self.ax = plt.subplots(1,dpi=50, figsize=(1, 1), 
            sharey=True, facecolor='white')
		super().__init__(self.fig) 
		im = self.ax.imshow(data2d)
		self.ax.set_title('Temperatura\n')

		self.fig.colorbar(im, ax=self.ax, label='Interactive colorbar')
		
class Canvas_aceleracion(FigureCanvas):
	def __init__(self, parent=None):     
		self.fig , self.ax = plt.subplots(1,dpi=100, figsize=(10, 10), 
										  sharey=True, facecolor='white')
		super().__init__(self.fig) 
		x = np.arange(0.1, 4, 0.5)
		y = np.exp(-x)
		self.ax.set_title('Aceleración\n')
		self.ax.errorbar(x, y, xerr=0.2, yerr=0.4)

class Canvas_angulo(FigureCanvas):
	def __init__(self, parent=None):     
		self.fig , self.ax = plt.subplots(1,dpi=100, figsize=(10, 10), 
										  sharey=True, facecolor='white')
		super().__init__(self.fig) 
		x = np.arange(0.1, 4, 0.5)
		y = np.exp(-x)
		self.ax.set_title('Ángulo\n')
		self.ax.errorbar(x, y, xerr=0.2, yerr=0.4)

class Canvas_distancia(FigureCanvas):
	def __init__(self, parent=None):
		self.fig , self.ax = plt.subplots(1,dpi=100, figsize=(4, 4), 
										  sharey=True, facecolor='white')
		super().__init__(self.fig) 
		self.ax.plot([1, 2, 3, 4], 'o-r')
		self.ax.set(ylabel='distancia', xlabel='cargas')

if __name__ == "__main__":
     app = QApplication(sys.argv)
     mi_app = VentanaPrincipal()
     mi_app.show()
     sys.exit(app.exec_())	
