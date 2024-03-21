from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt

class GraficaAltura(FigureCanvas):
	def __init__(self, parent=None):     
		self.fig , self.ax = plt.subplots(1,dpi=60, figsize=(1, 1), 
										  sharey=True, facecolor='white')
		super().__init__(self.fig) 
		x = np.arange(0.1, 4, 0.5)
		y = np.exp(-x)
		self.ax.set_title('Altura\n')
		self.ax.errorbar(x, y, xerr=0.2, yerr=0.4)