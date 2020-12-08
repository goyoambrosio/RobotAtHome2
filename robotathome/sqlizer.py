#!/usr/bin/env python
# -*- coding: utf-8 -*-

""" Robot@Home SQLizer """

__author__ = "Gregorio Ambrosio"
__contact__ = "gambrosio[at]uma.es"
__copyright__ = "Copyright 2020, Gregorio Ambrosio"
__date__ = "2020/12/05"
__license__ = "MIT"


from robotathome.dataset import Dataset
import sqlite3

def sql_connection():

    try:

        # con = sqlite3.connect(':memory:')
        # print("Connection is established: Database is created in memory")
        con = sqlite3.connect('robotathome.db')
        print("Connection is established: robotathome.db")
        return con

    except NameError:

        print(NameError)





def main():
    # rhds = Dataset("MyRobot@Home")
    rhds = Dataset("MyRobot@Home", autoload=False)

    # Characterized elements

    rhds.unit["chelmnts"].load_data()

    # print(rhds.unit["chelmnts"])
    # print(rhds.unit["chelmnts"].get_home_names())
    # print(rhds.unit["chelmnts"].get_category_home_sessions())
    # print(rhds.unit["chelmnts"].get_category_rooms())
    # print(rhds.unit["chelmnts"].get_category_objects())

    con = sql_connection()
    cursor_obj = con.cursor()

    # Table creation

    cursor_obj.execute("DROP TABLE IF EXISTS homes")
    cursor_obj.execute("CREATE TABLE homes(id integer PRIMARY KEY, name text)")

    cursor_obj.execute("DROP TABLE IF EXISTS home_sessions")
    cursor_obj.execute("CREATE TABLE home_sessions(" +
                       "id integer PRIMARY KEY, " +
                       "home_id integer, " +
                       "name text)"
                       )

    cursor_obj.execute("DROP TABLE IF EXISTS room_types")
    cursor_obj.execute("CREATE TABLE room_types(id integer PRIMARY KEY, " +
                       "name text)")


    cursor_obj.execute("DROP TABLE IF EXISTS rooms")
    cursor_obj.execute("CREATE TABLE rooms(" +
                       "id integer PRIMARY KEY, " +
                       "home_id integer, " +
                       "home_session_id integer, " +
                       "room_type_id integer, " +
                       "name text)"
                       )

    con.commit()

    # ================
    #      Homes
    # ================

    homes = rhds.unit["chelmnts"].get_home_names()
    # for home in homes:
    #     sql_str = "INSERT INTO homes(name) VALUES('" + home + "')"
    #     cursor_obj.execute(sql_str)

    # homes_dict = dict(enumerate(homes, start=1))
    # print(homes_dict.items())

    cursor_obj.executemany("INSERT INTO homes VALUES(?,?)",
                           list(enumerate(homes, start=0)))
    con.commit()

    # ================
    #    Room types
    # ================

    room_types = rhds.unit["chelmnts"].get_category_rooms()
    cursor_obj.executemany("INSERT INTO room_types VALUES(?,?)",
                           room_types.items())
    con.commit()

    # ===============
    #  Home Sessions
    # ===============

    homes_dict = dict(enumerate(homes, start=1))
    # Two options for reversing a dictionary
    # homes_dict_reversed = {value: key for (key, value) in homes_dict.items()}
    homes_dict_reversed = dict(map(reversed, homes_dict.items()))
    # print(homes_dict_reversed)

    home_sessions = rhds.unit["chelmnts"].home_sessions
    for home_session in home_sessions:
        home_id = homes_dict_reversed[home_session.get_home_name()]
        print(home_id, home_session.id, home_session.name)
        cursor_obj.execute('INSERT INTO home_sessions(id, home_id, name) \
                           VALUES(?, ?, ?)',
                           (home_session.id, home_id, home_session.name)
                           )
    # ===============
    #      Rooms
    # ===============
        for room in home_session.rooms:
            # print(room)
            print(room.id, home_id, home_session.id, room.type_id, room.name)
            cursor_obj.execute('INSERT INTO rooms(id, home_id, home_session_id,\
                                                  room_type_id, name) \
                               VALUES(?, ?, ?, ?, ?)',
                               (room.id, home_id, home_session.id,
                                room.type_id, room.name)
                               )
    # ===============
    #     Objects
    # ===============

    # ===============
    #    Relations
    # ===============

    # ===============
    #  Observations
    # ===============

    con.commit()













    return 0


if __name__ == "__main__":
    main()
