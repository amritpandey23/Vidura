from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField


class SettingsForm(FlaskForm):
    config = TextAreaField("Site Settings")
    important_dates = TextAreaField("Important Dates")
    notes = TextAreaField("Notes")
    submit = SubmitField("Save")
