from flask import Blueprint, request, flash, redirect, url_for

from tracker import db
from tracker.daily_logs.forms import DailyLogForm
from tracker.daily_logs.models import Log
from tracker.utils import render

daily_logs = Blueprint("logs", __name__, url_prefix="/logs")
from tracker import app
from tracker.utils2 import get_or_initialize_config

config = get_or_initialize_config(app)


@daily_logs.route("/")
def logs():
    page = request.args.get("page", 1, type=int)
    logs = Log.query.order_by(Log.date.desc(), Log.id.desc()).paginate(
        page=page, per_page=10
    )
    RESOURCE_CHOICES = [
        (item["value"], item["label"])
        for item in config["task_form_configuration"]["RESOURCE_CHOICES"]
    ]
    return render("logs.html", logs=logs, RESOURCE_CHOICES=RESOURCE_CHOICES)


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
