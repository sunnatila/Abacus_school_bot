from datetime import datetime
from pprint import pprint

from utils.db_api.sql_commands import Database

# obj = Database()
# print(obj.select_user("sdvs"))
# print(obj.column_names_user())
# obj.add_user("1234qwe", "Ilhomjon", "94746131", "ascasvsvsv")
# print(obj.select_users())
# print(obj.select_user("e232f3"))
# obj.update_suggestion('e232f3')
# obj.update_user('e232f3', "Ilxomjon", 916589340)
# obj.delete_user('e232f3')
# obj.add_user("e232f3", "Ali Valiyev", 916589465, "ecevvrveve")
# print(obj.column_names_science())
# obj.add_science("Fizika")
# print(obj.select_sciences())  # 1
# print(obj.column_names_class())
# obj.add_class(5)
# print(obj.select_classes())  # 1
# print(obj.column_names_tests())
# obj.add_test(3, 2, "vevevre", 10, "qwefwef", 60, True, 10, True)
# obj.update_access_test(5)
# print(obj.select_tests())
# print(obj.select_free_active_tests(3, 2))
# print(obj.select_test(5)[10])
# print(obj.select_free_tests(1, 1))
# print(obj.select_premium_active_tests(3, 2))
# print(obj.column_names_solvedtests())
# print(obj.select_solvedtests())
# pprint(obj.select_solvedtests())
# obj.update_permission_solvedtest('e232f3', 1)
# obj.start_progress_solvedtest('e232f3', 1, datetime.now(), datetime.now())
# print(obj.select_free_solvedtests('e232f3', 1, 1))
# print(obj.select_premium_solvedtests('e232f3', 1, 1))
# print(obj.select_user_solvedtest('e232f3', 3))
# obj.add_solvedtest('e232f3', 5)
# obj.update_permission_solvedtest('e232f3', 5)
# print(obj.column_names_solvedtests())
# obj.start_progress_solvedtest('e232f3', 5, datetime.now(), datetime.now())
# obj.stop_progress_solvedtest('e232f3', 5, 50)
# print(obj.select_user_solvedtest('e232f3', 5))
# obj.add_test(3, 2, "vevevre", 10, "qwefwef", 60, True, 10000, True)
# print(obj.select_premium_active_sorted_tests())
