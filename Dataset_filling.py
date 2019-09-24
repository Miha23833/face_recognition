import DataBase
import datetime
import logging
import tkinter
import cv2

NAME = ''  # Имя для нового лица


def dataset_filling():  # функция для вызова из модуля main
    logging.basicConfig(filename='face_recognizer.log', level=logging.INFO)
    logger = logging.getLogger('Dataset_filling')
    DataBase.create_table()
    count = 1  # Количество пройденных циклов распознавания лица. После 30 циклов программа заканчивает видеозахват

    def write_name():  # Функция записывает в глобальную переменную NAME тест, введённый в поле имени лица
        global NAME
        if len(enter_name.get()) >= 50:
            NAME = enter_name.get()[:50]
        else:
            NAME = enter_name.get()

    cap = cv2.VideoCapture(0)  # Создается класс VideoCapture, принимающий индекс подключенной камеры
    cascade_path = 'haarcascade_frontalface_default.xml'  # Загрузка классификатора для обнаружения лиц - каскады Хаара
    face_cascade = cv2.CascadeClassifier(cascade_path)

    # Установка разрешения окна с выводом изображения
    cap.set(3, 1440)
    cap.set(4, 900)

    # Создаём информирующее окно, куда также будем вводить имя для лица
    root = tkinter.Tk()
    root.resizable(width=False, height=False)
    root.geometry('300x140')
    text = tkinter.Label(root, text='Введите имя и фамилию\n для нового пользователя\n на латинице', font='arial 15')
    enter_name = tkinter.Entry(root, width=20, font='arial 13')
    warning = tkinter.Label(root, text='После ввода текста \nсмотрите в камеру и ждите')
    enter_button = tkinter.Button(root, text='OK', font='Arial 14')
    enter_button.bind('<Button-1>', lambda event: (write_name(), root.quit()))
    enter_name.bind('<Return>', lambda event: (write_name(), root.quit()))
    text.pack()
    enter_name.pack()
    enter_button.place(x='243', y='75', heigh=23)
    warning.pack()
    root.mainloop()

    if NAME == '':
        return None

    ID = DataBase.select_max()
    if not ID:
        ID = 1
    if ID == 0:
        ID = 1
    logger.info('['+str(datetime.datetime.now())+'] - '+'started recognizing face as '+NAME)
    while True:  # Бесконечный цикл, в котором считывается изображение с вдеокамеры и передаётся на экран
        ret, frame = cap.read()  # метод read возвращает True и изображение с камеры или False и None, если камеры нет
        if not ret:  # Если камера не найдена, создаётся окно с текстом "Камера не найдена". После закрытия окна
            # цикл прекращается и программа закрывается
            logger.error('['+str(datetime.datetime.now())+'] - '+'camera not found!')
            root = tkinter.Tk()
            root.geometry('200x50')
            root.resizable(width=False, height=False)
            not_f = tkinter.Label(root, text='Камера не найдена')
            not_f.place(x=45, y=10)
            root.mainloop()
            return None
        frame = cv2.flip(frame, 1)  # отзеркаливание по горизонтали
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Чёрно-белый фильтр

        faces = face_cascade.detectMultiScale(  # распознавание лица на кадре
            gray,  # Входное изображение для распознавания, но в оттенках серого
            scaleFactor=1.2,  # это параметр, определяющий размер изображения при каждой шкале изображения.
            # Он используется для создания масштабной пирамиды.
            minNeighbors=5,  # параметр, указывающий, сколько соседей должно иметь каждый прямоугольник кандидата,
            # чтобы сохранить его. Более высокое число дает более низкие ложные срабатывания.
            minSize=(20, 20)  # минимальный размер прямоугольника, который считается лицом
        )

        for (x, y, w, h) in faces:  # Цикл, в котором в экране вывода изображения вокруг распознанного лица появляется
            # квадрат, а также сохраняется изображение распознанного лица
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            cv2.imwrite('dataset/User.'+str(ID)+'.'+str(count)+'.jpg', gray[y:y+h, x:x+w])
            logger.info('['+str(datetime.datetime.now())+'] - '+'recognized as '+NAME +
                        ' and saved as '+'dataset/User.'+str(ID)+'.'+str(count)+'.jpg')
            count += 1  # Количество распознанных лиц. Увеличивается тогда, когда распознаётся лицо

        cv2.imshow('Capturing video', frame)  # метод imshow выводит изображение на экран

        #  название выводимого окна и изображение, которое будет выводиться
        if cv2.waitKey(1) & 0xFF == ord('q'):  # при нажатии на кнопку q цикл прекращается
            break
        if cv2.getWindowProperty('Capturing video', cv2.WND_PROP_VISIBLE) < 1:  # при закрытии окна цикл прекращается
            break
        if count >= 71:  # Ограничение на запись изображений.
            break

    DataBase.add_user(NAME)
    cap.release()  # отключаемся от камеры
    cv2.destroyAllWindows()  # закоываем все окна, которые открылись этой программой
    logger.info('['+str(datetime.datetime.now())+'] - '+'Recognizing done')
