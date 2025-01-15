from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import RadioField, TextField, FileField


# Форма для загрузки изображения и выбора параметров.
class ImgForm(FlaskForm):
    # Кнопки-переключатели.
    choice_func = RadioField('Выберите функцию:',
                             choices=[('sin', 'sin'),
                                      ('cos', 'cos'),
                                      ('sin+cos', 'sin+cos')], default='sin')
                                      
    arg_func_value = TextField('Введите аргумент функции:', default=0.5)
    sin_frequency = TextField('Частота sin:', default=1.0)
    sin_phase = TextField('Фаза sin:', default=0.0)
    cos_frequency = TextField('Частота cos:', default=1.0)
    cos_phase = TextField('Фаза cos:', default=0.0)

    img = FileField('Загрузите изображение:',
                    validators=[FileRequired(),
                                FileAllowed(['jpg', 'jpeg', 'png'],
                                            'Только файлы изображений!')])
