from tkinter import N
from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
    event,
    text,
    Enum,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship

Base = declarative_base()


def after_create_post(target, connection, **kw):
    connection.execute(
        text(
            f"""
    CREATE TRIGGER tg_{target}_updated_at
    AFTER UPDATE
    ON {target} FOR EACH ROW
    BEGIN
    UPDATE {target} SET updated_at = current_timestamp
        WHERE id = old.id;
    END;
        """
        )
    )


post_image = Table(
    "post_image",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id")),
    Column("image_id", Integer, ForeignKey("image.id")),
)

post_account = Table(
    "post_account",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id")),
    Column("account_id", Integer, ForeignKey("account.id")),
)

post_hashtag_group = Table(
    "post_hashtag_group",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id")),
    Column("hashtag_group_id", Integer, ForeignKey("hashtag_group.id")),
)

# book_publisher = Table(
#     "book_publisher",
#     Base.metadata,
#     Column("book_id", Integer, ForeignKey("book.book_id")),
#     Column("publisher_id", Integer, ForeignKey("publisher.publisher_id")),
# )


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    deleted_at = Column(DateTime, nullable=True, default=None)
    is_deleted = Column(Boolean, nullable=False, default=False)
    notes = Column(String)
    text = Column(String)
    location = Column(String)
    gps_lat = Column(Float)
    gps_long = Column(Float)

    images = relationship("Image", secondary=post_image, backref="post")
    accounts = relationship("Account", secondary=post_account, backref="posts")
    hashtag_group = relationship(
        "HashtagGroup", secondary=post_hashtag_group, backref="posts"
    )


event.listen(Post.__table__, "after_create", after_create_post)


class Image(Base):
    __tablename__ = "image"
    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    deleted_at = Column(DateTime, nullable=True, default=None)
    is_deleted = Column(Boolean, nullable=False, default=False)
    notes = Column(String)
    original_filename = Column(String)
    original_filepath = Column(String)
    exposure_program = Column(String)

    fnumber = Column(Float)
    focal_length = Column(Float)
    iso = Column(Integer)
    exposure = Column(Float)
    px_width = Column(Integer)
    px_height = Column(Integer)

    make = Column(String)
    model = Column(String)
    software = Column(String)
    lens_model = Column(String)
    date_captured = Column(DateTime)


event.listen(Image.__table__, "after_create", after_create_post)


class Hashtag(Base):
    __tablename__ = "hashtag"
    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    deleted_at = Column(DateTime, nullable=True, default=None)
    is_deleted = Column(Boolean, nullable=False, default=False)
    notes = Column(String)
    text = Column(String)
    hashtag_group_id = Column(ForeignKey("hashtag_group.id"), nullable=True, index=True)
    hashtag_group = relationship(
        "HashtagGroup",
        innerjoin=True,
        backref=backref(
            "hashtags",
            cascade="all, delete-orphan",
            innerjoin=True,
        ),
    )


event.listen(Hashtag.__table__, "after_create", after_create_post)


class HashtagGroup(Base):
    __tablename__ = "hashtag_group"
    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    deleted_at = Column(DateTime, nullable=True, default=None)
    is_deleted = Column(Boolean, nullable=False, default=False)
    notes = Column(String)
    text = Column(String)


event.listen(HashtagGroup.__table__, "after_create", after_create_post)


class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    deleted_at = Column(DateTime, nullable=True, default=None)
    is_deleted = Column(Boolean, nullable=False, default=False)
    notes = Column(String)
    ig_id = Column(String)
    username = Column(String)


event.listen(Account.__table__, "after_create", after_create_post)


class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    created_at = Column(
        DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    deleted_at = Column(DateTime, nullable=True, default=None)
    is_deleted = Column(Boolean, nullable=False, default=False)
    notes = Column(String)

    account_id = Column(ForeignKey("account.id"), nullable=True, index=True)
    account = relationship(
        "Account",
        innerjoin=True,
        backref=backref(
            "tasks",
            cascade="all, delete-orphan",
        ),
    )
    post_id = Column(ForeignKey("post.id"), nullable=True, index=True)
    post = relationship(
        "Post",
        innerjoin=True,
        backref=backref(
            "tasks",
            cascade="all, delete-orphan",
        ),
    )

    scheduled = Column(Boolean, nullable=False, default=False)
    schedule_dt = Column(DateTime, nullable=True, default=None)

    type = Column(Enum("post", "story", "print_notes"), nullable=False)

    trying = Column(Boolean, nullable=False, default=False)
    trying_dt = Column(DateTime, nullable=True, default=None)
    tries_done = Column(Integer, nullable=False, default=0)
    tries_todo = Column(Integer, nullable=False, default=0)
    done = Column(Boolean, nullable=False, default=False)
    has_giveup = Column(Boolean, nullable=True, default=None)


event.listen(Task.__table__, "after_create", after_create_post)


# class Publisher(Base):
#     __tablename__ = "publisher"
#     publisher_id = Column(Integer, primary_key=True)
#     name = Column(String)
#     authors = relationship(
#         "Author", secondary=author_publisher, back_populates="publishers"
#     )
#     books = relationship(
#         "Book", secondary=book_publisher, back_populates="publishers"
#     )


# # coding: utf-8
# from sqlalchemy import (
#     JSON,
#     Column,
#     Date,
#     DateTime,
#     Enum,
#     Float,
#     ForeignKey,
#     Index,
#     Integer,
#     String,
#     Table,
#     Text,
#     text,
# )
# # from sqlalchemy.dialects.mysql import INTEGER, TINYINT
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import backref, relationship

# Base = declarative_base()
# metadata = Base.metadata


# class Task(Base):
#     __tablename__ = "task"
#     __table_args__ = {"comment": "List of all "}

#     id = Column(Integer, primary_key=True)
#     created_at = Column(
#         DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
#     )
#     updated_at = Column(
#         DateTime,
#         nullable=False,
#         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
#     )
#     deleted_at = Column(DateTime)
#     is_deleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
#     action_key = Column(String(100))
#     phrase = Column(Text)
#     ranking = Column(Float, server_default=text("'1200'"))
#     plus_selection_ranking = Column(
#         Float,
#         server_default=text("'0'"),
#         comment="Number to be added to the ranking only on selection",
#     )
#     notes = Column(Text, comment="Aditional information")


# class Advertiser(Base):
#     __tablename__ = "advertiser"
#     __table_args__ = {
#         "comment": "Table containing the advertizer generated data (chs, explanations)"
#     }

#     id = Column(INTEGER(11), primary_key=True)
#     created_at = Column(
#         DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
#     )
#     updated_at = Column(
#         DateTime,
#         nullable=False,
#         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
#     )
#     deleted_at = Column(DateTime)
#     is_deleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
#     model = Column(String(50))
#     client_health_score = Column(Float)
#     client_health_updated_at = Column(DateTime)
#     last_activity_date = Column(DateTime)
#     raw_increase_prediction = Column(JSON)
#     raw_decrease_prediction = Column(JSON)
#     raw_extra_attr = Column(JSON)
#     client_health_cluster_id = Column(String(100))
#     notes = Column(Text, comment="Aditional information")

#     valid_games = relationship(
#         "Game",
#         primaryjoin="and_(foreign(Game.advertiser_id) == Advertiser.id, foreign(Game.expire_at) > "
#         "func.now(), foreign(Game.finished) == 0)",
#         uselist=True,
#     )


# class Attribute(Base):
#     __tablename__ = "attribute"
#     __table_args__ = (
#         Index(
#             "attribute_model_source_column_key_uindex",
#             "model",
#             "source_column",
#             "key",
#             unique=True,
#         ),
#         {
#             "comment": "Each client may have many attributes: increase_pred, decrease_pred, extra_attr"
#         },
#     )

#     id = Column(INTEGER(11), primary_key=True)
#     created_at = Column(
#         DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
#     )
#     updated_at = Column(
#         DateTime,
#         nullable=False,
#         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
#     )
#     deleted_at = Column(DateTime)
#     is_deleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
#     key = Column(String(50))
#     model = Column(String(50))
#     source_column = Column(String(50))
#     notes = Column(Text, comment="Aditional information")


# t_rpl_chub_adv_delivery = Table(
#     "rpl_chub_adv_delivery",
#     metadata,
#     Column("advertiser_id", INTEGER(11)),
#     Column("activity_date", Date),
#     Column("risk_score", Float(asdecimal=True)),
#     Column("model_type", String(100)),
#     Column("client_health_score", Float),
#     Column("increase_prediction", JSON),
#     Column("decrease_prediction", JSON),
#     Column("increase_other", JSON),
#     Column("decrease_other", JSON),
#     Column("extra_attr", JSON),
#     Column("revenue_13w", Float),
#     Column(
#         "created_at", DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
#     ),
# )


# class AdvertiserAttribute(Base):
#     __tablename__ = "advertiser_attribute"
#     __table_args__ = (
#         Index(
#             "advertiser_attribute_advertiser_id_attribute_id_index",
#             "advertiser_id",
#             "attribute_id",
#         ),
#         Index(
#             "advertiser_attribute_advertiser_id_attribute_id_uindex",
#             "advertiser_id",
#             "attribute_id",
#             unique=True,
#         ),
#         {
#             "comment": "Each client may have many attributes: increase_pred, decrease_pred, extra_attr"
#         },
#     )

#     id = Column(INTEGER(11), primary_key=True)
#     created_at = Column(
#         DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
#     )
#     updated_at = Column(
#         DateTime,
#         nullable=False,
#         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
#     )
#     advertiser_id = Column(ForeignKey("advertiser.id"), nullable=False, index=True)
#     attribute_id = Column(ForeignKey("attribute.id"), nullable=False, index=True)
#     attribute_order = Column(
#         INTEGER(11),
#         comment="This is the order received from Myriad, it's based on the column it arrived.",
#     )

#     advertiser = relationship(
#         "Advertiser",
#         backref=backref("advertiser_attribute"),
#         innerjoin=True,
#     )
#     attribute = relationship(
#         "Attribute",
#         backref=backref("advertiser_attribute"),
#         innerjoin=True,
#     )


# class AttributeAction(Base):
#     __tablename__ = "attribute_action"
#     __table_args__ = {"comment": "Action eligible for that attribute"}

#     id = Column(INTEGER(11), primary_key=True)
#     created_at = Column(
#         DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
#     )
#     updated_at = Column(
#         DateTime,
#         nullable=False,
#         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
#     )
#     attribute_id = Column(ForeignKey("attribute.id"), nullable=False, index=True)
#     action_id = Column(ForeignKey("action.id"), nullable=False, index=True)

#     action = relationship(
#         "Action",
#         backref=backref("attribute_action"),
#         innerjoin=True,
#     )
#     attribute = relationship(
#         "Attribute",
#         backref=backref("attribute_action"),
#         innerjoin=True,
#     )


# class Game(Base):
#     __tablename__ = "game"
#     __table_args__ = {
#         "comment": "Game, is everytime we made the actions avaiable for a given client"
#     }

#     id = Column(INTEGER(11), primary_key=True)
#     created_at = Column(
#         DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
#     )
#     updated_at = Column(
#         DateTime,
#         nullable=False,
#         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
#     )
#     deleted_at = Column(DateTime)
#     is_deleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
#     prent_company_id = Column(INTEGER(11))
#     advertiser_id = Column(ForeignKey("advertiser.id"), index=True)
#     expire_at = Column(DateTime)
#     rep_id = Column(INTEGER(11), comment="Optional rep_id")
#     players_count = Column(INTEGER(11))
#     finished = Column(TINYINT(1), nullable=False, server_default=text("'0'"))

#     advertiser = relationship(
#         "Advertiser",
#         backref=backref("game"),
#     )


# class GameAction(Base):
#     __tablename__ = "game_action"
#     __table_args__ = {
#         "comment": "Game Action, are the actions avaiable in that specific game"
#     }

#     id = Column(INTEGER(11), primary_key=True)
#     created_at = Column(
#         DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP")
#     )
#     updated_at = Column(
#         DateTime,
#         nullable=False,
#         server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
#     )
#     deleted_at = Column(DateTime)
#     is_deleted = Column(TINYINT(1), nullable=False, server_default=text("'0'"))
#     game_id = Column(ForeignKey("game.id"), index=True)
#     action_id = Column(ForeignKey("action.id"), index=True)
#     result = Column(Enum("todo", "won", "lost", "draw"))
#     previous_elo = Column(Float)
#     next_elo = Column(Float)
#     diff_elo = Column(Float)

#     action = relationship(
#         "Action",
#         backref=backref("game_action"),
#         lazy="joined",
#         innerjoin=True,
#     )
#     game = relationship(
#         "Game",
#         backref=backref(
#             "game_action",
#             lazy="joined",
#             innerjoin=True,
#         ),
#         lazy="joined",
#         innerjoin=True,
#     )
