from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt

class GraficaPresion(FigureCanvas):    
	def __init__(self, parent=None):
		self.fig , self.ax = plt.subplots()
		super().__init__(self.fig) 
		self.ax.plot([0,50, 60, 80, 90], 'o-r')
		self.ax.set(xlabel='m^2', ylabel='N')
		self.ax.set_title('presion')
			