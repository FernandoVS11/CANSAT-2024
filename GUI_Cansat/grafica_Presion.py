from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt
import  serial,time

# try:
#     ard = serial.Serial("COM3", 9600)     
#     datos =ard.readline()    
# except:
#     print("Error de coneccion con el puerto")
#     raise

class GraficaPresion(FigureCanvas):    
	def __init__(self, parent=None):
		self.fig , self.ax = plt.subplots()
		super().__init__(self.fig) 
		self.ax.set_ylabel('presion', fontsize=12)
		self.ax.set_xlabel('tiempo', fontsize=12)
		self.ax.set_title('Presion')
		self.ax.plot([0,50,40,20,30,10], 'o-c')
		#time.sleep(1)  
		
			