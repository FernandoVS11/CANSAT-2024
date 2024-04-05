# @autor: Magno Efren
# Youtube: https://www.youtube.com/c/MagnoEfren
import sys
import numpy as np
import pyqtgraph.opengl as gl
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QPropertyAnimation, QIODevice
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
from imagenes import logo

from grafica_Aceleracion_Caida import *
from grafica_Aceleracion_Subida import *
from grafica_Altura import *
from grafica_Angulo import *
from grafica_Presion import *
import pyqtgraph as pg

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
		self.serial = QSerialPort()
		self.serial_port = 'COM3'
		self.baud_rate = 9600

		self.serial.waitForReadyRead(100)
		self.serial.setBaudRate(self.baud_rate)
		self.serial.setPortName(self.serial_port)
		self.serial.open(QIODevice.ReadOnly)
		print("conexion con el puerto")

		self.serial.readyRead.connect(self.read_data)
		self.x = list(np.linspace(0,100,100))
		self.y = list(np.linspace(0,0,100))
		self.z = list(np.linspace(0,0,100))

		self.gfc_temperatura = pg.PlotWidget(title='Temperatura')
		self.gfc_presion = pg.PlotWidget(title='Presión')
		self.gfc_altura = pg.PlotWidget(title='Altura')
		self.gfc_angulo = pg.PlotWidget(title='Ángulo')
		self.gfc_aceleracion_subida = gl.GLViewWidget()
		self.gfc_aceleracion_caida = gl.GLViewWidget()

		self.presion.addWidget(self.gfc_presion)
		self.altura.addWidget(self.gfc_altura)	
		self.temperatura.addWidget(self.gfc_temperatura)
		self.aceleracion_subida.addWidget(self.gfc_aceleracion_subida)
		self.aceleracion_caida.addWidget(self.gfc_aceleracion_caida)
		self.angulo.addWidget(self.gfc_angulo)

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
		if self.isMaximized() == False and event.buttons() == QtCore.Qt.LeftButton:
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
	def read_data(self):
		if not self.serial.canReadLine():return
		rx = self.serial.readLine()
		x = str(rx,'utf-8').strip()
		data_from_arduino = float(x)
		print(data_from_arduino)

		self.presion_label.setText(str(data_from_arduino)+' pa')
		self.altura_label.setText(str(data_from_arduino)+' m')
		self.roll_label.setText(str(data_from_arduino)+'°')
		self.pitch_label.setText(str(data_from_arduino)+'°')
		self.yaw_label.setText(str(data_from_arduino)+'°')
		self.temperatura_label.setText(str(data_from_arduino)+'°C')
		self.y_coord_label_subida.setText(str(data_from_arduino)+'m/s^2')
		self.z_coord_label_subida.setText(str(data_from_arduino)+'m/s^2')
		self.x_coord_label_caida.setText(str(data_from_arduino)+'m/s^2')
		self.y_coord_label_caida.setText(str(data_from_arduino)+'m/s^2')
		self.z_coord_label_caida.setText(str(data_from_arduino)+'m/s^2')
		self.altura_max_label.setText(str(data_from_arduino)+' m')
		self.x_coord_label.setText(str(data_from_arduino)+'m/s^2')
		self.y_coord_label.setText(str(data_from_arduino)+'m/s^2')
		self.z_coord_label.setText(str(data_from_arduino)+'m/s^2')
		self.vel_max_label.setText(str(data_from_arduino)+' m/s')
		self.distancia_label.setText(str(data_from_arduino)+' m/s')
		
		self.y = self.y[1:]
		self.y.append(data_from_arduino)
		lines_angulo = [self.y,self.y,self.y]

		self.gfc_temperatura.clear()
		self.gfc_temperatura.plot(self.x,self.y, color='red')

		
		self.gfc_presion.clear()
		self.gfc_presion.plot(self.x,self.y, color='red')

		
		self.gfc_altura.clear()
		self.gfc_altura.plot(self.x,self.y, color='red')

		self.gfc_angulo.clear()
		self.gfc_angulo.plot(self.x, np.sin(self.y), pen='r', name='Sin(x)')
		self.gfc_angulo.plot(self.x, np.cos(self.y), pen='g', name='Cos(x)')
		self.gfc_angulo.plot(self.x, np.tan(self.y), pen='b', name='Tan(x)')

		axis_x = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [100, 0, 0]]), color=(1.0, 0.0, 0.0, 1.0), width=3)
		axis_y = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [0, 100, 0]]), color=(0.0, 1.0, 0.0, 1.0), width=3)
		axis_z = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [0, 0, 100]]), color=(0.0, 0.0, 1.0, 1.0), width=3)
		self.gfc_aceleracion_subida.addItem(axis_x)
		self.gfc_aceleracion_subida.addItem(axis_y)
		self.gfc_aceleracion_subida.addItem(axis_z)
        
        # Creamos datos de ejemplo para la línea 3D
		x = self.y
		y = self.y
		z = self.y
        
        # Añadimos la línea a la visualización 3D
		self.line_plot = gl.GLLinePlotItem(pos=np.column_stack((x, y, z)), color=(1.0, 1.0, 1.0, 1.0), width=3)
		self.gfc_aceleracion_subida.addItem(self.line_plot)
		
		axis_x2 = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [100, 0, 0]]), color=(1.0, 0.0, 0.0, 1.0), width=3)
		axis_y2 = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [0, 100, 0]]), color=(0.0, 1.0, 0.0, 1.0), width=3)
		axis_z2 = gl.GLLinePlotItem(pos=np.array([[0, 0, 0], [0, 0, 100]]), color=(0.0, 0.0, 1.0, 1.0), width=3)
		
		self.gfc_aceleracion_caida.addItem(axis_x2)
		self.gfc_aceleracion_caida.addItem(axis_y2)
		self.gfc_aceleracion_caida.addItem(axis_z2)
        
        # Creamos datos de ejemplo para la línea 3D
		x = self.y
		y = self.y
		z = self.y
        
        # Añadimos la línea a la visualización 3D
		self.line_plot = gl.GLLinePlotItem(pos=np.column_stack((x, y, z)), color=(1.0, 1.0, 1.0, 1.0), width=3)
		self.gfc_aceleracion_caida.addItem(self.line_plot)

if __name__ == "__main__":
	app = QApplication(sys.argv)
	my_app= VentanaPrincipal()
	print('Salí de la ventana principal')
	my_app.show()
	isRun=False
	sys.exit(app.exec_())	