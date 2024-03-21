from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt

class GraficaAceleracion(FigureCanvas):
	def __init__(self, parent=None):     
		self.fig , self.ax = plt.subplots(1,dpi=100, figsize=(10, 10), 
										  sharey=True, facecolor='white')
		super().__init__(self.fig) 
		x = np.arange(0.1, 4, 0.5)
		y = np.exp(-x)
		self.ax.set_title('Aceleración\n')
		self.ax.errorbar(x, y, xerr=0.2, yerr=0.4)