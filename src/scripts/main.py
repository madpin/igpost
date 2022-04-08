import time

import click
import keyring
import climage

from src.db import db
from src.photo import image
import pprint

pp = pprint.PrettyPrinter(indent=4)


@click.group()
@click.pass_context
@click.option("--debug/--no-debug", default=False)
def cli(ctx, debug):
    ctx.ensure_object(dict)

    ctx.obj["DEBUG"] = debug


# menu_obj = {
#     "Ig": {
#         "summary": "Post a photo to Instagram1",
#         "func": lambda: print("This is a test function1"),
#         "menu": {
#             "1": {
#                 "summary": "Post a photo to Instagram",
#                 "func": lambda: print("photo to Instagram"),
#             },
#             "Text 2": {
#                 "summary": "Get a followers snapshot",
#                 "func": lambda: print("followers snapshot"),
#             },
#         },
#     },
#     "Scheduler": {
#         "summary": "Schedule tasks",
#         "func": lambda: print("This is another test function"),
#         "menu": {
#             "": {
#                 "summary": "Post a photo to Instagram",
#                 "func": lambda: print("photo to Instagram"),
#             },
#             "Text 2": {
#                 "summary": "Get a followers snapshot",
#                 "func": lambda: print("followers snapshot"),
#             },
#         },
#     },
#     "Tests": {
#         "summary": "Test Tasks",
#         "func": lambda: print("This is another test function"),
#         "menu": {
#             "": {
#                 "summary": "Test Ig Account Login",
#                 "func": lambda: print("photo to Instagram"),
#             },
#             "Text 2": {
#                 "summary": "Test scheduled images path",
#                 "func": lambda: print("followers snapshot"),
#             },
#         },
#     },
#     "Playground": {
#         "summary": "Tests with files/account",
#         # "func": lambda: print("This is another test function"),
#         "menu": {
#             "None1": {
#                 "summary": "Create DB",
#                 "func": db.create_db,
#                 # "func_args": {"db_file": "$(HOME)/.igpost/igpost.db"},
#             },
#             "None2": {
#                 "summary": "Upgrade DB",
#                 "func": db.upgrade_db,
#             },
#         },
#     },
#     "Config": {
#         "summary": "Setup and configure your account",
#         # 'func': _menu_config,
#         "menu": {
#             "Ig Account": {
#                 "summary": "Setup Account",
#                 "func": lambda: print("This is a test function"),
#             },
#             "Text 2": {
#                 "summary": "This is another summary",
#                 "func": lambda: print("This is another test function"),
#             },
#         },
#     },
# }

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
        "func": lambda: print("This is another test function"),
        "menu": [
            {
                "summary": "Post a photo to Instagram",
                "func": lambda: print("photo to Instagram"),
            },
            {
                "summary": "Get a followers snapshot",
                "func": lambda: print("followers snapshot"),
            },
        ],
    },
    {
        "key": "Tests",
        "summary": "Test Tasks",
        "func": lambda: print("This is another test function"),
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
        "key": "Text 2",
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
        print(len(cur_menu))
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


@cli.command()
@click.pass_context
def menu_config(ctx):
    # print(menu_obj['Config'])
    # return _menu(menu_obj["Config"]["menu"])
    pass


@cli.group("ig")
def cli1_1():
    pass


@cli.group("scheduler")
def cli1_2():
    pass


@cli.group("tests")
def cli1_3():
    pass


@cli.group("playground")
def cli1_4():
    pass


@cli.group("config")
def cli1_5():
    pass


@cli1_4.command()
@click.argument("filename")
def exif_info(filename):
    exif_data = image.exif_info(filename)
    pp.pprint(exif_data)


@cli1_4.command()
@click.argument("filename")
def print_in_console(filename):

    # converts the image to print in terminal
    # inform of ANSI Escape codes
    output = climage.convert(filename)
    print(output)


# @g1_2.command()
# def menu_test():
#     obj = {
#         'Text 1': {
#             'summary': 'This is a summary',
#             'func': lambda: print('This is a test function')
#         },
#         'Text 2': {
#             'summary': 'This is another summary',
#             'func': lambda: print('This is another test function')
#         },
#     }

#     for i, (key, value) in enumerate(obj.items()):
#         i += 1
#         click.echo(f"{i}: {key} - {value['summary']}")
#     c1 = int(click.getchar())
#     # click.echo(list(obj.items())[c1-1])
#     click.echo(list(obj.values())[c1-1]['func']())


# @g1_2.command()
# def get_keyring():
#     print("Keyring method: " + str(keyring.get_keyring()))


# @g1_2.command()
# def set_password():
#     # the service is just a namespace for your app
#     service_id = 'IM_YOUR_APP!'

#     username = 'dustin'

#     # optionally, abuse `set_password` to save username onto keyring
#     # we're just using some known magic string in the username field
#     keyring.set_password(service_id, "username", username)

#     # save password
#     keyring.set_password(service_id, username, "password")


# @g1_2.command()
# def get_passwords():
#     service_id = 'IM_YOUR_APP!'

#     username = keyring.get_password(service_id, "username")
#     password = keyring.get_password(service_id, username)
#     click.echo(f"username: {username}")
#     click.echo(f"password: {password}")


# @g1_1.command()
# # @g1_1.pass_context
# def cli3(ctx):
#     click.echo('This is the 3!')


# @g1_1.command()
# # @g1_1.pass_context
# def cli2(ctx):
#     """Example script."""
#     click.clear()

#     click.echo('Hello World!')
#     click.secho('Some more text', bg='blue', fg='white')

#     click.echo('Continue? [yn] ', nl=False)
#     while True:
#         c = click.getchar()
#         click.echo()
#         if c == 'y':
#             click.echo('We will go on')
#             break
#         elif c == 'n':
#             click.echo('Abort!')
#             break
#         else:
#             click.echo('Invalid input :(')
#     l = list(range(10))
#     with click.progressbar([1, 2, 3], label='Modifying user accounts',
#                            ) as bar:
#         for x in bar:
#             # print(f"sleep({x})...")
#             time.sleep(x)
