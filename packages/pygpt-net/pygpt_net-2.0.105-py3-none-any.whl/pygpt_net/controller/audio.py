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

from pygpt_net.core.dispatcher import Event
from pygpt_net.item.ctx import CtxItem


class Audio:
    def __init__(self, window=None):
        """
        Audio/voice controller

        :param window: Window instance
        """
        self.window = window

    def setup(self):
        """Setup controller"""
        self.update()

    def toggle_input(self, state: bool, btn: bool = True):
        """Toggle audio/voice"""
        self.window.core.dispatcher.dispatch(Event('audio.input.toggle', {"value": state}))

    def toggle_output(self):
        """Toggle audio/voice"""
        if self.window.controller.plugins.is_enabled('audio_azure'):
            self.disable_output()
        else:
            self.enable_output()

    def enable_output(self):
        """Enable audio/voice"""
        self.window.controller.plugins.enable('audio_azure')
        if self.window.controller.plugins.is_enabled('audio_azure') \
                and (self.window.core.plugins.plugins['audio_azure'].options['azure_api_key'] is None
                     or self.window.core.plugins.plugins['audio_azure'].options['azure_api_key'] == ''):
            self.window.ui.dialogs.alert("Azure API KEY is not set. Please set it in plugins settings.")
            self.window.controller.plugins.disable('audio_azure')
        self.window.core.config.save()
        self.update()

    def disable_output(self):
        """Disable audio/voice"""
        self.window.controller.plugins.disable('audio_azure')
        self.window.core.config.save()
        self.update()

    def disable_input(self, update: bool = True):
        """Disable audio/voice"""
        self.window.controller.plugins.disable('audio_openai_whisper')
        self.window.core.config.save()
        if update:
            self.update()

    def stop_input(self):
        """Stop audio/voice"""
        self.window.core.dispatcher.dispatch(Event('audio.input.stop', {"value": True}), True)

    def stop_output(self):
        """Stop audio/voice"""
        self.window.core.dispatcher.dispatch(Event('audio.output.stop', {"value": True}), True)

    def update(self):
        """Update UI and listeners"""
        self.update_listeners()
        self.update_menu()

    def is_output_enabled(self) -> bool:
        """
        Check if any audio output is enabled

        :return: True if enabled
        """
        if self.window.controller.plugins.is_enabled('audio_azure') \
                or self.window.controller.plugins.is_enabled('audio_openai_tts'):
            return True
        return False

    def update_listeners(self):
        """Update listeners"""
        is_output = False
        if self.window.controller.plugins.is_enabled('audio_azure'):
            is_output = True
        if self.window.controller.plugins.is_enabled('audio_openai_tts'):
            is_output = True
        if not is_output:
            self.stop_output()

        if not self.window.controller.plugins.is_enabled('audio_openai_whisper'):
            self.toggle_input(False)
            self.stop_input()
            if self.window.ui.plugin_addon['audio.input'].btn_toggle.isChecked():
                self.window.ui.plugin_addon['audio.input'].btn_toggle.setChecked(False)

    def update_menu(self):
        """Update menu"""
        if self.window.controller.plugins.is_enabled('audio_azure'):
            self.window.ui.menu['audio.output.azure'].setChecked(True)
        else:
            self.window.ui.menu['audio.output.azure'].setChecked(False)

        if self.window.controller.plugins.is_enabled('audio_openai_tts'):
            self.window.ui.menu['audio.output.tts'].setChecked(True)
        else:
            self.window.ui.menu['audio.output.tts'].setChecked(False)

        if self.window.controller.plugins.is_enabled('audio_openai_whisper'):
            self.window.ui.menu['audio.input.whisper'].setChecked(True)
        else:
            self.window.ui.menu['audio.input.whisper'].setChecked(False)

    def read_text(self, text: str):
        """
        Process selected text

        :param text: selected text
        """
        ctx = CtxItem()
        ctx.output = text
        all = False
        if self.window.controller.audio.is_output_enabled():
            event = Event('ctx.after')
        else:
            all = True
            event = Event('audio.read_text')  # to all plugins (even if disabled)
        event.ctx = ctx
        self.window.core.dispatcher.dispatch(event, all)
