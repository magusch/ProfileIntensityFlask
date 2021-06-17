from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, HiddenField
from flask_wtf.file import FileField,  FileAllowed


class UploadForm(FlaskForm):
    samplename = StringField('Название образца', default='Образец')
    filename = FileField(label='Изображение')


class DownloadFile(FlaskForm):
    limit = FloatField('Значение предела', default='1.0')