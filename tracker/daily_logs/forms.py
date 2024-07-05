from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, TextAreaField, SubmitField, SelectField
from wtforms.validators import Optional

RESOURCE_CHOICES = [("None", ""), ("P", "Productive"), ("S", "Self")]


class DailyLogForm(FlaskForm):
    def __init__(self, incomplete_tasks, formdata=None, **kwargs):
        super(DailyLogForm, self).__init__(formdata=formdata, **kwargs)
        self.tasks.choices = [
            (f"{task.id}", f"{task.resource_type} - {task.name}")
            for task in incomplete_tasks
        ]

    tasks = SelectMultipleField("Tasks", validators=[Optional()])
    resource_type = SelectField(
        "Resource Type", choices=RESOURCE_CHOICES, validators=[Optional()]
    )
    explanation = TextAreaField("Explanation", validators=[Optional()])
    blockers = TextAreaField("Blockers", validators=[Optional()])
    submit = SubmitField("Log")
