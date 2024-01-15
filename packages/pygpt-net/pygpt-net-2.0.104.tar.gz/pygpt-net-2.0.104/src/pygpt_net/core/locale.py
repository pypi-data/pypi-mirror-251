#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# ================================================== #
# This file is a part of PYGPT package               #
# Website: https://pygpt.net                         #
# GitHub:  https://github.com/szczyglis-dev/py-gpt   #
# MIT License                                        #
# Created By  : Marcin Szczygliński                  #
# Updated Date: 2024.01.10 04:03:00                  #
# ================================================== #

import json
import os
import configparser
import io

from pygpt_net.config import Config


class Locale:
    def __init__(self, domain: str = None, config=None):
        """
        Locale core

        :param domain: translation domain
        :param config: Config instance
        """
        if config is None:
            self.config = Config()
        else:
            self.config = config
        self.lang = 'en'
        self.data = {}
        self.config.init(False)
        if self.config.has('lang'):
            self.lang = self.config.get('lang')
        self.load(self.lang, domain)

    def reload(self, domain: str = None):
        """
        Reload translations for domain

        :param domain: translation domain
        """
        self.config.load(False)
        if self.config.has('lang'):
            self.lang = self.config.get('lang')
        self.load(self.lang, domain)

    def load_fallback(self, domain: str = None):
        """
        Load base translations (fallback to en)
        """
        lang = 'en'
        locale_id = 'locale'
        if domain is not None:
            locale_id = domain

        # at first check if file exists in user data dir (override)
        path = os.path.join(self.config.get_user_path(), 'locale', locale_id + '.' + lang + '.ini')
        if not os.path.exists(path):
            # if not check to file exists in app data dir
            path = os.path.join(self.config.get_app_path(), 'data', 'locale', locale_id + '.' + lang + '.ini')
        if not os.path.exists(path):
            return None
        try:
            ini = configparser.ConfigParser()
            data = io.open(path, mode="r", encoding="utf-8")
            ini.read_string(data.read())
            self.data[locale_id] = dict(ini.items('LOCALE'))
        except Exception as e:
            print(e)

    def load(self, lang: str, domain: str = None):
        """
        Load translation ini file

        :param lang: language code
        :param domain: translation domain
        """
        self.load_fallback(domain)  # always load base translations (fallback to en)

        if type(lang) is not str:
            lang = 'en'
        locale_id = 'locale'
        if domain is not None:
            locale_id = domain

        # at first check if file exists in user data dir (override)
        path = os.path.join(self.config.get_user_path(), 'locale', locale_id + '.' + lang + '.ini')
        if not os.path.exists(path):
            # if not check to file exists in app data dir
            path = os.path.join(self.config.get_app_path(), 'data', 'locale', locale_id + '.' + lang + '.ini')
        if not os.path.exists(path):
            return None
        try:
            ini = configparser.ConfigParser()
            data = io.open(path, mode="r", encoding="utf-8")
            ini.read_string(data.read())
            parsed = dict(ini.items('LOCALE'))
            if locale_id not in self.data:
                self.data[locale_id] = {}
            for key in parsed:
                self.data[locale_id][key] = parsed[key]  # update translations
        except Exception as e:
            print(e)

    def get(self, key: str, domain: str = None) -> str:
        """
        Return translation for key and domain

        :param key: translation key
        :param domain: translation domain
        :return: translated string
        """
        locale_id = 'locale'
        if domain is not None:
            locale_id = domain

        if locale_id not in self.data:
            self.load(self.lang, domain)

        if locale_id in self.data and key in self.data[locale_id]:
            return self.data[locale_id][key].replace('\\n', "\n")
        else:
            return key
