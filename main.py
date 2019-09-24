import face_recognition
import Dataset_filling
import datetime
import Training
import tkinter
import logging


logging.basicConfig(filename='face_recognizer.log', level=logging.INFO)
logger = logging.getLogger('Main')
logger.info('['+str(datetime.datetime.now())+'] - '+'Programm started')

root = tkinter.Tk()
root.resizable(width=False, height=False)
root.geometry('300x178')
root.title('Что нужно сделать?')
dataset_filling_button = tkinter.Button(text='Дополнить базу лиц\n для распознавания', heigh=3,
                                        command=Dataset_filling.dataset_filling)
training_button = tkinter.Button(text='Тренировать распознаватель', heigh=2, font='Arial 14',
                                 command=Training.training)
recognition_button = tkinter.Button(text='Включить распознавание лиц', heigh=2, font='Arial 14',
                                    command=face_recognition.recognition)
dataset_filling_button.pack(fill=tkinter.X)
training_button.pack(fill=tkinter.X)
recognition_button.pack(fill=tkinter.X)
root.mainloop()

logger.info('['+str(datetime.datetime.now())+'] - '+'Programm closed')
