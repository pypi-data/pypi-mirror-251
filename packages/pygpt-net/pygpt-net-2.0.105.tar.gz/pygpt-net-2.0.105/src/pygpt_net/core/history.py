#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.31 04:00:00                  #
# ================================================== #

from pygpt_net.item.ctx import CtxItem
from pygpt_net.provider.history.txt_file import TxtFileProvider


class History:

    def __init__(self, window):
        """
        History core

        :param window: Window instance
        """
        self.window = window
        self.provider = TxtFileProvider(window)
        self.path = None

    def install(self):
        """Install provider data"""
        self.provider.install()

    def append(self, ctx: CtxItem, mode: str):
        """
        Append text to history

        :param ctx: CtxItem instance
        :param mode: mode (input | output)
        """
        self.provider.append(ctx, mode)
