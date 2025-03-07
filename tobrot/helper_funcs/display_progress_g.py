#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import math
import os
import time

from tobrot import (
    FINISHED_PROGRESS_STR,
    UN_FINISHED_PROGRESS_STR,
    EDIT_SLEEP_TIME_OUT
)


async def progress_for_pyrogram_g(
    current,
    total,
    ud_type,
    message,
    start
):
    """ generic progress display for Telegram Upload / Download status """
    now = time.time()
    diff = now - start
    if round(diff % 10.00) == 0 or current == total:
        # if round(current / total * 100, 0) % 5 == 0:
        percentage = current * 100 / total
        speed = current / diff
        elapsed_time = round(diff) * 1000
        time_to_completion = round((total - current) / speed) * 1000
        estimated_total_time = elapsed_time + time_to_completion

        elapsed_time = time_formatter(milliseconds=elapsed_time)
        estimated_total_time = time_formatter(milliseconds=estimated_total_time)

        progress = "╭────── ⌊ 📥 Downloading ⌉</b>\n<b>│ </b>\n<b>├〚 {0}{1} 〛{2}</b>\n<b>│</b>".format(
            ''.join([FINISHED_PROGRESS_STR for i in range(math.floor(percentage / 5))]),
            ''.join([UN_FINISHED_PROGRESS_STR for i in range(20 - math.floor(percentage / 5))]),
            round(percentage, 2))

        tmp = progress + "\n<b>├ Done : {0}</b>\n<b>├ Total : {1}</b>\n</b>├ Speed : {2}</b>\n<b>├ ETA : {3}</b>\n│</b>\n<b>│</b>\n<b><b>│   ╔╦═══• •✠•❀  ❀•✠• •═══╦╗</b>\n<b>╰─⟰  ᴜsɪɴɢ ᴇɴɢɪɴᴇ ᴘʏʀᴏɢʀᴀᴍ  ⟱ </b>\n<b>      ╚╩═══• •✠•❀  ❀•✠• •═══╩╝</b>".format(
            humanbytes(current),
            humanbytes(total),
            humanbytes(speed),
            # elapsed_time if elapsed_time != '' else "0 s",
            estimated_total_time if estimated_total_time != '' else "0 s"
        )
        try:
            await message.edit(
                "{}\n {}".format(
                    ud_type,
                    tmp
                )
            )
        except:
            pass


def humanbytes(size: int) -> str:
    """ converts bytes into human readable format """
    # https://stackoverflow.com/a/49361727/4723940
    # 2**10 = 1024
    if not size:
        return ""
    power = 2 ** 10
    number = 0
    dict_power_n = {
        0: " ",
        1: "Ki",
        2: "Mi",
        3: "Gi",
        4: "Ti"
    }
    while size > power:
        size /= power
        number += 1
    return str(round(size, 2)) + " " + dict_power_n[number] + 'B'


def time_formatter(milliseconds: int) -> str:
    """ converts seconds into human readable format """
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + "d, ") if days else "") + \
        ((str(hours) + "h, ") if hours else "") + \
        ((str(minutes) + "m, ") if minutes else "") + \
        ((str(seconds) + "s, ") if seconds else "") + \
        ((str(milliseconds) + "ms, ") if milliseconds else "")
    return tmp[:-2]
