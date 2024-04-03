from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from main import VentanaPrincipal
import collections
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

class GraficaTemperatura(FigureCanvas):
	def __init__(self):
		fig = plt.figure()
		ax = plt.axes(xlim=(0,100), ylim=(0,6))
		samples =100
		sample_time = 200
		line_label = "Temperatura"
		lines = ax.plot([],[], color='r', marker='o',label=line_label)[0]
		line_value_text = ax.text(.85,.95,'', transform=ax.transAxes)
		data = collections.deque([0] * samples, maxlen= samples)
		plt.title("Temperatura", fontsize=15)
		ax.set_xlabel("tiempo", fontsize=12)
		ax.set_ylabel("temp", fontsize=12) 
		anim = animation.FuncAnimation(fig, VentanaPrincipal.plotData, fargs=(data,samples,lines,line_value_text,line_label), interval=sample_time) 
		plt.show()
		super().__init__(fig)