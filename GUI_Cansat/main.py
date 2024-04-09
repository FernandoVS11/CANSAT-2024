# @autor: Magno Efren
# Youtube: https://www.youtube.com/c/MagnoEfren
import sys, time
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

tiempo_inicio = time.time()
class VentanaPrincipal(QMainWindow):
	velocidad_si ='m/s'
	aceleracion_si ='m/s^2'
	presion= 'pa'
	grados_si='°'
	distancia_si='m'
	temperatura_si ='°C'
	radio_tierra= 6378
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
		self.serial_port = 'COM4'
		self.baud_rate = 9600

		self.serial.waitForReadyRead(100)
		self.serial.setBaudRate(self.baud_rate)
		self.serial.setPortName(self.serial_port)
		
		try:
			self.serial.open(QIODevice.ReadOnly)
			print('conexion')
		except:
			print('no entra')

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
		if not self.serial.canReadLine():return 'No entre al read data'
		rx = self.serial.readLine()
		print(str(rx,'utf-8').strip())
		x = str(rx,'utf-8').strip().split(',')
		data_from_arduino = []
		for data in x:
			if data == '0.000000\x00':
				data_from_arduino.append(0.000000)
			else:
				data_from_arduino.append(float(data))
			print(data)
	
		self.x_coord_label_subida.setText(str(data_from_arduino[0])+self.aceleracion_si )
		self.y_coord_label_subida.setText(str(data_from_arduino[1])+self.aceleracion_si )
		self.z_coord_label_subida.setText(str(data_from_arduino[2])+self.aceleracion_si )
		self.x_coord_label_caida.setText(str(data_from_arduino[0])+self.aceleracion_si )
		self.y_coord_label_caida.setText(str(data_from_arduino[1])+self.aceleracion_si )
		self.z_coord_label_caida.setText(str(data_from_arduino[2])+self.aceleracion_si )
		self.x_coord_label.setText(str(data_from_arduino[9]))
		self.y_coord_label.setText(str(data_from_arduino[10]))
		self.yaw_label.setText(str(data_from_arduino[3])+self.grados_si)
		self.pitch_label.setText(str(data_from_arduino[4])+self.grados_si)
		self.roll_label.setText(str(data_from_arduino[5])+self.grados_si)
		self.temperatura_label.setText(str(data_from_arduino[6])+self.temperatura_si)
		self.presion_label.setText(str(data_from_arduino[7])+self.presion)
		self.altura_label.setText(str(data_from_arduino[8])+self.distancia_si)
		self.altura_max_label.setText(str(data_from_arduino[8])+self.distancia_si)
		global tiempo_inicio
		tiempo_trasncurrido = time.time() - tiempo_inicio
		velocidad_maxima = data_from_arduino[8]/tiempo_trasncurrido
		self.vel_max_label.setText(str(velocidad_maxima)+self.velocidad_si)
		distancia = self.radio_tierra * np.arccos(np.sin(data_from_arduino[9])*np.sin(data_from_arduino[9])
											+(np.abs(data_from_arduino[10]+data_from_arduino[10])
											*np.cos(data_from_arduino[10])*np.cos(data_from_arduino[10])))
		self.distancia_label.setText(distancia+self.distancia_si)
		
		self.y = self.y[1:]
		self.y.append(data_from_arduino)

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