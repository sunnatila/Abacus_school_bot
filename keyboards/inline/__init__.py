from . import checksubs
from .ref_inline_button import create_ref_link
from .admin_settings import settings_callback_data, make_sciences_inlines, make_class_inlines
from .confirm_buttons import confirm_responses_button, premium_or_free_test_button, activate_callback_data, \
    access_test_button
from .all_tests import make_all_tests_inlines, all_test_callback_data, activate_test_buttons, de_activate_test_buttons, \
    edit_test_buttons
from .test_solution import solution_test_cd, check_test_cd, admin_check_test_cd, make_check_cd, update_permission_button
from .test_solution import sciences_keyboards, classes_keyboards, tests_keyboards, confirm_button, check_test_button, \
    buy_button, transfer_type_keyboards, certificate_download, download_certificate_cd
from .result_tests import result_tests_callback_data, result_tests_inlines, result_test_inline, back_result_inline
