import re
import logging

from pyrogram import filters
from pyrogram.types import InlineQuery, CallbackQuery, Message
from pyrogram.enums import ParseMode

from test_tele.features.pyrogram.pixiv import inline_pixiv, get_px_file
from test_tele.features.pyrogram.gelbooru import inline_gelbooru, get_gb_file
from test_tele.features.pyrogram.tsumino import inline_tsumino, generate_telegraph, cari_konten
from test_tele.features.pyrogram.pornpics import inline_pornpics, get_pp_file
from test_tele.features.pyrogram.furry import inline_furry, get_fur_file


async def run_pyrogram():
    from test_tele.live_pyrogram import APP
    app = APP

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    @app.on_message(filters.text | filters.photo)
    async def incoming_message_handler(app, message: Message):
        """Handle spesific incoming message"""
        try:
            if message.text:
                pattern = r'ID\s\:\s(.+)'
                match = re.search(pattern, message.text)
                if match:
                    telepages = await cari_konten(match.group(1))
                    if not telepages:
                        await generate_telegraph(match.group(1))
            elif message.photo:
                logging.warning("ya ini photo")
                # logging.warning(message.photo)
                
        except Exception as err:
            logging.error(err, exc_info=True)
    

    @app.on_inline_query()
    async def inline_handler(app, inline_query: InlineQuery):
        """Handle inline query search"""
        query_handlers = {
            '.md': inline_tsumino,
            '.px': inline_pixiv,
            '.rp': inline_pornpics,
            '.fur': inline_furry
            # '.2d': inline_vanillarock
        }

        for query_prefix, handler in query_handlers.items():
            if inline_query.query.lower().startswith(query_prefix):
                await handler(app, inline_query)
                break
        else:
            await inline_gelbooru(app, inline_query)


    @app.on_callback_query(filters.regex(r"(?:md|gb|px|rp|fur|2d)"))
    async def callback_query_handler(app, callback_query: CallbackQuery):
        """Get callback query from inline keyboard"""
        handlers = {
            "md": None,
            "gb": get_gb_file,
            "px": get_px_file,
            "rp": get_pp_file,
            "fur": get_fur_file
            # "2d": get_vr_file
        }

        for prefix, handler in handlers.items():
            if callback_query.data.startswith(prefix):
                if prefix == "md":
                    telepages = await cari_konten(callback_query.data.replace(f"{prefix} ", ''))
                    if not telepages:
                        return await app.send_message(callback_query.from_user.id, 'Please wait while the telegraph is being generated')

                    text = f"[{telepages[0]['title']}]({telepages[0]['url']})\nAuthor : {telepages[0]['author_name']}"
                    return await app.send_message(
                        callback_query.from_user.id,
                        text,
                        parse_mode=ParseMode.MARKDOWN,
                        disable_notification=True,
                        protect_content=True
                    )
                else:
                    image_file = await handler(callback_query.data.replace(f"{prefix} ", ''))
                    await app.send_document(callback_query.from_user.id, image_file)
                    break
        else:
            pass


    await app.start()