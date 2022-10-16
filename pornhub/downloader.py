import os
import asyncio

from .config import log_chat, sub_chat
from .function import download_progress_hook
from pornhub_api import PornhubApi
from pornhub_api.backends.aiohttp import AioHttpBackend
from youtube_dl.utils import DownloadError

from pyrogram import Client, filters
from pyrogram.types import (
    Message, InlineQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    CallbackQuery,
    InlineQueryResultArticle,
    InputTextMessageContent,
)
from pyrogram.errors import ChatAdminRequired, UserNotParticipant, ChatWriteForbidden


if os.path.exists("downloads"):
    print("file is exists")
else:
    print("file has made")


active = []
queues = []


async def run_async(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None, func, *args, **kwargs)


def url(filter, client, update):
    if "www.pornhub" in update.text:
        return True
    else:
        return False

url_filter = filters.create(url, name="url_filter")


@Client.on_message(~filters.edited & filters.incoming & filters.private, group=-1)
async def force_channel(c: Client, u: Message):
    if not sub_chat:
        return
    try:
        try:
            await c.get_chat_member(sub_chat, u.from_user.id)
        except UserNotParticipant:
            if sub_chat.isalpha():
                url = "https://t.me/" + sub_chat
            else:
                chat_info = await c.get_chat(sub_chat)
                url = chat_info.invite_link
            try:
                await u.reply_text(
                    f"Hi {u.from_user.first_name}!\n\nYou must join the redirected channel in order to use this bot, if you've done it, please restart this bot!",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("• Join Channel •", url=url),
                            ],
                        ],
                    ),
                )
                await u.stop_propagation()
            except ChatWriteForbidden:
                pass
    except ChatAdminRequired:
        c.send_message(log_chat, "Can't manage the provided channel, make sure I'm the admin on the channel!")


@Client.on_inline_query()
async def inline_search(c: Client, q: InlineQuery):
    query = q.query
    backend = AioHttpBackend()
    api = PornhubApi(backend=backend)
    results = []
    try:
        src = await api.search.search(query)
    except ValueError as e:
        results.append(
            InlineQueryResultArticle(
                title="I can't found it!",
                description="The video can't be found, try again later.",
                input_message_content=InputTextMessageContent(
                    message_text="video not found!"
                ),
            ),
        )
        await InlineQuery.answer(
            results,
            switch_pm_text="• Results •",
            switch_pm_parameter="start",
        )

        return


    videos = src.videos
    await backend.close()
    

    for vid in videos:

        try:
            pornstars = ", ".join(v for v in vid.pornstars)
            categories = ", ".join(v for v in vid.categories)
            tags = ", #".join(v for v in vid.tags)
        except:
            pornstars = "N/A"
            categories = "N/A"
            tags = "N/A"
        capt = (f"Title: `{vid.title}`\n"
                f"Duration: `{vid.duration}`\n"
                f"Views: `{vid.views}`\n\n"
                f"**{pornstars}**\n"
                f"Category: {categories}\n\n"
                f"{tags}"
                f"Link: {vid.url}")

        text = f"{vid.url}"
         
        results.append(
            InlineQueryResultArticle(
                title=vid.title,
                input_message_content=InputTextMessageContent(
                    message_text=msg,
                ),
            ),
        )
        description=f"Duration: `{vid.duration}`\nViews: `{vid.views}`\nRating: `{vid.rating}`",
        thumb_url=vid.thumb,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("watch in web", url=vid.url),
                ],
            ],
        )

    await InlineQuery.answer(
        results,
        switch_pm_text="• Results •",
        switch_pm_parameter="start",
    )


@app.on_message(url_filter)
async def options(c: Client, m: Message):
    print(m.text)
    await m.reply_text(
        "Tap the button to continue action!", 
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Download", callback_data=f"d_{m.text}",
                    ),
                ],[
                    InlineKeyboardButton(
                        "watch in web", url=m.text,
                    ),
                ],
            ],
        ),
    )


@app.on_callback_query(filters.regex("^d"))
async def get_video(c: Client, q: CallbackQuery):
    url = q.data.split("_",1)[1]
    msg = await q.message.edit("Downloading...")
    user_id = q.message.from_user.id

    if "some" in active:
        await q.message.edit("Sorry, you can only download videos at a time!")
        return
    else:
        active.append(user_id)

    ydl_opts = {
            "progress_hooks": [lambda d: download_progress_hook(d, q.message, c)]
        }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            await run_async(ydl.download, [url])
        except DownloadError:
            await q.message.edit("Sorry, an error occurred")
            return


    for file in os.listdir('.'):
        if file.endswith(".mp4"):
            await q.message.reply_video(
                f"{file}",
                caption="The content you requested has been successfully downloaded, enjoy!",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("• Donate •", url="https://trakteer.id/levina-crqid/tip"),
                        ],
                    ],
                ),
            )
            os.remove(f"{file}")
            break
        else:
            continue


    await msg.delete()
    active.remove(user_id)