import os
import re
import cv2
import matplotlib.pyplot as plt
import numpy as np

import matplotlib
matplotlib.use('Agg')

# Обрабатывает путь до файла
def secure_filename(filename):
    # Удаляем путь, если случайно передан полный путь
    filename = os.path.basename(filename)
    # Заменяем недопустимые символы (кроме букв, цифр, тире, подчёркивания и точки)
    filename = re.sub(r'[^a-zA-Z0-9.\-_]', '_', filename)
    # Возвращаем безопасное имя
    return filename

# Функция умножения изображения на функцию sin или cos.
def processing_of_img(filename_img, choice_func, arg_func_value, sin_freq=1.0, sin_phase=0.0, cos_freq=1.0, cos_phase=0.0):
    # Загружаем изображение
    img = cv2.imread(filename_img, cv2.IMREAD_COLOR).astype(np.float32)
    # Преобразование изображения в float для точности операций.
    img = img.astype(np.float64)

    # Получаем размеры изображения
    height, width, _ = img.shape

    # Создаём сетку координат
    x = np.linspace(0, 2 * np.pi, width)  # Горизонтальные координаты
    y = np.linspace(0, 2 * np.pi, height)  # Вертикальные координаты
    X, Y = np.meshgrid(x, y)

    arg_func_value = float(arg_func_value)


    # Выбираем функцию для модификации
    if choice_func == 'sin':
        modulator = np.sin(arg_func_value * X)  # Применяем sin
    elif choice_func == 'cos':
        modulator = np.cos(arg_func_value * X)  # Применяем cos
    elif choice_func == 'sin+cos':
        modulator = (np.sin(sin_freq * X + sin_phase) + 
                     np.cos(cos_freq * X + cos_phase))  # Комбинация sin и cos
    else:
        raise ValueError("Некорректная функция!")

    # Применяем модификатор к изображению
    modulator = modulator[:, :, np.newaxis]  # Добавляем ось для совместимости
    img_done = img * modulator  # Умножаем изображение на модификатор
    img_done = np.clip(img_done, 0, 255).astype(np.uint8)  # Ограничиваем значения от 0 до 255

    # Генерируем имя для нового файла
    filename, file_extension = os.path.splitext(filename_img)
    filename_img_done = f"{filename}_done{file_extension}"

    # Сохраняем результат
    cv2.imwrite(filename_img_done, img_done)

    return filename_img_done


# Функция для построения графика распределения цветов.
def to_create_plot(filename):
    print(filename)
    # Чтение изображения.
    img = cv2.imread(filename, cv2.IMREAD_COLOR)

    # Разбиение имени файла.
    filename, file_extension = os.path.splitext(filename)
    filename_plot = filename + '_plot' + file_extension

    img_lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)

    y, x, z = img_lab.shape
    flat_lab = np.reshape(img_lab, [y * x, z])

    colors = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    colors = np.reshape(colors, [y * x, z]) / 255.

    # Построение графика распределения цветов.
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(xs=flat_lab[:, 2], ys=flat_lab[:, 1], zs=flat_lab[:, 0], s=10, c=colors, lw=0)
    # Установка осей.
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    # Сохранение графика в файл.
    fig.savefig(filename_plot)

    return filename_plot
