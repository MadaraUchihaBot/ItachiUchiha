import time
import importlib

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from pyrogram.handlers import CallbackQueryHandler

from Itachi import app  # Assuming you have initialized the Pyrogram app as 'app'
from Itachi.database import sql_adduser  # Update the import path accordingly
from Itachi.helpers import create_menu
from Itachi.tools.time import get_readable_time

# Import your modules
from Itachi.Plugin import info, greeting, banunban, muteunmute

# Define your START_TXT, HELP_TXT, and ABOUT_TXT here
START_TXT = "Im alive master, still in development.\n\n" \
            "It is gonna be an open source public group management bot with all latest features and modules.\n\n" \
            "- My developer: @ishikki_akabane\n" \
            "- Alive since {}"

HELP_TXT = "wait, bot is still in development\n\n" \
           "Visit @devslab or contact @ishikki_akabane"

ABOUT_TXT = "waitooooo broo\nbot is still in development\n:)"

# Your start command handler
@app.on_message(filters.command("start"))
async def start_command(_, message):
    uptime = get_readable_time((time.time() - StartTime))
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="☑ Add ItachiBot ☑",
                    url="t.me/RukaProbot?startgroup=true"
                )
            ],
            [
                InlineKeyboardButton(text="OWNER", url="tg://user?id=your_owner_id"),
                InlineKeyboardButton(text="ABOUT", callback_data="ishikki=about")
            ],
            [
                InlineKeyboardButton(text="updates", url="t.me/updatesxd"),
                InlineKeyboardButton(text="commands", callback_data="ishikki=help")
            ]
        ]
    )
    await message.reply_video(
        video=ISHIKKI_IMAGE.RUKA_IMG_START,
        caption=START_TXT.format(uptime),
        reply_markup=keyboard
    )

# Your help command handler
@app.on_message(filters.command("help"))
async def help_command(_, message):
    keyboard = await create_menu()
    await message.reply_video(
        video=ISHIKKI_IMAGE.RUKA_IMG_START,
        caption=HELP_TXT,
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=keyboard
    )

# Callback function for handling button presses
@app.callback_query_handler(filters.regex(r"^module=(.*)"))
async def button_callback(query):
    data = query.data
    if data.split("=")[0] == "module":
        module_name = data.split('=')[1]
        module = importlib.import_module(f'Itachi.Plugin.{module_name}')
        help_text = getattr(module, '__help__', 'No help available.')
        await query.edit_message_caption(
            caption=help_text,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton(text="Back", callback_data="ishikki=help")]
                ]
            )
        )

# Callback function for handling custom callbacks (ishikki)
@app.callback_query_handler(filters.regex(r"^ishikki=(.*)"))
async def custom_callback(query):
    data = query.data
    if data.split("=")[0] == "ishikki":
        if data.split("=")[1] == "help":
            keyboard = await create_menu()
            await query.edit_message_caption(
                caption=HELP_TXT,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=keyboard
            )
        elif data.split("=")[1] == "about":
            await query.edit_message_caption(
                caption=ABOUT_TXT,
                parse_mode=ParseMode.MARKDOWN
            )
        elif data.split("=")[1] == "back_btn":
            uptime = get_readable_time((time.time() - StartTime))
            await query.edit_message_caption(
                caption=START_TXT.format(uptime),
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="☑ Add ItachiBot ☑",
                                url="t.me/RukaProbot?startgroup=true"
                            )
                        ],
                        [
                            InlineKeyboardButton(text="OWNER", url="tg://user?id=your_owner_id"),
                            InlineKeyboardButton(text="ABOUT", callback_data="ishikki=about")
                        ],
                        [
                            InlineKeyboardButton(text="updates", url="t.me/updatesxd"),
                            InlineKeyboardButton(text="commands", callback_data="ishikki=help")
                        ]
                    ]
                )
            )
        else:
            await query.edit_message_caption(
                caption=ABOUT_TXT,
                parse_mode=ParseMode.MARKDOWN
            )

# Error handler
@app.on_error()
async def error_handler(_, error):
    # Your error handling logic here
    pass

# Register your plugin handlers
info.register(app)
greeting.register(app)
banunban.register(app)
muteunmute.register(app)

if __name__ == "__main__":
    app.run()
