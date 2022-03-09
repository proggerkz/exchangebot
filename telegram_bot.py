from create_bot import dp
from aiogram.utils import executor
from russian import russian, other
from admin import admin

russian.register_step_russian(dp)
admin.register_step_admin(dp)
other.check_text(dp)
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
