from math import fabs, floor, modf, trunc
from time import time

import matplotlib.pyplot as plt
import PyQt5.QtCore as QtCore
from numpy import around, cos, pi, sign, sin
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QBrush, QColor, QImage, QPainter, QPen, QPixmap, QRgba64


class Window(QtWidgets.QMainWindow):
	def __init__(self):
		QtWidgets.QWidget.__init__(self)
		uic.loadUi("D:/kg/lab_03/window.ui", self)
		self.drawView.scale(1, 1)
		self.mainscene = QtWidgets.QGraphicsScene()
		self.drawView.setScene(self.mainscene)
		self.height = self.drawView.height()
		self.width = self.drawView.width()
		self.mainscene.setSceneRect(0, 0, self.width - 2, self.height - 2)
		self.pen = QPen()
		self.pen.setWidth(0)
		self.color_line = QColor(Qt.black)
		self.color_bground = QColor(Qt.white)
		self.drawView.isVisible = True

		self.chooseGroundButton.clicked.connect(lambda: get_color_back(self))
		self.chooseLineButton.clicked.connect(lambda: get_color_line(self))
		self.cleanButton.clicked.connect(lambda: clear_draw(self))
		self.createLineButton.clicked.connect(lambda: draw_line(self))
		self.beamButton.clicked.connect(lambda: draw_beam(self))
		self.efficientButton.clicked.connect(lambda: count_time(self))
		self.pushButton.clicked.connect(lambda: com_step(self))

		lineview = QtWidgets.QGraphicsScene(340, 420, 61, 51)
		lineview.setBackgroundBrush(self.color_line)
		self.lineView.setScene(lineview)
		self.pen.setColor(self.color_line)

def integer(num):
	return int(num + (0.5 if num > 0 else -0.5))

def check_not_point(x0, y0, x1, y1):
	result = True
	if fabs(x0 - x1) <= 1e-6 and fabs(y0 - y1) <= 1e-6:
		result = False
	return result

def DDA_algorithm(my_window, x0, y0, x1, y1, draw = True, step = False):
	if check_not_point(x0, y0, x1, y1) == True:

		dx = x1 - x0
		dy = y1 - y0
		length = max(fabs(dx), fabs(dy))
		dx /= length
		dy /= length

		x = x0
		y = y0
		x_temp = x
		y_temp = y
		steps = 1
		i = 0
		while i <= length:
			if draw:
				draw_point(my_window, integer(x), integer(y))
			else:
				integer(x), integer(y)
			x += dx
			y += dy
			if (step):
				if not ((integer(x + dx) == integer(x) and integer(y + dy) != integer(y)) or (integer(x + dx) != integer(x) and integer(y + dy) == integer(y))):
					steps += 1
			x_temp = x
			y_temp = y
			i += 1
		if step:
			return steps
	else:
		draw_point(my_window, integer(x0), integer(y0))
		return 0

def brezenham_int(my_window, x0, y0, x1, y1, draw = True, step = False):
	if check_not_point(x0, y0, x1, y1) == True:
		x = x0
		y = y0
		dx = x1 - x0
		dy = y1 - y0
		sx = sign(dx)
		sy = sign(dy)
		dx = fabs(dx)
		dy = fabs(dy)

		change = 0
		if dy > dx:
			dx, dy = dy, dx
			change = 1
		error = 2 * dy - dx
		steps = 1
		i = 0
		while i <= dx:
			x_temp = x
			y_temp = y
			if draw:
				draw_point(my_window, x, y)
			if error >= 0:
				if change == 1:
					x += sx
				else:
					y += sy
				error -= 2 * dx
			if error <= 0:
				if change == 1:
					y += sy
				else:
					x += sx
				error += 2 * dy
			i += 1
			if step:
				if not (x_temp == x and y_temp != y or x_temp != x and y_temp == y):
					steps += 1
		if step:
			return steps
	else:
		draw_point(my_window, x0, y0)
		return 0

def brezenham_float(my_window, x0, y0, x1, y1, draw = True, step = False):
	if check_not_point(x0, y0, x1, y1) == True:
		x = x0
		y = y0
		dx = x1 - x0
		dy = y1 - y0
		sx = sign(dx)
		sy = sign(dy)
		dx = fabs(dx)
		dy = fabs(dy)

		change = 0
		if dy > dx:
			dx, dy = dy, dx
			change = 1
		m = dy / dx
		error = m - 0.5
		steps = 1
		i = 0
		while i <= dx:
			x_temp = x
			y_temp = y
			if draw:
				draw_point(my_window, x, y)
			if error > 0:
				if change == 1:
					x += sx
				else:
					y += sy
				error -= 1
			if error < 0:
				if change == 1:
					y += sy
				else:
					x += sx
			error += m
			i += 1
			if step:
				if not (x_temp == x and y_temp != y or x_temp != x and y_temp == y):
					steps += 1
		if step:
			return steps
	else:
		draw_point(my_window, x0, y0)
		return 0

def brezenham_no_step(my_window, x0, y0, x1, y1, draw = True, step = False):
	I = 255
	if check_not_point(x0, y0, x1, y1) == True:
		x = x0
		y = y0
		dx = x1 - x0
		dy = y1 - y0

		sx = sign(dx)
		sy = sign(dy)

		dx = fabs(dx)
		dy = fabs(dy)
		change = 0
		if dy > dx:
			dx, dy = dy, dx
			change = 1
		m = dy / dx
		error = I / 2
		m *= I
		W = I - m
		steps = 1
		draw_point(my_window, x, y, integer(error))
		i = 0
		while i <= dx:
			x_temp = x
			y_temp = y
			if error < W:
				if not change:
					x += sx
				else:
					y += sy
				error += m
			else:
				x += sx
				y += sy
				error -= W
			i += 1
			if draw:
				draw_point(my_window, x, y, integer(error))
			else:
				integer(error)
			if step:
				if not (x_temp == x and y_temp != y or x_temp != x and y_temp == y):
					steps += 1
		if step:
			return steps
	else:
		draw_point(my_window, x0, y0)
		return 0

def wu(my_window, x0, y0, x1, y1, draw = True, step = False):
	I = 255
	if check_not_point(x0, y0, x1, y1) == True:
		dx = x1 - x0
		dy = y1 - y0
		m = 1
		steps = 1
		go = 1
		x = x0
		y = y0
		if fabs(dy) > fabs(dx):
			if dy:
				m = dx / dy
			m1 = m

			if y0 > y1:
				m1 *= -1
				go *= -1

			for y_cur in range(integer(y0), integer(y1) + 1, go):
				p1 = x - floor(x)
				p2 = 1 - p1

				if draw:
					draw_point(my_window, x, y_cur, integer(p2 * I))
					draw_point(my_window, x + 1, y_cur, integer(p1 * I))
				else:
					integer(p1 * I), integer(p2 * I)

				if step and y_cur < y1:
					if integer(x) != integer(x + m):
						steps += 1

				x += m1

		else:
			if dx:
				m = dy / dx
			m1 = m

			if x0 > x1:
				go *= -1
				m1 *= -1

			for x_cur in range(integer(x0), integer(x1) + 1, go):
				p1 = y - floor(y)
				p2 = 1 - p1
				if draw:
					draw_point(my_window, x_cur, y, integer(p2 * I))
					draw_point(my_window, x_cur, y + 1, integer(p1 * I))
				else:
					integer(p1 * I), integer(p2 * I)
				if steps and x_cur < x1:
					if integer(y) != integer(y + m):
						steps += 1

				y += m1
	else:
		draw_point(my_window, x0, y0)
		return 0


def lib_func(my_window, x0, y0, x1, y1, draw = True):
	if draw:
		my_window.mainscene.addLine(x0, y0, x1, y1, pen = my_window.pen)
	if draw == False:
		my_window.mainscene.clear()

def get_color_back(my_window):
	color = QtWidgets.QColorDialog.getColor(initial = Qt.white, title = 'Цвет фона', options = QtWidgets.QColorDialog.DontUseNativeDialog)
	if color.isValid():
		my_window.color_bground = color
		my_window.drawView.setBackgroundBrush(color)
		back_view = QtWidgets.QGraphicsScene(340, 360, 61, 51)
		back_view.setBackgroundBrush(color)
		my_window.backView.setScene(back_view)



def get_color_line(my_window):
	color = QtWidgets.QColorDialog.getColor(initial = Qt.black, title = 'Цвет линии', options = QtWidgets.QColorDialog.DontUseNativeDialog)
	if color.isValid():
		my_window.color_line = color
		lineview = QtWidgets.QGraphicsScene(340, 420, 61, 51)
		lineview.setBackgroundBrush(color)
		my_window.lineView.setScene(lineview)
		my_window.pen.setColor(color)

def clear_draw(my_window):
	my_window.mainscene.clear()

def get_coords(my_window):
	x0 = my_window.x0Input.value()
	y0 = my_window.y0Input.value()
	x1 = my_window.x1Input.value()
	y1 = my_window.y1Input.value()
	return x0, y0, x1, y1

def draw_point(my_window, x, y, alpha = 255):
	color = my_window.color_line
	QtGui.QColor.setAlpha(color, alpha)
	my_window.pen.setColor(color)
	my_window.mainscene.addLine(x, y, x, y, my_window.pen)

def draw_line(my_window):
	x0, y0, x1, y1 = get_coords(my_window)
	alf = my_window.listAlg.currentRow()
	if alf == 0:
		DDA_algorithm(my_window, x0, y0, x1, y1)
	elif alf == 1:
		brezenham_int(my_window, x0, y0, x1, y1)
	elif alf == 2:
		brezenham_float(my_window, x0, y0, x1, y1)
	elif alf == 3:
		brezenham_no_step(my_window, x0, y0, x1, y1)
	elif alf == 4:
		wu(my_window, x0, y0, x1, y1)
	elif alf == 5:
		lib_func(my_window, x0, y0, x1, y1)
	my_window.drawView.update()

def count_next_beam_point(x0, y0, radius, angle):
	x1 = x0 + radius * cos(angle * pi / 180)
	y1 = y0 + radius * sin(angle * pi / 180)
	return x1, y1

def get_beam(my_window):
	x0 = my_window.xkInput.value()
	y0 = my_window.ykInput.value()
	radius = my_window.rInput.value()
	angle = my_window.deltaAlphaInput.value()
	return x0, y0, radius, angle

def draw_beam(my_window):
	xk, yk, radius, angle = get_beam(my_window)
	alf = my_window.listAlg.currentRow()
	if alf == 0:
		draw_func = DDA_algorithm
	elif alf == 1:
		draw_func = brezenham_int
	elif alf == 2:
		draw_func = brezenham_float
	elif alf == 3:
		draw_func = brezenham_no_step
	elif alf == 4:
		draw_func = wu
	elif alf == 5:
		draw_func = lib_func
	beam_draw(my_window, xk, yk, radius, angle, draw_func)

def beam_draw(my_window, xk, yk, radius, angle, draw_func, draw = True):
	step = 0
	while abs(step) < 360:
		x, y = count_next_beam_point(xk, yk, radius, step)
		draw_func(my_window, xk, yk, x, y, draw)
		step += angle

def count_time(my_window):
	xk, yk, radius, angle = get_beam(my_window)
	my_time = []

	start_1 = time()
	for i in range(20):
		beam_draw(my_window, xk, yk, radius, angle, DDA_algorithm, draw = False)
	my_time.append(time() - start_1)

	start_2 = time()
	for i in range(20):
		beam_draw(my_window, xk, yk, radius, angle, brezenham_int, draw = False)
	my_time.append(time() - start_2)

	start_3 = time()
	for i in range(20):
		beam_draw(my_window, xk, yk, radius, angle, brezenham_float, draw = False)
	my_time.append(time() - start_3)

	start_4 = time()
	for i in range(20):
		beam_draw(my_window, xk, yk, radius, angle, brezenham_no_step, draw = False)
	my_time.append(time() - start_4)

	start_5 = time()
	for i in range(20):
		beam_draw(my_window, xk, yk, radius, angle, wu, draw = False)
	my_time.append(time() - start_5)

	start_6 = time()
	for i in range(20):
		beam_draw(my_window, xk, yk, radius, angle, lib_func, draw = False)
	my_time.append(time() - start_6)

	for i in range(len(my_time)):
	   my_time[i] /= 20

	plt.figure(figsize = (10, 5))
	plt.rcParams['font.size'] = '14'

	plt.bar(["ЦДА", "Брезенхем\n(float)", "Брезенхем\n(int)", "Брезенхем\n(сглаживание)", "Ву", "Библиотечная"], my_time, color = "red")
	plt.title("Исследование времени выполнения\n{0} - длина отрезка; {1} - угол пучка".format(radius, angle))
	plt.ylabel("Время в секундах")
	my_window.mainscene.clear()
	plt.show()

def count_step(my_window, xk, yk, radius, angle, draw_func):
	x, y = count_next_beam_point(xk, yk, radius, angle)
	return draw_func(my_window, xk, yk, x, y, draw = False, step = True)

def com_step(my_window):
	xk, yk, radius, angle = get_beam(my_window)
	my_step_DDA = []
	my_step_brez_int = []
	my_step_brez_float = []
	my_step_brez_no_step = []
	my_step_wu = []
	for i in range(1, 90):
		my_step_DDA.append(count_step(my_window, xk, yk, radius, i, DDA_algorithm))
		my_step_brez_int.append(count_step(my_window, xk, yk, radius, i, brezenham_int))
		my_step_brez_float.append(count_step(my_window, xk, yk, radius, i, brezenham_float))
		my_step_brez_no_step.append(count_step(my_window, xk, yk, radius, i, brezenham_no_step))
		my_step_wu.append(count_step(my_window, xk, yk, radius, i, wu))
	plt.figure(figsize = (10, 5))
	plt.rcParams['font.size'] = '14'
	my_angle = [i for i in range(1, 90)]
	plt.plot(my_angle, my_step_DDA, label = 'ЦДА', color = "green")
	plt.plot(my_angle, my_step_brez_int, label = 'Брезенхем (int)', color = "red")
	plt.plot(my_angle, my_step_brez_float, label = 'Брезенхем (float)', color = "blue")
	plt.plot(my_angle, my_step_brez_no_step, label = 'Брезенхем (сглаживание)', color = "black")
	plt.plot(my_angle, my_step_wu, label = 'Ву', color = "gray")
	plt.title("Исследование ступенчатости\n{0} - длина отрезка;".format(radius))
	plt.legend()
	plt.ylabel("Максимальное колличество ступенек.")
	plt.xlabel("Угол в градусах.")
	my_window.mainscene.clear()
	plt.show()
if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	w = Window()
	w.show()
	sys.exit(app.exec_())
