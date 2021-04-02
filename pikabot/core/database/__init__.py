#!/usr/bin/env python3
#
# Copyright (C) 2020 by ItzSjDude@Github, < https://github.com/ItzSjDude/PikachuUserbot >.
#
# This file is part of < https://github.com/ItzSjDude/PikachuUserbot > project,
# and is released under the "GNU v3.0 License Agreement".
#
# Please see < https://github.com/ItzSjDude/PikachuUserbot/blob/master/LICENSE >
#
# All rights reserved

from sqlalchemy import *
import os
from sqlalchemy.ext.declarative import *
from sqlalchemy.orm import *
_get = os.environ.get

# the secret configuration specific things


def start() -> scoped_session:
    engine = create_engine(_get("DATABASE_URL"))
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


try:
    BASE = declarative_base()
    SESSION = start()
except AttributeError as e:
    # this is a dirty way for the work-around required for #23
    print("DB_URI is not configured. Features depending on the database might have issues.")
    print(str(e))


class Pdb(BASE):
    __tablename__ = "pdb"
    client = Column(String, primary_key=True, nullable=False)
    var = Column(String)
    value = Column(UnicodeText)

    def __init__(self, client, var, value):
        self.client = str(client)
        self.var = str(variable)
        self.value = value


class BotUsers(BASE):
    __tablename__ = "botusers"
    pika_id = Column(String(14), primary_key=True)

    def __init__(self, pika_id):
        self.pika_id = pika_id


class PikaChats(BASE):
    __tablename__ = "PikaTg"
    pika_id = Column(String(14), primary_key=True)

    def __init__(self, pika_id):
        self.pika_id = pika_id


class GMute(BASE):
    __tablename__ = "gmute"
    sender = Column(String(14), primary_key=True)
    pika_id = Column(Numeric, primary_key=True)

    def __init__(self, sender, pika_id):
        self.sender = str(sender)
        self.pika_id = pika_id


class GBan(BASE):
    __tablename__ = "gban"
    sender = Column(String(14), primary_key=True)
    pika_id = Column(Numeric, primary_key=True)
    reason = Column(UnicodeText)

    def __init__(self, sender, pika_id, reason=""):
        self.sender = str(sender)
        self.pika_id = str(pika_id)
        self.reason = reason


class Mute(BASE):
    __tablename__ = "mute"
    sender = Column(String(14), primary_key=True)
    chat_id = Column(String(14), primary_key=True)
    pika_id = Column(Numeric, primary_key=True)

    def __init__(self, sender, chat_id, pika_id):
        self.sender = str(sender)
        self.chat_id = str(chat_id)
        self.pika_id = pika_id


class Notes(BASE):
    __tablename__ = "notes"
    chat_id = Column(String(14), primary_key=True)
    keyword = Column(UnicodeText, primary_key=True, nullable=False)
    reply = Column(UnicodeText)
    f_mesg_id = Column(Numeric)
    client_id = Column(Numeric, primary_key=True)

    def __init__(self, chat_id, keyword, reply, f_mesg_id, client_id):
        self.chat_id = str(chat_id)
        self.keyword = keyword
        self.reply = reply
        self.f_mesg_id = f_mesg_id
        self.client_id = client_id


class PMPermit(BASE):
    __tablename__ = "pmpermit"
    chat_id = Column(String(14), primary_key=True)
    reason = Column(String(127))
    pika_id = Column(Numeric, primary_key=True)

    def __init__(self, chat_id, pika_id, reason=""):
        self.chat_id = chat_id
        self.reason = reason
        self.pika_id = pika_id


class Welcome(BASE):
    __tablename__ = "welcome"
    chat_id = Column(String(14), primary_key=True)
    pika_id = Column(Numeric, primary_key=True)
    cust_wc = Column(UnicodeText)
    cl_wc = Column(Boolean, default=False)
    prev_wc = Column(BigInteger)
    mf_id = Column(UnicodeText)

    def __init__(self, chat_id, pika_id, cust_wc, cl_wc, prev_wc, mf_id=None):
        self.chat_id = chat_id
        self.pika_id = pika_id
        self.cust_wc = cust_wc
        self.cl_wc = cl_wc
        self.prev_wc = prev_wc
        self.mf_id = mf_id


Pdb.__table__.create(checkfirst=True)
Mute.__table__.create(checkfirst=True)
BotUsers.__table__.create(checkfirst=True)
PikaChats.__table__.create(checkfirst=True)
GMute.__table__.create(checkfirst=True)
GBan.__table__.create(checkfirst=True)
Notes.__table__.create(checkfirst=True)
PMPermit.__table__.create(checkfirst=True)
Welcome.__table__.create(checkfirst=True)


def pget(client, var):
    try:
        return SESSION.query(Pdb).filter(
            Pdb.client == str(client),
            Pdb.var == str(var)).first().value
    except BaseException:
        return None
    finally:
        SESSION.close()


def pset(client, var, value):
    if SESSION.query(Pdb).filter(
            Pdb.client == str(client),
            Pdb.var == str(var)).one_or_none():
        delgvar(variable)
    adder = Pdb(str(client), str(var), value)
    SESSION.add(adder)
    SESSION.commit()


def pdel(client, var):
    rem = SESSION.query(Pdb).filter(
        Pdb.client == str(client),
        Pdb.var == str(var)) .delete(
        synchronize_session="fetch")
    if rem:
        SESSION.commit()


def add_welcome(chat_id, pika_id, cust_wc, cl_wc, prev_wc, mf_id):
    add_wc = Welcome(chat_id, pika_id, cust_wc, cl_wc, prev_wc, mf_id)
    SESSION.add(add_wc)
    SESSION.commit()


def remove_welcome(chat_id, pika_id):
    rm_wc = SESSION.query(Welcome).get((str(chat_id), pika_id))
    if rm_wc:
        SESSION.delete(rm_wc)
        SESSION.commit()


def upd_prev_welcome(chat_id, pika_id, prev_wc):
    _update = SESSION.query(Welcome).get((str(chat_id), pika_id))
    _update.prev_wc = prev_wc
    SESSION.commit()


def get_welcome(chat_id, pika_id):
    try:
        return SESSION.query(Welcome).get((str(chat_id), pika_id))
    except Exception as e:
        pikalog.error(str(e))
        return
    finally:
        SESSION.close()


def clean_welcome(chat_id, pika_id, cl_wc):
    clnn = SESSION.query(Welcome).get((str(chat_id), pika_id))
    clnn.cl_wc = cl_wc
    SESSION.commit()


def approve(chat_id, pika_id, reason):
    adder = PMPermit(str(chat_id), pika_id, str(reason))
    SESSION.add(adder)
    SESSION.commit()


def disapprove(chat_id, pika_id):
    rem = SESSION.query(PMPermit).get((str(chat_id), pika_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def get_all_approved(pika_id):
    rem = SESSION.query(PMPermit).filter(PMPermit.pika_id == pika_id).all()
    SESSION.close()
    return rem


def is_approved(chat_id, pika_id):
    try:
        return SESSION.query(PMPermit).filter(
            PMPermit.chat_id == str(chat_id),
            PMPermit.pika_id == pika_id).one()
    except BaseException:
        return None
    finally:
        SESSION.close()


def get_note(chat_id, keyword, client_id):
    try:
        return SESSION.query(Notes).get((str(chat_id), keyword, client_id))
    finally:
        SESSION.close()


def get_notes(chat_id, client_id):
    try:
        return SESSION.query(Notes).filter(
            Notes.chat_id == str(chat_id),
            Notes.client_id == client_id).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def add_note(chat_id, keyword, reply, f_mesg_id, client_id):
    to_check = get_note(chat_id, keyword, client_id)
    if not to_check:
        adder = Notes(str(chat_id), keyword, reply, f_mesg_id, client_id)
        SESSION.add(adder)
        SESSION.commit()
        return True
    else:
        rem = SESSION.query(Notes).get((str(chat_id), keyword, client_id))
        SESSION.delete(rem)
        SESSION.commit()
        adder = Notes(str(chat_id), keyword, reply, f_mesg_id, client_id)
        SESSION.add(adder)
        SESSION.commit()
        return False


def rm_note(chat_id, keyword, client_id):
    to_check = get_note(chat_id, keyword, client_id)
    if not to_check:
        return False
    else:
        rem = SESSION.query(Notes).get((str(chat_id), keyword, client_id))
        SESSION.delete(rem)
        SESSION.commit()
        return True


def is_muted(sender, chat_id, pika_id):
    user = SESSION.query(Mute).get((str(sender), str(chat_id), pika_id))
    if user:
        return True
    else:
        return False


def mute(sender, chat_id, pika_id):
    adder = Mute(str(sender), str(chat_id), pika_id)
    SESSION.add(adder)
    SESSION.commit()


def unmute(sender, chat_id, pika_id):
    rem = SESSION.query(Mute).get((str(sender), str(chat_id), pika_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def get_all_muted(pika_id):
    rem = SESSION.query(Mute).filter(Notes.pika_id == pika_id).all()
    SESSION.close()
    return rem


def is_gbanned(sender, pika_id):
    try:
        _pikaG = SESSION.query(GBan).get((str(sender), str(pika_id)))
        if _pikaG:
            return str(_pikaG.reason)
    finally:
        SESSION.close()


def gban(sender, pika_id, reason):
    adder = GBan(str(sender), str(pika_id), str(reason))
    SESSION.add(adder)
    SESSION.commit()


def ungban(sender, pika_id):
    rem = SESSION.query(GBan).get((str(sender), str(pika_id)))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def is_gmuted(sender):
    try:
        return SESSION.query(GMute).all()
    except BaseException:
        return None
    finally:
        SESSION.close()


def gmute(sender, pika_id):
    adder = GMute(str(sender), pika_id)
    SESSION.add(adder)
    SESSION.commit()


def ungmute(sender, pika_id):
    rem = SESSION.query(GMute).get((str(sender), pika_id))
    if rem:
        SESSION.delete(rem)
        SESSION.commit()


def add_pika(pika_id):
    pika = PikaChats(str(pika_id))
    SESSION.add(pika)
    SESSION.commit()


def is_pika_exist(pika_id):
    try:
        pika = SESSION.query(PikaChats).filter(
            PikaChats.pika_id == str(pika_id)).one()
        if pika:
            return True
    except BaseException:
        return None
    finally:
        SESSION.close()


def get_pika_chats():
    try:
        pika = SESSION.query(PikaChats).all()
        if pika:
            return pika
    except BaseException:
        return None
    finally:
        SESSION.close()


def add_user(pika_id: int):
    pika = BotUsers(str(pika_id))
    SESSION.add(pika)
    SESSION.commit()


def is_user_exist(pika_id):
    try:
        pika = SESSION.query(BotUsers).filter(
            BotUsers.pika_id == str(pika_id)).one()
        if pika:
            return True
    except BaseException:
        return None
    finally:
        SESSION.close()


def get_added_users():
    pika = SESSION.query(BotUsers).all()
    SESSION.close()
    return pika


class pdb(object):
    Api_id = _get("API_ID")
    Api_hash = _get("API_HASH")
    Bf_uname = _get("TG_BOT_USER_NAME_BF_HER")
    Omega = _get("TG_BOT_TOKEN_BF_HER")
    Alpha = pget("alpha", "session")
    Beta = pget("beta", "session")
    Gaama = pget("gaama", "session")
    Delta = pget("delta", "session")
    Asstt = pget("omega", "assistant")
    Botlog_chat = int(_get("BOTLOG_CHATID"))
