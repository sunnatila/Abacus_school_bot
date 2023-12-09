from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn
ADMINS = env.list("ADMINS")  # adminlar ro'yxati
IP = env.str("ip")  # Xosting ip manzili
CHANNELS = ["@abacusschool_ls"]  # @kanal2023kan

click_url = env.str("click_url")
click_qr = env.str("click_qr")

uzum_url = env.str("uzum_url")
uzum_qr = env.str("uzum_qr")

xazna_url = env.str("xazna_url")
xazna_qr = env.str("xazna_qr")

karta = env.str("karta")
karta_name = env.str("karta_name")

bot_image = env.str("bot_image")
