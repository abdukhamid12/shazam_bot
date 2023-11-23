from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

menu = InlineKeyboardMarkup(row_width=1)

menu.add(
  InlineKeyboardButton("Рассылка", callback_data="rassilka")
)