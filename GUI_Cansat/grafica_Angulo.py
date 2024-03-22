import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class GraficaAngulo(FigureCanvas):
	def __init__(self, parent=None):
		u = [2,3,1]
		v= [0,5,4]
		q= [7,-8,10]

		self.fig=plt.figure()
		self.ax= plt.axes(projection ="3d")
		self.ax.set_xlim([-10,10])
		self.ax.set_ylim([-10,10])
		self.ax.set_zlim([0,10])

		start = [0,0,0]
		self.ax.quiver(start[0], start[1], start[2], u[0], u[1], u[2], color='r')
		self.ax.quiver(start[0], start[1], start[2], v[0], v[1], v[2], color='g')
		self.ax.quiver(start[0], start[1], start[2], q[0], q[1], q[2], color='b')
		
		self.ax.plot([], [], [], color="r", label="40°")
		self.ax.plot([], [], [], color="g", label="50°")
		self.ax.plot([], [], [], color="b", label="60°")
		self.ax.set_xlabel("x")
		self.ax.set_ylabel("y")
		self.ax.set_zlabel("z")
		self.ax.legend()
		super().__init__(self.fig) 