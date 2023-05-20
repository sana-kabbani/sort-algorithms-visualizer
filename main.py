import random
import time
import numpy as np

from matplotlib.backends.backend_qt5agg import \
    NavigationToolbar2QT as NavigationToolbar
from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer

class MatplotlibWidget(QMainWindow):

    # Declare class var
    xdata = None
    ydata = None
    loop_state = False
    algor = None
    plot_type= None
    switch_no = 0

    def __init__(self):
        
        # Constructor
        QMainWindow.__init__(self)

        # Read UI
        loadUi("sort_project.ui",self)
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.low = None
        self.high = None
        self.pivot_index = None
     
        self.initial_graph()
        self.MplWidget.canvas.axes.get_xaxis().set_visible(False)
        self.MplWidget.canvas.axes.get_yaxis().set_visible(False)

        self.custom.toggled.connect(self.custome)
        self.random.toggled.connect(self.Random)
        


        # Connect methods to Radio buttons  :
        self.Bubble.toggled.connect(lambda: self.algorithm("bubble"))
        self.Insertion.toggled.connect(lambda : self.algorithm("insertion"))
        self.Merge.toggled.connect(lambda: self.algorithm("merge"))
        self.Selection.toggled.connect(lambda : self.algorithm("selection"))
        self.Quick.toggled.connect(lambda : self.algorithm("quick"))
         
        self.Scatter.toggled.connect(lambda : self.plot("scatter"))
        self.Bar.toggled.connect(lambda : self.plot("bar"))
        self.Stem.toggled.connect(lambda : self.plot("stem"))
        self.sayi.setText(str(self.switch_no))
        

        # Update Graph when spin-box is changed
        self.spnBars.valueChanged.connect(self.update_new_graph)
        self.create_button.clicked.connect(self.create)
        

        self.reset_button.clicked.connect(self.reset)
        self.start_button.clicked.connect(lambda: self.start(self.algor))
        self.stop_button.clicked.connect(self.stop_sort)
    def custome(self):
        self.groupBox.setEnabled(False)
        self.groupBox_2.setEnabled(True)
    def Random(self):
        self.groupBox.setEnabled(True)
        self.groupBox_2.setEnabled(False)
        
    def create(self):
        
        text = self.list.text()
        
        self.numbers_list = text.split()
        
        try:
            self.numbers_list = [int(number) for number in self.numbers_list]
            self.old_list = self.numbers_list
            self.update_new_graph()
        except: 
           print("An exception occurred")
        
        
        
        
        
        
           
#frames            
    def new_frame2(self, index):
        
         
        time.sleep(self.ani_time())
        self.MplWidget.canvas.axes.clear()

        # renk liste oluşturmak
        bar_color = ["#00A7E1"] * (len(self.ydata)-1)
        bar_color.insert(index,"ffa500")
        
        self.draw_graph(self.xdata, self.ydata, bar_color)
        QtCore.QCoreApplication.processEvents()
        
    def new_frame_switch(self, highlight_bar,ikinci ):
     
        time.sleep(self.ani_time())
        self.MplWidget.canvas.axes.clear()

        # renk liste oluşturmak
        bar_color = ["#00A7E1"] * (len(self.ydata)-2)
        bar_color.insert(highlight_bar,"#ffa500")
        bar_color.insert(ikinci,"#ffa500")
       
        self.draw_graph(self.xdata, self.ydata, bar_color)
        QtCore.QCoreApplication.processEvents()
    def new_frame(self, i):
        time.sleep(self.ani_time())
        self.MplWidget.canvas.axes.clear()

        bar_color = ["#00A7E1"] * (len(self.ydata)-1)
        for i in  range(i) :
           bar_color.insert(i ,"red")

        self.draw_graph(self.xdata, self.ydata, bar_color)
        QtCore.QCoreApplication.processEvents()
    

    def ani_time(self):
        # Sütun miktarına ölçeklenmiş sıralama bekleme süresini belirleme
        
        ani_speed = self.speed_slider.value()

        #Kaydırıcı değerinden uyku süresini belirleyen doğrusal formül
        ani_interval = (-1/295)*ani_speed + 1
        return(ani_interval)
        
    def reset(self):
        
        self.MplWidget.canvas.axes.clear()
        if self.groupBox.isEnabled():
            bar_count = self.spnBars.value()
            scram_ys = [i for i in range(1, bar_count +1)]
            xs = scram_ys.copy()
            
            
        
            for j in range(0, len(scram_ys)-1):
                target = random.randint(j, len(scram_ys)-1)
                scram_ys[j] , scram_ys[target] = scram_ys[target], scram_ys[j]
        
        elif self.groupBox_2.isEnabled():
            value = self.numbers_list
            scram_ys = self.old_list 
            xs =  [i for i in range(1, len(self.old_list) +1)]
        
       
       
        self.ydata = scram_ys.copy()
        self.xdata = xs.copy()

        
        self.draw_graph(xs, scram_ys, None)

    def update_new_graph(self):
        # Update canvas on change event from the spin edit
        self.MplWidget.canvas.axes.clear()
        # Değiştirilen boyutta yeni veri kümesi oluştur
        if self.groupBox.isEnabled():
            bar_count = self.spnBars.value()
            ys = [i for i in range(1, bar_count +1)]
            xs = ys.copy()
        elif self.groupBox_2.isEnabled():
            value = self.numbers_list
            ys = self.numbers_list 
            xs =  [i for i in range(1, len(self.numbers_list) +1)]
            
        
            

        
        
        

        # mevcut olan  sınıfının değişkenlere  veri gönder
        self.ydata = ys.copy()
        self.xdata = xs.copy()

        # Grafiğe yeni veriler çizin
        self.draw_graph(xs, ys, None)
        
    def initial_graph(self):
     
        self.update_new_graph()

    def draw_graph(self, xs, ys, bar_color):
        # x-listesinden ve y-listesinden grafik çizin
        if bar_color is None:
            if self.plot_type == "scatter":
                self.MplWidget.canvas.axes.scatter(xs, ys, color = "#00A7E1")
            elif self.plot_type == "stem":
                xs = np.array(xs)
                ys = np.array(ys)
                if xs.size == 0 or ys.size == 0:
                    print("Error: Empty data arrays.")
                else:
                   sorted_indices = np.argsort(xs)
                   sorted_xs = xs[sorted_indices]
                   sorted_ys = ys[sorted_indices]
                   self.MplWidget.canvas.axes.stem(sorted_xs, sorted_ys, linefmt='C0-', markerfmt='C0o', basefmt='k-')
                
            else:
                self.MplWidget.canvas.axes.bar(xs, ys, color = "#00A7E1")
                                
        else:
            # Renk parametresi seçilen  vurgulayacaktır (switch)
            if self.plot_type == "scatter":
                  self.MplWidget.canvas.axes.scatter(xs, ys, color = bar_color)
            elif self.plot_type == "stem":
                xs = np.array(xs)
                ys = np.array(ys)
                if xs.size == 0 or ys.size == 0:
                    print("Error: Empty data arrays.")
                else:
                   sorted_indices = np.argsort(xs)
                   sorted_xs = xs[sorted_indices]
                   sorted_ys = ys[sorted_indices]
                   self.MplWidget.canvas.axes.stem(sorted_xs, sorted_ys, linefmt=  '-', markerfmt='o', basefmt='k-')

                
            else:
                self.MplWidget.canvas.axes.bar(xs, ys, color = bar_color)
        self.MplWidget.canvas.draw()      

    def buttons(self, tfstate):
        self.Bubble.setEnabled(tfstate)
        self.Insertion.setEnabled(tfstate)
        self.Merge.setEnabled(tfstate)
        self.Selection.setEnabled(tfstate)
        self.Quick.setEnabled(tfstate)
        self.Bar.setEnabled(tfstate)
        self.Stem.setEnabled(tfstate)
        self.Scatter.setEnabled(tfstate)
        self.create_button.setEnabled(tfstate)
        self.start_button.setEnabled(tfstate)
        self.reset_button.setEnabled(tfstate)
      
 #algorithms    
    def  bubble_sort(self):
        # veri kopyala
        yarray = self.ydata.copy()

        # Düğmeleri devre dışı bırak
        self.buttons(False)

        # Tüm öğeler arasında döngü
        for i in range(len(yarray)):

            # Son i öğeleri sıralanacağı için yeni bitiş noktası belirleyin 
            endp = len(yarray) - i
            self.bigo.setText("θ(n^2)")
            
            
            for j in range(0 , endp):
                if not self.loop_state:
                   break
                
                # Döngünün liste dışına çıkmasını engelle
                if j+1 == len(yarray):
                    pass
                else:
                    if yarray[j] > yarray[j+1]:
                        self.new_frame_switch(j,j+1)

                        yarray[j], yarray[j+1] = yarray[j+1], yarray[j]
                        self.switch_no = self.switch_no + 1
                        self.sayi.setText(str(self.switch_no))
                          
                        self.ydata = yarray    
                        self.new_frame_switch(j,j+1)
                        
            
       
            if not self.loop_state:
                   break

        self.buttons(True)
   
    def insert_sort(self):
        yarray = self.ydata.copy()
        self.bigo.setText("θ(n^2)")

        
        self.buttons(False)

   
        for i in range(len(yarray)):
            if not self.loop_state:
                break

            if (i+1) == len(yarray):
               
                break 
            else:
                
                if yarray[i] > yarray[i+1]:
                   
                    for k in reversed(range(i+1)):
                        if not self.loop_state:
                            break
                        if yarray[k+1] < yarray[k]:
                            self.new_frame_switch(k,k+1)
                            yarray[k], yarray[k+1] = yarray[k+1] , yarray[k]

                          
                            self.ydata = yarray
                           

                           
                            
                            
                            self.new_frame_switch(k,k+1)
                        else:
                            break

        self.buttons(True)
         
    def merge_sort(self):
        yarray = self.ydata.copy()
        self.buttons(False)
        self.bigo.setText("θ(nlog(n))")

        yarray = self.merge_split(yarray)

        self.ydata = yarray
        self.new_frame(0)
        
        self.buttons(True)

    def merge_split(self, arr):
        length = len(arr)
        if not self.loop_state:
           return arr

 
        if length == 1:
            return(arr)
        
        midp = length//2

        # Tek bir öğe dönene kadar bölmek için kendini çağır, sınıf değişkenini güncelle
        arr_1 = self.merge_split(arr[:midp])
        self.merge_update(arr_1, self.ydata)
        arr_2 = self.merge_split(arr[midp:])
        self.merge_update(arr_2, self.ydata)
        
        self.new_frame(0)

      # Yarım listeleri sıralamak için çağrı birleştirme
        return(self.merge(arr_1, arr_2))

    def merge_update(self, sub_list, main_list):
        
        # Get index of the sorted elements in the main list
        pos = []
        for value in sub_list:
            pos.append(main_list.index(value))

        # Remove elem from main list
        for v in sub_list:
            main_list.remove(v)
        
        # Find range
        high = max(pos)
        low = min(pos)

        # Insert same elements back to main list, from sorted list (in order)
        for i in range(low, high+1):
            main_list.insert(i, sub_list[i-low])
        
    def merge(self, arr_1, arr_2):
         
        sorted_arr = []

        # Use append and pop, given already sorted lists 
        while arr_1 and arr_2:
            
            if arr_1[0] < arr_2[0]:
                # arr1[0] smaller
                sorted_arr.append(arr_1.pop(0))
            else:
                # arr2[0] smaller
                sorted_arr.append(arr_2.pop(0))

        # Append from sorted sublist, as one of the sub-list will be empty
        while arr_1:
            sorted_arr.append(arr_1.pop(0))

        while arr_2:
            sorted_arr.append(arr_2.pop(0))

        return(sorted_arr)
            
    def select_sort(self):
        self.bigo.setText("θ(n^2)")
        
    
        yarray = self.ydata.copy()


        self.buttons(False)
        l=0

        # Loop through list
        for i in range(len(yarray)):
            if not self.loop_state:
                break

            # Alt listedeki en küçük sayı için min'i yerleştirin
            min = 0
            
# Sıralanmamış alt listeyi yineleyin
            for j in range(i,len(yarray)):
                if not self.loop_state:
                    break
                
                
                if ( min == 0 ):
                    min = yarray[j]
                elif yarray[j] < min:
                    min = yarray[j]
                    l = j

                
                self.new_frame_switch(l , j)
            
           # En alttaki çubuğu okuyun ve sıralanan kısma ekleyin
            shifter_index = yarray.index(min)
            yarray.pop(shifter_index)
            yarray.insert(i, min)

            self.ydata = yarray

            self.new_frame(i+1)

        self.buttons(True)
    
    def quick_sort(self):
       self.bigo.setText("θ(nlog(n))")

       yarray = self.ydata.copy()
       self.buttons(False)
       self.quick_sort_recursive(yarray, 0, len(yarray) - 1)
       self.ydata = yarray
       self.buttons(True)
     
    def quick_sort_recursive(self, arr, low, high):
        if not self.loop_state:
               return arr
        if low < high:
            
            # Diziyi bölümlere ayırın ve pivot dizinini alın
            pivot_index = self.partition(arr, low, high)
            self.low = low
            self.high = high
            self.pivot_index = pivot_index
        
            # Sol ve sağ alt dizilerde yinelemeli olarak hızlı sıralama çağırın
            self.quick_sort_recursive(arr, low, pivot_index - 1)
            self.quick_sort_recursive(arr, pivot_index + 1, high)       
    
    def partition(self, arr, low, high):
    # Pivot olarak en sağdaki elemanı seçin
       pivot = arr[high]
       i = low - 1
       self.new_frame2(high)

       for j in range(low, high):
           if arr[j] <= pivot:  
            # Öğeleri değiştir
               i += 1
               self.new_frame_switch(i,j)
               arr[i], arr[j] = arr[j], arr[i]


               self.ydata = arr
               self.new_frame_switch(i,j)

# Pivotu son konumuna getirin
       arr[i + 1], arr[high] = arr[high], arr[i + 1]
       self.new_frame2(i+1)

       self.ydata = arr
       return i + 1
                          
    def start(self , value):
        self.loop_state = True
        if(value == "bubble"):
            self.bubble_sort()
        if(value == "insertion"):
            self.insert_sort()
        if(value == "selection"):
            self.select_sort()
        if(value == "merge"):
            self.merge_sort()
        if(value == "quick"):
            self.quick_sort()
    def algorithm(self , value):
        if value =="bubble":
            self.algor = "bubble"
        if value =="insertion":
            self.algor = "insertion"
        if value =="merge":
            self.algor = "merge"
        if value =="selection":
            self.algor = "selection"
        if value == "quick":
           self.algor = "quick"
   
    def plot(self , value):
        if value =="scatter":
            self.plot_type = "scatter"
        if value =="bar":
            self.plot_type = "bar"
        if value =="stem":
            self.plot_type = "stem"

    def stop_sort(self):
    #Sıralama işlemini durdurmak için döngü durumunu Yanlış olarak ayarlayın
       self.loop_state = False

#çalıştırma  
app = QApplication([])
window = MatplotlibWidget()
window.show()
app.exec_()