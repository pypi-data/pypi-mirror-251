#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2023.12.25 21:00:00                  #
# ================================================== #

from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenu

from pygpt_net.utils import trans


class Menu:
    def __init__(self, window=None):
        """
        Menu setup

        :param window: Window instance
        """
        self.window = window

    def setup(self):
        """Setups all menus"""
        self.window.ui.menu = {}
        self.setup_file()
        self.setup_plugins()
        self.setup_audio()
        self.setup_config()
        self.setup_lang()
        self.setup_theme()
        self.setup_about()

        # debug menu
        if self.window.core.config.get('debug'):
            self.setup_debug()

    def setup_file(self):
        """Setup file menu"""
        self.window.ui.menu['app.exit'] = QAction(QIcon.fromTheme("application-exit"), trans("menu.file.exit"),
                                                  self.window, shortcut="Ctrl+Q", triggered=self.window.close)

        self.window.ui.menu['app.clear_history'] = QAction(QIcon.fromTheme("edit-delete"),
                                                           trans("menu.file_clear_history"), self.window)
        self.window.ui.menu['app.ctx.new'] = QAction(QIcon.fromTheme("edit-new"), trans("menu.file.new"), self.window)

        self.window.ui.menu['app.clear_history'].triggered.connect(
            lambda: self.window.controller.ctx.delete_history())

        self.window.ui.menu['app.ctx.new'].triggered.connect(
            lambda: self.window.controller.ctx.new())

        self.window.ui.menu['menu.app'] = self.window.menuBar().addMenu(trans("menu.file"))
        self.window.ui.menu['menu.app'].addAction(self.window.ui.menu['app.ctx.new'])
        self.window.ui.menu['menu.app'].addAction(self.window.ui.menu['app.clear_history'])
        self.window.ui.menu['menu.app'].addAction(self.window.ui.menu['app.exit'])

    def setup_plugins(self):
        """Setup plugins menu"""
        self.window.ui.menu['plugins.settings'] = QAction(QIcon.fromTheme("preferences-other"),
                                                          trans("menu.plugins.settings"), self.window)

        self.window.ui.menu['plugins.settings'].triggered.connect(
            lambda: self.window.controller.plugins.settings.toggle_editor())

        self.window.ui.menu['plugins'] = {}
        self.window.ui.menu['menu.plugins'] = self.window.menuBar().addMenu(trans("menu.plugins"))
        self.window.ui.menu['menu.plugins'].setStyleSheet(self.window.controller.theme.get_style('menu'))  # Windows fix
        self.window.ui.menu['menu.plugins'].addAction(self.window.ui.menu['plugins.settings'])

    def setup_audio(self):
        """Setup audio menu"""
        self.window.ui.menu['audio.output.azure'] = QAction(trans("menu.audio.output.azure"),
                                                            self.window, checkable=True)
        self.window.ui.menu['audio.output.tts'] = QAction(trans("menu.audio.output.tts"),
                                                          self.window, checkable=True)
        self.window.ui.menu['audio.input.whisper'] = QAction(trans("menu.audio.input.whisper"),
                                                             self.window, checkable=True)

        self.window.ui.menu['audio.output.azure'].triggered.connect(
            lambda: self.window.controller.plugins.toggle('audio_azure'))
        self.window.ui.menu['audio.output.tts'].triggered.connect(
            lambda: self.window.controller.plugins.toggle('audio_openai_tts'))
        self.window.ui.menu['audio.input.whisper'].triggered.connect(
            lambda: self.window.controller.plugins.toggle('audio_openai_whisper'))

        self.window.ui.menu['menu.audio'] = self.window.menuBar().addMenu(trans("menu.audio"))
        self.window.ui.menu['menu.audio'].addAction(self.window.ui.menu['audio.output.azure'])
        self.window.ui.menu['menu.audio'].addAction(self.window.ui.menu['audio.output.tts'])
        self.window.ui.menu['menu.audio'].addAction(self.window.ui.menu['audio.input.whisper'])

    def setup_config(self):
        """Setup config menu"""
        self.window.ui.menu['config.settings'] = QAction(QIcon.fromTheme("preferences-other"),
                                                         trans("menu.config.settings"), self.window)
        self.window.ui.menu['config.models'] = QAction(QIcon.fromTheme("preferences-other"),
                                                         trans("menu.config.models"), self.window)

        css_files = []
        css_files.append("style.css")
        css_files.append("style.dark.css")
        css_files.append("style.light.css")
        css_files.append("markdown.css")
        css_files.append("markdown.dark.css")
        css_files.append("markdown.light.css")

        json_files = []
        json_files.append("attachments.json")
        json_files.append("assistants.json")
        json_files.append("config.json")
        json_files.append("indexes.json")
        json_files.append("models.json")

        # create submenu for css files
        self.window.ui.menu['config.edit.css'] = QMenu(trans("menu.config.edit.css"), self.window)

        # create submenu for JSON files
        self.window.ui.menu['config.edit.json'] = QMenu(trans("menu.config.edit.json"), self.window)

        for css_file in css_files:
            name = css_file.split("/")[-1]
            self.window.ui.menu['config.edit.css.' + name] = QAction(QIcon.fromTheme("document-edit"),
                                                                name, self.window)
            self.window.ui.menu['config.edit.css.' + name].triggered.connect(
                lambda checked=True, file=css_file: self.window.controller.settings.toggle_file_editor(file))
            self.window.ui.menu['config.edit.css'].addAction(self.window.ui.menu['config.edit.css.' + name])

        for json_file in json_files:
            name = json_file
            self.window.ui.menu['config.edit.json.' + name] = QAction(QIcon.fromTheme("document-edit"),
                                                                name, self.window)
            self.window.ui.menu['config.edit.json.' + name].triggered.connect(
                lambda checked=True, file=json_file: self.window.controller.settings.toggle_file_editor(file))
            self.window.ui.menu['config.edit.json'].addAction(self.window.ui.menu['config.edit.json.' + name])

        self.window.ui.menu['config.open_dir'] = QAction(QIcon.fromTheme("folder-open"),
                                                         trans("menu.config.open_dir"), self.window)
        self.window.ui.menu['config.save'] = QAction(QIcon.fromTheme("document-save"),
                                                     trans("menu.config.save"), self.window)

        self.window.ui.menu['config.settings'].triggered.connect(
            lambda: self.window.controller.settings.toggle_editor('settings'))

        self.window.ui.menu['config.models'].triggered.connect(
            lambda: self.window.controller.model.editor.toggle_editor())

        self.window.ui.menu['config.open_dir'].triggered.connect(
            lambda: self.window.controller.settings.open_config_dir())

        self.window.ui.menu['config.save'].triggered.connect(
            lambda: self.window.controller.settings.save_all())

        self.window.ui.menu['menu.config'] = self.window.menuBar().addMenu(trans("menu.config"))
        self.window.ui.menu['menu.config'].addAction(self.window.ui.menu['config.settings'])
        self.window.ui.menu['menu.config'].addAction(self.window.ui.menu['config.models'])
        self.window.ui.menu['menu.config'].addMenu(self.window.ui.menu['config.edit.css'])
        self.window.ui.menu['menu.config'].addMenu(self.window.ui.menu['config.edit.json'])
        self.window.ui.menu['menu.config'].addAction(self.window.ui.menu['config.open_dir'])
        self.window.ui.menu['menu.config'].addAction(self.window.ui.menu['config.save'])

    def setup_debug(self):
        """Setup debug menu"""
        self.window.ui.menu['debug.config'] = QAction(trans("menu.debug.config"), self.window, checkable=True)
        self.window.ui.menu['debug.context'] = QAction(trans("menu.debug.context"), self.window, checkable=True)
        self.window.ui.menu['debug.presets'] = QAction(trans("menu.debug.presets"), self.window, checkable=True)
        self.window.ui.menu['debug.models'] = QAction(trans("menu.debug.models"), self.window, checkable=True)
        self.window.ui.menu['debug.plugins'] = QAction(trans("menu.debug.plugins"), self.window, checkable=True)
        self.window.ui.menu['debug.attachments'] = QAction(trans("menu.debug.attachments"), self.window, checkable=True)
        self.window.ui.menu['debug.assistants'] = QAction(trans("menu.debug.assistants"), self.window, checkable=True)
        self.window.ui.menu['debug.indexes'] = QAction(trans("menu.debug.indexes"), self.window, checkable=True)
        self.window.ui.menu['debug.ui'] = QAction(trans("menu.debug.ui"), self.window, checkable=True)
        self.window.ui.menu['debug.logger'] = QAction(trans("menu.debug.logger"), self.window, checkable=True)

        self.window.ui.menu['debug.config'].triggered.connect(
            lambda: self.window.controller.debug.toggle('config'))
        self.window.ui.menu['debug.context'].triggered.connect(
            lambda: self.window.controller.debug.toggle('context'))
        self.window.ui.menu['debug.presets'].triggered.connect(
            lambda: self.window.controller.debug.toggle('presets'))
        self.window.ui.menu['debug.models'].triggered.connect(
            lambda: self.window.controller.debug.toggle('models'))
        self.window.ui.menu['debug.plugins'].triggered.connect(
            lambda: self.window.controller.debug.toggle('plugins'))
        self.window.ui.menu['debug.attachments'].triggered.connect(
            lambda: self.window.controller.debug.toggle('attachments'))
        self.window.ui.menu['debug.assistants'].triggered.connect(
            lambda: self.window.controller.debug.toggle('assistants'))
        self.window.ui.menu['debug.indexes'].triggered.connect(
            lambda: self.window.controller.debug.toggle('indexes'))
        self.window.ui.menu['debug.logger'].triggered.connect(
            lambda: self.window.controller.debug.toggle_logger())
        self.window.ui.menu['debug.ui'].triggered.connect(
            lambda: self.window.controller.debug.toggle('ui'))

        self.window.ui.menu['menu.debug'] = self.window.menuBar().addMenu(trans("menu.debug"))
        self.window.ui.menu['menu.debug'].addAction(self.window.ui.menu['debug.config'])
        self.window.ui.menu['menu.debug'].addAction(self.window.ui.menu['debug.context'])
        self.window.ui.menu['menu.debug'].addAction(self.window.ui.menu['debug.presets'])
        self.window.ui.menu['menu.debug'].addAction(self.window.ui.menu['debug.models'])
        self.window.ui.menu['menu.debug'].addAction(self.window.ui.menu['debug.plugins'])
        self.window.ui.menu['menu.debug'].addAction(self.window.ui.menu['debug.attachments'])
        self.window.ui.menu['menu.debug'].addAction(self.window.ui.menu['debug.assistants'])
        self.window.ui.menu['menu.debug'].addAction(self.window.ui.menu['debug.indexes'])
        self.window.ui.menu['menu.debug'].addAction(self.window.ui.menu['debug.ui'])
        self.window.ui.menu['menu.debug'].addAction(self.window.ui.menu['debug.logger'])

    def setup_lang(self):
        """Setup lang menu"""
        self.window.ui.menu['lang'] = {}
        self.window.ui.menu['menu.lang'] = self.window.menuBar().addMenu(trans("menu.lang"))
        self.window.ui.menu['menu.lang'].setStyleSheet(self.window.controller.theme.get_style('menu'))  # Windows fix

    def setup_theme(self):
        """Setus theme menu"""
        self.window.ui.menu['theme'] = {}
        self.window.ui.menu['menu.theme'] = self.window.menuBar().addMenu(trans("menu.theme"))
        self.window.ui.menu['menu.theme'].setStyleSheet(self.window.controller.theme.get_style('menu'))  # Windows fix

    def setup_about(self):
        """Setup about menu"""
        self.window.ui.menu['info.about'] = QAction(QIcon.fromTheme("help-about"), trans("menu.info.about"),
                                                    self.window)
        self.window.ui.menu['info.changelog'] = QAction(QIcon.fromTheme("history"), trans("menu.info.changelog"),
                                                        self.window)
        self.window.ui.menu['info.updates'] = QAction(QIcon.fromTheme("history"), trans("menu.info.updates"),
                                                      self.window)
        self.window.ui.menu['info.website'] = QAction(QIcon.fromTheme("network-wireless"), trans("menu.info.website"),
                                                      self.window)
        self.window.ui.menu['info.docs'] = QAction(QIcon.fromTheme("network-wireless"), trans("menu.info.docs"),
                                                   self.window)
        self.window.ui.menu['info.pypi'] = QAction(QIcon.fromTheme("network-wireless"), trans("menu.info.pypi"),
                                                   self.window)
        self.window.ui.menu['info.snap'] = QAction(QIcon.fromTheme("network-wireless"), trans("menu.info.snap"),
                                                   self.window)
        self.window.ui.menu['info.github'] = QAction(QIcon.fromTheme("network-wireless"), trans("menu.info.github"),
                                                     self.window)

        self.window.ui.menu['info.about'].triggered.connect(
            lambda: self.window.controller.dialogs.info.toggle('about'))
        self.window.ui.menu['info.changelog'].triggered.connect(
            lambda: self.window.controller.dialogs.info.toggle('changelog'))
        self.window.ui.menu['info.updates'].triggered.connect(
            lambda: self.window.controller.launcher.check_updates())
        self.window.ui.menu['info.website'].triggered.connect(
            lambda: self.window.controller.dialogs.info.goto_website())
        self.window.ui.menu['info.docs'].triggered.connect(
            lambda: self.window.controller.dialogs.info.goto_docs())
        self.window.ui.menu['info.pypi'].triggered.connect(
            lambda: self.window.controller.dialogs.info.goto_pypi())
        self.window.ui.menu['info.snap'].triggered.connect(
            lambda: self.window.controller.dialogs.info.goto_snap())
        self.window.ui.menu['info.github'].triggered.connect(
            lambda: self.window.controller.dialogs.info.goto_github())

        self.window.ui.menu['menu.about'] = self.window.menuBar().addMenu(trans("menu.info"))
        self.window.ui.menu['menu.about'].addAction(self.window.ui.menu['info.about'])
        self.window.ui.menu['menu.about'].addAction(self.window.ui.menu['info.changelog'])
        self.window.ui.menu['menu.about'].addAction(self.window.ui.menu['info.updates'])
        self.window.ui.menu['menu.about'].addAction(self.window.ui.menu['info.docs'])
        self.window.ui.menu['menu.about'].addAction(self.window.ui.menu['info.pypi'])
        self.window.ui.menu['menu.about'].addAction(self.window.ui.menu['info.snap'])
        self.window.ui.menu['menu.about'].addAction(self.window.ui.menu['info.website'])
        self.window.ui.menu['menu.about'].addAction(self.window.ui.menu['info.github'])
