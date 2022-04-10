from datetime import datetime, timedelta
from os import path
from pathlib import Path

from migrate.versioning.api import upgrade
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from src.db.model import Account, Base, Hashtag, HashtagGroup, Image, Post, Task

folder_path = path.join(Path.home(), ".igpost")
Path(folder_path).mkdir(parents=True, exist_ok=True)
default_db_file = path.join(folder_path, "igpost.db")

engine = create_engine(f"sqlite:///{default_db_file}", echo=False)
Session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))


def create_db():
    Base.metadata.create_all(engine)
    create_first_records()


def upgrade_db():
    Base.metadata.create_all(engine)


def create_first_records():
    session = Session()

    a1 = session.query(Account).filter(Account.username == "thiagomadpin").one_or_none()
    if a1 is None:
        a1 = Account()
        a1.username = "thiagomadpin"
        a1.notes = "This is my personal account"
        session.add(a1)

    a2 = session.query(Account).filter(Account.username == "madindub").one_or_none()
    if a2 is None:
        a2 = Account()
        a2.username = "madindub"
        a2.notes = "This is a test account"
        session.add(a2)

    # ########################################################################
    # ########################################################################

    hg_dub = (
        session.query(HashtagGroup).filter(HashtagGroup.text == "Dublin").one_or_none()
    )
    if hg_dub is None:
        hg_dub = HashtagGroup()
        hg_dub.text = "Dublin"
        session.add(hg_dub)

    hg_stf = (
        session.query(HashtagGroup).filter(HashtagGroup.text == "Street").one_or_none()
    )
    if hg_stf is None:
        hg_stf = HashtagGroup()
        hg_stf.text = "Street"
        session.add(hg_stf)

    hg_photo = (
        session.query(HashtagGroup).filter(HashtagGroup.text == "Photos").one_or_none()
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

        count = session.query(Hashtag).filter(Hashtag.text == hashtag).count()
        if count == 0:
            h = Hashtag()
            h.text = hashtag
            h.hashtag_group = hashtag_group
            session.add(h)

    # ########################################################################
    # ########################################################################
    note_txt = "Print this please.§"
    t1 = session.query(Task).filter(Task.notes == note_txt).one_or_none()
    if t1 is None:
        t1 = Task()
        t1.notes = note_txt
        t1.task_type = "print_notes"
        t1.scheduled = True
        t1.schedule_dt = datetime.now() - timedelta(1)
        t1.tries_todo = 1
        t1.account = a2
        session.add(t1)
    session.commit()

    # ########################################################################
    # ########################################################################
    images_path = [
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05416-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC01261-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03402-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03485-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03638-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03674-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03693-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05535-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05541-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05544-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05554-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05606-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05622-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05643-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05678-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC06848-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC07277-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC07330-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC07341-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC07393-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC07400-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC00475-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC00589-HDR-fullsize-2.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC00589-HDR-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC00662-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC00917-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC01261-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC01269-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC01309-HDR-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03120-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03402-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03429-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03451-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03483-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03485-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03499-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03509-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03555-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03617-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03624-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03638-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03655-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03674-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03675-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03680-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03687-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03693-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03759-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03763-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03778-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03797-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03804-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03830-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03845-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03849-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03866-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03884-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03887-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03945-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC03960-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04068-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04100-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04101-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04102-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04123-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04128-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04150-Pano-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04182-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04222-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04231-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04243-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04250-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04266-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04282-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04327-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04487-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04542-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04608-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04629-HDR-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04682-HDR-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04692-HDR-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04706-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04792-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04816-HDR-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04821-HDR-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04840-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC04881-HDR-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05113-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05115-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05116-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05117-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05118-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05119-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05120-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05123-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05124-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05126-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05127-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05128-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05130-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05131-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05132-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05133-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05134-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05149-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05390-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05396-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05408-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05415-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05416-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05424-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05426-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05433-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05438-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05445-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05446-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05447-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05450-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05463-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05469-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05493-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05505-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05515-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05535-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05541-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05544-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05554-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05606-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05622-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05643-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC05678-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC06848-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC07277-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC07330-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC07341-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC07393-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC07400-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC07404-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC07479-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC07486-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC07505-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC07516-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC07533-fullsize.jpg",
        "/Users/tpinto/Desktop/Photos Exports/FullSize/DSC07539-fullsize.jpg",
    ]
    for image_path in images_path:
        img = (
            session.query(Image)
            .filter(Image.original_filepath == image_path)
            .one_or_none()
        )
        if img is None:
            img = Image()
            img.original_filepath = image_path
            session.add(img)
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
