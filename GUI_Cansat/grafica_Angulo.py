import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import pyqtgraph as pg

class GraficaAngulo():
	def __init__(self, p1, y):
		p1.setLabels(left='pitch')
		## create a new ViewBox, link the right axis to its coordinate system
		self.p2 = pg.ViewBox()
		p1.showAxis('right')
		p1.scene().addItem(self.p2)
		p1.getAxis('right').linkToView(self.p2)
		self.p2.setXLink(p1)
		p1.getAxis('right').setLabel('roll', color='#0000ff')

		## create third ViewBox. 
		## this time we need to create a new axis as well.
		self.p3 = pg.ViewBox()
		ax3 = pg.AxisItem('right')
		p1.layout.addItem(ax3, 2, 3)
		p1.scene().addItem(self.p3)
		ax3.linkToView(self.p3)
		self.p3.setXLink(p1)
		ax3.setZValue(-10000)
		ax3.setLabel('yaw', color='#ff0000')

		self.updateViews(p1)
		p1.vb.sigResized.connect(self.updateViews)


		p1.plot(np.sin(y))
		self.p2.addItem(pg.PlotCurveItem(np.sin(y), pen='b'))
		self.p3.addItem(pg.PlotCurveItem(np.sin(y), pen='r'))
	def updateViews(self,p1):
		## view has resized; update auxiliary views to match
		global p2, p3
		self.p2.setGeometry(p1.vb.sceneBoundingRect())
		self.p3.setGeometry(p1.vb.sceneBoundingRect())
		
		## need to re-update linked axes since this was called
		## incorrectly while views had different shapes.
		## (probably this should be handled in ViewBox.resizeEvent)
		self.p2.linkedViewChanged(p1.vb, self.p2.XAxis)
		self.p3.linkedViewChanged(p1.vb, self.p3.XAxis)