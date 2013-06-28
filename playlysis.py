"""This script loads the android app's update notes from Google Play
using the stored ids from fetch_ids module
"""

__author__ = "Matias, Nicolas"
__version__ = "0.1"

import sys
import logging
import datetime
import StringIO


import requests
import pymongo

from pytagcloud import create_tag_image, make_tags
from pytagcloud.lang.counter import get_tag_counts


FORMAT = '%(asctime)-15s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)

flhdl = logging.FileHandler('log/play_parser.log')

logger = logging.getLogger('GPParser')
logger.setLevel(logging.INFO)
logger.addHandler(flhdl)

logger.info('Conecting to host {}:{}'.format('localhost', '27017'))
client = pymongo.MongoClient("localhost", 27017)
db = client.test


def get_notes(startdate, enddate):
    return db.updates.find({"dt": {
        "$gte": startdate,
        "$lt": enddate
    }})


def handleException(excType, excValue, traceback, logger=logger):
    logger.error("Uncaught exception", exc_info=(excType, excValue, traceback))


sys.excepthook = handleException

if __name__ == '__main__':

    count = 0
    duplicated = 0
    progress_index = 1
    mem_file = StringIO.StringIO()

    startdate = datetime.datetime(2013, 06, 10)
    enddate = datetime.datetime(2013, 06, 11)

    n_notes = db.updates.count()

    logger.info("Progress 0 %  of {} notes".format(n_notes))

    try:
        for note in get_notes(startdate, enddate):
            mem_file.write(note['update_note'])

            if count == int(progress_index * 0.10 * n_notes):
                logger.info("Progress {} %  of {} apps".format(100 * (float(count) / n_notes), n_notes))
                progress_index += 1

        logger.info("Process finished")

        tags = make_tags(get_tag_counts(mem_file.getvalue()), maxsize=120)

        create_tag_image(tags[:100], 'cloud_large.png', size=(900, 600))

    except Exception:
        mem_file.close()
        raise
