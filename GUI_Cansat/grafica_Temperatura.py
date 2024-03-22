from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt

class GraficaTemperatura(FigureCanvas):
	def __init__(self, parent=None):
		self.fig , self.ax = plt.subplots()
		time=[1,2,3,4,5,6,7,8]
		temp=[18.1,15.8,10,11.5,20,21.2,10.2,15.2]
		self.ax = plt.plot(time,temp, color='c', marker='o')
		plt.title("Temperatura", fontsize=15)
		plt.xlabel("time", fontsize=12)
		plt.ylabel("temp", fontsize=12)
		super().__init__(self.fig) 	