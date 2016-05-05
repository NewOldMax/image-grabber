from flask.ext.wtf import Form
from wtforms import TextField, IntegerField, SelectField, validators
from wtforms.validators import Required

class GrabberForm(Form):
    site_url = TextField('Url:', [validators.Required(), validators.URL()])
    image_count = IntegerField('Count to grab:', [validators.Required(), validators.NumberRange(1, 100)], default=5)
    work_type = SelectField('Work type:', choices=[('single', 'Single page'), ('crawler', 'Web Crawler (beta)')])
    image_type = SelectField('Image type:', choices=[('all', 'All'), ('image/gif', 'GIF'), ('image/jpeg', 'JPEG'), ('image/png', 'PNG'), ('image/svg+xml', 'SVG'), ('image/tiff', 'TIFF'), ('image/vnd.microsoft.icon', 'ICO'), ('image/vnd.wap.wbmp', 'WBMP'), ('image/bmp', 'BMP')])