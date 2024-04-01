from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt

class GraficaAceleracionSubida(FigureCanvas):
	def __init__(self):
		self.fig=plt.figure()
		super().__init__(self.fig) 

		self.ax= plt.axes(projection="3d")
		x_data= 10
		y_data= 10
		z_data= 10

		self.ax.plot(x_data, y_data, z_data)
		self.ax.set_title("Aceleracion")
		self.ax.set_xlabel("m/s")
		self.ax.set_ylabel("s")
		self.ax.set_zlabel("m/s^2")