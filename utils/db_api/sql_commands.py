import sqlite3
from datetime import datetime

import pytz


class Database:
    def __init__(self, db_path: str = 'db.sqlite3'):
        self.db_name = db_path

    @property
    def connect(self):
        conn = sqlite3.connect(
            database=self.db_name,
        )
        return conn

    def column_names_user(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_user"""
        cur.execute(SQL)
        res = [column[0] for column in cur.description]
        conn.close()
        return res

    def add_user(self, user_id, fullname, phone_number, mention):
        conn = self.connect
        cur = conn.cursor()
        SQL = """insert into testapp_user(user_id, fullname, phone_number, mention, suggestions)
            values
            (?, ?, ?, ?, ?)
        """
        cur.execute(SQL, (user_id, fullname, phone_number, mention, 0))
        conn.commit()
        conn.close()
        print(f"fullname: {fullname}, id: {user_id} foydalanuvchi bazaga qo'shildi!")

    def update_user_fullname(self, user_id, fullname):
        conn = self.connect
        cur = conn.cursor()
        SQL = """update testapp_user set fullname=? where user_id=?"""
        cur.execute(SQL, (fullname, user_id))
        conn.commit()
        conn.close()
        print(f"id: {user_id} foydalanuvchi fullnamesi o'zgartirildi!")

    def update_user_phone(self, user_id, phone_number):
        conn = self.connect
        cur = conn.cursor()
        SQL = """update testapp_user set phone_number=? where user_id=?"""
        cur.execute(SQL, (phone_number, user_id))
        conn.commit()
        conn.close()
        print(f"id: {user_id} foydalanuvchi nomeri o'zgartirildi!")

    def update_suggestion(self, user_id):
        conn = self.connect
        cur = conn.cursor()
        cur.execute("select fullname, suggestions from testapp_user where user_id=?", (user_id,))
        fullname, suggest = cur.fetchone()
        SQL = """update testapp_user set suggestions=? where user_id=?"""
        cur.execute(SQL, (suggest + 1, user_id))
        conn.commit()
        conn.close()
        print(f"fullname: {fullname}, id: {user_id} foydalanuvchi yana bir foydalanuvchi taklif qildi!")

    def select_users(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_user"""
        cur.execute(SQL)
        res = cur.fetchall()
        conn.close()
        return res

    def select_count_users(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select count(*) from testapp_user"""
        cur.execute(SQL)
        res = cur.fetchone()[0]
        conn.close()
        return res

    def select_user(self, user_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_user where user_id=?"""
        cur.execute(SQL, (user_id, ))
        res = cur.fetchone()
        conn.close()
        return res

    def delete_user(self, user_id):
        conn = self.connect
        cur = conn.cursor()
        cur.execute("select fullname from testapp_user where user_id=?", (user_id, ))
        fullname = cur.fetchone()[0]
        SQL = """delete from testapp_user where user_id=?"""
        cur.execute(SQL, (user_id,))
        conn.commit()
        conn.close()
        print(f"fullname: {fullname}, id: {user_id} foydalanuvchi bazagdan o'chirildi!")

    def column_names_science(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_science"""
        cur.execute(SQL)
        res = [column[0] for column in cur.description]
        conn.close()
        return res

    def add_science(self, name, teacher=None):
        conn = self.connect
        cur = conn.cursor()
        SQL = """insert into testapp_science(name, teacher)
            values
            (?, ?)
        """
        cur.execute(SQL, (name, teacher))
        conn.commit()
        conn.close()
        print(f"{name} fani bazaga qo'shildi!")

    def update_science(self, science_id, name):
        conn = self.connect
        cur = conn.cursor()
        SQL = """update testapp_science set name=? where id=?
        """
        cur.execute(SQL, (name, science_id))
        conn.commit()
        conn.close()
        print(f"{name} fani yangilandi!")

    def delete_science(self, science_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = """delete from testapp_science where id=?"""
        cur.execute(SQL, (science_id, ))
        conn.commit()
        conn.close()
        print(f"Fan o'chirildi!")

    def select_sciences(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_science"""
        cur.execute(SQL)
        res = cur.fetchall()
        conn.close()
        return res

    def select_science(self, science_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_science where id=?"""
        cur.execute(SQL, (science_id, ))
        res = cur.fetchone()
        conn.close()
        return res

    def column_names_class(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_classnumber"""
        cur.execute(SQL)
        res = [column[0] for column in cur.description]
        conn.close()
        return res

    def add_class(self, class_number):
        conn = self.connect
        cur = conn.cursor()
        SQL = """insert into testapp_classnumber(class_number)
            values
            (?)
        """
        cur.execute(SQL, (class_number, ))
        conn.commit()
        conn.close()
        print(f"{class_number}-sinf bazaga qo'shildi!")

    def update_class(self, class_id, number):
        conn = self.connect
        cur = conn.cursor()
        SQL = """update testapp_classnumber set class_number=? where id=?
        """
        cur.execute(SQL, (number, class_id))
        conn.commit()
        conn.close()
        print(f"{number}-sinf yangilandi!")

    def delete_class(self, class_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = """delete from testapp_classnumber where id=?"""
        cur.execute(SQL, (class_id, ))
        conn.commit()
        conn.close()
        print(f"Sinf o'chirildi!")

    def select_classes(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_classnumber order by class_number"""
        cur.execute(SQL)
        res = cur.fetchall()
        conn.close()
        return res

    def select_class(self, class_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_classnumber where id=?"""
        cur.execute(SQL, (class_id, ))
        res = cur.fetchone()
        conn.close()
        return res

    def column_names_tests(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_test"""
        cur.execute(SQL)
        res = [column[0] for column in cur.description]
        conn.close()
        return res

    def add_test(self, class_number_id, science_id, question, quantity, response, time, premium=False, amount=0, access=False):
        conn = self.connect
        cur = conn.cursor()
        SQL = """insert into testapp_test(access, question, quantity, response, premium, amount, time, class_number_id, science_id, at_time)
            values
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        tashkent_timezone = pytz.timezone('Asia/Tashkent')
        cur.execute(SQL, (access, question, quantity, response, premium, amount, time, class_number_id, science_id, datetime.now(tashkent_timezone)))
        conn.commit()
        conn.close()
        print(f"Yangi test bazaga qo'shildi!")

    def update_test(self, test_id, class_number_id, science_id, question, quantity, response, time, premium=False, amount=0, access=False):
        conn = self.connect
        cur = conn.cursor()
        SQL = """update testapp_test set access=?, question=?, quantity=?, response=?, premium=?, amount=?, time=?, class_number_id=?, science_id=?, at_time=? where id=?
        """
        tashkent_timezone = pytz.timezone('Asia/Tashkent')
        cur.execute(SQL, (access, question, quantity, response, premium, amount, time, class_number_id, science_id, datetime.now(tashkent_timezone), test_id))
        conn.commit()
        conn.close()
        print(f"Test o'zgartirildi!")

    def update_access_test(self, test_id):
        conn = self.connect
        cur = conn.cursor()
        res = cur.execute("select access from testapp_test where id=?", (test_id, )).fetchone()[0]
        SQL = """update testapp_test set access=? where id=?"""
        if res:
            cur.execute(SQL, (False, test_id))
        else:
            cur.execute(SQL, (True, test_id))
        conn.commit()
        conn.close()
        print(f"Testning faollik xususiyati o'zgardi!")

    def select_tests(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_test"""
        cur.execute(SQL)
        res = cur.fetchall()
        conn.close()
        return res

    def select_count_active_tests(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select count(*) from testapp_test where access=True"""
        cur.execute(SQL)
        res = cur.fetchone()[0]
        conn.close()
        return res

    def select_test(self, test_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_test where id=?"""
        cur.execute(SQL, (test_id, ))
        res = cur.fetchone()
        conn.close()
        return res

    def select_free_active_tests(self, class_number_id, science_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_test where class_number_id=? and science_id=? and premium=False and access=True"""
        cur.execute(SQL, (class_number_id, science_id))
        res = cur.fetchall()
        conn.close()
        return res

    def select_free_active_sorted_tests(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = """SELECT *
        FROM testapp_test
        WHERE premium = FALSE AND access = TRUE
        ORDER BY class_number_id, science_id;
        """
        cur.execute(SQL)
        res = cur.fetchall()
        conn.close()
        return res

    def select_free_no_active_tests(self, class_number_id, science_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_test where class_number_id=? and science_id=? and premium=False and access=False"""
        cur.execute(SQL, (class_number_id, science_id))
        res = cur.fetchall()
        conn.close()
        return res

    def select_free_no_active_sorted_tests(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = """SELECT *
        FROM testapp_test
        WHERE premium = FALSE AND access = FALSE
        ORDER BY class_number_id, science_id;
        """
        cur.execute(SQL)
        res = cur.fetchall()
        conn.close()
        return res

    def select_premium_active_tests(self, class_number_id, science_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_test where class_number_id=? and science_id=? and premium=True and access=True"""
        cur.execute(SQL, (class_number_id, science_id))
        res = cur.fetchall()
        conn.close()
        return res

    def select_premium_active_sorted_tests(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = """SELECT *
        FROM testapp_test
        WHERE premium = TRUE AND access = TRUE
        ORDER BY class_number_id, science_id;
        """
        cur.execute(SQL)
        res = cur.fetchall()
        conn.close()
        return res

    def select_premium_no_active_tests(self, class_number_id, science_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_test where class_number_id=? and science_id=? and premium=True and access=False"""
        cur.execute(SQL, (class_number_id, science_id))
        res = cur.fetchall()
        conn.close()
        return res

    def select_premium_no_active_sorted_tests(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = """SELECT *
        FROM testapp_test
        WHERE premium = TRUE AND access = FALSE
        ORDER BY class_number_id, science_id;
        """
        cur.execute(SQL)
        res = cur.fetchall()
        conn.close()
        return res

    def column_names_solvedtests(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_solvedtest"""
        cur.execute(SQL)
        res = [column[0] for column in cur.description]
        conn.close()
        return res

    def select_solvedtests(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_solvedtest"""
        cur.execute(SQL)
        res = cur.fetchall()
        conn.close()
        return res

    def select_test_solved_tests(self, test_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_solvedtest where test_id=? and start IS NOT NULL ORDER BY score DESC, start;"""
        cur.execute(SQL, (test_id, ))
        res = cur.fetchall()
        conn.close()
        return res

    def select_count_solvedtests(self):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select count(*) from testapp_solvedtest where start IS NOT NULL"""
        cur.execute(SQL)
        res = cur.fetchone()[0]
        conn.close()
        return res

    def select_solvedtest(self, solvedtest_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_solvedtest where id=?"""
        cur.execute(SQL, (solvedtest_id,))
        res = cur.fetchone()
        conn.close()
        return res

    def select_user_solvedtest(self, user_id, test_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_solvedtest where user_id=? and test_id=?"""
        cur.execute(SQL, (user_id, test_id))
        res = cur.fetchone()
        conn.close()
        return res

    def select_user_solvedtests_ids(self, user_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select test_id from testapp_solvedtest where user_id=? and start IS NOT NULL"""
        cur.execute(SQL, (user_id, ))
        res = cur.fetchall()
        res = tuple(map(lambda array: array[0], res))
        conn.close()
        return res

    def select_user_solved_tests(self, user_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_solvedtest where user_id=? and start IS NOT NULL order by start desc"""
        cur.execute(SQL, (user_id, ))
        res = cur.fetchall()
        conn.close()
        return res

    def add_solvedtest(self, user_id, test_id, check_image=None):
        conn = self.connect
        cur = conn.cursor()
        cur.execute("select premium from testapp_test where id=?", (test_id, ))
        premium = cur.fetchone()[0]
        SQL = """insert into testapp_solvedtest(user_id, test_id, permission, progress, quantity, score, check_image)
                    values
                    (?, ?, ?, ?, ?, ?, ?)
                """
        cur.execute(SQL, (user_id, test_id, not premium, False, 0, 0, check_image))
        conn.commit()
        conn.close()
        print(f"id: {user_id} foydalanuvchi test_id: {test_id} testni yechmoqchi!")

    def get_permission_user_test(self, user_id, test_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = """select * from testapp_solvedtest where user_id=? and test_id=?"""
        cur.execute(SQL, (user_id, test_id))
        res = cur.fetchone()
        conn.close()
        if res is None:
            return False
        return [1]

    def update_permission_solvedtest(self, user_id, test_id):
        conn = self.connect
        cur = conn.cursor()
        SQL = """update testapp_solvedtest set permission=? where user_id=? and test_id=?"""
        cur.execute(SQL, (True, user_id, test_id))
        conn.commit()
        conn.close()
        print(f"id: {user_id} foydalanuvchi test_id: {test_id} testni yechish uchun ruxsat oldi!")

    def update_check_image_solved_test(self, user_id, test_id, check_image):
        conn = self.connect
        cur = conn.cursor()
        SQL = """update testapp_solvedtest set check_image=? where user_id=? and test_id=?"""
        cur.execute(SQL, (check_image, user_id, test_id))
        conn.commit()
        conn.close()
        print(f"id: {user_id} foydalanuvchi test_id: {test_id} testni yechish uchun to'lov chekini yubordi!")

    def start_progress_solvedtest(self, user_id, test_id, start, stop):
        conn = self.connect
        cur = conn.cursor()
        cur.execute("select quantity from testapp_solvedtest where user_id=? and test_id=?", (user_id, test_id))
        quantity = cur.fetchone()[0]
        SQL = """update testapp_solvedtest set progress=?, start=?, stop=?, quantity=? where user_id=? and test_id=?"""
        cur.execute(SQL, (True, start, stop, quantity+1, user_id, test_id))
        conn.commit()
        conn.close()
        print(f"id: {user_id} foydalanuvchi test_id: {test_id} testni yechmoqda!")

    def update_quantity_solvedtest(self, user_id, test_id):
        conn = self.connect
        cur = conn.cursor()
        cur.execute("select quantity from testapp_solvedtest where user_id=? and test_id=?", (user_id, test_id))
        quantity = cur.fetchone()[0]
        SQL = """update testapp_solvedtest set quantity=? where user_id=? and test_id=?"""
        cur.execute(SQL, (quantity+1, user_id, test_id))
        conn.commit()
        conn.close()
        print(f"id: {user_id} foydalanuvchi test_id: {test_id} testni yana yechishni amalga oshirdi!")

    def stop_progress_solvedtest(self, user_id, test_id, score, certificate=None):
        conn = self.connect
        cur = conn.cursor()
        SQL = """update testapp_solvedtest set score=?, certificate=? where user_id=? and test_id=?"""
        cur.execute(SQL, (score, certificate, user_id, test_id))
        conn.commit()
        conn.close()
        print(f"id: {user_id} foydalanuvchi test_id: {test_id} testni yechib boldi!")
