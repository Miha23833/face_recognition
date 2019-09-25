import DataBase
import datetime
import logging
import tkinter
import cv2


def recognition():
    DataBase.create_table()
    logging.basicConfig(filename='face_recognizer.log', level=logging.INFO)
    logger = logging.getLogger('face_recognition')
    logging.info('['+str(datetime.datetime.now())+'] - '+'START RECOGNITION')
    names = []
    data = DataBase.read_data()
    for key in data:
        names.append(data[key])

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    try:
        recognizer.read('training/trainer.yml')
    except cv2.error:
        logger.error('[' + str(datetime.datetime.now()) + '] - ' + 'not found trainer.yml')
        root = tkinter.Tk()
        root.geometry('200x50')
        root.resizable(width=False, height=False)
        not_f = tkinter.Label(root, text='Сначала нужно\n обучить программу')
        not_f.place(x=45, y=10)
        root.mainloop()
        return None

    cascade_path = 'haarcascade_frontalface_default.xml'  # Загрузка классификатора для обнаружения лиц - каскады Хаара
    face_cascade = cv2.CascadeClassifier(cascade_path)

    font = cv2.FONT_HERSHEY_SIMPLEX

    face_id = 0  # объявление id лица, которое распознает программа

    cap = cv2.VideoCapture(0)  # Создается класс VideoCapture, принимающий индекс подключенной камеры

    minw = 0.1*cap.get(3)
    minh = 0.1*cap.get(4)

    # Установка разрешения окна с выводом изображения
    cap.set(3, 1440)
    cap.set(4, 900)

    while True:  # Бесконечный цикл, в котором считывается изображение с вдеокамеры и передаётся на экран
        ret, frame = cap.read()  # метод read возвращает True и изображение с камеры или False и None, если камеры нет
        if not ret:  # Если камера не найдена, создаётся окно с текстом "Камера не найдена". После закрытия окна
            # цикл прекращается и программа закрывается
            logger.error('[' + str(datetime.datetime.now()) + '] - ' + 'camera not found!')
            root = tkinter.Tk()
            root.geometry('200x50')
            root.resizable(width=False, height=False)
            not_f = tkinter.Label(root, text='Камера не найдена')
            not_f.place(x=45, y=10)
            root.mainloop()
            return None
        frame = cv2.flip(frame, 1)  # отзеркаливание по горизонтали
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(  # распознавание лица на кадре
            gray,  # Входное изображение для распознавания, но в оттенках серого
            scaleFactor=1.2,  # это параметр, определяющий размер изображения при каждой шкале изображения.
            # Он используется для создания масштабной пирамиды.
            minNeighbors=5,  # параметр, указывающий, сколько соседей должно иметь каждый прямоугольник кандидата,
            # чтобы сохранить его. Более высокое число дает более низкие ложные срабатывания.
            minSize=(int(minw), int(minh)),  # минимальный размер прямоугольника, который считается лицом
        )

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            detected_face_id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            # Получаем id

            if confidence < 50:
                face_id = names[detected_face_id]
                confidence = "  {0}%".format(round(100 - confidence))
                logger.info('['+str(datetime.datetime.now())+'] - '+'Recognized {} with {}%'
                                                                    ' confidence'.format(face_id, confidence))
            else:
                face_id = "unknown"
                confidence = ''
                logger.info('['+str(datetime.datetime.now())+'] - '+'recognized face, but identity could not be'
                                                                    ' determined')

            cv2.putText(frame, str(face_id), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(frame, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        cv2.imshow('Capturing video', frame)  # метод imshow выводит изображение на экран. Принимаемые аргументы:
        #  название выводимого окна и изображение, которое будет выводиться
        if cv2.waitKey(10) & 0xFF == 27:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):  # при нажатии на кнопку q цикл прекращается
            break
        if cv2.getWindowProperty('Capturing video', cv2.WND_PROP_VISIBLE) < 1:  # при закрытии окна цикл прекращается
            break

    cap.release()  # отключаемся от камеры
    cv2.destroyAllWindows()  # закоываем все окна, которые открылись этой программой
