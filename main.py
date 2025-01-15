import os

from flask import Flask, render_template

from ImgForm import ImgForm
from funcs import processing_of_img, to_create_plot, secure_filename

app = Flask(__name__)

# Используем CSRF-токен.
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY


# Декоратор для вывода страницы по умолчанию (главной страницы).
@app.route("/")
def index():
    # Передаем данные в шаблон и вызываем его.
    return render_template('index.html')


# Декоратор для вывода страницы загрузки изображения.
@app.route('/run_app', methods=['GET', 'POST'])
def run_app():
    # Форма.
    form = ImgForm()
    if form.validate_on_submit():
        # Получаем имя файла-изображения.
        filename_img = os.path.join(r'./static/images',
                                 secure_filename(form.img.data.filename))
        print(filename_img)
        # Сохраняем первый файл-изображение на сервере.
        form.img.data.save(filename_img)

        # Производим обработку изображения по указанным опциям.
        filename_img_done = processing_of_img(filename_img, form.choice_func.data,
                                              form.arg_func_value.data)

        # Создаём график распределения цветов для исходного изображения.
        filename_img_plot = to_create_plot(filename_img)
        # Создаём график распределения цветов для полученного изображения.
        filename_img_done_plot = to_create_plot(filename_img_done)

        # Передаём переменные в шаблон.
        return render_template('result.html',
                               img=filename_img,
                               img_done=filename_img_done,
                               img_plot=filename_img_plot,
                               img_done_plot=filename_img_done_plot,
                               )
    else:
        return render_template('form.html', form=form, result=u'Загрузите файл-изображение!')


# Запуск.
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5003, debug=False)
