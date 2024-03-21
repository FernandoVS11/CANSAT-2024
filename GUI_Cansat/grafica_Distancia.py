from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt

class GraficaDistancia(FigureCanvas):
	def __init__(self, parent=None):
		self.fig , self.ax = plt.subplots(1,dpi=100, figsize=(4, 4), 
										  sharey=True, facecolor='white')
		super().__init__(self.fig) 
		self.ax.plot([1, 2, 3, 4], 'o-r')
		self.ax.set(ylabel='distancia', xlabel='cargas')