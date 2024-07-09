from flask import Blueprint, request, flash, redirect, url_for
import datetime
from tracker.tasks.forms import TaskForm, TaskFilterForm
from tracker.tasks.models import Task
from sqlalchemy import or_, desc
from tracker import db
from tracker.utils import render

tasks = Blueprint("tasks", __name__, url_prefix="/tasks")


@tasks.route("/add", methods=["POST"])
def add_task():
    form = TaskForm(request.form)
    if form.validate():
        task = Task(
            name=form.name.data,
            description=form.description.data,
            date_of_allotment=form.date_of_allotment.data,
            due_date=form.due_date.data,
            category=form.category.data,
            resource_type=form.resource_type.data,
            progress_status=form.progress_status.data,
            priority=form.priority.data,
            blockers=form.blockers.data,
            external_link=form.external_link.data,
            progress_counter=form.progress_counter.data,
            close_date=form.close_date.data,
        )
        try:
            db.session.add(task)
            db.session.commit()
        except Exception as e:
            flash("Problems adding task to db", "danger")
        finally:
            flash("Task successfully added", "success")
    else:
        flash("Validating Task failed", "warning")
    return redirect(url_for("home"))


@tasks.route("/delete/<int:task_id>", methods=["GET", "POST"])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully", "success")
    return redirect(url_for("home"))


@tasks.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    task = Task.query.get_or_404(task_id)
    back = url_for("home")

    if request.args.get("back"):
        back = request.args.get("back")

    edit_task_form = TaskForm(obj=task)

    if edit_task_form.validate_on_submit():
        edit_task_form.populate_obj(task)
        try:
            db.session.commit()
        except Exception as e:
            flash("Error updating record in database", "danger")
        finally:
            flash("Record updated successfully", "success")
            return redirect(url_for("home"))
    return render("edit_task.html", edit_task_form=edit_task_form, back=back)


@tasks.route("/task/<int:task_id>")
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    return render("view_task.html", task=task, datetime=datetime)


@tasks.route("/filter", methods=["POST"])
def filter_tasks():
    form = TaskFilterForm(request.form)
    if form.validate_on_submit():
        categories_string = ""
        priorities_string = ""
        progress_status_string = ""
        resource_type = form.resource_type.data
        categories = form.category.data
        if categories != ["None"]:
            categories_string = ";".join(categories)
        priorities = form.priority.data
        if priorities != ["None"]:
            priorities_string = ";".join(priorities)
        progress_status = form.progress_status.data
        if progress_status != ["None"]:
            progress_status_string = ";".join(progress_status)
        date_of_allotment_start = form.date_of_allotment_start.data
        date_of_allotment_end = form.date_of_allotment_end.data
        due_date_start = form.due_date_start.data
        due_date_end = form.due_date_end.data
        close_date_start = form.close_date_start.data
        close_date_end = form.close_date_end.data
        return redirect(
            url_for(
                "tasks.all_tasks",
                filter="true",
                resource_type=resource_type,
                categories=categories_string,
                priorities=priorities_string,
                progress_status=progress_status_string,
                date_of_allotment_end=date_of_allotment_end,
                date_of_allotment_start=date_of_allotment_start,
                due_date_start=due_date_start,
                due_date_end=due_date_end,
                close_date_start=close_date_start,
                close_date_end=close_date_end,
            )
        )
    return redirect(url_for("home", back=request.path))


@tasks.route("/", methods=["GET", "POST"])
def all_tasks():

    # Searching tasks
    query = request.args.get("query")

    if query:
        tasks = Task.query.filter(Task.name.ilike(f"%{query}%")).all()
        return render(
            "all_tasks.html", tasks=tasks, datetime=datetime, search_term=query
        )

    page = request.args.get("page", 1, type=int)
    per_page = 15

    filter = request.args.get("filter")
    if filter != None:
        resource_type = request.args.get("resource_type")
        categories = request.args.get("categories")
        priorities = request.args.get("priorities")
        progress_status = request.args.get("progress_status")
        date_of_allotment_start = request.args.get("date_of_allotment_start")
        date_of_allotment_end = request.args.get("date_of_allotment_end")
        due_date_start = request.args.get("due_date_start")
        due_date_end = request.args.get("due_date_end")
        close_date_start = request.args.get("close_date_start")
        close_date_end = request.args.get("close_date_end")

        query = Task.query.filter(Task.archive_status == False)
        if resource_type != "None" and resource_type != "":
            query = query.filter(Task.resource_type == resource_type)
        if categories != "":
            categories = categories.split(";")
            query = query.filter(Task.category.in_(categories))
        if priorities != "":
            priorities = priorities.split(";")
            query = query.filter(Task.priority.in_(priorities))
        if progress_status != "":
            progress_status = progress_status.split(";")
            query = query.filter(Task.progress_status.in_(progress_status))
        if date_of_allotment_start and date_of_allotment_end:
            query = query.filter(Task.date_of_allotment >= date_of_allotment_start)
            query = query.filter(Task.date_of_allotment <= date_of_allotment_end)
        if due_date_start and due_date_end:
            query = query.filter(
                or_(Task.due_date == None, Task.due_date >= due_date_start)
            )
            query = query.filter(
                or_(Task.due_date == None, Task.due_date <= due_date_end)
            )
        if close_date_start and close_date_end:
            query = query.filter(
                or_(Task.close_date == None, Task.close_date >= close_date_start)
            )
            query = query.filter(
                or_(Task.close_date == None, Task.close_date <= close_date_end)
            )

        tasks = query.order_by(Task.date_of_allotment.desc())
    else:
        tasks = Task.query.order_by(Task.date_of_allotment.desc())
        tasks = tasks.paginate(page=page, per_page=per_page)

    return render("all_tasks.html", tasks=tasks, datetime=datetime)
