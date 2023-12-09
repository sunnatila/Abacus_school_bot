from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from data.config import click_url, xazna_url, uzum_url
from loader import db

solution_test_cd = CallbackData('solution_test', 'level', 'science_id', 'class_id', 'test_id', 'confirm', 'price',
                                'transfer')
check_test_cd = CallbackData('check_test', 'test_id')


async def make_callback_data(level, science_id='0', class_id='0', test_id='0', confirm='0', price='0', transfer=''):
    return solution_test_cd.new(level=level, science_id=science_id, class_id=class_id, test_id=test_id, confirm=confirm,
                                price=price, transfer=transfer)


async def sciences_keyboards():
    CURRENT_LEVEL = 0

    markup = InlineKeyboardMarkup(row_width=2)
    sciences = db.select_sciences()

    for category in sciences:
        markup.insert(InlineKeyboardButton(
            text=category[1],
            callback_data=await make_callback_data(
                level=CURRENT_LEVEL + 1,
                science_id=category[0],
            )
        )
        )
    markup.insert(InlineKeyboardButton(text='❌', callback_data=await make_callback_data(CURRENT_LEVEL - 1)))
    return markup


async def classes_keyboards(science_id):
    CURRENT_LEVEL = 1

    markup = InlineKeyboardMarkup(row_width=2)
    classes = db.select_classes()

    for product in classes:
        markup.insert(
            InlineKeyboardButton(
                text=f"{product[1]}-sinf",
                callback_data=await make_callback_data(CURRENT_LEVEL + 1, science_id, class_id=product[0])
            )
        )
    markup.insert(InlineKeyboardButton(
        text='🔙 Orqaga', callback_data=await make_callback_data(CURRENT_LEVEL - 1)
    ))

    return markup


async def tests_keyboards(user_id, premium, science_id, class_id):
    CURRENT_LEVEL = 2

    markup = InlineKeyboardMarkup(row_width=2)
    if premium:
        tests = db.select_premium_active_tests(class_id, science_id)
    else:
        tests = db.select_free_active_tests(class_id, science_id)

    solved_tests = db.select_user_solvedtests_ids(user_id)
    i = 1
    for test in tests:
        if test[0] in solved_tests:
            text = f"{i}-test ✅"
        else:
            if premium:
                if db.get_permission_user_test(user_id, test[0]):
                    text = f"{i}-test ✔️"
                else:
                    text = f"{i}-test"
            else:
                text = f"{i}-test"
        markup.insert(
            InlineKeyboardButton(
                text=text,
                callback_data=await make_callback_data(
                    CURRENT_LEVEL + 1,
                    science_id=science_id,
                    class_id=class_id,
                    test_id=test[0]
                )
            )
        )
        i += 1
    markup.insert(InlineKeyboardButton(text="🔙 Orqaga", callback_data=await make_callback_data(CURRENT_LEVEL - 1,
                                                                                               science_id=science_id)))

    return markup


async def confirm_button(science_id, class_id, test_id):
    CURRENT_LEVEL = 3

    markup = InlineKeyboardMarkup(row_width=1)

    markup.insert(
        InlineKeyboardButton(
            text="✍🏻 Testni boshlash",
            callback_data=await make_callback_data(
                level=CURRENT_LEVEL + 1,
                science_id=science_id,
                class_id=class_id,
                test_id=test_id,
                confirm='1'
            )
        )
    )
    markup.insert(InlineKeyboardButton(text="🔙 Orqaga", callback_data=await make_callback_data(CURRENT_LEVEL - 1,
                                                                                               science_id=science_id,
                                                                                               class_id=class_id)))
    return markup


async def buy_button(science_id, class_id, test_id):
    CURRENT_LEVEL = 3

    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text="🔙 Orqaga", callback_data=await make_callback_data(CURRENT_LEVEL - 1,
                                                                                               science_id=science_id,
                                                                                               class_id=class_id)))
    markup.insert(
        InlineKeyboardButton(
            text="💳 Karta orqali",
            callback_data=await make_callback_data(
                level=CURRENT_LEVEL + 1,
                science_id=science_id,
                class_id=class_id,
                test_id=test_id,
            )
        )
    )
    return markup


async def buy2_button(science_id, class_id, test_id):
    CURRENT_LEVEL = 3

    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(InlineKeyboardButton(text="🔙 Orqaga", callback_data=await make_callback_data(CURRENT_LEVEL - 1,
                                                                                               science_id=science_id,
                                                                                               class_id=class_id, )))
    markup.insert(
        InlineKeyboardButton(
            text="💳 Qayta to'lov",
            callback_data=await make_callback_data(
                level=CURRENT_LEVEL + 1,
                science_id=science_id,
                class_id=class_id,
                test_id=test_id,
            )
        )
    )
    return markup


async def transfer_type_keyboards(science_id, class_id, test_id, price):
    CURRENT_LEVEL = 4

    markup = InlineKeyboardMarkup(row_width=1)

    markup.insert(
        InlineKeyboardButton(
            text="Click Up ilovasi orqali",
            callback_data=await make_callback_data(
                level=CURRENT_LEVEL + 1,
                science_id=science_id,
                class_id=class_id,
                test_id=test_id,
                price=price,
                transfer='click',
            )
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text="Uzum bank ilovasi orqali",
            callback_data=await make_callback_data(
                level=CURRENT_LEVEL + 1,
                science_id=science_id,
                class_id=class_id,
                test_id=test_id,
                price=price,
                transfer='uzum',
            )
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text="Xazna ilovasi orqali",
            callback_data=await make_callback_data(
                level=CURRENT_LEVEL + 1,
                science_id=science_id,
                class_id=class_id,
                test_id=test_id,
                price=price,
                transfer='xazna',
            )
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text="Karta raqam orqali",
            callback_data=await make_callback_data(
                level=CURRENT_LEVEL + 1,
                science_id=science_id,
                class_id=class_id,
                test_id=test_id,
                price=price,
                transfer='karta',
            )
        )
    )
    markup.insert(InlineKeyboardButton(text="🔙 Orqaga", callback_data=await make_callback_data(CURRENT_LEVEL - 1,
                                                                                               science_id=science_id,
                                                                                               class_id=class_id,
                                                                                               test_id=test_id,
                                                                                               price=price)))
    return markup


async def transfer_success_keyboards(science_id, class_id, test_id, price, transfer_type):
    CURRENT_LEVEL = 5

    markup = InlineKeyboardMarkup(row_width=1)
    if transfer_type == "xazna":
        url = xazna_url
    elif transfer_type == "uzum":
        url = uzum_url
    else:
        url = click_url

    markup.insert(
        InlineKeyboardButton(
            text="📲 Ilovaga o'tish", url=url
        )
    )
    markup.insert(InlineKeyboardButton(text="🔙 Orqaga", callback_data=await make_callback_data(CURRENT_LEVEL - 1,
                                                                                               science_id=science_id,
                                                                                               class_id=class_id,
                                                                                               test_id=test_id,
                                                                                               price=price)))
    return markup


async def check_test_button(test_id):
    markup = InlineKeyboardMarkup(row_width=1)

    markup.insert(
        InlineKeyboardButton(text="🏁 Testni tekshirish", callback_data=check_test_cd.new(test_id=test_id))
    )
    return markup

admin_check_test_cd = CallbackData('check', 'test_id', 'user_id', 'transfer', 'permission')


async def make_check_cd(test_id, user_id, transfer, permission):
    return admin_check_test_cd.new(test_id=test_id, user_id=user_id, transfer=transfer, permission=permission)


async def update_permission_button(test_id, user_id, transfer):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.insert(
        InlineKeyboardButton(
            text="✅ Ruxsat berish",
            callback_data=await make_check_cd(test_id, user_id, transfer=transfer, permission='true')
        )
    )
    markup.insert(
        InlineKeyboardButton(
            text="🚫 Rad etish",
            callback_data=await make_check_cd(test_id, user_id, transfer=transfer, permission='false')
        )
    )
    return markup


download_certificate_cd = CallbackData('certificate', 'user_id', 'test_id')


async def certificate_download(user_id, test_id):
    certificate_download_markup = InlineKeyboardMarkup(row_width=1)
    certificate_download_markup.insert(
        InlineKeyboardButton(
            text="🖨 Sertifikat",
            callback_data=download_certificate_cd.new(user_id=user_id, test_id=test_id)
        )
    )
    return certificate_download_markup
