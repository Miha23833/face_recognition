import tkinter
import cv2

cap = cv2.VideoCapture(0)  # Создается класс VideoCapture, принимающий индекс подключенной камеры

while True:  # Бесконечный цикл, в котором считывается изображение с вдеокамеры и передаётся на экран
    ret, frame = cap.read()  # метод read возвращает True и изображение с камеры или False и None, если камеры нет
    if not ret:  # Если камера не найдена, создаётся окно с текстом "Камера не найдена". После закрытия окна
        # цикл прекращается и программа закрывается
        root = tkinter.Tk()
        root.geometry('200x50')
        root.resizable(width=False, height=False)
        not_f = tkinter.Label(root, text='Камера не найдена')
        not_f.place(x=45, y=10)
        root.mainloop()
        break
    cv2.imshow('Capturing video', frame)  # метод imshow выводит изображение на экран. Принимаемые аргументы:
    #  название выводимого окна и изображение, которое будет выводиться
    if cv2.waitKey(1) & 0xFF == ord('q'):  # при нажатии на кнопку q цикл прекращается
        break
    if cv2.getWindowProperty('Capturing video', cv2.WND_PROP_VISIBLE) < 1:  # при закрытии окна цикл прекращается
        break

cap.release()  # отключаемся от камеры
cv2.destroyAllWindows()  # закоываем все окна, которые открылись этой программой
