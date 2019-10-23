import sqlite3
import calendar
import datetime
from user import User


class DBHelper:
    def __init__(self, dbname: object = "./MyDataBase") -> object:
        self.dbname = dbname
        self.conn = sqlite3.connect(dbname, check_same_thread=False)

    def new_user(self, id, username, uname, ulname, rank):
        try:
            stmt = "INSERT OR IGNORE INTO Users(User_id, Username, User_Name, User_Last_Name, Rank)VALUES(?,?, ?, ?, ?)"
            args = (id, username, uname, ulname, rank)
            self.conn.execute(stmt, args)

        except (sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
            print("ERROR DATABASE new_user", e)
            self.conn.close()
        else:
            self.conn.commit()

    def new_user_phone(self, phone):
        try:
            stmt = "INSERT OR IGNORE INTO Users (User_id, Phone) VALUES (?, ?)"
            args = (phone, phone)
            self.conn.execute(stmt, args)
            self.conn.commit()
        except (sqlite3.OperationalError, sqlite3.ProgrammingError):
            print("ERROR DATABASE new_user_phone")
            self.conn.close()

    def get_userinfo(self, get, key):
        try:
            if get == 0:
                stmt = "SELECT * FROM Users WHERE User_id = (?)"

            if get == 1:
                stmt = "SELECT * FROM Users WHERE Phone = (?)"

            args = (key,)
            self.conn.execute(stmt, args)
            for x in self.conn.execute(stmt, args):
                return User(x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8], x[9])
        except (sqlite3.OperationalError, sqlite3.ProgrammingError):
            print("ERROR DATABASE get_userinfo")
            self.conn.close()

    def set_user_rname(self, name, id):
        try:
            stmt = "UPDATE Users SET User_Rname = (?) where User_id = (?)"
            args = (name, id)
            self.conn.execute(stmt, args)
            self.conn.commit()
        except (sqlite3.OperationalError, sqlite3.ProgrammingError):
            print("ERROR DATABASE set_user_name")
            self.conn.close()

    def set_user_rlname(self, lname, id):
        try:
            stmt = "UPDATE Users SET User_Rlast_Name = (?) where User_id = (?)"
            args = (lname, id)
            self.conn.execute(stmt, args)
            self.conn.commit()
        except (sqlite3.OperationalError, sqlite3.ProgrammingError):
            print("ERROR DATABASE set_user_rlname")
            self.conn.close()

    def set_phone(self, phone, id):
        try:
            stmt = "UPDATE Users SET Phone = (?) where User_id = (?)"
            args = (phone, id)
            self.conn.execute(stmt, args)
        except (sqlite3.OperationalError, sqlite3.ProgrammingError):
            print("ERROR DATABASE set_phone")
            self.conn.close()
        else:
            self.conn.commit()

    def setRank(self, Rank, id):
        try:
            stmt = "UPDATE Users SET Rank = (?) where User_id = (?)"
            args = (Rank, id)
            self.conn.execute(stmt, args)
        except (sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
            print("ERROR DATABASE set_rank", e)
            self.conn.close()
        else:
            self.conn.commit()

    def setUsername(self, username, id):
        try:
            stmt = "UPDATE or IGNORE Users SET Username = (?) where User_id = (?)"
            args = (username, id)
            self.conn.execute(stmt, args)

        except (sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
            print("ERROR DATABASE set_rank", e)
            self.conn.close()

        else:
            self.conn.commit()


    def get_all_phones(self):
        stmt = "SELECT Phone FROM Users "
        cur = self.conn.cursor()
        phones = [phone[0] for phone in cur.execute(stmt)]
        print(phones)
        return phones

    def get_all_masters(self):
        stmt = "SELECT * FROM Users WHERE Rank = 'MASTER' "
        cur = self.conn.cursor()
        masters = [master[0] for master in cur.execute(stmt)]
        return masters

    def buffer(self, id, buf):
        try:
            stmt = "UPDATE Users SET User_Note_id = (?) where User_id = (?)"
            args = (buf, id)
            self.conn.execute(stmt, args)
            self.conn.commit()
        except (sqlite3.OperationalError, sqlite3.ProgrammingError):
            print("ERROR DATABASE buffer")
            self.conn.close()


    def remove_buf(self, id):
        try:
            stmt = "UPDATE Users SET User_Note_id = NULL where User_id = (?)"
            args = (id,)
            self.conn.execute(stmt, args)
            self.conn.commit()
            print("ID 83 on DB - {}".format(id))
        except (sqlite3.OperationalError, sqlite3.ProgrammingError):
            self.conn.close()
            print("ERROR DATABASE remote_buffer")


    def set_comment(self,comment, id):
        try:
            stmt = "UPDATE Users SET Comment = (?) where User_id = (?)"
            args = (comment, id)
            self.conn.execute(stmt, args)
        except sqlite3.DatabaseError as err:
            print("ERROR SET COMMENT")
            #TODO DataBaseLog(err)
        else:
            self.conn.commit()

    def make_note(self, date, half, id, note_id):
        try:
            print("make_note_DB")
            print(date, half, id, note_id)
            stmt = "UPDATE Users SET User_Note_id = (?) where User_id = (?)"
            args = (note_id, id)
            self.conn.execute(stmt, args)
            if half == 1:
                stmt = "UPDATE Dates SET half1_id = (?) where date = (?)"
            elif half == 2:
                stmt = "UPDATE Dates SET half2_id = (?) where date = (?)"
            args = (id, date)
            self.conn.execute(stmt, args)
            self.conn.commit()
        except (sqlite3.OperationalError, sqlite3.ProgrammingError):
            print("ERROR DATABASE make_note")

    def remove_note(self, date, half, id):
        try:
            print(date)
            stmt = "UPDATE Users SET User_Note_id = NULL where User_id = (?)"
            args = (id,)
            self.conn.execute(stmt, args)
            if half == 1:
                stmt = "UPDATE Dates SET half1_id = NULL where date = (?)"
            elif half == 2:
                stmt = "UPDATE Dates SET half2_id = NULL where date = (?)"
            args2 = (date,)
            self.conn.execute(stmt, args2)
            self.conn.commit()
        except (sqlite3.OperationalError, sqlite3.ProgrammingError):
            print("ERROR DATABASE remove_note")

    def update_work(self, work, date):
        try:
            stmt = "UPDATE Dates SET work = (?) where date = (?)"
            print(work)
            args = (work, date)
            self.conn.execute(stmt, args)
            self.conn.commit()
        except (sqlite3.OperationalError, sqlite3.ProgrammingError):
            self.conn.close()
            print("ERROR DATABASE update_work")

    def get_work(self, date):
        try:
            stmt = "SELECT work FROM Dates WHERE date = (?)"
            args = (date,)
            return [x[0] for x in self.conn.execute(stmt, args)]
        except (sqlite3.OperationalError, sqlite3.ProgrammingError):
            self.conn.close()
            print("ERROR DATABASE get_work")

    def get_halfs(self, date):
        try:
            stmt = "SELECT half1_id, half2_id FROM Dates WHERE date = (?)"
            args = (date,)
            res = []
            for x in self.conn.execute(stmt, args):
                res.append(x[0])
                res.append(x[1])
            return res
        except (sqlite3.OperationalError, sqlite3.ProgrammingError):
            self.conn.close()
            print("ERROR DATABASE get_halfs")

    def addteb(self):
        try:
            now = datetime.datetime.now()
            c = calendar.Calendar(0)

            call = c.monthdayscalendar(now.year, now.month)
            for week in call:
                for day in week:
                    if day != 0 and day < 10:
                        self.conn.execute("insert OR IGNORE into Dates values (?, ?,?,?,?,?)",
                                          (datetime.date(now.year, now.month, day), None, None, None, None, None))
            self.conn.commit()
        except (sqlite3.OperationalError, sqlite3.ProgrammingError):
            print("ERROR DATABASE addteb")
