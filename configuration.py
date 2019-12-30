#!/usr/bin/env python
"""
conofiguration.py has all the configuration constants
"""

import sys
DB_NAME = 'studentmanagement'
DB_APP_CONFIG_SQLALCHEMY_TRACK_MODIFICATIONS = False
DB_APP_CONFIG_SECRET_KEY = "random string"


DOCKER_DB_URL = "postgres://postgres@db:5432"
LOCAL_DB_URL = "postgres://postgres:root@localhost:5432"


class ProductionDBServiceURL(): # pylint: disable=too-few-public-methods
    """
    Class which provide prodiction db service related URLs

    """

    @staticmethod
    def get_production_mode_db_url():

        """
        :param argument_list: argument_list from user while running server
        :return: db url for current mode
        """
        production_mode_url = None
        argument_list = sys.argv
        if len(argument_list) == 2 and argument_list[1] == "-l":
            production_mode_url = LOCAL_DB_URL
        else:
            production_mode_url = DOCKER_DB_URL

        return production_mode_url
