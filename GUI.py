
import matplotlib


matplotlib.use("QT5Agg")
import sys


from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas


from matplotlib.figure import Figure

import UI

import os


class matplotlibWidget(QtWidgets.QWidget):
    
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.vbl = QtWidgets.QVBoxLayout()
        self.vbl.addWidget(self.canvas)
        self.setLayout(self.vbl)
from window import *




class GUI(QtWidgets.QMainWindow):
    

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        from procedural_city_generation.additional_stuff.IOHelper import StdoutRedirector


        redirector=StdoutRedirector(self.ui.console,app)
        sys.stdout=redirector

        
        UI.setRoadmapGUI(self)
        self.ui.roadmap_widget.hide()
        self.ui.roadmap_Run.clicked.connect(self.start_roadmap)
        self.createTable("roadmap")
        self.ui.roadmap_splitter.setSizes([90, 800])

        self.ui.roadmap_table.hide()
        

        UI.setPolygonsGUI(self)
        self.ui.polygons_widget.hide()
        self.ui.polygons_Run.clicked.connect(self.start_polygons)
        self.createTable("polygons")
        self.ui.polygons_splitter.setSizes([90, 800])

       
        UI.setBuilding_generationGUI(self)
        self.ui.building_generation_widget.hide()
        self.ui.building_generation_Run.clicked.connect(self.start_building_generation)
        self.createTable("building_generation")
        self.ui.building_generation_splitter.setSizes([90, 800])

        
        self.ui.visualization_Run.clicked.connect(UI.visualization)
        self.createTable("visualization")
        self.ui.visualization_splitter.setSizes([90, 800])

        
        self.ui.clean_directories.clicked.connect(self.clean_directories)


        sys.stderr=redirector
    


    #TODO Finish method
    def saveOptions(self, submodule="roadmap"):
        button=getattr(self.ui, submodule+"_save_button")
        table=getattr(self.ui, submodule+"_table")
        button.hide()
        table.hide()
    
            
    def createTable(self, submodule):
	
	
        h=891
        w=891

        from procedural_city_generation.additional_stuff.Param import paramsFromJson, jsonFromParams


        from procedural_city_generation.additional_stuff.Singleton import Singleton


	
	
        params=paramsFromJson(os.getcwd()+"\\procedural_city_generation\\inputs\\"+submodule+".conf")
        
	
        table=QtWidgets.QTableWidget(getattr(self.ui, submodule+"_frame"))
        save_button=QtWidgets.QPushButton(getattr(self.ui, submodule+"_frame"), text="Save")
        save_button.setGeometry(QtCore.QRect(w-100, h, 100, 31))
        save_button.hide()
        default_button=QtWidgets.QPushButton(getattr(self.ui, submodule+"_frame"), text="Reset Defaults")
        default_button.setGeometry(QtCore.QRect(w-260, h, 150, 31))
        default_button.hide()
        table.hide()

	
        table.setGeometry(QtCore.QRect(0, 0, w, h))
        table.setColumnCount(6)
        table.setHorizontalHeaderItem(0, QtWidgets.QTableWidgetItem("Parameter Name"))
        table.setColumnWidth(0, int(0.2*w))
        table.setHorizontalHeaderItem(1, QtWidgets.QTableWidgetItem("Description"))
        table.setColumnWidth(1, int(0.5*w))
        table.setHorizontalHeaderItem(2, QtWidgets.QTableWidgetItem("Default Value"))
        table.setColumnWidth(2, int(0.125*w))
        table.setHorizontalHeaderItem(3, QtWidgets.QTableWidgetItem("Value"))
        table.setColumnWidth(3, int(0.125*w))
        table.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem("min"))
        table.setColumnWidth(4, int(0.1*w))
        table.setHorizontalHeaderItem(5, QtWidgets.QTableWidgetItem("max"))
        table.setColumnWidth(5, int(0.1*w))
        table.setRowCount(len(params))
	
	
        i=0
        for parameter in params:
            g=QtWidgets.QTableWidgetItem(str(parameter.name) )
            g.setFlags( g.flags() & ~QtCore.Qt.ItemIsEditable )
            g.setBackground(QtGui.QBrush(QtGui.QColor(235, 235, 235)))
            table.setItem( i, 0 , g)
             
            g=QtWidgets.QTableWidgetItem(str(parameter.description))
            g.setFlags( g.flags() & ~QtCore.Qt.ItemIsEditable)
            g.setBackground(QtGui.QBrush(QtGui.QColor(235, 235, 235)))
            table.setItem( i, 1 , g)
             
            g=QtWidgets.QTableWidgetItem(str(parameter.default))
            g.setFlags( g.flags() & ~QtCore.Qt.ItemIsEditable)
            g.setBackground(QtGui.QBrush(QtGui.QColor(235, 235, 235)))
            table.setItem( i, 2 , g)
             
            g=QtWidgets.QTableWidgetItem(str(parameter.value))
            table.setItem( i, 3 , g)

            s = "" if parameter.value_lower_bound is None else str(parameter.value_lower_bound)
            g=QtWidgets.QTableWidgetItem(s)
            g.setFlags( g.flags() & ~QtCore.Qt.ItemIsEditable)
            g.setBackground(QtGui.QBrush(QtGui.QColor(235, 235, 235)))
            table.setItem( i, 4 , g)

            s = "" if parameter.value_upper_bound is None else str(parameter.value_upper_bound)
            g=QtWidgets.QTableWidgetItem(s)
            g.setFlags( g.flags() & ~QtCore.Qt.ItemIsEditable)
            g.setBackground(QtGui.QBrush(QtGui.QColor(235, 235, 235)))
            table.setItem( i, 5 , g)
            i+=1


	
        getattr(self.ui, submodule+"_Options").clicked.connect(table.show)
        getattr(self.ui, submodule+"_Options").clicked.connect(save_button.show)
        getattr(self.ui, submodule+"_Options").clicked.connect(default_button.show)
        setattr(self.ui, submodule+"_table", table)

        def save_params():
            for i, param in enumerate(params):
                it=table.item(i, 3).text()
                try:
                    it=eval(str(it))
                except:
                    it=str(it)
                param.setValue(it)
                Singleton(submodule).kill()
            jsonFromParams(os.getcwd()+"/procedural_city_generation/inputs/"+submodule+".conf", params)
            print("Save successful")
            save_button.hide()
            default_button.hide()
            table.hide()
            print(UI.donemessage)

        save_button.clicked.connect(save_params)
        setattr(self.ui, submodule+"_save_button", save_button)

        def default_params():
            for i, param in enumerate(params):
                table.item(i, 3).setText(str(param.default))


        default_button.clicked.connect(default_params)
        setattr(self.ui, submodule+"_default_button", default_button)



    def plot(self, x, y, linewidth=1, color="red"):
        self.active_widget.canvas.ax.plot(x, y, linewidth=linewidth, color=color)
       
    def clear(self):
        self.active_widget.canvas.ax.clear()
                
    def start_roadmap(self):
        self.active_widget=self.ui.roadmap_widget
        self.active_widget.show()
        self.clear()
        UI.roadmap()
        
    def start_polygons(self):
        self.active_widget=self.ui.polygons_widget
        self.active_widget.show()
        self.clear()
        UI.polygons()

    def start_building_generation(self):
        self.active_widget=self.ui.building_generation_widget
        self.active_widget.show()
        self.clear()
        UI.building_generation()

    def clean_directories(self):
        from procedural_city_generation.additional_stuff.clean_tools import clean_pyc_files


        print("removing all .pyc files")
        clean_pyc_files(os.getcwd())
        print("removing all items in /procedural_city_generation/temp/ directory")
        os.system("rm -f " +os.getcwd()+"/procedural_city_generation/temp/*")
        print("removing all items in /procedural_city_generation/outputs/ directory")
        os.system("rm -f " +os.getcwd()+"/procedural_city_generation/outputs/*")
        print(UI.donemessage)
        
    def set_xlim(self, tpl):
        self.active_widget.canvas.ax.set_xlim(tpl)
        
    def set_ylim(self, tpl):
        self.active_widget.canvas.ax.set_ylim(tpl)
        
    def update(self):
        self.active_widget.canvas.draw()
        global app
        app.processEvents()


class FigureSaver:
    class __FigureSaver:
        def __init__(self, fig=None):
            self.plot=fig.plot
            self.show=fig.show
    instance=None

    def __init__(self, fig=None):
        if not FigureSaver.instance and (fig is not None):
            FigureSaver.instance=FigureSaver.__FigureSaver(fig)


    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        setattr(self.instance, name, value)

class MplCanvas(FigureCanvas):

    def __init__(self):
        self.fig = Figure(frameon=False)
        self.ax = self.fig.add_subplot(111)
        self.ax.get_yaxis().set_visible(False)
        self.ax.get_xaxis().set_visible(False)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)





if __name__  ==  "__main__":
    global app
    app = QtWidgets.QApplication(sys.argv)
    myapp = GUI()
    myapp.show()
    app.exec_()