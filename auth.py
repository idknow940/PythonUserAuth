import hashlib
import sqlite3
import sys
import os

import settings


class Auth:
    def __init__(self):
        self.create_db(os.path.join(os.getcwd(), settings.DB_FILE_NAME))
        self.con = sqlite3.connect(os.path.join(os.getcwd(), settings.DB_FILE_NAME))
        self.cursor = self.con.cursor()
        self._logged = False

    def register(self):
        username = input("")
        password = input("")
        username_checked = self.check_username(username)
        pass_checked = self.check_password(password)
        pass_hashed = hashlib.sha256(password.encode("utf-8"))
        if username_checked and pass_checked:
            self.create_table()
            try:
                self.cursor.execute("""INSERT INTO user (username,password) VALUES(?,?)"""
                                    , (username, pass_hashed.hexdigest()))
                self.con.commit()
            except sqlite3.Error as e:
                print(e)
                sys.exit()
        else:
            print("password should be at least {} chars"
                  " and username should be at least {} chars and it should be unique".format(settings.PASS_LENGTH,
                                                                                             settings.USERNAME_LENGTH))
            sys.exit()

    def login(self):
        username = input("")
        password = input("")
        username_checked = self.check_username(username)
        pass_checked = self.check_password(password)
        if pass_checked and username_checked:
            pass_hashed = hashlib.sha256(password.encode("utf-8"))
            self.cursor.execute(
                """SELECT * FROM user WHERE username = ? AND password = ? """, (
                    username, pass_hashed.hexdigest()))
            users = self.cursor.fetchone()
            if users:
                self._logged = True
                print("Successfully logged in as {}!".format(users[1]))
            else:
                self._logged = False
                print("Failed to log in!")
                sys.exit()
        else:
            print("password should be at least {} chars"
                  " and username should be at least {} chars and it should be unique".format(settings.PASS_LENGTH,
                                                                                             settings.USERNAME_LENGTH))
            sys.exit()

    def create_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS user ( 
                id integer PRIMARY KEY AUTOINCREMENT, 
                username text UNIQUE NOT NULL,
                password text NOT NULL);
            """)

    @staticmethod
    def check_username(username):
        if len(username) >= settings.USERNAME_LENGTH:
            return True
        else:
            return False

    @staticmethod
    def check_password(password):
        if len(password) >= settings.PASS_LENGTH:
            return True
        else:
            return False

    @property
    def logged_in(self):
        return self._logged

    @staticmethod
    def create_db(path):
        if not os.path.exists(path):
            with open(settings.DB_FILE_NAME, 'x'):
                pass

    @staticmethod
    def delete_db(path):
        if os.path.exists(path):
            os.remove(path)


def main():
    rol = input("register|login>>> ")
    auth = Auth()
    match rol:
        case "register":
            auth.register()
        case "login":
            auth.login()
        case _:
            main()


if __name__ == '__main__':
    main()
