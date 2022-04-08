from os import path
from pathlib import Path

from migrate.versioning.api import upgrade
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from src.db.model import Base
from src.db.model import (
    Post,
    Image,
    Hashtag,
    HashtagGroup,
    Account,
    Task,
)

folder_path = path.join(Path.home(), ".igpost")
Path(folder_path).mkdir(parents=True, exist_ok=True)
default_db_file = path.join(folder_path, "igpost.db")

engine = create_engine(f"sqlite:///{default_db_file}", echo=True)


def create_db():
    Base.metadata.create_all(engine)
    create_first_records()


def upgrade_db():
    Base.metadata.create_all(engine)


def create_first_records():
    with Session(engine) as session:

        a1 = (
            session.query(Account)
            .filter(Account.username == "thiagomadpin")
            .one_or_none()
        )
        if a1 is None:
            a1 = Account()
            a1.username = "thiagomadpin"
            a1.notes = "This is my personal account"
            session.add(a1)

        a2 = (
            session.query(Account)
            .filter(Account.username == "madindub")
            .one_or_none()
        )
        if a2 is None:
            a2 = Account()
            a2.username = "madindub"
            a2.notes = "This is a test account"
            session.add(a2)

        # ########################################################################
        # ########################################################################

        hg_dub = (
            session.query(HashtagGroup)
            .filter(HashtagGroup.text == "Dublin")
            .one_or_none()
        )
        if hg_dub is None:
            hg_dub = HashtagGroup()
            hg_dub.text = "Dublin"
            session.add(hg_dub)

        hg_stf = (
            session.query(HashtagGroup)
            .filter(HashtagGroup.text == "Street")
            .one_or_none()
        )
        if hg_stf is None:
            hg_stf = HashtagGroup()
            hg_stf.text = "Street"
            session.add(hg_stf)


        hg_photo = (
            session.query(HashtagGroup)
            .filter(HashtagGroup.text == "Photos")
            .one_or_none()
        )
        if hg_photo is None:
            hg_photo = HashtagGroup()
            hg_photo.text = "Photos"
            session.add(hg_photo)

        # ########################################################################
        # ########################################################################

        hashtags_dict = {
            "photography": hg_photo,
            "photooftheday": hg_photo,
            "instagood": hg_photo,
            "photo": hg_photo,
            "streetphotography": hg_stf,
            "SPiCollective": hg_stf,
            "streetfinder": hg_stf,
            "streetclassics": hg_stf,
            "dublin": hg_dub,
            "ireland": hg_dub,
        }

        for hashtag, hashtag_group in hashtags_dict.items():

            count = (
                session.query(Hashtag)
                .filter(Hashtag.text == hashtag)
                .count()
            )
            if count == 0:
                h = Hashtag()
                h.text = hashtag
                h.hashtag_group = hashtag_group
                session.add(h)

        # ########################################################################
        # ########################################################################

        t1 = (
            session.query(Task)
            .filter(Task.notes == "Print this please.")
            .one_or_none()
        )
        if t1 is None:
            t1 = Task()
            t1.notes = "Print this please."
            t1.type = 'print_notes'
            t1.account = a2
            session.add(t1)
        session.commit()


# import sqlite3
# from sqlite3 import Error
# from pathlib import Path
# from os import path

# folder_path = path.join(Path.home(), ".igpost")
# Path(folder_path).mkdir(parents=True, exist_ok=True)
# default_db_file = path.join(folder_path, "igpost.db")
# # default_db_file = 'igpost.db'
# def printy(str):
#     print(str)


# def create_connection(db_file):
#     """create a database connection to a SQLite database"""
#     conn = None
#     try:
#         conn = sqlite3.connect(default_db_file)
#         print(sqlite3.version)
#     except Error as e:
#         print(e)
#     finally:
#         if conn:
#             conn.close()
