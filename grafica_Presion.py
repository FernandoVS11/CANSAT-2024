from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt

class GraficaPresion(FigureCanvas):    
	def __init__(self, parent=None):
		self.fig , self.ax = plt.subplots(1,dpi=60, figsize=(1, 1), 
										  sharey=True, facecolor='white')
		super().__init__(self.fig) 
		t = np.arange(0., 5., 0.2)
		self.ax.set_title('Presión\n')
		self.ax.plot(t, t, 'r--', t, t**2, 'bs', t, t**3, 'g^')
			