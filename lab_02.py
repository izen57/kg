import copy
from math import *
from tkinter import *
from tkinter import messagebox

import numpy as np

root = Tk()
root.geometry('1000x600')

Canv = Canvas(root, width = 800, height = 600)
Canv.pack(side = 'left')

Buttons = Frame(root)

Transfer = Frame(Buttons)
Scale = Frame(Buttons)
Turn = Frame(Buttons)

# Перенос
TrvalueL = Label(Transfer, text = 'Перенос').grid(row = 0, column = 0, columnspan = 4)
TrxL = Label(Transfer, text = 'dX').grid(row = 1, column = 0)
TryL = Label(Transfer, text = 'dY').grid(row = 1, column = 2)

# Масштабирование
SvalueL = Label(Scale, text = 'Масштабирование').grid(row = 0, column = 0, columnspan = 4)
SxL = Label(Scale, text = 'Xc').grid(row = 1, column = 0)
SyL = Label(Scale, text = 'Yc').grid(row = 1, column = 2)
ScxL = Label(Scale, text = 'KX').grid(row = 2, column = 0)
ScyL = Label(Scale, text = 'KY').grid(row = 2, column = 2)

# Поворот
TuvalueL = Label(Turn, text = 'Поворот').grid(row = 0, column = 0, columnspan = 4)
TuxL = Label(Turn, text = '  X').grid(row = 1, column = 0)
TuyL = Label(Turn, text = 'Y').grid(row = 1, column = 2)
TuangL = Label(Turn, text = 'Угол').grid(row = 2, column = 0, columnspan = 2)

# Перенос
TrxV = Entry(Transfer, width = 5)
TryV = Entry(Transfer, width = 5)

# Масштабирование
SxV = Entry(Scale, width = 5)
SyV = Entry(Scale, width = 5)
ScxV = Entry(Scale, width = 5)
ScyV = Entry(Scale, width = 5)

# Поворот
TuxV = Entry(Turn, width = 5)
TuyV = Entry(Turn, width = 5)
TuangV = Entry(Turn, width = 10)

#Перенос
TrxV.grid(row = 1, column = 1)
TryV.grid(row = 1, column = 3)

# Масштабирование
SxV.grid(row = 1, column = 1)
SyV.grid(row = 1, column = 3)
ScxV.grid(row = 2, column = 1)
ScyV.grid(row = 2, column = 3)

# Поворот
TuxV.grid(row = 1, column = 1)
TuyV.grid(row = 1, column = 3)
TuangV.grid(row = 2, column = 2, columnspan = 2)

center = []
begin_center = []
square = [[], [], [], []]
begin_square = [[], [], [], []]
triangle = [[], [], []]
begin_triangle = [[], [], []]
ellips = []
begin_ellips = [[], []]
back_center = []
back_square = [[], [], [], []]
back_triangle = [[], [], []]
back_ellips = []
axis_x = []
axis_y = []

def create():
	global center, square, triangle, ellips, begin_center, begin_square, begin_triangle, begin_ellips

	center.append(800 / 2)
	center.append(600 / 2)

	begin_center = copy.deepcopy(center)

	square[0].append(center[0] - 100)
	square[0].append(center[1] - 100)
	square[1].append(center[0] + 100)
	square[1].append(center[1] - 100)
	square[2].append(center[0] + 100)
	square[2].append(center[1] + 100)
	square[3].append(center[0] - 100)
	square[3].append(center[1] + 100)

	begin_square = copy.deepcopy(square)

	triangle[0].append(square[0][0] + (square[1][0] - square[0][0]) / 2)
	triangle[0].append(square[0][1])
	triangle[1].append(square[2][0])
	triangle[1].append(square[2][1])
	triangle[2].append(square[3][0])
	triangle[2].append(square[3][1])

	begin_triangle = copy.deepcopy(triangle)

	ellipse_height = 20
	ellipse_width = hypot(triangle[1][0] - triangle[0][0], triangle[1][1] - triangle[0][1])
	a, b = ellipse_width / 2, ellipse_height / 2

	def add_ellipse_at(dx, dy, angle):
		for t in range(0, 180):
			x = a * cos(radians(t)) * cos(angle) - b * sin(radians(t)) * sin(angle) + dx
			y = a * cos(radians(t)) * sin(angle) + b * sin(radians(t)) * cos(angle) + dy
			ellips.append([x, y])

	angle = atan(2 / 1)
	dx = (triangle[1][0] + triangle[0][0]) / 2
	dy = (triangle[1][1] + triangle[0][1]) / 2
	add_ellipse_at(dx, dy, angle)

	angle = atan(-2 / 1)
	dx = (triangle[2][0] + triangle[0][0]) / 2
	dy = (triangle[2][1] + triangle[0][1]) / 2
	add_ellipse_at(dx, dy, angle)

	angle = radians(180)
	dx = (triangle[2][0] + triangle[1][0]) / 2
	dy = (triangle[2][1] + triangle[1][1]) / 2
	a = (triangle[2][0] - triangle[1][0]) / 2
	add_ellipse_at(dx, dy, angle)

	begin_ellips = copy.deepcopy(ellips)

def draw():
	Canv.delete('all')

	Canv.create_oval(center, center, width = 0, fill = 'red')
	Canv.create_text(center, text = 'Центр\n{0}, {1}'.format(center[0], center[1]))

	for i in range(4):
		Canv.create_oval(square[i], square[i], width = 0, fill = 'blue')

	Canv.create_line(square[0], square[1])
	Canv.create_line(square[1], square[2])
	Canv.create_line(square[2], square[3])
	Canv.create_line(square[0], square[3])

	Canv.create_line(triangle[0], triangle[1])
	Canv.create_line(triangle[1], triangle[2])
	Canv.create_line(triangle[0], triangle[2])

	for i in range(len(ellips)):
		Canv.create_oval(ellips[i], ellips[i])

	Canv.create_line(0, 3, 800, 3)
	Canv.create_text(790, 10, text = 'X')
	Canv.create_line(3, 0, 3, 600)
	Canv.create_text(12, 585, text = 'Y')
	Canv.create_text(12, 10, text = '0')

	for i in range(100, 800, 100):
		Canv.create_text(i, 10, text = str(i))
	for i in range(100, 600, 100):
		Canv.create_text(16, i, text = str(i))


def Transfer_ep():
	global back_triangle, back_square, back_ellips, back_center, center, square, triangle, ellips

	flag = False
	try:
		Trx = float(TrxV.get())
		Try = float(TryV.get())
	except ValueError:
		messagebox.showerror('Ошибка', 'Некорректный ввод коэффициентов перемещения.')
		flag = True

	if flag is False:
		back_center.clear()
		back_center = copy.deepcopy(center)
		center.clear()
		center.append(back_center[0] + Trx)
		center.append(back_center[1] + Try)

		back_square.clear()
		back_square = copy.deepcopy(square)
		square.clear()
		for element in back_square:
			x = element[0] + Trx
			y = element[1] + Try
			square.append([x, y])

		back_triangle.clear()
		back_triangle = copy.deepcopy(triangle)
		triangle.clear()
		for element in back_triangle:
			x = element[0] + Trx
			y = element[1] + Try
			triangle.append([x, y])

		back_ellips.clear()
		back_ellips = copy.deepcopy(ellips)
		ellips.clear()
		for element in back_ellips:
			x = element[0] + Trx
			y = element[1] + Try
			ellips.append([x, y])

		draw()

def Scale_ep():
	global back_triangle, back_square, back_ellips, back_center, center, square, triangle, ellips

	flag = False
	try:
		Xc = float(SxV.get())
		Yc = float(SyV.get())
	except ValueError:
		messagebox.showerror('Ошибка', 'Некорректный ввод центра масштабирования.')
		flag = True
	try:
		kx = float(ScxV.get())
		ky = float(ScyV.get())
	except ValueError:
		messagebox.showerror('Ошибка', 'Некорректный ввод коэффициентов масштабирования.')
		flag = True

	if flag is False:
		back_center.clear()
		back_center = copy.deepcopy(center)
		center.clear()
		center.append(kx * back_center[0] + Xc * (1 - kx))
		center.append(ky * back_center[1] + Yc * (1 - ky))

		back_square.clear()
		back_square = copy.deepcopy(square)
		square.clear()
		for element in back_square:
			x = kx * element[0] + Xc * (1 - kx)
			y = ky * element[1] + Yc * (1 - ky)
			square.append([x, y])

		back_triangle.clear()
		back_triangle = copy.deepcopy(triangle)
		triangle.clear()
		for element in back_triangle:
			x = kx * element[0] + Xc * (1 - kx)
			y = ky * element[1] + Yc * (1 - ky)
			triangle.append([x, y])

		back_ellips.clear()
		back_ellips = copy.deepcopy(ellips)
		ellips.clear()
		for element in back_ellips:
			x = kx * element[0] + Xc * (1 - kx)
			y = ky * element[1] + Yc * (1 - ky)
			ellips.append([x, y])

		draw()

def Turn_ep():
	global back_triangle, back_square, back_ellips, back_center, center, square, triangle, ellips

	flag = False
	try:
		Xc = float(TuxV.get())
		Yc = float(TuyV.get())
	except ValueError:
		messagebox.showerror('Ошибка', 'Некорректный ввод центра поворота.')
		flag = True

	try:
		teta = float(TuangV.get())
	except ValueError:
		messagebox.showerror('Ошибка', 'Некорректный ввод угла поворота.')
		flag = True

	if flag is False:
		teta = radians(teta)

		back_center.clear()
		back_center = copy.deepcopy(center)
		center.clear()
		center.append(Xc + (back_center[0] - Xc) * cos(teta) + (back_center[1] - Yc) * sin(teta))
		center.append(Yc - (back_center[0] - Xc) * sin(teta) + (back_center[1] - Yc) * cos(teta))

		back_square.clear()
		back_square = copy.deepcopy(square)
		square.clear()
		for element in back_square:
			x = Xc + (element[0] - Xc) * cos(teta) + (element[1] - Yc) * sin(teta)
			y = Yc - (element[0] - Xc) * sin(teta) + (element[1] - Yc) * cos(teta)
			square.append([x, y])

		back_triangle.clear()
		back_triangle = copy.deepcopy(triangle)
		triangle.clear()
		for element in back_triangle:
			x = Xc + (element[0] - Xc) * cos(teta) + (element[1] - Yc) * sin(teta)
			y = Yc - (element[0] - Xc) * sin(teta) + (element[1] - Yc) * cos(teta)
			triangle.append([x, y])

		back_ellips.clear()
		back_ellips = copy.deepcopy(ellips)
		ellips.clear()
		for element in back_ellips:
			x = Xc + (element[0] - Xc) * cos(teta) + (element[1] - Yc) * sin(teta)
			y = Yc - (element[0] - Xc) * sin(teta) + (element[1] - Yc) * cos(teta)
			ellips.append([x, y])

		draw()

def Back_ep():
	global back_triangle, back_square, back_ellips, back_center, center, square, triangle, ellips

	if not back_center or not back_ellips or not back_square or not back_triangle:
		messagebox.showerror('Ошибка', 'Невозможно вернуться на шаг назад')

	center = copy.deepcopy(back_center)

	triangle = copy.deepcopy(back_triangle)

	square = copy.deepcopy(back_square)

	ellips = copy.deepcopy(back_ellips)

	draw()

def Begin_ep():
	global begin_triangle, begin_square, begin_ellips, begin_center, center, square, triangle, ellips, back_center, back_square, back_ellips, back_triangle

	back_center.clear()
	back_center = copy.deepcopy(center)
	center.clear()
	center = copy.deepcopy(begin_center)

	back_triangle.clear()
	back_triangle = copy.deepcopy(triangle)
	triangle.clear()
	triangle = copy.deepcopy(begin_triangle)

	back_square.clear()
	back_square = copy.deepcopy(square)
	square.clear()
	square = copy.deepcopy(begin_square)

	back_ellips.clear()
	back_ellips = copy.deepcopy(ellips)
	ellips.clear()
	ellips = copy.deepcopy(begin_ellips)

	draw()

def begin_begin_ep():
	global begin_triangle, begin_square, begin_ellips, begin_center, center, square, triangle, ellips, back_center, back_square, back_ellips, back_triangle

	center = copy.deepcopy(begin_center)
	triangle = copy.deepcopy(begin_triangle)
	square = copy.deepcopy(begin_square)
	ellips = copy.deepcopy(begin_ellips)

	back_center.clear()
	back_ellips.clear()
	back_square.clear()
	back_triangle.clear()

	draw()

create()
draw()

TransferButton = Button(Buttons, text = 'Перенос', command = Transfer_ep, width = 8)
ScaleButton = Button(Buttons, text = 'Масштаб', command = Scale_ep, width = 8)
TurnButton = Button(Buttons, text = 'Поворот', command = Turn_ep, width = 8)
BackButton = Button(Buttons, text = 'Назад', command = Back_ep, width = 12, height = 1)
BeginButton = Button(Buttons, text = 'Исходное', command = Begin_ep, width = 12, height = 1)
Begin_begin_btn = Button(Buttons, text = 'В начало', comman = begin_begin_ep, width = 12, height = 1)

Transfer.grid(row = 0, column = 0, columnspan = 2)
TransferButton.grid(row = 1, column = 0, columnspan = 2)
Label(Buttons, text = '~~~~~~~~~~~~~~').grid(row = 2, column = 0, columnspan = 4)
Label(Buttons, text = '~~~~~~~~~~~~~~').grid(row = 3, column = 0, columnspan = 4)

Scale.grid(row = 4, column = 0, columnspan = 2)
ScaleButton.grid(row = 5, column = 0, columnspan = 2)
Label(Buttons, text = '~~~~~~~~~~~~~~').grid(row = 6, column = 0, columnspan = 4)
Label(Buttons, text = '~~~~~~~~~~~~~~').grid(row = 7, column = 0, columnspan = 4)

Turn.grid(row = 8, column = 0, columnspan = 2)
TurnButton.grid(row = 9, column = 0, columnspan = 2)
Label(Buttons, text = '~~~~~~~~~~~~~~').grid(row = 10, column = 0, columnspan = 4)
Label(Buttons, text = '~~~~~~~~~~~~~~').grid(row = 11, column = 0, columnspan = 4)
BackButton.grid(row = 12, column = 0, columnspan = 4)
BeginButton.grid(row = 13, column = 0, columnspan = 4)
Begin_begin_btn.grid(row = 14, column = 0, columnspan = 4)

Buttons.pack(side = 'top')
Canv.pack()

root.mainloop()
