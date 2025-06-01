from flask import Blueprint, request, flash, redirect, url_for, jsonify
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
    parent_id = task.parent_id
    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully", "success")
    
    # If it was a subtask, redirect back to the parent task view
    if parent_id:
        return redirect(url_for("tasks.view_task", task_id=parent_id))
    return redirect(url_for("home"))


@tasks.route("/edit/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    """Handle both modal and page edits"""
    task = Task.query.get_or_404(task_id)
    
    if request.method == "POST":
        form = TaskForm(request.form)
        if form.validate():
            parent_task_id = task.parent_id
            if parent_task_id is not None:
                parent_task = Task.query.get_or_404(parent_task_id)
                if parent_task.progress_status == "Completed":
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX request
                        return jsonify({'error': 'Cannot edit a task that is already completed.'}), 400
                    flash("Cannot edit a task that is already completed.", "danger")
                    return redirect(url_for("tasks.view_task", task_id=parent_task_id))
                elif (
                    parent_task.progress_status == "Not Started"
                    and form.progress_status.data != "Not Started"
                ):
                    parent_task.progress_status = "Ongoing"
                    db.session.commit()
            
            # Update task with form data
            form.populate_obj(task)
            try:
                db.session.commit()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX request
                    return jsonify({'message': 'Task updated successfully'})
                flash("Record updated successfully", "success")
            except Exception as e:
                db.session.rollback()
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX request
                    return jsonify({'error': str(e)}), 500
                flash("Error updating record in database", "danger")
            
            if not request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # Only redirect for non-AJAX requests
                back = request.args.get("back", url_for("tasks.view_task", task_id=task_id))
                return redirect(back)
            return jsonify({'message': 'Task updated successfully'})
        elif request.headers.get('X-Requested-With') == 'XMLHttpRequest':  # AJAX request with validation errors
            return jsonify({'error': 'Validation failed', 'errors': form.errors}), 400
    
    # GET request - render edit form page
    edit_task_form = TaskForm(obj=task)
    back = request.args.get("back", url_for("tasks.view_task", task_id=task_id))
    return render("edit_task.html", edit_task_form=edit_task_form, back=back)


@tasks.route("<int:task_id>")
def view_task(task_id):
    task = Task.query.get_or_404(task_id)
    form = TaskForm()
    return render("view_task.html", task=task, datetime=datetime, form=form)


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


@tasks.route("/category/<string:category>", methods=["GET"])
def get_tasks_by_category(category):
    """
    Fetch all tasks that belong to the specified category.
    """
    tasks = Task.query.filter_by(category=category).all()
    return render("all_tasks.html", tasks=tasks, datetime=datetime)


@tasks.route("/<int:task_id>/add_subtask", methods=["GET", "POST"])
def add_subtask(task_id):
    parent_task = Task.query.get_or_404(task_id)
    form = TaskForm()

    if form.validate_on_submit():
        subtask = Task(
            name=form.name.data,
            description=form.description.data,
            date_of_allotment=form.date_of_allotment.data,
            due_date=form.due_date.data,
            category=form.category.data,
            resource_type=form.resource_type.data,
            progress_status=form.progress_status.data,
            priority=form.priority.data,
            progress_counter=form.progress_counter.data,
            blockers=form.blockers.data,
            external_link=form.external_link.data,
            close_date=form.close_date.data,
            parent=parent_task,
        )
        db.session.add(subtask)
        db.session.commit()
        flash("Subtask added successfully!", "success")
        return redirect(url_for("tasks.view_task", task_id=task_id))

    return render("view_task.html", task=parent_task, form=form)


@tasks.route("<int:parent_task_id>/subtask/<int:subtask_id>/complete", methods=["GET"])
def mark_subtask_complete(parent_task_id, subtask_id):
    subtask = Task.query.get_or_404(subtask_id)
    if subtask.parent_id != parent_task_id:
        flash("Subtask does not belong to the specified parent task.", "danger")
        return redirect(url_for("tasks.view_task", task_id=parent_task_id))

    subtask.progress_status = "Completed"
    subtask.close_date = datetime.datetime.today()
    db.session.commit()
    flash("Subtask marked as completed!", "success")
    return redirect(url_for("tasks.view_task", task_id=parent_task_id))


@tasks.route(
    "<int:parent_task_id>/subtask/<int:subtask_id>/incomplete", methods=["GET"]
)
def mark_subtask_incomplete(parent_task_id, subtask_id):
    subtask = Task.query.get_or_404(subtask_id)
    if subtask.parent_id != parent_task_id:
        flash("Subtask does not belong to the specified parent task.", "danger")
        return redirect(url_for("tasks.view_task", task_id=parent_task_id))

    subtask.progress_status = "Not Started"
    subtask.close_date = None
    db.session.commit()
    flash("Subtask marked as incomplete!", "success")
    return redirect(url_for("tasks.view_task", task_id=parent_task_id))


# Add these routes to your existing tasks.py file


@tasks.route(
    "<int:parent_task_id>/subtask/<int:subtask_id>/update_progress", methods=["POST"]
)
def update_subtask_progress(parent_task_id, subtask_id):
    """Update the progress status of a subtask via dropdown"""
    subtask = Task.query.get_or_404(subtask_id)
    if subtask.parent_id != parent_task_id:
        flash("Subtask does not belong to the specified parent task.", "danger")
        return redirect(url_for("tasks.view_task", task_id=parent_task_id))

    new_progress_status = request.form.get("progress_status")

    # Validate the progress status
    valid_statuses = ["Not Started", "Ongoing", "Completed", "Dropped"]
    if new_progress_status not in valid_statuses:
        flash("Invalid progress status.", "danger")
        return redirect(url_for("tasks.view_task", task_id=parent_task_id))

    # Update the subtask
    subtask.progress_status = new_progress_status

    # Set close_date when marking as completed
    if new_progress_status == "Completed":
        subtask.close_date = datetime.datetime.today()
    elif new_progress_status in ["Not Started", "Ongoing", "Dropped"]:
        # Clear close_date if marking as not completed
        subtask.close_date = None

    try:
        db.session.commit()
        flash(f"Subtask progress updated to '{new_progress_status}'!", "success")
    except Exception as e:
        db.session.rollback()
        flash("Error updating subtask progress.", "danger")

    return redirect(url_for("tasks.view_task", task_id=parent_task_id))


@tasks.route("<int:parent_task_id>/subtask/<int:subtask_id>/archive", methods=["GET"])
def archive_subtask(parent_task_id, subtask_id):
    """Archive or unarchive a subtask"""
    subtask = Task.query.get_or_404(subtask_id)
    if subtask.parent_id != parent_task_id:
        flash("Subtask does not belong to the specified parent task.", "danger")
        return redirect(url_for("tasks.view_task", task_id=parent_task_id))

    # Toggle the archive status
    subtask.archive_status = not subtask.archive_status
    action = "archived" if subtask.archive_status else "unarchived"

    try:
        db.session.commit()
        flash(f"Subtask has been {action} successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error {action} subtask.", "danger")

    return redirect(url_for("tasks.view_task", task_id=parent_task_id))


@tasks.route("/get_subtask/<int:subtask_id>")
def get_subtask(subtask_id):
    """Get subtask data for editing in modal"""
    subtask = Task.query.get_or_404(subtask_id)
    return jsonify({
        'name': subtask.name,
        'description': subtask.description,
        'date_of_allotment': subtask.date_of_allotment.strftime('%Y-%m-%d'),
        'due_date': subtask.due_date.strftime('%Y-%m-%d') if subtask.due_date else '',
        'category': subtask.category,
        'resource_type': subtask.resource_type,
        'progress_status': subtask.progress_status,
        'priority': subtask.priority,
        'progress_counter': subtask.progress_counter,
        'blockers': subtask.blockers,
        'external_link': subtask.external_link,
        'close_date': subtask.close_date.strftime('%Y-%m-%d') if subtask.close_date else ''
    })
