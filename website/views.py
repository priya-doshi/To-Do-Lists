from flask import Blueprint, render_template, request, flash, jsonify, redirect
from flask_login import login_required, current_user
from .models import Todo
from . import db
import json

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    allTodo = Todo.query.all()
    return render_template("home.html", allTodo=allTodo, user=current_user)


@views.route('/todo_form', methods=['GET', 'POST'])
@login_required
def todo_form():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        status = request.form['status']
        todo = Todo(title=title, desc=desc, status=status,
                    user_id=current_user.id)
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    allTodo = Todo.query.all()

    return render_template("todo_form.html", allTodo=allTodo, user=current_user)


@views.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        status = request.form['status']
        todo = Todo.query.filter_by(id=id).first()
        todo.title = title
        todo.desc = desc
        todo.status = status
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(id=id).first()
    return render_template('update.html', user=current_user, todo=todo)


@views.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = Todo.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")
