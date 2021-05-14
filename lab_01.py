# На плоскости дано множество точек и треугольник (задан вершинами). Найти все окружности, каждая из которых проходит хотя бы через три различные
# точки заданного множества, у которых прямая, проходящая через две вершины треугольника, проходит и через центр окружности. Среди найденных
# окружностей выбрать ту, для которой искомая прямая образует минимальный угол с осью ординат. Сделать в граф. режиме вывод изображения.

import copy
import traceback
from math import acos, degrees, fabs, sqrt
from tkinter import *
from tkinter import messagebox, ttk

def add():
	AddWin = Tk()
	AddWin.title('Добавление точек')
	AddWin.geometry('400x150+50+50')
	Input = Label(AddWin, text = 'Введите координаты точки: ')
	Input.grid(row = 0, column = 0, columnspan = 2)

	entryX = Entry(AddWin)
	valueX = Label(AddWin, width = 1, text = 'X', anchor = 'w')
	valueX.grid(row = 1, column = 0)
	entryX.grid(row = 2, column = 0)

	entryY = Entry(AddWin)
	valueY = Label(AddWin, width = 1, text = 'Y', anchor = 'w')
	valueY.grid(row = 1, column = 1)
	entryY.grid(row = 2, column = 1)

	def check():
		var1.set(not var1.get())

	var1 = BooleanVar()
	c1 = Checkbutton(AddWin, text = 'Вершина', command = check)
	c1.grid(row = 2, column = 3)

	win = Tk()
	win.title('Точки')
	win.geometry('485x200+50+250')

	table = ttk.Treeview(win)
	table['columns'] = ('one', 'two')
	table.column('one', width = 140, stretch = True, anchor = 'c')
	table.column('two', width = 140, stretch = True, anchor = 'c')
	table.heading('one', text = 'X', anchor = 'w')
	table.heading('two', text = 'Y', anchor = 'w')
	table.grid()

	def inputX(event):
		valueX.configure(text = 'X ' + str(entryX.get()))

	entryX.bind('<Return>', inputX)
	entryX.grid()

	def inputY(event):
		valueY.configure(text = 'Y ' + str(entryY.get()))

	entryY.bind('<Return>', inputY)
	entryY.grid()

	OK = Button(AddWin, text = 'OK', width = 5, height = 5)
	Cancel = Button(AddWin, text = 'Закрыть', width = 7, height = 5)

	global count
	count = 0

	def consent(event):
		global count
		try:
			if [float(entryX.get()), float(entryY.get())] in points:
				messagebox.showerror('Ошибка', 'Данная точка уже была введена')
				return
			if var1.get():
				triangle.append([float(entryX.get()), float(entryY.get())])
			points.append([float(entryX.get()), float(entryY.get())])
			entryX.delete(0, END)
			entryY.delete(0, END)
			for i in range(count, len(points)):
				if points[i] in triangle:
					table.insert('', 0, text = '▲ №' + str(i + 1), values = (points[i][0], points[i][1]))
				else:
					table.insert('', 0, text = '№' + str(i + 1), values = (points[i][0], points[i][1]))
			table.grid()
			win.update()
			count += 1
		except ValueError:
			messagebox.showerror('Ошибка', 'Некорректный ввод')

	OK.bind('<Button-1>', consent)
	OK.grid(row = 3, column = 0)

	def cancel(event):
		AddWin.destroy()
		win.destroy()
	
	Cancel.bind('<Button-1>', cancel)
	Cancel.grid(row = 3, column = 1)
	AddWin.update()

def delete():
	if not len(points):
		messagebox.showerror('Ошибка', 'Список точек пуст')
		return
	AddWin = Tk()
	AddWin.title('Удаление точки')
	AddWin.geometry('400x150+50+50')
	Input = Label(AddWin, text = 'Введите координаты точки: ')

	Input.grid(row = 1, column = 0, columnspan = 2)
	frameX = Frame(AddWin)
	valueX = Label(frameX, width = 1, text = 'X', anchor = 'w')
	frameX.grid(row = 2, column = 0)
	valueX.grid(row = 1, column = 0)

	frameY = Frame(AddWin)
	valueY = Label(frameY, width = 1, text = 'Y', anchor = 'w')
	frameY.grid(row = 2, column = 1)
	valueY.grid(row = 1, column = 0)

	entryX = Entry(frameX)
	entryY = Entry(frameY)

	win = Tk()
	win.title('Точки')
	win.geometry('485x200+50+250')

	table = ttk.Treeview(win)
	table['columns'] = ('one', 'two')
	table.column('one', width = 140, stretch = True, anchor = 'c')
	table.column('two', width = 140, stretch = True, anchor = 'c')
	table.heading('one', text = 'X', anchor = 'w')
	table.heading('two', text = 'Y', anchor = 'w')
	for i in range(len(points)):
		if points[i] in triangle:
			table.insert('', 0, text = '▲ №' + str(i + 1), values = (points[i][0], points[i][1]))
		else:
			table.insert('', 0, text = '№' + str(i + 1), values = (points[i][0], points[i][1]))
	table.grid()

	def inputX(event):
		valueX.configure(text = 'X ' + str(entryX.get()))

	entryX.bind('<Return>', inputX)
	entryX.grid()

	def inputY(event):
		valueY.configure(text = 'Y ' + str(entryY.get()))

	entryY.bind('<Return>', inputY)
	entryY.grid()

	OK = Button(AddWin, text = 'Удалить', width = 5, height = 5)
	cancel = Button(AddWin, text = 'Отмена', width = 7, height = 5)

	def consent(event):
		i = 0
		flag = False
		try:
			while i < len(points):
				if points[i][0] == float(entryX.get()) and points[i][1] == float(entryY.get()):
					flag = True
					break
				i += 1
			if flag is False:
				messagebox.showerror('Ошибка', 'Точка не найдена')
				return
			if points[i] in triangle:
				triangle.pop(triangle.index(points[i]))
			points.pop(i)
			AddWin.destroy()
			win.destroy()
		except:
			messagebox.showerror('Ошибка', 'Некорректный ввод')

	OK.bind('<Button-1>', consent)
	OK.bind('<Return>', consent)
	OK.grid(row = 3, column = 0)

	def Cancel(event):
		AddWin.destroy()
		win.destroy()

	cancel.bind('<Button-1>', Cancel)
	cancel.grid(row = 3, column = 1)
	AddWin.update()

def delete_all():
	if not len(points):
		messagebox.showerror('Ошибка', 'Список точек пуст')
	elif messagebox.askyesno('Удаление точек', 'Вы точно хотите удалить все точки?') is True:
		points.clear()
		triangle.clear()

def change():
	if not len(points):
		messagebox.showerror('Ошибка', 'Список точек пуст')
		return
	AddWin = Tk()
	AddWin.title('Изменение координат')
	AddWin.geometry('300x280+50+50')
	Input = Label(AddWin, text = 'Введите номер точки: ')
	Input.pack()
	frameX = Frame(AddWin)
	frameX.pack(side = TOP, fill = X, padx = 5, pady = 5)

	def check():
		var1.set(True)

	var1 = BooleanVar()
	c1 = Checkbutton(AddWin, text = 'Вершина', variable = var1, command = check)
	c1.pack(padx = 10, pady = 10)

	inp = Label(AddWin, text = 'Введите новые координаты точки')
	inp.pack()

	frameXx = Frame(AddWin)
	valueXx = Label(frameXx, width = 12, text = 'X', anchor = 'w')
	frameXx.pack(side = TOP, fill = X, padx = 5, pady = 5)
	valueXx.pack(side = 'left')

	frameYy = Frame(AddWin)
	valueYy = Label(frameYy, width = 12, text = 'Y', anchor = 'w')
	frameYy.pack(side = TOP, fill = X, padx = 5, pady = 5)
	valueYy.pack(side = 'left')

	entryX = Entry(frameX)
	# entryY = Entry(frameY)
	entryXx = Entry(frameXx)
	entryYy = Entry(frameYy) 

	win = Tk()
	win.title('Точки')
	win.geometry('485x200+50+350')

	table = ttk.Treeview(win)
	table['columns'] = ('one', 'two')
	table.column('one', width = 140, stretch = True, anchor = 'c')
	table.column('two', width = 140, stretch = True, anchor = 'c')
	table.heading('one', text = 'X', anchor = 'w')
	table.heading('two', text = 'Y', anchor = 'w')

	for i in range(len(points)):
		if points[i] in triangle:
			table.insert('', 0, text = '▲ №' + str(i + 1), values = (points[i][0], points[i][1]))
		else:
			table.insert('', 0, text = '№' + str(i + 1), values = (points[i][0], points[i][1]))
	table.pack()

	def inputX(event):
		valueX.configure(text = 'X ' + str(entryX.get()))

	entryX.bind('<Return>', inputX)
	entryX.pack()

	def inputXx(event):
		valueXx.configure(text = 'X ' + str(entryXx.get()))

	entryXx.bind('<Return>', inputXx)
	entryXx.pack()

	def inputYy(event):
		valueYy.configure(text = 'Y ' + str(entryYy.get()))

	entryYy.bind('<Return>', inputYy)
	entryYy.pack()

	OK = Button(AddWin, text = 'Изменить', width = 7, height = 5)
	cancel = Button(AddWin, text = 'Отмена', width = 7, height = 5)

	def consent(event):
		try:
			if 0 <= int(entryX.get()) - 1 <= len(points):
				if var1.get() is True and points[int(entryX.get()) - 1] in triangle:
					temp = copy.deepcopy(triangle)
					triangle[temp.index(points[int(entryX.get()) - 1])][0] = float(entryXx.get())
					triangle[temp.index(points[int(entryX.get()) - 1])][1] = float(entryYy.get())
				elif var1.get() is True and points[int(entryX.get()) - 1] not in triangle:
					triangle.append(points[int(entryX.get()) - 1])
				if var1.get() is False and points[int(entryX.get()) - 1] in triangle:
					triangle.pop(triangle.index(points[int(entryX.get()) - 1]))
				points[int(entryX.get()) - 1][0] = float(entryXx.get())
				points[int(entryX.get()) - 1][1] = float(entryYy.get())
			else:
				messagebox.showerror('Ошибка', 'Точка не найдена')
				return
			AddWin.destroy()
			win.destroy()
		except:
			traceback.print_exc()
			messagebox.showerror('Ошибка', 'Некорректный ввод')

	OK.bind('<Button-1>', consent)
	OK.pack(side = 'left')

	def Cancel(event):
		AddWin.destroy()

	cancel.bind('<Button-1>', Cancel)
	cancel.pack(side = 'right')
	AddWin.update()

def table():
	if not len(points):
		messagebox.showerror('Ошибка', 'Список точек пуст')
		return

	win = Tk()
	win.title('Таблица')
	win.geometry('480x220')

	table = ttk.Treeview(win)
	table['columns'] = ('one', 'two')
	table.column('one', width = 140, stretch = True, anchor = 'c')
	table.column('two', width = 140, stretch = True, anchor = 'c')
	table.heading('one', text = 'X', anchor = 'w')
	table.heading('two', text = 'Y', anchor = 'w')

	for i in range(len(points)):
		if points[i] in triangle:
			table.insert('', 0, text = '▲ №' + str(i + 1), values = (points[i][0], points[i][1]))
		else:
			table.insert('', 0, text = '№' + str(i + 1), values = (points[i][0], points[i][1]))

	table.grid()
	win.update()

def draw():
	if not len(points):
		messagebox.showerror('Ошибка', 'Точки отсутствуют')
		return

	def compare(a, b):
		if fabs(a - b) < 0.0001:
			return True
		else:
			return False

	top = Tk()
	top.geometry('1000x600')
	top.title('Рисунок')

	x_scale = 600
	x_factor = 0.85
	y_scale = 600
	y_factor = 0.85

	canva = Canvas(top, width = x_scale, height = y_scale, bg = 'white')
	canva.pack(side = LEFT)

	center = [0, 0]

	def find_min_x(array):
		result = array[0][0]
		for i in range(len(array)):
			if array[i][0] < result:
				result = array[i][0]
		return result
	
	def find_min_y(array):
		result = array[0][1]
		for i in range(len(array)):
			if array[i][1] < result:
				result = array[i][1]
		return result

	def find_max_x(array):
		result = array[0][0]
		for i in range(len(array)):
			if array[i][0] > result:
				result = array[i][0]
		return result

	def find_max_y(array):
		result = array[0][1]
		for i in range(len(array)):
			if array[i][1] > result:
				result = array[i][1]
		return result
	
	coord_canv = []
	triangle_canv = []

	X_min, Y_min = find_min_x(points), find_min_y(points)
	X_max, Y_max = find_max_x(points), find_max_y(points)
	delta_X = X_max - X_min
	delta_Y = Y_max - Y_min

	delta = max(delta_X, delta_Y)

	for i in range(len(points)):
		if len(points) != 1:
			kx = (X_max - points[i][0]) / delta
			ky = (Y_max - points[i][1]) / delta
			coord_canv.append([10 + (1 - kx) * x_scale * x_factor, 10 + ky * y_scale * y_factor])
			if points[i] in triangle:
				triangle_canv.append([10 + (1 - kx) * x_scale * x_factor, 10 + ky * y_scale * y_factor])
		else:
			coord_canv.append(points[i])
			if points[i] in triangle:
				triangle_canv.append(points[i])

	kx_center = (X_max - center[0]) / delta
	ky_center = (Y_max - center[1]) / delta
	center[0] = 10 + (1 - kx_center) * x_scale * x_factor
	center[1] = 10 + ky_center * y_scale * y_factor

	canva.create_line(center, center[0], 0)
	canva.create_line(center, x_scale, center[1])
	canva.create_line(center, center[0], y_scale)
	canva.create_line(center, 0, center[1])


	for i in range(len(coord_canv)):
		canva.create_oval(coord_canv[i], coord_canv[i], width = 0, fill = 'black')
		canva.create_text(coord_canv[i][0] + 40, coord_canv[i][1], text = '{0}: ({1}, {2})'.format(i + 1, points[i][0], points[i][1]))

	def distance_from_point(point1, point2):
		return sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

	def distance_from_line(point1, point2, point0):
		return compare(fabs(point0[0] * (point2[1] - point1[1]) - point0[1] * (point2[0] - point1[0]) + point2[0] * point1[1] - point2[1] * point1[0]) \
			/ sqrt((point2[1] - point1[1]) ** 2 + (point2[0] - point1[0]) ** 2), 0)

	def angle(x1, y1, x2, y2):
		return degrees(acos((x1 * x2 + y1 * y2) / (sqrt(x1 * x1 + y1 * y1) * sqrt(x2 * x2 + y2 * y2))))

	def okr(x1, y1, x2, y2, x3, y3):
		xc = (-1 / 2) * (y1 * (x2 ** 2 + y2 ** 2 - x3 **2 - y3 ** 2) + y2 * (x3 ** 2 + y3 ** 2 - x1 ** 2 - y1 ** 2) + y3 * (x1 ** 2 + y1 ** 2 - x2 ** 2 - y2 ** 2)) \
			/ (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
		yc = (1 / 2) * (x1 * (x2 ** 2 + y2 ** 2 - x3 **2 - y3 ** 2) + x2 * (x3 ** 2 + y3 ** 2 - x1 ** 2 - y1 ** 2) + x3 * (x1 ** 2 + y1 ** 2 - x2 ** 2 - y2 ** 2)) \
			/ (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2))
		return xc, yc

	if len(triangle) == 3:
		passing_array = []
		x1, y1 = triangle[1][0] - triangle[0][0], triangle[1][1] - triangle[0][1]
		x2, y2 = triangle[2][0] - triangle[1][0], triangle[2][1] - triangle[1][1]
		x3, y3 = triangle[2][0] - triangle[0][0], triangle[2][1] - triangle[0][1]
		if (x3 - x1) * (x2 - x1) == (y3 - y1) * (y2 - y1):
			messagebox.showerror('Ошибка', 'Нельзя построить треугольник')
			return
		canva.create_line(triangle_canv[0], triangle_canv[1], fill = 'blue')
		canva.create_line(triangle_canv[1], triangle_canv[2], fill = 'blue')
		canva.create_line(triangle_canv[0], triangle_canv[2], fill = 'blue')

		for i in range(len(points)):
			for j in range(len(points)):
				for k in range(len(points)):
					if points[i] in triangle or points[j] in triangle or points[k] in triangle or points[i] in passing_array or points[j] in passing_array or points[k] in passing_array:
						continue

					try:
						point_x, point_y = okr(points[i][0], points[i][1], points[j][0], points[j][1], points[k][0], points[k][1])
					except ZeroDivisionError:
						continue

					point = [point_x, point_y]
					radius = distance_from_point(point, points[i])

					if distance_from_line(triangle[0], triangle[1], point) is True:
						kx = (X_max - point_x) / delta
						ky = (Y_max - point_y) / delta
						same_point = [10 + (1 - kx) * x_scale * x_factor, 10 + ky * y_scale * y_factor]
						circle.append([[same_point, point], [distance_from_point(same_point, coord_canv[i]), radius], triangle_canv[0], triangle_canv[1]])
						passing_array.append(points[i])
						passing_array.append(points[j])
						passing_array.append(points[k])
					elif distance_from_line(triangle[1], triangle[2], point) is True:
						kx = (X_max - point_x) / delta
						ky = (Y_max - point_y) / delta
						same_point = [10 + (1 - kx) * x_scale * x_factor, 10 + ky * y_scale * y_factor]
						circle.append([[same_point, point], [distance_from_point(same_point, coord_canv[i]), radius], triangle_canv[1], triangle_canv[2]])
						passing_array.append(points[i])
						passing_array.append(points[j])
						passing_array.append(points[k])
					elif distance_from_line(triangle[0], triangle[2], point) is True:
						kx = (X_max - point_x) / delta
						ky = (Y_max - point_y) / delta
						same_point = [10 + (1 - kx) * x_scale * x_factor, 10 + ky * y_scale * y_factor]
						circle.append([[same_point, point], [distance_from_point(same_point, coord_canv[i]), radius], triangle_canv[0], triangle_canv[2]])
						passing_array.append(points[i])
						passing_array.append(points[j])
						passing_array.append(points[k])
	elif 0 < len(triangle) < 3 or len(triangle) > 3:
		messagebox.showerror('Ошибка', 'Для построения треугольника необходимо три точки')
		return

	if circle:
		min_angle = 360
		for i in range(len(circle)):
			canva.create_line(circle[i][0][0], circle[i][3], dash = (4, 2))
			canva.create_oval((circle[i][0][0][0] - circle[i][1][0]), circle[i][0][0][1] - circle[i][1][0], circle[i][0][0][0] + circle[i][1][0], circle[i][0][0][1] + circle[i][1][0], outline = 'orange')
			# ось ординат: (0, 0), (0, 1)
			angle1 = angle(0, 1, circle[i][3][0] - circle[i][2][0], circle[i][3][1] - circle[i][2][1])
			if angle1 < min_angle:
				min_angle = angle1
				center = circle[i][0][1]
				radius = circle[i][1][1]
				canv_center = circle[i][0][0]
				canv_radius = circle[i][1][0]
		canva.create_oval(canv_center[0] - canv_radius, canv_center[1] - canv_radius, canv_center[0] + canv_radius, canv_center[1] + canv_radius, outline = 'green')
		text = 'Центр искомой окружности: ' + str(center) + '\nРадиус искомой окружности: ' + str(radius)
	else:
		text = 'Окружность не найдена'

	circle.clear()
	info = Label(top, text = text)
	info.pack(side = RIGHT)

points = []
circle = []
triangle = []

root = Tk()
root.title('Задание')
root.geometry('500x300+550+100')

task = Label(text = 'На плоскости дано множество точек и треугольник (задан вершинами).\nНайти все окружности, каждая из которых проходит хотя бы\n\
	через три различные точки заданного множества,\nу которых прямая, проходящая через две вершины треугольника,\nпроходит и через центр окружности.\
	\nСреди найденных окружностей выбрать ту,\nдля которой искомая прямая образует минимальный угол с осью ординат.\
	\nСделать в граф. режиме вывод изображения.\n\nМихаил Коротыч\nИУ7-45Б')
task.pack()

m = Menu(root)
root.config(menu = m)

cm = Menu(m)
m.add_cascade(label = 'Меню', menu = cm)
cm.add_command(label = 'Добавить точки', command = add)
cm.add_command(label = 'Удалить точку', command = delete)
cm.add_command(label = 'Удалить все точки', command = delete_all)
cm.add_command(label = 'Изменить координаты точки', command = change)
cm.add_command(label = 'Таблица точек', command = table)
cm.add_command(label = 'Решить', command = draw)
cm.add_command(label = 'Выход', command = quit)

root.mainloop()
