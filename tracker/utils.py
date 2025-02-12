from flask import render_template
from markdown2 import Markdown
from sqlalchemy import func
from sqlalchemy import func

from tracker.daily_logs.forms import DailyLogForm
from tracker.tasks.forms import TaskFilterForm, TaskForm
from tracker.tasks.models import Task
from tracker import app
from tracker.utils2 import initialize_app

config = initialize_app(app)
from tracker.utils2 import initialize_app

config = initialize_app(app)


def render(template_name, **args):
    markdowner = Markdown()
    daily_log_form = DailyLogForm(get_incomplete_tasks())
    task_filter_form = TaskFilterForm()
    task_form = TaskForm()
    return render_template(
        template_name,
        daily_log_form=daily_log_form,
        task_filter_form=task_filter_form,
        task_form=task_form,
        site_name=app.config["SITE_NAME"],
        markdowner=markdowner,
        **args,
    )


def get_incomplete_tasks():
    incomplete_high_priority_tasks = Task.query.filter(
        Task.progress_status != "Completed",
        Task.priority == "High",
        Task.progress_status != "Dropped",
    ).all()

    incomplete_medium_priority_tasks = Task.query.filter(
        Task.progress_status != "Completed",
        Task.priority == "Medium",
        Task.progress_status != "Dropped",
    ).all()

    incomplete_low_priority_tasks = Task.query.filter(
        Task.progress_status != "Completed",
        Task.priority == "Low",
        Task.progress_status != "Dropped",
    ).all()

    last_log_day_length = 7
    try:
        last_log_day_length = config["open_task_log_days"]
    except KeyError:
        last_log_day_length = 7

    last_week_closed_tasks = Task.query.filter(
        Task.progress_status != "Ongoing",
        Task.close_date.isnot(None),
        (
            func.julianday(func.date("now")) - func.julianday(Task.close_date)
            <= last_log_day_length
        ),
    ).all()

    # Combine incomplete tasks of different priorities
    incomplete_tasks = (
        incomplete_high_priority_tasks
        + incomplete_medium_priority_tasks
        + incomplete_low_priority_tasks
        + last_week_closed_tasks
        + last_week_closed_tasks
    )

    # tasks = incomplete_tasks
    tasks = sorted(
        incomplete_tasks, key=lambda task: task.date_of_allotment, reverse=True
    )

    return tasks
