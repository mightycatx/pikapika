#!/usr/bin/env python3
#
# Copyright (C) 2020 by ItzSjDude@Github, < https://github.com/ItzSjDude/PikachuUserbot >.
#
# This file is part of < https://github.com/ItzSjDude/PikachuUserbot > project,
# and is released under the "GNU v3.0 License Agreement".
#
# Please see < https://github.com/ItzSjDude/PikachuUserbot/blob/master/LICENSE >
#
# All rights reserved

from . import pikabot
import asyncio 
import uvloop
pikaloop = uvloop.new_event_loop()
asyncio.set_event_loop(pikloop)

if __name__ == "__main__":  
    pikaloop.run_until_complete(pikabot())
