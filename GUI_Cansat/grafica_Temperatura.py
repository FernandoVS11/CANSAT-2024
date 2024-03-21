from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt

class GraficaTemperatura(FigureCanvas):
	def __init__(self, parent=None): 
		t = np.linspace(0, 2 * np.pi, 1024)
		data2d = np.sin(t)[:, np.newaxis] * np.cos(t)[np.newaxis, :]

		self.fig, self.ax = plt.subplots(1,dpi=50, figsize=(1, 1), 
            sharey=True, facecolor='white')
		super().__init__(self.fig) 
		im = self.ax.imshow(data2d)
		self.ax.set_title('Temperatura\n')

		self.fig.colorbar(im, ax=self.ax, label='Interactive colorbar')