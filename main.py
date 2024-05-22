
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout,
                               QPushButton, QWidget, QStackedLayout,QLineEdit,
                               QGridLayout, QLabel,QTableWidget, 
                               QTableWidgetItem,QGroupBox, QCheckBox,
                               QScrollArea)
from PySide6.QtGui import QAction, QColor , QPainter, QPixmap
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog
import io
import time
import networkx as nx
import math as m
from math import cos,sin, pi, sqrt

from sympy import Symbol, expand

#==========================================================================
#                      СЧЕТНЫЕ ФУНКЦИИ
#==========================================================================

def cartesian_to_qrectf(x, y, height,width):
    y_qrectf = height - y
    x_1231 = width + x
    return x_1231, y_qrectf

def my_eval(str1):
    str2 = f"lambda x, y: {str1}"
    return eval(str2)

def my_eval_with_t(str1):
    x = Symbol("x")
    y = Symbol("y")
    t = Symbol("t")
    sssstr = expand(str1)
    print(str(sssstr))
    str2 = f"lambda x, y, t: {str(sssstr)}"
    #str2 = f"lambda x, y, t: {str1}"
    return eval(str2)

def enc(str1):
    if type(str1)!=type("a"):        str1 = str(str1)
    return "(" + str1 + ")"

def cell_dribling(item, leng):#*
    lengnew = leng*2
    new1 = 2*item-1+(item-1)//leng*lengnew
    new2 = new1+1
    new3 = new1+lengnew
    new4 = new2+lengnew
    return [new1, new2, new3, new4]

def generate_50to150andback():
    while True:
        for i in range(100*50, 100*151, 1):
            yield int(i/100)
        for i in range(100*149, 100*49, -1 ):
            yield int(i/100)

def generate_100to150andback():
    while True:
        for i in range(100, 151, 20):
            yield i
        for i in range(149, 100, -20 ):
            yield i

#==========================================================================
#          ГЛАВНОЕ ОКНО И ВСЕ ВЫЧИСЛЕНИЯ ВНУТРИ ЭТОГО КЛАССА
#==========================================================================

class MainWindow(QMainWindow):
    
    def __init__(self,name11):
        super(MainWindow, self).__init__()
        self.name = name11
        self.setWindowTitle("Топологическая сортировка")
        self.layout_stack = QStackedLayout()

#--------------ОКНО ДЛЯ ВВОДА СИСТЕМЫ И ЧТО-ТО ЕЩЕ-------------------------

        self.layout_input = QGridLayout()

        self.group1 = QGroupBox("Система уравнений")
        self.group1.setMaximumSize(300, 200) 
        layout1 = QGridLayout()
        self.funlabel1 = QLabel("dx/dt = ")
        self.funlabel2 = QLabel("dy/dt = ")        
        self.fun1 = QLineEdit( " y " )
        self.fun2 = QLineEdit( " - a*x - b*x**3 - d*y  + B * cos(w*t) " )
        layout1.addWidget(self.funlabel1,0,0)
        layout1.addWidget(self.funlabel2,1,0)
        layout1.addWidget(self.fun1,0,1)
        layout1.addWidget(self.fun2,1,1)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,1 , 0)
        
        self.group1 = QGroupBox("Значения параметров")
        self.group1.setMaximumSize(300, 200) 
        layout1 = QGridLayout()
        self.allparam = QLineEdit( "a = -1; b = 1; d = 0.25; B = 0; w = 1" )
        layout1.addWidget(self.allparam , 0 , 0 )
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,1 ,1)
        
        self.group1 = QGroupBox("Точки задающие область")
        self.group1.setMaximumSize(300, 100) 
        layout1 = QGridLayout()
        self.dot1 = QLineEdit( " -2,-2 ")
        self.dot12 = QLabel( "x")
        self.dot2 = QLineEdit( " 2,2 ")
        
        layout1.addWidget(self.dot1 , 0 , 0 )
        layout1.addWidget(self.dot12 , 0 , 1 )
        layout1.addWidget(self.dot2 , 0, 2)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,2 ,0 )
        
        self.group1 = QGroupBox("Параметры отображения") #    отображаемых в ячейки")
        self.group1.setMaximumSize(300, 100) 
        layout1 = QGridLayout()
        self.ssssssss1 = QLabel("Период отображения T")
        self.bigt = QLineEdit( " 1 ")
        layout1.addWidget(self.ssssssss1 , 0 , 0 )
        layout1.addWidget(self.bigt , 0 , 1 )
        self.ssssssss2 = QLabel("Отображаем точек в ячейке ")
        self.countp = QLineEdit( " 36 ")
        layout1.addWidget(self.ssssssss2 , 1 , 0 )        
        layout1.addWidget(self.countp , 1, 1)
        self.ssssssss3 = QLabel("Шагов отображения")
        self.textitercountrk4 = QLineEdit( " 100 ")
        layout1.addWidget(self.ssssssss3 , 3 , 0 )
        layout1.addWidget(self.textitercountrk4 , 3, 1)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,2 ,1 )
        
        self.group1 = QGroupBox("Построить итераций и Достроить итераций")
        self.group1.setMaximumSize(300, 200) 
        layout1 = QGridLayout()
        self.button1 = QPushButton("Построить график для итераций:")
        self.globiterc1 = QLineEdit( " 6 ")
        self.button3 = QPushButton("Проитерировать существующий:")
        self.globiterc2 = QLineEdit( " 1 ")
        self.button1.clicked.connect(self.iterate_from_start)
        self.button3.clicked.connect(self.iterate_from_current)
        layout1.addWidget(self.button1 , 0, 0)
        layout1.addWidget(self.globiterc1 , 0, 1)
        layout1.addWidget(self.button3 , 1 , 0 )
        layout1.addWidget(self.globiterc2 , 1, 1)
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,3 ,0 )
        
        self.group1 = QGroupBox("Кнопки")
        self.group1.setMaximumSize(300, 100) 
        layout1 = QGridLayout()
        self.button2 = QPushButton("Отчистить старые данные и занести новые ")
        self.button2.clicked.connect(self.start1)
        layout1.addWidget( self.button2 ,3 ,1 )
        self.buttonkosaragu = QPushButton("Вывести примерные координаты аттрактора ")
        self.buttonkosaragu.clicked.connect(self.finddotattraktor)
        layout1.addWidget( self.buttonkosaragu ,4 ,1 )
        self.group1.setLayout(layout1)        
        self.layout_input.addWidget( self.group1 ,3 ,1 )
        
        self.widget_input = QWidget()
        self.widget_input.setLayout(self.layout_input)
        self.layout_stack.addWidget(self.widget_input)
        
#-------------ОКНО ДЛЯ ОТОБРАЖЕНИЯ ГРАФИКА--------------------------

        self.layout_graph = QVBoxLayout()
        
        self.grW_HIGHT = 2000
        self.grW_WIDTH = 2000

        self.original_pixmap = QPixmap(self.grW_HIGHT, self.grW_WIDTH)
        self.original_pixmap.fill(Qt.white)
        self.display_pixmap = self.original_pixmap.scaled(700, 700, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        #self.picture_out1.setPixmap(self.display_pixmap)

        self.picture_out1 = QLabel()
        #self.picture_out1.setMinimumSize(self.grW_WIDTH, self.grW_HIGHT)
        self.layout_graph.addWidget( self.picture_out1)
        
        #pixmap = QPixmap(self.grW_HIGHT, self.grW_WIDTH)
        #pixmap.fill(Qt.white)
        self.picture_out1.setPixmap(self.display_pixmap)

        self.widget_graph = QWidget()
        self.widget_graph.setLayout(self.layout_graph)
        self.layout_stack.addWidget(self.widget_graph)

#------------ОКНО ДЛЯ ОТОБРАЖЕНИЯ РЕЗУЛЬТАТОВ---------------------

        self.layout_out = QGridLayout()

        self.res_out1 = QLabel()
        self.res_out1.setWordWrap(True)
        self.scroll_area = QScrollArea()
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.res_out1)

        self.res_neout1 = ""
        self.res_out1.setText(f"Количество ячеек,\n Время итерации")
        self.scroll_area.setWidget(self.res_out1)

        #self.layout_out.addWidget( self.res_out1)
        self.layout_out.addWidget( self.scroll_area)

        self.widget_out = QWidget()
        self.widget_out.setLayout(self.layout_out)
        self.layout_stack.addWidget(self.widget_out)

#-----------ДОПОЛНИТЕЛЬНЫЕ НАСТРОЙКИ-------------------------------------------

        self.layout_extra = QGridLayout()

        self.group1 = QGroupBox("настройки графика")
        self.group1.setMaximumSize(500, 300)
        layout1 = QGridLayout()
        self.txt_extra_page = QLabel()
        self.txt_extra_page.setText(f" вступают в силу на новой итерации ")
        layout1.addWidget( self.txt_extra_page,0,0)
        self.exlab1 = QLabel("высота окна графика")
        self.txtgrW_HIGHT = QLineEdit( "700 ")
        self.exlab2 = QLabel("ширина окна графика")
        self.txtgrW_WIDTH = QLineEdit( "700 ")
        self.exlab3 = QLabel("отобразить области с точкой аттрактора")
        self.checkboxex3 = QCheckBox("", self)
        self.checkboxex3.toggle()
        
        layout1.addWidget(self.exlab1 , 1 , 0 )
        layout1.addWidget(self.txtgrW_HIGHT , 1 , 1 )
        layout1.addWidget(self.exlab2 , 2 , 0 )
        layout1.addWidget(self.txtgrW_WIDTH , 2 , 1 )
        layout1.addWidget(self.exlab3 , 3 , 0 )
        layout1.addWidget(self.checkboxex3 , 3 , 1 )
        
        self.buttonextrasett = QPushButton("Применить параметры ")
        self.buttonextrasett.clicked.connect(self.extra_settings_upload)
        layout1.addWidget( self.buttonextrasett ,99 ,1 )

        self.buttonextra_manual_csd = QPushButton("Обрезать")
        self.buttonextra_manual_csd.clicked.connect(self.manual_condence_sort_delete)
        layout1.addWidget( self.buttonextra_manual_csd ,100 ,1 )
        
        self.group1.setLayout(layout1)
        self.layout_extra.addWidget( self.group1 ,0 ,0 )

        self.widget_extra = QWidget()
        self.widget_extra.setLayout(self.layout_extra)
        self.layout_stack.addWidget(self.widget_extra)

#-----------СМЕНА ОКОН-------------------------------------------

        self.central_widget = QWidget()
        self.central_widget.setLayout(self.layout_stack)
        self.setCentralWidget(self.central_widget)

        self.menu = self.menuBar()
        self.viewMenu = self.menu.addMenu("Отображаемое окно")
        self.uploadMenu = self.menu.addMenu("Загрузка системы из файла")
        self.extraMenu = self.menu.addMenu("Дополнительные настройки")
        
        self.switchAction1 = QAction("Ввод", self)
        self.switchAction1.triggered.connect(self.switch_layout_input)
        self.viewMenu.addAction(self.switchAction1)
        
        self.switchAction2 = QAction("Графики", self)
        self.switchAction2.triggered.connect(self.switch_layout_graph)
        self.viewMenu.addAction(self.switchAction2)
        
        self.switchAction3 = QAction("Результат", self)
        self.switchAction3.triggered.connect(self.switch_layout_out)
        self.viewMenu.addAction(self.switchAction3)
        #---
        self.switchAction4 = QAction("Доп настройки 1", self)
        self.switchAction4.triggered.connect(self.switch_layout_extra)
        self.extraMenu.addAction(self.switchAction4)
        #-------
        self.uploadAction1 = QAction("Выбрать файл для загрузки", self)
        self.uploadAction1.triggered.connect(self.uploadandreadsystem1)
        self.uploadMenu.addAction(self.uploadAction1)        

    def switch_layout_input(self):
        self.layout_stack.setCurrentIndex(0)

    def switch_layout_graph(self):
        self.layout_stack.setCurrentIndex(1)

    def switch_layout_out(self):
        self.layout_stack.setCurrentIndex(2)
    #---
    def switch_layout_extra(self):
        self.layout_stack.setCurrentIndex(3)
    #------

#-----------ЗАГРУЗКА СИСТЕМЫ ИЗ ФАЙЛА-------------------------------------------

    def uploadandreadsystem1(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Select a .txt file", "", "Text Files (*.txt)")
        if filename:
            with io.open(filename, mode='r', encoding='utf-8') as file:
                content = file.read()
            
            lines = content.splitlines()
            if lines[0][0]!='<' and lines[0][1]!='>':
                print("не тот файл //нет <> в первой строке")
                return
            print(lines)
            
            self.fun1.setText((lines[1].split('<>'))[1])
            self.fun2.setText((lines[2].split('<>'))[1])
            
            self.allparam.setText((lines[3].split('<>'))[1])
            
            self.dot1.setText((lines[4].split('<>'))[1])
            self.dot2.setText((lines[5].split('<>'))[1])
            
            self.countp.setText((lines[6].split('<>'))[1])
            self.textitercountrk4.setText((lines[7].split('<>'))[1])
            
            self.globiterc1.setText((lines[8].split('<>'))[1])

        
    

#=========СОБСТВЕННО РАСЧЕТЫ ВНУТРИ КЛАССА=================

#-----------------------ЗАГРУЗКА ПАРАМЕТРОВ ИЗ ИНТЕРФЕЙСА------------------------------------------------------------------

    def get_func_period(self)->float:
        return eval( self.bigt.text() )

    def start1(self):
        self.x0, self.y0 = eval( self.dot1.text())
        self.x1, self.y1 = eval( self.dot2.text())
        #self.h = eval( self.koefh.text() )
        self.h = 0.5
        #itercount = eval(self.iterp.text())
        self.pointcounter = int(sqrt(eval(self.countp.text() )))
        self.rk4itercount = eval( self.textitercountrk4.text() )

        self.list_par_val = [ eval(chunk1.split("=")[1])
                            for chunk1 in self.allparam.text().split(";")]
        self.list_par_nam = [ (chunk1.split("=")[0]).strip()
                            for chunk1 in self.allparam.text().split(";")]
        
        print(self.list_par_val)
        print(self.list_par_nam)
        
        self.iterc = eval( self.globiterc1.text() )
        self.iterc2 = eval( self.globiterc2.text() )
        
        strxfunc =  str( self.fun1.text() )
        stryfunc =  str( self.fun2.text() )

        for i,e in enumerate( self.list_par_nam):
            strxfunc = strxfunc.replace(e, enc(self.list_par_val[i]))
            stryfunc = stryfunc.replace(e, enc(self.list_par_val[i]))
        print( self.x0, self.y0,  self.x1, self.y1, self.h ,  
              self.pointcounter, self.iterc, self.iterc2,
              strxfunc, stryfunc)

        self.xfunc = my_eval_with_t(strxfunc)
        self.yfunc = my_eval_with_t(stryfunc)
        self.xposition = lambda cell, leng: self.x0+self.h*(cell-(cell-1)//leng*leng-1)
        self.yposition = lambda cell, leng: self.y1-self.h*((cell-1)//leng+1)
        
        self.const_startt = 0
        self.const_endt = self.get_func_period()
        
        self.lengx = abs(self.x1 - self.x0) / self.h
        self.lengy = abs(self.y1 - self.y0) / self.h
        self.list_good_dots = [q for q in range(1, int(self.lengx*self.lengy))]
        self.G = nx.DiGraph()
        self.flag_from_iterate = 0
        self.flag_to_iterate = -1
        self.res_neout1 = ""

        self.mashtab = self.grW_HIGHT/abs(self.y0-self.y1)

        print("start1 done")

#-----------------------ЗАГРУЗКА ДОП НАСТРОЕК ИЗ ИНТЕРФЕЙСА------------------------------------------------------------------

    def extra_settings_upload(self):
        newwidth = eval( self.txtgrW_WIDTH.text())
        newhight = eval( self.txtgrW_HIGHT.text())
        self.display_pixmap = self.original_pixmap.scaled(newwidth, newhight, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.picture_out1.setPixmap(self.display_pixmap)

    def manual_condence_sort_delete(self):
        self.storetopological_order = list(nx.topological_sort(self.G1))
        self.storescc = [elem for elem in self.storescc if len(list(self.storescc))!=1]
        
        self.list_good_dots = self.storetopological_order
        print(len(self.list_good_dots))
        cutbeforeme = -1
        for elem in self.list_good_dots:
            if elem > 2000000000:
                if cutbeforeme == -1:
                    cutbeforeme = elem
                    break
            
        print(cutbeforeme,self.list_good_dots.index(cutbeforeme))
        self.G1.remove_nodes_from(self.list_good_dots[:self.list_good_dots.index(cutbeforeme)])
        self.list_good_dots = self.list_good_dots[self.list_good_dots.index(cutbeforeme):]
        print(len(self.list_good_dots))

        for elem in self.dict_storesccnode.keys():
            index_todelete = self.list_good_dots.index(elem)
            self.list_good_dots = self.list_good_dots[:index_todelete] + list(self.dict_storesccnode[elem]) + self.list_good_dots[index_todelete+1:]
        
        self.h = self.h*2
        self.lengx = self.lengx/2
        self.imagecreation()
        
        self.G.clear()
        self.newbuf = self.list_good_dots
        self.list_good_dots = []
        for i in range(0, len(self.newbuf)):
            r1 = cell_dribling(self.newbuf[i], self.lengx)
            self.list_good_dots += r1
        
        self.h *= 0.5
        self.lengx *= 2


#-----------------------ИТЕРАЦИЯ АЛГОРИТМА------------------------------------------------------------------
    
    def iterate_from_start(self):
        self.start1()
        self.flag_to_iterate =  eval( self.globiterc1.text() )
        self.mainiteration()
    
    def iterate_from_current(self):
        self.flag_from_iterate = self.flag_to_iterate
        self.flag_to_iterate =  self.flag_to_iterate + eval( self.globiterc2.text() )
        self.mainiteration()
    
    def mainiteration(self):
        for gh in range(self.flag_from_iterate+1, (self.flag_to_iterate+1)):
            start_time = time.time()
            
            self.calculate_symbolic_representation_dynamic_system(self.x0, self.x1, self.y0, self.y1, self.h, self.lengx, self.G, self.list_good_dots, self.pointcounter,gh)

            if gh ==  (self.flag_to_iterate):
                self.imagecreation()
                
            self.G.clear()
            self.newbuf = self.list_good_dots
            self.list_good_dots = []
            for i in range(0, len(self.newbuf)):
                r1 = cell_dribling(self.newbuf[i], self.lengx)
                self.list_good_dots += r1
            
            self.h *= 0.5
            self.lengx *= 2
            print(gh, " iteration is done! Time elapsed: ", (time.time() - start_time))
            print( ( (self.x1-self.x0 )*(self.y1-self.y0) ) / ( self.h**2 ) )
            self.res_neout1 = self.res_neout1 + f"\n {gh} итерация. Занято времени {time.time() - start_time}\n Количество ячеек {( (self.x1-self.x0 )*(self.y1-self.y0) ) / ( 4 * self.h**2 ) }"
            if gh ==  (self.flag_to_iterate):
                self.res_neout1 = self.res_neout1 + f" \nНа этой итерации также был нарисован график и посчитана топологическая сортировка графа "
                self.res_out1.setText(self.res_neout1)

#--------------------ОТОБРАЖЕНИЕ ТОЧЕК ИЗ ХОРОШИХ ЯЧЕЕК---------------------------------------------------------------------

    def calculate_symbolic_representation_dynamic_system(self, xdown, xup, ydown, yup, h, leng, G, s_list, pt,gh):
        cou = 1
        xtmp = xdown
        ytmp = yup
        xckl = xdown
        yckl = yup
        cell_list = []
        shag = (self.const_endt - self.const_startt)/eval(self.textitercountrk4.text())
        print(shag)
        counter_the_one_we_are_on_now = 0
        
        while yckl > ydown:
            while xckl < xup:
                counter_the_one_we_are_on_now += 1
                if counter_the_one_we_are_on_now in self.list_good_dots:
                    set11 = set()

                    for i in range(0, pt):
                        ytmp -= 1 / pt*h

                        for j in range(0, pt):
                            xtmp += 1 / pt*h
                            ttmp = 0
                            xrzc = xtmp
                            yrzc = ytmp
                            ttmp += shag
                            while ttmp<=self.const_endt:
                                
                                #k1 = shag * self.xfunc(xrzc, yrzc,ttmp)
                                #k2 = shag * self.xfunc(xrzc + 0.5 * shag, yrzc + 0.5 * k1,ttmp)
                                #k3 = shag * self.xfunc(xrzc + 0.5 * shag, yrzc + 0.5 * k2,ttmp)
                                #k4 = shag * self.xfunc(xrzc + shag, yrzc + k3,ttmp)
                                #xrz = xrzc + (1/6) * (k1 + 2*k2 + 2*k3 + k4)
                                
                                #k1 = shag * self.yfunc(xrzc, yrzc,ttmp)
                                #k2 = shag * self.yfunc(xrzc + 0.5 * shag, yrzc + 0.5 * k1,ttmp)
                                #k3 = shag * self.yfunc(xrzc + 0.5 * shag, yrzc + 0.5 * k2,ttmp)
                                #k4 = shag * self.yfunc(xrzc + shag, yrzc + k3,ttmp)
                                #yrz = yrzc + (1/6) * (k1 + 2*k2 + 2*k3 + k4)
                                
                                xrz = xrzc + self.xfunc(xrzc, yrzc,ttmp)*shag
                                yrz = yrzc + self.yfunc(xrz, yrzc,ttmp)*shag
                                
                                ttmp += shag
                                xrzc = xrz
                                yrzc = yrz

                            cell = m.floor(((yup - yrz) / h)) * leng + m.ceil((xrz - xdown) / h) // 1 + 1
                            set11.add(cell)

                        xtmp = xckl

                    for cell in list(set11):
                        self.G.add_edge(cou, cell)
                    
                xckl += h
                xtmp = xckl
                ytmp = yckl
                
                cou += 1
                cell_list.clear()
            yckl -= h
            xckl = xdown
            xtmp = xckl
            ytmp = yckl
                    
        if gh<7:
            for i in range(abs(7 - gh)):
                nodesbeforethat = self.G.number_of_nodes()
                nodes_to_remove = [node for node, in_degree in self.G.in_degree() if in_degree <= 0]
                self.G.remove_nodes_from(nodes_to_remove)
                if self.G.number_of_nodes() == nodesbeforethat:
                    break
            self.list_good_dots = list(self.G.nodes())
            self.storescc = list( nx.strongly_connected_components(self.G) )

        if gh>=4:
            self.condence_sort_delete(gh)
            return;
        
        if gh == self.flag_to_iterate:
            self.condence_sort_delete(gh)
        #    return;            

        return

#---------КОНДЕНСИРОВАТЬ ТОП СОРТИРОВАТЬ ГРАФ И УДАЛИТЬ ЛИШНИЕ ЯЧЕЙКИ-----------------------------------------

    def condence_sort_delete(self,gh):
        thatonenumber = 2147483647;
        self.G1 = nx.DiGraph(self.G)
        self.storescc = list( nx.strongly_connected_components(self.G) )
        self.dict_storesccnode = {}
        for ii,c1 in enumerate(self.storescc):
            if len(c1)==1:
                for edge in self.G.edges(list(c1)[0]):
                    if edge[0]==edge[1]:
                        self.G1.remove_edge(edge[0],edge[1])
                continue;
            
            thatonenumber1 = thatonenumber - ii
            self.G1.remove_nodes_from(c1)
            self.dict_storesccnode[thatonenumber1] = c1
            
            if len(c1)>= 8:
                print(f"{list(c1)[0:2]} .. {list(c1)[-3:-1]} -> {thatonenumber1}")
            else:
                print(f"{c1} -> {thatonenumber1}")
            self.G1.add_node(thatonenumber1)
            
            for node11 in c1:
                for edge in self.G.edges(node11):
                    if edge[0]==edge[1]:
                        pass
                    if edge[1] not in c1:
                        #print(thatonenumber1, edge[1])
                        self.G1.add_edge(thatonenumber1, edge[1])
                        continue;
                    if edge[0] not in c1:
                        #print(thatonenumber1, edge[1])
                        self.G1.add_edge( edge[0],thatonenumber1)
                        continue;
        
        if (nx.is_directed_acyclic_graph(self.G1)):
            print(" graph got condensed fine ")

        ia = 1
        if gh<=6:
            ia = 7-gh
        
        for i in range(ia):
            self.storetopological_order = list(nx.topological_sort(self.G1))
            self.storescc = [elem for elem in self.storescc if len(list(self.storescc))!=1]
            
            self.list_good_dots = self.storetopological_order
            print(len(self.list_good_dots))
            cutbeforeme = -1
            cutafterme = -1
            for elem in self.list_good_dots:
                if elem > 2000000000:
                    if cutbeforeme == -1:
                        cutbeforeme = elem
                    cutafterme = elem
            
            if cutbeforeme == -1:
                break
            print(cutbeforeme,self.list_good_dots.index(cutbeforeme))
            if self.list_good_dots.index(cutbeforeme) == 0:
                break
            print(cutafterme,self.list_good_dots.index(cutafterme))
            
            self.G1.remove_nodes_from(self.list_good_dots[:self.list_good_dots.index(cutbeforeme)])
            self.list_good_dots = self.list_good_dots[self.list_good_dots.index(cutbeforeme):]
            print(len(self.list_good_dots))

        #self.list_good_dots = list(nx.lexicographical_topological_sort(self.G1))

        for elem in self.dict_storesccnode.keys():
            index_todelete = self.list_good_dots.index(elem)
            #print(index_todelete,len(self.list_good_dots))
            self.list_good_dots = self.list_good_dots[:index_todelete] + list(self.dict_storesccnode[elem]) + self.list_good_dots[index_todelete+1:]
            #print(index_todelete,len(self.list_good_dots))

#---------ПОСТРОИТЬ ИЗОБРАЖЕНИЕ-----------------------------------------

    def imagecreation(self):
        pixmap = QPixmap(self.grW_HIGHT, self.grW_WIDTH)
        pixmap.fill(Qt.white)

        painter = QPainter(pixmap)
        painter.setPen(QColor(255, 0, 0))#
        painter.setBrush(QColor(255, 0, 0))
        
        painter.drawRect(int(self.grW_WIDTH/2), 0, 0, self.grW_HIGHT) #VERTICAL
        painter.drawRect(0, int(self.grW_HIGHT/2), self.grW_WIDTH, 0) #HORISONTAL
        
        painter.setPen(QColor(0, 0, 0))#
        painter.setBrush(QColor(0, 0, 0))
        myh = int(self.h*self.mashtab)
        if myh<1:
            myh = 1
        
        #----
        generator5 = generate_50to150andback()
        
        for ccc in self.list_good_dots:
            makeanumber50to150 = next(generator5)
            painter.setPen(QColor(makeanumber50to150, makeanumber50to150, makeanumber50to150))
            painter.setBrush(QColor(makeanumber50to150, makeanumber50to150, makeanumber50to150))
            x,y = cartesian_to_qrectf(self.xposition(ccc, self.lengx), self.yposition(ccc, self.lengx),  max([self.y1,self.y0]), max([self.x1,self.x0]) )
            painter.drawRect( x*self.mashtab,y*self.mashtab , myh, myh)
        
        generator10 = generate_100to150andback()

        if self.checkboxex3.isChecked():
            for ccc in self.storescc:
                if len(ccc)<=1:
                    continue;
                makeanumber50to150 = next(generator10)
                painter.setPen(QColor(makeanumber50to150, 0, 0))
                painter.setBrush(QColor(makeanumber50to150, 0, 0))

                for num1 in ccc:
                    x,y = cartesian_to_qrectf(self.xposition(num1, self.lengx), self.yposition(num1, self.lengx),  max([self.y1,self.y0]), max([self.x1,self.x0]) )
                    painter.drawRect( x*self.mashtab,y*self.mashtab , myh, myh)  
        
        painter.end()

        newwidth = eval( self.txtgrW_WIDTH.text())
        newhight = eval( self.txtgrW_HIGHT.text())
        self.display_pixmap = pixmap.scaled(newwidth, newhight, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        self.picture_out1.setPixmap(self.display_pixmap)
        if pixmap.save('output.png'):
            print(" image saved")    

#---------НАЙТИ +- ТОЧКИ АТТРАКТОРОВ-----------------------------------------

    def finddotattraktor(self):
        self.h *= 2
        self.lengx *= 0.5
        self.lengy = self.lengx
        pt = 15
        shag = 0.01
        h = self.h
        self.res_neout1 = self.res_neout1 + f"\nПредполагаемые точки аттракторов: \n"
        
        for elem11 in self.storetopological_order:
            if elem11 >= 2000000000:
                nodesofscc = list(self.dict_storesccnode[elem11])
                breakboth = False
                for cell in nodesofscc:
                    x0 = self.xposition(cell, self.lengx)
                    y0 = self.yposition(cell, self.lengy)
                    xtmp = x0
                    ytmp = y0
                    if breakboth == True:
                            break
                    for i in range(0, pt):
                        ytmp -= 1 / pt*h
                        if breakboth == True:
                            break
                        for j in range(0, pt):
                            xtmp += 1 / pt*h
                            ttmp = 0
                            xrzc = xtmp
                            yrzc = ytmp
                            ttmp += shag
                            while True:
                                if ttmp>self.const_endt:
                                    break
                                try:
                                    xrz = xrzc + self.xfunc(xrzc, yrzc,ttmp)*shag
                                    yrz = yrzc + self.yfunc(xrzc, yrzc,ttmp)*shag
                                except OverflowError:
                                    xrz = 100000
                                    yrz = 100000
                                    ttmp = self.const_endt
                                ttmp += shag
                                
                            if xrz < x0+h and xrz > x0 and yrz < y0 and yrz > y0-h:
                                print(xrz,yrz,i,cell)
                                breakboth = True
                                self.res_neout1 = self.res_neout1 + f" {xrz}, {yrz} \n"
                                break

        self.res_out1.setText(self.res_neout1)
        self.h *= 0.5
        self.lengx *= 2
        self.lengy = self.lengx
        pass


#==============ВЫЗОВ КЛАССА ОКНА============================================

app = QApplication([])
window = MainWindow("window")
window.show()
app.exec()
