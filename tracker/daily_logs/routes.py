from io import BytesIO
from datetime import datetime, timedelta

from flask import Blueprint, request, flash, redirect, url_for, jsonify, send_file

from tracker import db
from tracker.daily_logs.forms import DailyLogForm, LogsCompilationForm
from tracker.daily_logs.models import Log
from tracker.utils import render
from tracker.tasks.models import Task

daily_logs = Blueprint("logs", __name__, url_prefix="/logs")
from tracker import app
from tracker.utils2 import get_or_initialize_config

config = get_or_initialize_config(app)


@daily_logs.route("/")
def logs():
    logs_compilation_form = LogsCompilationForm()

    page = request.args.get("page", 1, type=int)
    logs = Log.query.order_by(Log.date.desc(), Log.id.desc()).paginate(
        page=page, per_page=10
    )
    RESOURCE_CHOICES = [
        (item["value"], item["label"])
        for item in config["task_form_configuration"]["RESOURCE_CHOICES"]
    ]
    return render(
        "logs.html",
        logs_compilation_form=logs_compilation_form,
        logs=logs,
        RESOURCE_CHOICES=RESOURCE_CHOICES,
    )


@daily_logs.route("/add_log", methods=["POST"])
def add_log():
    form = DailyLogForm([], request.form)
    if form.submit():
        selected_tasks = form.tasks.data
        task_ids = ",".join(selected_tasks)
        log = Log(
            resource_type=form.resource_type.data,
            task_ids=task_ids,
            explanation=form.explanation.data,
            blockers=form.blockers.data,
            date=form.log_date.data,
        )
        try:
            db.session.add(log)
            db.session.commit()
        except Exception as e:
            print(e)
            flash("Error while adding data to database", "danger")
        finally:
            flash("Log entry added successfully.", "success")
    return redirect(url_for("logs.logs"))


@daily_logs.route("/delete_log/<int:log_id>", methods=["GET"])
def delete_log(log_id):
    log = Log.query.get_or_404(log_id)
    db.session.delete(log)
    db.session.commit()
    flash("Log Deleted successfully", "success")
    return redirect(url_for("logs.logs"))


@daily_logs.route("/compile_logs", methods=["GET", "POST"])
def compile_logs():
    form = LogsCompilationForm()
    if form.validate_on_submit():
        start_date = form.start_date.data
        end_date = form.end_date.data

    if start_date > end_date:
        flash("Start date cannot be after end date.", "danger")
        return redirect(url_for("logs.download_logs"))

    logs = (
        Log.query.filter(Log.date.between(start_date, end_date))
        .order_by(Log.date.desc(), Log.id.desc())
        .all()
    )

    output = BytesIO()
    output.write(f"# Logs between {start_date} and {end_date}\n\n".encode("utf-8"))
    for single_date in (
        start_date + timedelta(n) for n in range((end_date - start_date).days + 1)
    ):
        date_logs = [log for log in logs if log.date == single_date]
        if date_logs:
            output.write(f"## {single_date}\n".encode("utf-8"))
            for log in date_logs:
                output.write("### Activity\n".encode("utf-8"))
                output.write(f"{log.explanation}\n".encode("utf-8"))
                output.write("### Blocker\n".encode("utf-8"))
                output.write(f"{log.blockers}\n".encode("utf-8"))
                output.write("### Related Tasks\n".encode("utf-8"))
                task_ids = log.task_ids.split(";")
                tasks = Task.query.filter(Task.id.in_(task_ids)).all()
                task_names = [task.name for task in tasks]
                output.write(f"{', '.join(task_names)}\n\n".encode("utf-8"))

    output.seek(0)

    return send_file(
        output,
        mimetype="text/plain",
        as_attachment=True,
        download_name=f"log_activity-{start_date}-{end_date}.md",
    )
