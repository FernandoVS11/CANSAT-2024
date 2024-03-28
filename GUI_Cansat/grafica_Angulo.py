import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np


class GraficaAngulo(FigureCanvas):
	def __init__(self, x,y,z):
		# Fixing random state for reproducibility
		np.random.seed(19680801)

		dt = 0.01
		t = np.arange(0, 30, dt)

		# Two signals with a coherent part at 10 Hz and a random part
		s1 = np.sin(x)
		s2 = np.sin(y)
		s3 = np.sin(z)

		self.fig, self.ax = plt.subplots()
		self.ax = plt.plot(s1,s2,s3)
		plt.title("Angulo", fontsize=15)
		plt.xlabel("tiempo", fontsize=12)
		plt.ylabel("Grados", fontsize=12)
		super().__init__(self.fig) 