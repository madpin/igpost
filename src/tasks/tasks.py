from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.db.db import engine
from src.db.model import Task  # Post,; Image,; Hashtag,; HashtagGroup,; Account,


def get_open_tasks():
    with Session(engine) as session:
        return (
            session.query(Task)
            .filter(Task.scheduled == True)
            .filter(Task.done == False)
            .filter(Task.has_giveup == False)
            .filter(Task.tries_todo >= Task.tries_done)
            .all()
        )


def set_task_done(task: Task, commit: bool = True):
    with Session(engine) as session:
        task.done = True
        session.add(task)
        if commit:
            session.commit()
    return True


def set_trying(task: Task, wait_time: int = 60, commit: bool = True):
    if task.trying == True and task.trying_dt <= datetime.utcnow() + timedelta(
        seconds=wait_time
    ):
        return False

    with Session(engine) as session:
        task.trying = 1
        task.trying_dt = datetime.utcnow()
        if commit:
            session.commit()

    return True


def set_task_failed(task: Task, commit: bool = True):
    with Session(engine) as session:
        task.tries_done = task.tries_done + 1
        if task.tries_done >= task.tries_todo:
            task.has_giveup = True
        if commit:
            session.commit()
    return True


def do_your_magic():
    tasks = get_open_tasks()
    for task in tasks:
        set_task_done(task)
