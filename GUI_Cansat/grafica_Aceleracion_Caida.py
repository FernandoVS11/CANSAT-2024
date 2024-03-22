from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt

class GraficaAceleracionCaida(FigureCanvas):
	def __init__(self, parent=None):
		self.fig=plt.figure()
		super().__init__(self.fig) 

		self.ax= plt.axes(projection="3d")
		x_data= np.arange(0, 50, 0.1)
		y_data= np.arange(0, 50, 0.1)
		z_data= x_data * y_data

		self.ax.plot(x_data, y_data, z_data, color='r')
		self.ax.set_title("Aceleracion")
		self.ax.set_xlabel("m/s")
		self.ax.set_ylabel("s")
		self.ax.set_zlabel("m/s^2")