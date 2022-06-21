from django.forms import Form, FileField
from django.core.validators import FileExtensionValidator


class UploadFileForm(Form):
    file = FileField(label='файл', validators=[FileExtensionValidator(allowed_extensions=['xlsx', 'xls', 'csv'])])
