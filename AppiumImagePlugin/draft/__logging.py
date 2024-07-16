# -*- coding: utf-8 -*-

import base64
import os
from robot.libraries.BuiltIn import BuiltIn
from robot.libraries.BuiltIn import RobotNotRunningError
from robot.api import logger


class _LoggingKeywords():
    LOG_LEVEL_DEBUG = ['DEBUG']
    LOG_LEVEL_INFO = ['DEBUG', 'INFO']
    LOG_LEVEL_WARN = ['DEBUG', 'INFO', 'WARN']

    @property
    def _log_level(self):
        try:
            level = BuiltIn().get_variable_value("${APPIUM_LOG_LEVEL}", default='DEBUG')
        except RobotNotRunningError:
            level = 'DEBUG'
        return level

    def _debug(self, message):
        if self._log_level in self.LOG_LEVEL_DEBUG:
            logger.debug(message)

    def _info(self, message):
        if self._log_level in self.LOG_LEVEL_INFO:
            logger.info(message)

    def _warn(self, message):
        if self._log_level in self.LOG_LEVEL_WARN:
            logger.warn(message)

    def _html(self, message):
        logger.info(message, True, False)
    
    def _get_log_dir(self):
        variables = BuiltIn().get_variables()
        logfile = variables['${LOG FILE}']
        if logfile != 'NONE':
            return os.path.dirname(logfile)
        return variables['${OUTPUTDIR}']

    def _log(self, message, level='INFO'):
        level = level.upper()
        if (level == 'INFO'):
            self._info(message)
        elif (level == 'DEBUG'):
            self._debug(message)
        elif (level == 'WARN'):
            self._warn(message)
        elif (level == 'HTML'):
            self._html(message)

    def _log_list(self, items, what='item'):
        msg = ['Altogether %d %s%s.' % (len(items), what, ['s', ''][len(items) == 1])]
        for index, item in enumerate(items):
            msg.append('%d: %s' % (index+1, item))
        self._info('\n'.join(msg))
        return items
    
    def _embed_image_to_log(self, image_path, message="Image", width=10):
        with open(image_path, 'rb') as img_file:
            image_data = img_file.read()
            encoded_image_data = base64.b64encode(image_data).decode('utf-8')
        image_tag = f'<img src="data:image/png;base64,{encoded_image_data}" width="{width}%">'
        self._html(f" <br> {message}: <br> " + image_tag)
