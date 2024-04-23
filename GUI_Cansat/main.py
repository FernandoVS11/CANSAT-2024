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

import pyqtgraph as pg

tiempo_inicio = time.time()
class VentanaPrincipal(QMainWindow):
	velocidad_si ='m/s'
	aceleracion_si ='m/s^2'
	presion_si= 'pa'
	grados_si='°'
	distancia_si='m'
	temperatura_si ='°C'
	radio_tierra= 6378
	dato_arduino_estatico =[]
	data_from_arduino_estatico_antena_2 = []
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
		
		self.x = list(np.linspace(0,0,100))
		self.altura_data = list(np.linspace(0,0,100))
		self.presion_data = list(np.linspace(0,0,100))
		self.temperatura_data = list(np.linspace(0,0,100))
		self.yaw = list(np.linspace(0,0,100))
		self.pitch = list(np.linspace(0,0,100))
		self.roll = list(np.linspace(0,0,100))
		self.aceleracion_x = list(np.linspace(0,0,100))
		self.aceleracion_y = list(np.linspace(0,0,100))
		self.aceleracion_z = list(np.linspace(0,0,100))
		self.latitud = list(np.linspace(0,0,100))
		self.longitud = list(np.linspace(0,0,100))
		
		self.z = list(np.linspace(0,0,100))

		self.gfc_temperatura = pg.PlotWidget(title='Temperatura')
		self.gfc_presion = pg.PlotWidget(title='Presión')
		self.gfc_altura = pg.PlotWidget(title='Altura')
		self.gfc_angulo = pg.PlotWidget(title='Ángulo')
		self.gfc_aceleracion_subida = pg.PlotWidget(title='Aceleración Subida')
		self.gfc_aceleracion_caida = pg.PlotWidget(title='Aceleración Caída')

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
		data_from_arduino_antena_2 = []
		if len(x) == 3:
			for data in x:
				data_from_arduino_antena_2.append(float(data))
				self.data_from_arduino_estatico_antena_2 = data_from_arduino_antena_2  
		else:
			for data in x:
				data_from_arduino.append(float(data))	
			#data_from_arduino_antena_2.append(2)
			#data_from_arduino_antena_2.append(10)	
			self.dato_arduino_estatico = data_from_arduino
		#self.dato_arduino_estatico[2] = 0
		if self.dato_arduino_estatico[2] > 3:
			self.x_coord_label_subida.setText("0"+self.aceleracion_si )
			self.y_coord_label_subida.setText("0"+self.aceleracion_si )
			self.z_coord_label_subida.setText("0"+self.aceleracion_si )
			self.x_coord_label_caida.setText(str(self.dato_arduino_estatico[0])+self.aceleracion_si )
			self.y_coord_label_caida.setText(str(self.dato_arduino_estatico[1])+self.aceleracion_si )
			self.z_coord_label_caida.setText(str(self.dato_arduino_estatico[2])+self.aceleracion_si )
		else:
			self.x_coord_label_subida.setText(str(self.dato_arduino_estatico[0])+self.aceleracion_si )
			self.y_coord_label_subida.setText(str(self.dato_arduino_estatico[1])+self.aceleracion_si )
			self.z_coord_label_subida.setText(str(self.dato_arduino_estatico[2])+self.aceleracion_si )
			self.x_coord_label_caida.setText("0"+self.aceleracion_si )
			self.y_coord_label_caida.setText("0"+self.aceleracion_si )
			self.z_coord_label_caida.setText("0"+self.aceleracion_si )		

		self.x_coord_label.setText(str(self.dato_arduino_estatico[9]))
		self.y_coord_label.setText(str(self.dato_arduino_estatico[10]))
		self.yaw_label.setText(str(self.dato_arduino_estatico[3])+self.grados_si)
		self.pitch_label.setText(str(self.dato_arduino_estatico[4])+self.grados_si)
		self.roll_label.setText(str(self.dato_arduino_estatico[5])+self.grados_si)
		self.temperatura_label.setText(str(self.dato_arduino_estatico[6])+self.temperatura_si)
		self.presion_label.setText(str(self.dato_arduino_estatico[7])+self.presion_si)
		self.altura_label.setText(str(self.dato_arduino_estatico[8])+self.distancia_si)
		self.altura_max_label.setText(str(self.dato_arduino_estatico[8])+self.distancia_si)
		global tiempo_inicio
		tiempo_trasncurrido = time.time() - tiempo_inicio
		velocidad_maxima = self.dato_arduino_estatico[8]/tiempo_trasncurrido
		# velocidad_maxima = "{:.4f}".format(velocidad_maxima_arduino)
		self.vel_max_label.setText(str("{:.4f}".format(velocidad_maxima))+self.velocidad_si)
		
		if len(self.data_from_arduino_estatico_antena_2) != 0:				
			distancia = self.radio_tierra * np.arccos(np.sin(self.dato_arduino_estatico[9])*np.sin(self.data_from_arduino_estatico_antena_2[0])
												+(np.abs(self.dato_arduino_estatico[10]+self.data_from_arduino_estatico_antena_2[1])
												*np.cos(self.dato_arduino_estatico[10])*np.cos(self.data_from_arduino_estatico_antena_2[1])))
		else:
			distancia = 0
		self.distancia_label.setText(str(distancia)+self.distancia_si)
		
		self.altura_data = self.altura_data[1:]
		self.presion_data = self.presion_data[1:]
		self.temperatura_data = self.temperatura_data[1:]
		self.yaw = self.yaw[1:]
		self.pitch = self.pitch[1:]
		self.roll = self.roll[1:]
		self.aceleracion_x = self.aceleracion_x[1:]
		self.aceleracion_y = self.aceleracion_y[1:]
		self.aceleracion_z = self.aceleracion_z[1:]
		self.latitud = self.latitud[1:]
		self.longitud = self.longitud[1:]
		self.x = self.x[1:]

		self.altura_data.append(self.dato_arduino_estatico[8])
		self.presion_data.append(self.dato_arduino_estatico[7])
		self.temperatura_data.append(self.dato_arduino_estatico[6])
		self.yaw.append(self.dato_arduino_estatico[3])
		self.pitch.append(self.dato_arduino_estatico[4])
		self.roll.append(self.dato_arduino_estatico[5])
		self.aceleracion_x.append(self.dato_arduino_estatico[0])
		self.aceleracion_y.append(self.dato_arduino_estatico[1])
		self.aceleracion_z.append(self.dato_arduino_estatico[2])
		self.latitud.append(self.dato_arduino_estatico[9])
		self.longitud.append(self.dato_arduino_estatico[10])
		self.x.append(int(time.time()-tiempo_inicio))

		self.gfc_temperatura.clear()
		self.gfc_temperatura.plot(self.x,self.temperatura_data, color='red')

		
		self.gfc_presion.clear()
		self.gfc_presion.plot(self.x,self.presion_data, color='red')

		
		self.gfc_altura.clear()
		self.gfc_altura.plot(self.x,self.altura_data, color='red')

		self.gfc_angulo.clear()
		self.gfc_angulo.plot(self.x, self.yaw, pen='r', name='Yaw')
		self.gfc_angulo.plot(self.x, self.pitch, pen='g', name='Pitch')
		self.gfc_angulo.plot(self.x, self.roll, pen='b', name='Roll')

		if self.dato_arduino_estatico[2] < 3:
			self.aceleracion_x_subida = list(np.linspace(0,0,100))
			self.aceleracion_y_subida = list(np.linspace(0,0,100))
			self.aceleracion_z_subida = list(np.linspace(0,0,100))
			self.gfc_aceleracion_subida.clear()
			self.gfc_aceleracion_subida.plot(self.x, self.aceleracion_x_subida, pen='r', name='x')
			self.gfc_aceleracion_subida.plot(self.x, self.aceleracion_y_subida, pen='g', name='y')
			self.gfc_aceleracion_subida.plot(self.x, self.aceleracion_z_subida, pen='b', name='z')
		else:
			self.gfc_aceleracion_subida.clear()
			self.gfc_aceleracion_subida.plot(self.x, self.aceleracion_x, pen='r', name='x')
			self.gfc_aceleracion_subida.plot(self.x, self.aceleracion_y, pen='g', name='y')
			self.gfc_aceleracion_subida.plot(self.x, self.aceleracion_z, pen='b', name='z')



		if self.dato_arduino_estatico[2] < 3:
			self.gfc_aceleracion_caida.clear()
			self.gfc_aceleracion_caida.plot(self.x, self.aceleracion_x, pen='r', name='x')
			self.gfc_aceleracion_caida.plot(self.x, self.aceleracion_y, pen='g', name='y')
			self.gfc_aceleracion_caida.plot(self.x, self.aceleracion_z, pen='b', name='z')
		else:
			self.aceleracion_x_caida = list(np.linspace(0,0,100))
			self.aceleracion_y_caida = list(np.linspace(0,0,100))
			self.aceleracion_z_caida = list(np.linspace(0,0,100))
			self.gfc_aceleracion_caida.clear()
			self.gfc_aceleracion_caida.plot(self.x, self.aceleracion_x_caida, pen='r', name='x')
			self.gfc_aceleracion_caida.plot(self.x, self.aceleracion_y_caida, pen='g', name='y')
			self.gfc_aceleracion_caida.plot(self.x, self.aceleracion_z_caida, pen='b', name='z')




if __name__ == "__main__":
	app = QApplication(sys.argv)
	my_app= VentanaPrincipal()
	print('Salí de la ventana principal')
	my_app.show()
	isRun=False
	sys.exit(app.exec_())