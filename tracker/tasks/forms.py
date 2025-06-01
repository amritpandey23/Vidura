from datetime import date
from flask_wtf import FlaskForm
from wtforms import (
    TextAreaField,
    StringField,
    SelectField,
    SelectMultipleField,
    SubmitField,
    DateField,
    IntegerField,
    MultipleFileField,
)
from flask_pagedown.fields import PageDownField
from wtforms.validators import Optional, DataRequired, Length, URL
from flask_wtf.file import FileField, FileAllowed

from tracker import app

from tracker.utils2 import get_or_initialize_config

config = get_or_initialize_config(app)

RESOURCE_CHOICES = [
    (item["value"], item["label"])
    for item in config["task_form_configuration"]["RESOURCE_CHOICES"]
]
CATEGORY_CHOICES = [
    (item["value"], item["label"])
    for item in config["task_form_configuration"]["CATEGORY_CHOICES"]
]
PROGRESS_CHOICES = [
    (item["value"], item["label"])
    for item in config["task_form_configuration"]["PROGRESS_CHOICES"]
]
PRIORITY_CHOICES = [
    (item["value"], item["label"])
    for item in config["task_form_configuration"]["PRIORITY_CHOICES"]
]


def get_default_value(choices):
    for item in choices:
        if item.get("default") == "true":
            return item["value"]
    return None


RESOURCE_DEFAULT = get_default_value(
    config["task_form_configuration"]["RESOURCE_CHOICES"]
)
CATEGORY_DEFAULT = get_default_value(
    config["task_form_configuration"]["CATEGORY_CHOICES"]
)
PROGRESS_DEFAULT = get_default_value(
    config["task_form_configuration"]["PROGRESS_CHOICES"]
)
PRIORITY_DEFAULT = get_default_value(
    config["task_form_configuration"]["PRIORITY_CHOICES"]
)


class TaskForm(FlaskForm):
    name = StringField("Title", validators=[DataRequired(), Length(max=120)])
    description = PageDownField("Description")

    date_of_allotment = DateField(
        "Date of Allotment", default=date.today, validators=[DataRequired()]
    )
    due_date = DateField("Due Date", validators=[Optional()])

    category = SelectField(
        "Category",
        choices=CATEGORY_CHOICES,
        default=CATEGORY_DEFAULT,
        validators=[DataRequired()],
    )

    resource_type = SelectField(
        "Resource Type",
        choices=RESOURCE_CHOICES,
        default=RESOURCE_DEFAULT,
        validators=[DataRequired()],
    )

    progress_status = SelectField(
        "Progress Status",
        choices=PROGRESS_CHOICES,
        default=PROGRESS_DEFAULT,
        validators=[DataRequired()],
    )

    priority = SelectField(
        "Priority",
        choices=PRIORITY_CHOICES,
        default=PRIORITY_DEFAULT,
        validators=[DataRequired()],
    )

    progress_counter = IntegerField("Progress", validators=[DataRequired()], default=1)

    blockers = TextAreaField("Blockers")
    external_link = TextAreaField("External Link")
    attachment = MultipleFileField('Attachments', validators=[
        Optional(),
        FileAllowed(['pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx', 'txt'], 'Only PDF, images, documents and text files are allowed!')
    ])

    close_date = DateField("Close Date", validators=[Optional()])

    submit = SubmitField("Add")


class TaskFilterForm(FlaskForm):
    resource_type = SelectField(
        "Resource Type", choices=RESOURCE_CHOICES, validators=[DataRequired()]
    )

    category = SelectMultipleField(
        "Category", choices=CATEGORY_CHOICES, validators=[Optional()]
    )

    priority = SelectMultipleField(
        "Priority", choices=PRIORITY_CHOICES, validators=[Optional()]
    )

    progress_status = SelectMultipleField(
        "Progress Status", choices=PROGRESS_CHOICES, validators=[Optional()]
    )

    date_of_allotment_start = DateField(
        "Date of Allotment Start", validators=[Optional()]
    )
    date_of_allotment_end = DateField("Date of Allotment End", validators=[Optional()])

    due_date_start = DateField("Due Date", validators=[Optional()])
    due_date_end = DateField("Due Date", validators=[Optional()])

    close_date_start = DateField("Closing Date Start", validators=[Optional()])
    close_date_end = DateField("Closing Date End", validators=[Optional()])

    submit = SubmitField("Apply")
