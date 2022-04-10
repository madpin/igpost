# from email.policy import default
import pprint

# import time
import os
import uuid

import click

from src.db import db
from src.db import model
from src.lib import credentials
from src.lib import images
from src.lib import instagram
from src.lib import posts
from src.lib.tasks import do_your_magic, get_open_tasks

pp = pprint.PrettyPrinter(indent=4)

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


@click.group()
@click.pass_context
@click.option("--debug/--no-debug", default=False)
def cli(ctx, debug):
    ctx.ensure_object(dict)

    ctx.obj["DEBUG"] = debug


menu_obj = [
    {
        "key": "Ig",
        "summary": "Post a photo to Instagram1",
        "func": lambda: print("This is a test function1"),
        "menu": [
            {
                "summary": "Post a photo to Instagram",
                "func": lambda: print("photo to Instagram"),
            },
            {
                "key": "Text 2",
                "summary": "Get a followers snapshot",
                "func": lambda: print("followers snapshot"),
            },
        ],
    },
    {
        "key": "Tasks",
        "summary": "Schedule tasks",
        # "func": lambda: print("This is another test function"),
        "menu": [
            {
                "summary": "Post a photo to Instagram",
                "func": lambda: print("photo to Instagram"),
            },
            {
                "summary": "Get a followers snapshot",
                "func": lambda: print("followers snapshot"),
            },
            {
                "summary": "Playground",
                "func": lambda: print(do_your_magic()),
            },
        ],
    },
    {
        "key": "Tests",
        "summary": "Test Tasks",
        # "func": lambda: print("This is another test function"),
        "menu": [
            {
                "summary": "Test Ig Account Login",
                "func": lambda: print("photo to Instagram"),
            },
            {
                "summary": "Test scheduled images path",
                "func": lambda: print("followers snapshot"),
            },
        ],
    },
    {
        "key": "Db",
        "summary": "Tests with files/account",
        "func": lambda: print("This is another test function"),
        "menu": [
            {
                "summary": "Create DB",
                "func": db.create_db,
                # "func_args": ["db_file": "$(HOME)/.igpost/igpost.db"],
            },
            {
                "summary": "Upgrade DB",
                "func": db.upgrade_db,
            },
        ],
    },
    {
        "key": "Image/Post",
        "summary": "Operations related to Image/Post",
        "func": lambda: print("This is another test function"),
        "menu": [
            {
                "summary": "List Images",
                "func": lambda: print("List Images"),
                # "func_args": ["db_file": "$(HOME)/.igpost/igpost.db"],
            },
            {
                "summary": "Insert Image",
                "func": lambda: print("Insert Image"),
                # "func_args": ["db_file": "$(HOME)/.igpost/igpost.db"],
            },
            {
                "summary": "Process Image",
                "func": lambda: print("Process Image"),
                # "func_args": ["db_file": "$(HOME)/.igpost/igpost.db"],
            },
            {
                "summary": "Process Unprocessed",
                "func": images.process_unprocessed,
                # "func_args": ["db_file": "$(HOME)/.igpost/igpost.db"],
            },
        ],
    },
    {
        "key": "Setup",
        "summary": "Setup and configure your account",
        # 'func': _menu_config,
        "menu": [
            {
                "summary": "Setup Account",
                "func": lambda: print("This is a test function"),
            },
            {
                "summary": "This is another summary",
                "func": lambda: print("This is another test function"),
            },
        ],
    },
]


@cli.command()
@click.pass_context
@click.argument("p1", required=False)
@click.argument("p2", required=False)
@click.argument("p3", required=False)
def menu(ctx, p1=None, p2=None, p3=None):
    cur_menu = menu_obj
    for p in [p1, p2, p3]:
        if p is not None:
            ob = cur_menu[int(p) - 1]
            if "func" in ob:
                ob["func"](**ob.get("func_args", {}))
            if "menu" in ob:
                cur_menu = ob["menu"]
            else:
                return True
        else:
            break

    return _menu(cur_menu)


def _menu(menu_obj):
    click.clear()
    if len(menu_obj) == 0:
        return
    # print(menu_obj)

    for i, obj in enumerate(menu_obj):
        key = obj.get("key", None)
        i += 1
        if key is None or len(key) == 0 or key[:4] == "None":
            click.echo(f"{i}: {obj['summary']}")
        else:
            click.echo(f"{i}: {key} - {obj['summary']}")

    while True:
        try:
            click_char = int(click.getchar())
            break
        except (ValueError, TypeError):
            click.echo("Invalid input")

    current_item = menu_obj[click_char - 1]

    if "func" in current_item:
        current_item["func"](**current_item.get("func_args", {}))
    if "menu" in current_item:
        _menu(current_item["menu"])


# @cli.command()
# @click.pass_context
# def menu_config(ctx):
#     # print(menu_obj['Config'])
#     # return _menu(menu_obj["Config"]["menu"])
#     pass


@cli.group("ig")
def g_ig():
    pass


@cli.group("scheduler")
def g_scheduler():
    pass


@cli.group("tests")
def g_tests():
    pass


@cli.group("post_image")
def g_post_image():
    pass


@cli.group("playground")
def g_play():
    pass


# @cli.group("config")
# def g_play():
#     pass


@g_ig.command()
# @click.argument("filename")
def set_pw():
    raise NotImplementedError()
    # credentials.save_ig_cred("madpin", "password")


@g_ig.command()
@click.option("--username", "-u", required=True)
# @click.option("--password", "-p", required=True)
def get_pw(username):
    passw = credentials.get_ig_cred(username)
    print(passw)
    print("final")


@g_ig.command()
@click.option("--post_id", "-p", required=True)
@click.option("--username", "-u", required=True)
# @click.option("--password", "-p", required=True)
def publish(post_id, username):
    media_info = instagram.publish(post_id=post_id, username=username)
    print(media_info)


@g_ig.command()
@click.option("--post_id", "-p", required=True)
def demo_publish(post_id):
    with db.Session() as session:
        post = session.query(model.Post).filter(model.Post.id == post_id).first()

        for image in post.images:
            click.echo(images.image_chars(image.original_filepath))
        click.echo(post.title)
        click.echo(post.text)
        click.echo('\n'.join(posts.get_comments(post)))


@g_post_image.command()
@click.argument("filename", required=False)
def create_image(filename=None):
    if filename is None:
        filename = click.prompt("Please the image Filename")
        filename = filename.strip("'")

    if not os.path.exists(filename):
        click.echo(f"File {filename} does not exist")
        return

    img = images.create_image(filename)


@g_post_image.command()
@click.option("--filename", "-f", required=True)
@click.option("--title", "-t", required=True)
@click.option("--post_txt", "-p", default=None, show_default=True)
@click.option("--location", "-l", default="Dublin, Ireland", show_default=True)
@click.option("--username", "-u", default="madindub", show_default=True)
def create_post_image(filename, title, post_txt, location, username):
    if filename is None:
        filename = click.prompt("Please the image Filename")
        filename = filename.strip("'")

    if not os.path.exists(filename):
        click.echo(f"File {filename} does not exist")
        return

    if title is None:
        title = click.prompt("Please enter the title")
    # if post_txt is None:
    #     post_txt = click.prompt("Please enter the post content")

    posts.create_default_post(
        image_path=filename,
        title=title,
        post_txt=post_txt,
        location=location,
        username=username,
    )


# @cli1_5.command()
# @click.argument("filename")
# def create_image(filename):
#     img = image.create_image(filename)


@g_play.command()
@click.argument("filename")
def exif_info(filename):
    exif_data = images.exif_info(filename)
    pp.pprint(exif_data)


@g_play.command()
# @click.argument("filename")
def print_in_console():
    images = images.get_all_images()
    print(len(images))
    from prettytable import PrettyTable

    COLUMNS_NUM = 6

    t = PrettyTable(f"Column {i+1}" for i in range(COLUMNS_NUM))

    arr = []
    for i, img in enumerate(images):
        if img.notes is None:
            bitmap = images.image_chars(img.original_filepath)
            images.save_bitmap(img, bitmap)
        else:
            bitmap = img.notes
        arr.append(f"Image Id: {img.id}\n" + bitmap)
        if (i + 1) % COLUMNS_NUM == 0 and len(arr) > 0:
            t.add_row(arr)
            arr = []
    if len(arr) > 0:
        t.add_row(arr + [""] * (COLUMNS_NUM - len(arr)))
    print(t)
