# -*- coding: utf-8 -*-
__author__  = 'ShiQiankun'
__mail__    = 'seslovelol@outlook.com'
__status__  = 'Development'
__version__ = '1.01'
__date__    = 'Aug.07,2020'


import os
import sys
import time
import shutil
import logging
import logging.handlers
from lib.common import logger
from lib.common import add_bom
from lib.common import get_stat
from lib.common import check_ftp
from lib.common import upload_log
from lib.common import check_path
from lib.common import create_path
from lib.common import check_arglen
from lib.common import check_module
from lib.common import exit_process
from lib.common import check_package
from lib.common import break_process


def get_args(logger):
    """
        Get args.
        Args: localpath, updatepath, packagename, module, env, ftpinfo
    """
    check_arglen(6, 6, logger)
    local, update, package, module, env, ftpinfo = sys.argv[1:]
    logger.info('Begin to execute {} {} {} {} {} {} FTPINFO'.format(
        os.path.join(os.getcwd(), sys.argv[0]), local, update, package, module, env
    ))
    check_path(local, logger)
    check_package(local, package, logger)
    check_module(local, package, module, logger)
    create_path(update, logger)
    ftpinfo = check_ftp(ftpinfo, logger)
    return local, update, package, module, env, ftpinfo


def update_common(logger):
    """
        Update env directory from localpath to updatepath.
    """
    logger = logger()
    local, update, package, module, env, ftpinfo = get_args(logger)
    temp_path = '/'.join((local, 'log', module))
    create_path(temp_path, logger)
    handler, temp_log = file_logger(temp_path, logger)
    # Module's real path.
    env_path = os.path.join(local, package.split('.')[0], module, env)
    if os.path.isdir(env_path):
        result = copy_dir(env_path, update, logger)
        logger.info('Copy files from {} to {} successfully.'.format(env, update))
        get_stat(result, logger)
        logger.removeHandler(handler)
        add_bom(temp_log)
        upload_log(package, module, ftpinfo, temp_log, logger)
        exit_process(local, package, module, logger)
    else:
        logger.error('No such env dir {} in module {}'.format(env, module))
        logger.removeHandler(handler)
        add_bom(temp_log)
        upload_log(package, module, ftpinfo, temp_log, logger)
        break_process(local, package, module, logger)


def file_logger(path, logger):
    """
        Write messages to a log file.
    """
    log_name = time.strftime('%Y%m%d%H%M%S_update.log', time.localtime())
    log_path = os.path.join(path, log_name)
    handler = logging.FileHandler(log_path, encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s %(filename)s %(levelname)s : %(message)s')
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    return handler, log_path


def copy_dir(source, target, logger, copy_list=[]):
    """
        Copy sub files and dirs from source path to target path.
    """
    for name in os.listdir(source):
        source_path = os.path.join(source, name)
        target_path = os.path.join(target, name)
        if os.path.isfile(source_path):
            if os.path.isfile(target_path):
                copy_list.append(target_path)
            shutil.copy(source_path, target_path)
        else:
            if not os.path.isdir(target_path):
                logger.debug('Create target dir {} copy.'.format(target_path))
                os.makedirs(target_path)
            copy_dir(source_path, target_path, logger)
    return copy_list


if __name__ == "__main__":
    update_common(logger)