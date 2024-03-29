# @autor: Magno Efren
# Youtube: https://www.youtube.com/c/MagnoEfren
import sys,serial,time,collections
from threading import Thread
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore, QtWidgets
from PyQt5.uic import loadUi
import matplotlib.animation as animation

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
			serial_connection = serial.Serial(serial_port, baud_rate)
		except:
			print("Error de coneccion con el puerto")

		Samples =100
		sample_time = 200
		data = collections.deque([0] * self.Samples, maxlen= self.Samples)

		self.x = list(np.linspace(0,100,100))
		self.y = list(np.linspace(0,100,100))
		self.z = list(np.linspace(0,100,100))
		self.value_arduino = 0
		
		thread = Thread(target = getData)
		thread.start()

		while isRecieve != True:
			print("Starting receive data")
			time.sleep(0.1)
		anim = animation.FuncAnimation(fig, plotData, fargs=(Samples,serial_connection,lines,lineValueText,lineLabel), interval=sample_time)
		self.serial.readyRead.connect(self.read_ports)

		self.gfc_presion = GraficaPresion(self.x, self.y)
		self.gfc_altura = GraficaAltura(self.value_arduino)
		self.gfc_temperatura = GraficaTemperatura(self.x, self.y)
		self.gfc_aceleracion_subida = GraficaAceleracionSubida(self.x, self.y, self.z)
		self.gfc_aceleracion_caida = GraficaAceleracionCaida(self.x, self.y, self.z)
		self.gfc_angulo = GraficaAngulo(self.x, self.y, self.z)
		

		self.presion.addWidget(self.gfc_presion)
		self.altura.addWidget(self.gfc_altura)	
		self.temperatura.addWidget(self.gfc_temperatura)
		self.aceleracion_subida.addWidget(self.gfc_aceleracion_subida)
		self.aceleracion_caida.addWidget(self.gfc_aceleracion_caida)
		self.angulo.addWidget(self.gfc_angulo)
		# self.pause(0.05)
	def getData(self):
		time.sleep(1.0)
		serial_connection.reset_inout_buffer()
		while (isRun):
			global isRecieve
			global value
			value = float(serial_connection.readline().strip())
			isRecieve = True
	def plotData(self,Samples,serialConnection,lines,lineValueText,lineLabel):
		data.append(value)
		lines.set_data(range(Samples),data)
		lineValueText.set_text(lineLabel+' = '+ str(round(value,2)))
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

	def read_ports(self):
		if not self.serial.canReadLine(): return
		rx= self.serial.readLine()
		self.value_arduino= str(rx, "utf-8").strip()
		self.value_arduino = float(self.value_arduino)
		print(self.value_arduino)
		self.x =self.y[1:]
		self.x.append(self.value_arduino)
		self.y =self.y[1:]
		self.y.append(self.value_arduino)
		self.z =self.y[1:]
		self.z.append(self.value_arduino)
		# self.plt.clear()
		# self.plt.plot(self.x, self.y)	

if __name__ == "__main__":
    app = QApplication(sys.argv)
    VentanaPrincipal().show()
    sys.exit(app.exec_())	