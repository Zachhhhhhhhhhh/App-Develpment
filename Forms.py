from wtforms import Form, StringField, TextAreaField, validators, TimeField, SubmitField, RadioField, IntegerField
from flask_wtf.file import FileField, FileRequired, FileAllowed


class CreateServiceForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    availability = RadioField('Availability', choices=[('Available', 'Available'), ('Unavailable', 'Unavailable')],
                            default='A')


class CreateCarserviceForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=150), validators.DataRequired()])
    description = TextAreaField('Description', [validators.DataRequired()])
    location = TextAreaField('Location')
    hotline = TextAreaField('Hotline', [validators.DataRequired()])
    starting_hour = TimeField('Starting hour')
    ending_hour = TimeField('Ending hour')
    opening_days = StringField('Opening days', [validators.DataRequired()])
    availability = RadioField('Availability', choices=[('Available', 'Available'), ('Unavailable', 'Unavailable')],
                    default='A')
