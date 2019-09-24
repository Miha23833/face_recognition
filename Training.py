from PIL import Image
import numpy as np
import datetime
import logging
import cv2
import os


def training():  # функция для вызова из модуля main
    # путь к папке с лицами
    path = 'dataset'
    logging.basicConfig(filename='face_recognizer.log', level=logging.INFO)
    logger = logging.getLogger('Training')
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    #  получаем изображения и имена лиц на них
    def get_images_and_labels():
        image_paths = []
        for f in os.listdir(path):
            image_paths.append(os.path.join(path, f))
        face_samples = []
        ids_list = []
        for image_path in image_paths:
            img = Image.open(image_path).convert('L')  # Перевод изображения в оттенки серого
            img_numpy = np.array(img, 'uint8')  # Перевод изображения в целочисленный массив numpy
            face_id = int(os.path.split(image_path)[-1].split(".")[1])  # Получение имени лица из названия файла
            # картинки
            faces_detected = detector.detectMultiScale(img_numpy)  # распознавание лиц на картинке
            for (x, y, w, h) in faces_detected:  # Добавление распознанных лиц и их имён в соответсвующие списки
                face_samples.append(img_numpy[y:y+h, x:x+w])
                ids_list.append(face_id)
        return face_samples, ids_list

    faces, ids = get_images_and_labels()
    try:
        recognizer.train(faces, np.array(ids))
    except cv2.error:
        logger.error('['+str(datetime.datetime.now())+'] - '+'Training not successed because training images not found')
        return None

    # Сохранение результата как trainer/trainer.yml
    recognizer.write('training/trainer.yml')
    logger.info('['+str(datetime.datetime.now())+'] - '+'Training is successfuly.'
                                                        ' Results saved as training/trainer.xml')
