from PyQt5 import QtCore, QtGui, QtWidgets
from  mainwindow import  Ui_MainWindow
from secondui import Ui_Dialog
import sys
import json
import random

# create app and main window
app = QtWidgets.QApplication(sys.argv)

MainWindow = QtWidgets.QMainWindow()
SecondWindow = QtWidgets.QMainWindow()

ui = Ui_MainWindow()
secondui = Ui_Dialog()

ui.setupUi(MainWindow)
secondui.setupUi(SecondWindow)

MainWindow.show()

# create ButtonGroup to work with radio_btn

group_btn = QtWidgets.QButtonGroup()
group_btn.addButton(ui.rbtn1)
group_btn.addButton(ui.rbtn2)
group_btn.addButton(ui.rbtn3)
group_btn.addButton(ui.radioButton_4)

# create class to work with value in object
class Info():
    def __init__(self,translate,t_answ,f_answ1,f_answ2,f_answ3):

        self.translate = translate
        self.t_answ = t_answ
        self.f_answ1 =  f_answ1
        self.f_answ2 = f_answ2
        self.f_answ3 = f_answ3


# open and load info from json file to data
with open('info.json','r',encoding='utf-8') as file:
    data = json.load(file)

# create all necessary variables and list
key_list = list(data.keys())
index = 0
btn_list = [ui.rbtn1,ui.rbtn2,ui.rbtn3,ui.radioButton_4]

# set first question
ui.label.setText(key_list[0])

random.shuffle(btn_list)

btn_list[0].setText(data[key_list[0]][0])
btn_list[1].setText(data[key_list[0]][1])
btn_list[2].setText(data[key_list[0]][2])
btn_list[3].setText(data[key_list[0]][3])

# cheking correct answer or not
def chek_result():
    global index

    object = Info(key_list[index],data[key_list[index]][0],data[key_list[index]][1],data[key_list[index]][2],data[key_list[index]][3])

    true_answer = object.t_answ

    answer = btn_list[0].isChecked()
    true_text = btn_list[0].text()

    if answer:
        if true_text == true_answer:
            ui.label.setText('Correct')

    else:
        ui.label.setText('Incorrect')

    ui.answer_bt.setText('Go next')
    index += 1

    if index >= len(key_list):
        index = 0

# set next question, reset radio buttons and shuffle radio buttons
def next_q():
    global index

    group_btn.setExclusive(False)

    btn_list[0].setChecked(False)
    btn_list[1].setChecked(False)
    btn_list[2].setChecked(False)
    btn_list[3].setChecked(False)

    group_btn.setExclusive(True)

    ui.label.setText(key_list[index])

    random.shuffle(btn_list)

    btn_list[0].setText(data[key_list[index]][0])
    btn_list[1].setText(data[key_list[index]][1])
    btn_list[2].setText(data[key_list[index]][2])
    btn_list[3].setText(data[key_list[index]][3])

    ui.answer_bt.setText('Go answer')

# mix two functions in one
def mix_functions():
    if ui.answer_bt.text() == 'Go answer':
        chek_result()
    
    elif ui.answer_bt.text() == 'Go next':
        next_q()

# function to exit from program

def exit():
    app.closeAllWindows()

# function to go in second window

def go_second():
    secondui.translate.clear()
    secondui.t_word.clear()
    secondui.f_word1.clear()
    secondui.f_word2.clear()
    secondui.lineEdit_3.clear()

    MainWindow.close()
    SecondWindow.show()

# WORK WITH SECOND WINDOW

# function to add question and dump to json file

def add_q():
    global data
    global key_list

    translate = secondui.translate.text().strip()
    t_word = secondui.t_word.text().strip()
    f_word1 = secondui.f_word1.text().strip()
    f_word2 = secondui.f_word2.text().strip()
    f_word3 = secondui.lineEdit_3.text().strip()

    if translate == '':
        return
    
    elif t_word == '':
        return
    
    elif f_word1 == '':
        return
    
    elif f_word2 == '':
        return
    
    elif f_word3 == '':
        return
    
    data[translate] = [t_word,f_word1,f_word2,f_word3]

    with open('info.json','w',encoding='utf-8') as file:
        json.dump(data,file,indent=4)
    
    with open('info.json','r',encoding='utf-8') as file:
        data = json.load(file)

    key_list = list(data.keys())
    MainWindow.show()
    SecondWindow.close()

# go home function

def gohome():

    MainWindow.show()
    SecondWindow.close()


# connect all function with buttons

ui.add_question.clicked.connect(go_second)
ui.exit_bt.clicked.connect(exit)
ui.answer_bt.clicked.connect(mix_functions)

secondui.pushButton.clicked.connect(add_q)
secondui.pushButton_2.clicked.connect(gohome)

sys.exit(app.exec_())