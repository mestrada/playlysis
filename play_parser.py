"""This script loads the android app's update notes from Google Play
using the stored ids from fetch_ids module
"""

__author__ = "Matias, Nicolas"
__version__ = "0.1"

import sys
import logging
import datetime


import requests
import pymongo

from helpers import wait
from lxml import html

FORMAT = '%(asctime)-15s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)

flhdl = logging.FileHandler('log/play_parser.log')

logger = logging.getLogger('GPParser')
logger.setLevel(logging.DEBUG)
logger.addHandler(flhdl)

base_url = "https://play.google.com/store/apps/details"
# Example params: ?id=com.skout.android&hl=es

logger.info('Conecting to host {}:{}'.format('localhost', '27017'))
client = pymongo.MongoClient("localhost", 27017)
db = client.test


def get_update_notes(aid='com.skout.android', lang='en'):
    params = {
        'id': aid,
        'hl': lang
    }

    r = requests.get(base_url, params=params)

    a = html.fromstring(r.text)

    root = a.getroottree()

    div = root.xpath("//*[@class='doc-whatsnew-container']")
    element = div.pop()
    upd_notes = element.text_content()

    div_ver = root.xpath("//*[@itemprop='softwareVersion']")
    elem = div_ver.pop()
    version = elem.text_content()

    div_ver = root.xpath("//*[@itemprop='datePublished']")
    elem = div_ver.pop()
    published = elem.text_content()

    return upd_notes, version, published

if __name__ == '__main__':

    count = 0
    inserted = 0
    duplicated = 0
    progress_index = 1
    n_apps = db.apps.count()

    logger.info("Progress 0 %  of {} apps".format(n_apps))

    for app in db.apps.find():
        count += 1
        # Wait a random time
        wait(logger)

        logger.info(
            "Getting updates for {}"
            .format(app['appid'])
        )

        u, v, p = get_update_notes(app['appid'])

        try:
            db.updates.save({
                "appid": app['appid'],
                "versionCode": app['details']['appDetails']['versionCode'],
                "uploaded": app['details']['appDetails']['uploadDate'],
                "version": v,
                "update_note": u,
                "published": p,
                "dt": datetime.datetime.utcnow()
            })

            logger.debug("Updates notes for {} inserted".format(app['appid']))

            inserted += 1
        except pymongo.errors.DuplicateKeyError:
            logger.debug("Duplicate key {}".format(app['appid']))
            duplicated += 1
        except Exception:
            raise
        if count == int(progress_index * 0.10 * n_apps):
            logger.info("Progress {} %  of {} apps".format(float(count) / n_apps, n_apps))
            progress_index += 1

    logger.info(
        "{} update notes inserted {} duplicated."
        .format(inserted, duplicated))

    logger.info("Process finished")
