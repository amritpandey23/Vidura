from datetime import date
from flask_wtf import FlaskForm
from wtforms import (
    SelectMultipleField,
    TextAreaField,
    SubmitField,
    SelectField,
    DateField,
)
from wtforms.validators import Optional, DataRequired
from flask_pagedown.fields import PageDownField

from tracker import app
from tracker.utils2 import get_or_initialize_config

config = get_or_initialize_config(app)

RESOURCE_CHOICES = [
    (item["value"], item["label"])
    for item in config["task_form_configuration"]["RESOURCE_CHOICES"]
]


class DailyLogForm(FlaskForm):
    def __init__(self, incomplete_tasks, formdata=None, **kwargs):
        super(DailyLogForm, self).__init__(formdata=formdata, **kwargs)
        self.tasks.choices = [
            (f"{task.id}", f"{task.resource_type} - {task.name}")
            for task in incomplete_tasks
        ]

    log_date = DateField("Log Date", validators=[Optional()])
    tasks = SelectMultipleField("Tasks", validators=[Optional()])
    resource_type = SelectField(
        "Resource Type", choices=RESOURCE_CHOICES, validators=[Optional()]
    )
    explanation = PageDownField("Explanation", validators=[DataRequired()])
    blockers = PageDownField("Blockers", validators=[Optional()])
    submit = SubmitField("Log")


class LogsCompilationForm(FlaskForm):
    start_date = DateField(
        "Start Date", validators=[DataRequired()], default=date.today, format="%Y-%m-%d"
    )
    end_date = DateField(
        "End Date", validators=[DataRequired()], default=date.today, format="%Y-%m-%d"
    )
    submit = SubmitField("Compile")
