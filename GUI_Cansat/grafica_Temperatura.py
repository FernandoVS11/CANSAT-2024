from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt
from actualizar_Grafica import *
import matplotlib.animation as animation

class GraficaTemperatura(FigureCanvas, ActualizarGrafica):
	def __init__(self, x,y):
		self.fig , self.ax = plt.subplots()
		time= x
		temp= y
		self.ax = plt.plot(time,temp, color='r', marker='o')
		plt.title("Temperatura", fontsize=15)
		plt.xlabel("tiempo", fontsize=12)
		plt.ylabel("temp", fontsize=12)
		super().__init__(self.fig)
	def actualizar(self):
		return animation.FuncAnimation(self.fig, plotData, fargs=(self.Samples,self.serial_connection,self.lines,self.lineValueText,self.lineLabel), interval=self.sample_time) 	