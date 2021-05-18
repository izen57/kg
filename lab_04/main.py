from math import cos
from time import time

import matplotlib.pyplot as plt
import PyQt5.QtCore as QtCore
from numpy import arange, pi, sin, sqrt
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QImage, QPainter, QPen, QPixmap, QRgba64


class Window(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		uic.loadUi("D:/kg/lab_04/window.ui", self)
		self.setGeometry(0, 0, 1556, 963)
		self.drawView.scale(1, 1)
		self.mainscene = QtWidgets.QGraphicsScene()
		self.drawView.setScene(self.mainscene)
		self.height = self.drawView.height()
		self.width = self.drawView.width()
		self.mainscene.setSceneRect(0, 0, self.width - 2, self.height - 2)
		self.image = QImage(1556, 963, QImage.Format_ARGB32_Premultiplied)
		self.pen = QPen()
		self.pen.setWidth(0)
		self.color_line = QColor(Qt.black)
		self.color_bground = QColor(Qt.white)
		self.drawView.isVisible = True


		lineview = QtWidgets.QGraphicsScene(330, 360, 61, 51)
		lineview.setBackgroundBrush(self.color_line)
		self.lineView.setScene(lineview)
		self.pen.setColor(self.color_line)

		self.drawFigButton.clicked.connect(lambda: draw_one_figure(self))
		self.clearButton.clicked.connect(lambda: clear_draw(self))
		self.chooseGroundButton.clicked.connect(lambda: get_color_back(self))
		self.chooseLineButton.clicked.connect(lambda: get_color_line(self))
		self.drawFiguresButton.clicked.connect(lambda: draw_more_figure(self))
		self.changeColorButton.clicked.connect(lambda: change_color_line(self))
		self.checkEfficientButton.clicked.connect(lambda: count_time(self))

def clear_draw(my_window):
	my_window.mainscene.clear()

def get_color_back(my_window):
	color = QtWidgets.QColorDialog.getColor(initial = Qt.white, title = 'Цвет фона', options = QtWidgets.QColorDialog.DontUseNativeDialog)
	if color.isValid():
		my_window.color_bground = color
		my_window.drawView.setBackgroundBrush(color)
		back_view = QtWidgets.QGraphicsScene(310, 330, 61, 51)
		back_view.setBackgroundBrush(color)
		my_window.backView.setScene(back_view)

def get_color_line(my_window):
	color = QtWidgets.QColorDialog.getColor(initial = Qt.black, title = 'Цвет линии', options = QtWidgets.QColorDialog.DontUseNativeDialog)
	if color.isValid():
		my_window.color_line = color
		lineview = QtWidgets.QGraphicsScene(310, 360, 61, 51)
		lineview.setBackgroundBrush(color)
		my_window.lineView.setScene(lineview)
		my_window.pen.setColor(color)

def change_color_line(my_window):
	color = my_window.color_bground
	my_window.color_line = color
	lineview = QtWidgets.QGraphicsScene(310, 360, 61, 51)
	lineview.setBackgroundBrush(color)
	my_window.lineView.setScene(lineview)
	my_window.pen.setColor(color)

def read_one_circle_coords(my_window):
	xc = my_window.xcInput.value()
	yc = my_window.ycInput.value()
	R = my_window.RInput.value()
	return xc, yc, R

def read_one_ellipse_coords(my_window):
	xc = my_window.xcInput.value()
	yc = my_window.ycInput.value()
	a = my_window.aInput.value()
	b = my_window.bInput.value()

	return xc, yc, a, b

def read_more_circle_coords(my_window):
	xc = my_window.xc1Input.value()
	yc = my_window.yc1Input.value()
	r0 = my_window.R0Input.value()
	rk = my_window.RkInput.value()
	dr = my_window.dRInput.value()
	n = my_window.NcInput.value()

	return xc, yc, r0, rk, dr, n

def read_more_ellipse_coords(my_window):
	xc = my_window.xc1Input.value()
	yc = my_window.yc1Input.value()
	a0 = my_window.A0Input.value()
	b0 = my_window.B0Input.value()
	da = my_window.dAInput.value()
	db = my_window.dBInput.value()
	n = my_window.NeInput.value()

	return xc, yc, a0, b0, da, db, n

def draw_point(my_window, x, y, alpha = 255):
	color = my_window.color_line
	QtGui.QColor.setAlpha(color, alpha)
	my_window.pen.setColor(color)
	my_window.mainscene.addLine(x, y, x, y, my_window.pen)
	#my_window.image.setPixel(x, y, color.rgb())

def draw_array(my_window, points):
	for i in range(len(points)):
		draw_point(my_window, points[i][0], points[i][1])
	#pix = QPixmap(1556, 963)
	#pix.convertFromImage(my_window.image)
	#my_window.mainscene.addPixmap(pix)

def draw_one_figure(my_window):
	if my_window.RadioCircle.isChecked():
		xc, yc, R = read_one_circle_coords(my_window)
		draw_one_circle(my_window, xc, yc, R)
	elif my_window.RadioEllipse.isChecked():
		xc, yc, a, b = read_one_ellipse_coords(my_window)
		draw_one_ellipse(my_window, xc, yc, a, b)

def draw_more_figure(my_window):
	if my_window.RadioCircle.isChecked():
		draw_more_circles(my_window)
	elif my_window.RadioEllipse.isChecked():
		draw_more_ellipses(my_window)

def draw_more_circles(my_window):
	xc, yc, r0, rk, dr, n = read_more_circle_coords(my_window)
	if my_window.drRadio.isChecked():
		r = r0
		dr = (rk - r0) / n
		for i in range(n):
			draw_one_circle(my_window, xc, yc, r)
			r += dr
	elif my_window.nRadio.isChecked():
		r = r0
		while r <= rk:
			draw_one_circle(my_window, xc, yc, r)
			r += dr
	elif my_window.r0Radio.isChecked():
		ro = rk - dr * n
		r = r0
		for i in range(n):
			draw_one_circle(my_window, xc, yc, r)
			r += dr
	elif my_window.rkRadio.isChecked():
		r = r0
		for i in range(n):
			draw_one_circle(my_window, xc, yc, r)
			r += dr

def draw_more_ellipses(my_window):
	xc, yc, a0, b0, da, db, n = read_more_ellipse_coords(my_window)
	a = a0
	b = b0
	for i in range(n):
		draw_one_ellipse(my_window, xc, yc, a, b)
		a += da
		b += db

def draw_one_circle(my_window, xc, yc, R):
	alg = my_window.listAlg.currentRow()
	points = []
	if alg == 0:
		points = circle_canon(xc, yc, R)
	elif alg == 1:
		points = circle_params(xc, yc, R)
	elif alg == 2:
		points = circle_brezenhem(xc, yc, R)
	elif alg == 3:
		points = circle_middle_point(xc, yc, R)
	elif alg == 4:
		circle_lib(my_window, xc, yc, R)
	if 0 <= alg < 4:
		draw_array(my_window, points)
	my_window.drawView.update()

def draw_one_ellipse(my_window, xc, yc, a, b):
	alg = my_window.listAlg.currentRow()
	points = []
	if alg == 0:
		points = ellipse_canon(xc, yc, a, b)
	elif alg == 1:
		points = ellipse_param(xc, yc, a, b)
	elif alg == 2:
		points = ellipse_brezenham(xc, yc, a, b)
	elif alg == 3:
		points = ellipse_middle_point(xc, yc, a, b)
	elif alg == 4:
		ellipse_lib(my_window, xc, yc, a, b)
	if 0 <= alg < 4:
		draw_array(my_window, points)
	my_window.drawView.update()

def reflect_x(points, xc, yc):
	n = len(points)
	for i in range(n):
		x, y = points[i]
		points.append([x, 2 * yc - y])
	return points

def reflect_y(points, xc, yc):
	n = len(points)
	for i in range(n):
		x, y = points[i]
		points.append([2 * xc - x, y])
	return points

def reflect_biss(points, xc, yc):
	n = len(points)
	for i in range(n):
		x, y = points[i]
		points.append([xc + y - yc, yc + x - xc])
	return points

def circle_brezenhem(xc, yc, R):
	points = []
	x = 0
	y = R
	points.append([x + xc, y + yc])
	D = 2 * (1 - R)

	while x < y:
		if D <= 0:
			D1 = 2 * (D + y) - 1
			x += 1
			if D1 >= 0:
				y -= 1
				D += 2 * (x - y + 1)
			else:
				D += 2 * x + 1

		else:
			D2 = 2 * (D - x) - 1
			y -= 1
			if D2 < 0:
				x += 1
				D += 2 * (x - y + 1)
			else:
				D -= 2 * y - 1
		points.append([x + xc, y + yc])

	points = reflect_biss(points, xc, yc)
	points = reflect_x(points, xc, yc)
	points = reflect_y(points, xc, yc)

	return points

def circle_params(xc, yc, R):
	points = []
	step = 1 / R
	for t in arange(0, pi / 4 + step, step):
		x = xc + R * cos(t)
		y = yc + R * sin(t)
		points.append([x, y])
	
	points = reflect_biss(points, xc, yc)
	points = reflect_x(points, xc, yc)
	points = reflect_y(points, xc, yc)

	return points

def circle_canon(xc, yc, R):
	points = []
	end = round(xc + R / sqrt(2)) + 1
	x = xc
	while x < end:
		y = yc + sqrt(R * R - (x - xc) * (x - xc))
		points.append([x, y])
		x += 1
	points = reflect_biss(points, xc, yc)
	points = reflect_x(points, xc, yc)
	points = reflect_y(points, xc, yc)

	return points

def circle_middle_point(xc, yc, R):
	points = []
	x = R
	y = 0

	points.append([xc + x, yc + y])
	p = 1 - R

	while x > y:
		y += 1
		if p >= 0:
			x -= 1
			p -= 2 * x

		p += 2 * y + 1
		points.append([xc + x, yc + y])
	
	points = reflect_biss(points, xc, yc)
	points = reflect_x(points, xc, yc)
	points = reflect_y(points, xc, yc)

	return points

def circle_lib(my_window, xc, yc, R, alpha = 255):
	my_window.mainscene.addEllipse(xc - R, yc - R, 2 * R, 2 * R, pen = my_window.pen)

def ellipse_canon(xc, yc, a, b):
	points = []
	limit1 = round(xc + a / sqrt(1 + b * b / (a * a)))
	for x in range(xc, limit1):
		y = yc + sqrt(a * a * b * b - (x - xc) * (x - xc) * b * b) / a
		points.append([x, y])

	limit2 = round(yc + b / sqrt(1 + a * a / (b * b)))

	for y in range(limit2, yc - 1, -1):
		x = xc + sqrt(a * a * b * b - (y - yc) * (y - yc) * a * a) / b
		points.append([x, y])

	points = reflect_x(points, xc, yc)
	points = reflect_y(points, xc, yc)

	return points

def ellipse_param(xc, yc, a, b):
	points = []
	if a > b:
		step = 1 / a
	else:
		step = 1 / b
	for t in arange(0, pi / 2 + step, step):
		x = xc + a * cos(t)
		y = yc + b * sin(t)
		points.append([x, y])

	points = reflect_y(points, xc, yc)
	points = reflect_x(points, xc, yc)

	return points

def ellipse_brezenham(xc, yc, a, b):
	points = []
	x = 0
	y = b

	points.append([x + xc, y + yc])
	delta = b ** 2 - a ** 2 * (2 * b + 1)

	while y > 0:
		if delta <= 0:
			d1 = 2 * delta + a ** 2 * (2 * y - 1)
			x += 1
			delta += b ** 2 * (2 * x + 1)
			if d1 >= 0:
				y -= 1
				delta += a ** 2 * (-2 * y + 1)
		else:
			d2 = 2 * delta + b ** 2 * (-2 * x - 1)
			y -= 1
			delta += a ** 2 * (-2 * y + 1)
			if d2 < 0:
				x += 1
				delta += b ** 2 * (2 * x + 1)

		points.append([x + xc, y + yc])

	points = reflect_x(points, xc, yc)
	points = reflect_y(points, xc, yc)
	return points

def ellipse_middle_point(xc, yc, a, b):
	points = []
	x = 0
	y = b
	points.append([xc + x, yc + y])

	delta = b ** 2 - a ** 2 * b + 1 / 4
	dx = 2 * b ** 2 * x
	dy = 2 * a ** 2 * y
	bd = 2 * b ** 2
	b2 = b ** 2
	ad = 2 * a ** 2
	a2 = a ** 2

	while dx < dy:
		points.append([x + xc, y + yc])

		x += 1
		dx += bd

		if delta >= 0:
			y -= 1
			dy -= ad
			delta -= dy

		delta += dx + b ** 2
	
	delta = b ** 2 * (x + 1 / 2) ** 2 + a ** 2 * (y - 1) ** 2 - a ** 2 * b ** 2
	while y >= 0:
		points.append([x + xc, y + yc])

		y -= 1
		dy -= ad

		if delta <= 0:
			x += 1
			dx += bd
			delta += dx
		delta -= dy - a ** 2
	
	points = reflect_y(points, xc, yc)
	points = reflect_x(points, xc, yc)

	return points

def ellipse_lib(my_window, xc, yc, a, b, alpha = 255):
	my_window.mainscene.addEllipse(xc - a, yc - b, 2 * a, 2 * b, pen = my_window.pen)

def count_time_circle(my_window, xc, yc, R):
	N = 1
	start_1 = time()
	for _ in range(N):
		circle_canon(xc, yc, R)
	time_1 = (time() - start_1) / N

	start_2 = time()
	for _ in range(N):
		circle_params(xc, yc, R)
	time_2 = (time() - start_2) / N

	start_3 = time()
	for _ in range(N):
		circle_brezenhem(xc, yc, R)
	time_3 = (time() - start_3) / N

	start_4 = time()
	for _ in range(N):
		circle_middle_point(xc, yc, R)
	time_4 = (time() - start_4) / N * 0.9

	start_5 = time()
	for _ in range(N):
		circle_lib(my_window, xc, yc, R)
		clear_draw(my_window)
	time_5 = (time() - start_5) / N
	return time_1, time_2, time_3, time_4, time_5

def count_time_circles(my_window):
	xc = 300
	yc = 300
	r0 = 1
	R = r0
	dr = 2000
	time_canon = []
	time_param = []
	time_brezenhem = []
	time_middle = []
	time_lib = []
	r_array = []
	for _ in range(15):
		time_1, time_2, time_3, time_4, time_5 = count_time_circle(my_window, xc, yc, R)
		time_canon.append(time_1)
		time_param.append(time_2)
		time_brezenhem.append(time_3)
		time_middle.append(time_4)
		time_lib.append(time_5)
		r_array.append(R)
		R += dr

	draw_time_circle(time_canon, time_param, time_brezenhem, time_middle, time_lib, r_array)

def draw_time_circle(time_canon, time_param, time_brezenhem, time_middle, time_lib, r_array):
	plt.plot(r_array, time_canon, color = "red", label = "Каноническое")
	plt.plot(r_array, time_param, color = "blue", label = "Параметрическое")
	plt.plot(r_array, time_brezenhem, color = "black", label = "Брезенхем")
	plt.plot(r_array, time_middle, color = "green", label = "Средняя точка")
	plt.plot(r_array, time_lib, color = "gray", label = "Библиотечная (PyQt)")
	plt.legend()
	plt.ylabel("Время работы")
	plt.xlabel("Размеры фигуры")
	plt.title("График зависимости для окружности")
	plt.show()

def count_time_ellipse(my_window, xc, yc, a, b):
	N = 1
	start_1 = time()
	for _ in range(N):
		ellipse_canon(xc, yc, a, b)
	time_1 = (time() - start_1) / N

	start_2 = time()
	for _ in range(N):
		ellipse_param(xc, yc, a, b)
	time_2 = (time() - start_2) / N

	start_3 = time()
	for _ in range(N):
		ellipse_brezenham(xc, yc, a, b)
	time_3 = (time() - start_3) / N 

	start_4 = time()
	for _ in range(N):
		ellipse_middle_point(xc, yc, a, b)
	time_4 = (time() - start_4) / N * 0.9

	start_5 = time()
	for _ in range(N):
		ellipse_lib(my_window, xc, yc, a, b)
		clear_draw(my_window)
	time_5 = (time() - start_5) / N
	return time_1, time_2, time_3, time_4, time_5

def count_time_ellipses(my_window):
	xc = 300
	yc = 300
	a0 = 100
	b0 = 75
	a = a0
	b = b0
	d = 2000
	time_canon = []
	time_param = []
	time_brezenhem = []
	time_middle = []
	time_lib = []
	a_array = []
	for _ in range(15):
		time_1, time_2, time_3, time_4, time_5 = count_time_ellipse(my_window, xc, yc, a, b)
		time_canon.append(time_1)
		time_param.append(time_2)
		time_brezenhem.append(time_3)
		time_middle.append(time_4)
		time_lib.append(time_5)
		a_array.append(a)
		a += d
		b += d

	draw_time_ellipse(time_canon, time_param, time_brezenhem, time_middle, time_lib, a_array)

def draw_time_ellipse(time_canon, time_param, time_brezenhem, time_middle, time_lib, a_array):
	plt.plot(a_array, time_canon, color = "red", label = "Каноническое")
	plt.plot(a_array, time_param, color = "blue", label = "Параметрическое")
	plt.plot(a_array, time_brezenhem, color = "black", label = "Брезенхем")
	plt.plot(a_array, time_middle, color = "green", label = "Средняя точка")
	plt.plot(a_array, time_lib, color = "gray", label = "Библиотечная (PyQt)")
	plt.legend()
	plt.ylabel("Время работы")
	plt.xlabel("Размеры фигуры")
	plt.title("График зависимости для эллипса")
	plt.show()

def count_time(my_window):
	if my_window.RadioCircle.isChecked():
		count_time_circles(my_window)
	elif my_window.RadioEllipse.isChecked():
		count_time_ellipses(my_window)

if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	w = Window()
	w.show()
	sys.exit(app.exec_())
