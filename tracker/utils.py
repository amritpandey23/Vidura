import os, json
from flask import render_template

from tracker.daily_logs.forms import DailyLogForm
from tracker.tasks.forms import TaskFilterForm, TaskForm
from tracker.tasks.models import Task
from tracker import app


def render(template_name, **args):
    daily_log_form = DailyLogForm(get_incomplete_tasks())
    task_filter_form = TaskFilterForm()
    task_form = TaskForm()
    return render_template(
        template_name,
        daily_log_form=daily_log_form,
        task_filter_form=task_filter_form,
        task_form=task_form,
        site_name=app.config["SITE_NAME"],
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

    # Combine incomplete tasks of different priorities
    incomplete_tasks = (
        incomplete_high_priority_tasks
        + incomplete_medium_priority_tasks
        + incomplete_low_priority_tasks
    )

    # tasks = incomplete_tasks
    tasks = sorted(
        incomplete_tasks, key=lambda task: task.date_of_allotment, reverse=True
    )

    return tasks
