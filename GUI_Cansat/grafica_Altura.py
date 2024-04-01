from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import matplotlib.pyplot as plt

class GraficaAltura(FigureCanvas):
	def __init__(self):
		self.fig , self.ax = plt.subplots()
		super().__init__(self.fig) 
		altura = 321
		counts = 321
		bar_labels = 'red'
		bar_colors = 'tab:red'

		self.ax.bar(altura, counts, label=bar_labels, color=bar_colors)

		self.ax.set_ylabel('metros')
		self.ax.set_title('Altura')
