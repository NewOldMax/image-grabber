from flask.ext.wtf import Form
from wtforms import TextField, IntegerField, validators
from wtforms.validators import Required

class GrabberForm(Form):
    site_url = TextField('Url:', [validators.Required(), validators.URL()])
    image_count = IntegerField('Count to grab:', [validators.Required(), validators.NumberRange(1, 100)], default=5)