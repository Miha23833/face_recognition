  Что это такое?
  --------------
  Программа для распознавания лиц и вывода изображения 

  Скачать
  -------
  https://github.com/Miha23833/project_2/blob/develop/WebCamera.py.


  Установка
  ---------  
    Ввести в консоль python pyinstaller [путь к файлу main, включая сам файл], 
    или собрать python-проект в исполняемый файл другим способом.
    Поместить файл haarcascade_frontalface_default.xml в корневую папку собранного проекта

  Запуск
  ------
  Запустить файл main.py, который находится в папке dist.

  Использование
  -------------
  Изначально появляется меню с 3 вариантами выбора:
  
    -Дополнить базу лиц для распознавания - при нажатии у пользователя 
      спрашивается его имя и фамилия. После ввода включается камера и
      сохраняет 70 фотографий распознанного лица в папку dataset с именем
      пользователя и номером фотографии в названии. Закрытие программы 
      осуществляется с помощью кнопки q или Esc с обязательно включённой
      английской раскладкой. 

    -Тренировать распознаватель - обучить программу распознавать людей на
      основе фотографий, сохранённых в папке dataset

    -Включить распознавание лиц - на экран выводится изображение с веб камеры
      и программа обводит распознанные ей лица на этом изображении в квадрат.
      Те лица, которые программа смогла идентифицировать как известные 
      подписываются внизу квадрата именем и фамилией. Неопознанные лица
      подписываются как "Unknown"

  Возможные ошибки
  ----------------
  Если при подключении двух и более веб камер появляется ошибка об отсутсвии
  веб камеры, тогда следует подключить рабочую веб камеру к первому USB-порту.

  Дополнительно
  -------------
  Программа написана на python 3.7 на ОС Windows 10.
  Используемые библиотеки:
    Opencv-contrib-python,
    datetime,
    sqlite3,
    tkinter,
    loggong,   
    numpy,
    PIL,
    os.


  Ссылка на исходный код
  ----------------------

  https://github.com/Miha23833/project_2
