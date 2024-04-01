# @autor: Magno Efren
# Youtube: https://www.youtube.com/c/MagnoEfren
import serial, time
from threading import Thread
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi


from imagenes import logo

from grafica_Aceleracion_Caida import *
from grafica_Aceleracion_Subida import *
from grafica_Altura import *
from grafica_Angulo import *
from grafica_Presion import *
from grafica_Temperatura import *

isRecieve = False
isRun = True
value = 0.0
serial_connection = serial

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
		self.bt_cerrar.clicked.connect(lambda: self.close() and self.serial.close())

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
		
		serial_port = 'COM3'
		baud_rate = 9600
		try:
			self.serial_connection = serial.Serial(serial_port, baud_rate)
		except:
			print("Error de coneccion con el puerto")

		
		thread = Thread(target = getData)
		thread.start()

		while isRecieve != True:
			print("Starting receive data")
			time.sleep(0.1)
		
		self.gfc_presion = GraficaPresion()
		self.gfc_altura = GraficaAltura()
		self.gfc_temperatura = GraficaTemperatura()
		self.gfc_aceleracion_subida = GraficaAceleracionSubida()
		self.gfc_aceleracion_caida = GraficaAceleracionCaida()
		self.gfc_angulo = GraficaAngulo()
		

		self.presion.addWidget(self.gfc_presion)
		self.altura.addWidget(self.gfc_altura)	
		self.temperatura.addWidget(self.gfc_temperatura)
		self.aceleracion_subida.addWidget(self.gfc_aceleracion_subida)
		self.aceleracion_caida.addWidget(self.gfc_aceleracion_caida)
		self.angulo.addWidget(self.gfc_angulo)
		VentanaPrincipal.show()
		self.isRun=False
		thread.join()
		self.serial_connection.close()
	def plotData(self,data,samples,lines,line_value_text,line_label):
		data.append(value)
		lines.set_data(range(samples), data)
		line_value_text.set_text(line_label+' = '+ str(round(value,2)))
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
def getData(self):
	time.sleep(1.0)
	self.serial_connection.reset_inout_buffer()
	while (isRun):
		global isRecieve
		self.value = float(self.serial_connection.readline().strip())
		isRecieve = True

if __name__ == "__main__":
    app = QApplication(sys.argv)
    VentanaPrincipal()
    sys.exit(app.exec_())	