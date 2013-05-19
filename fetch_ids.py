"""This script loads the android app's id from Google Play
using the GooglePlayApi from https://github.com/egirault/googleplay-api
"""

__author__ = "Matias, Nicolas"
__version__ = "0.1"

import sys
import json
import logging

import pymongo

from googleplay import GooglePlayAPI
from helpers import obj_to_dict
from google.protobuf.message import DecodeError

FORMAT = '%(asctime)-15s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)

flhdl = logging.FileHandler('log/fetch_ids.log')
ch = logging.StreamHandler(sys.stdout)

logger = logging.getLogger('GooglePlay')
logger.setLevel(logging.DEBUG)
logger.addHandler(flhdl)

try:
    with open('config.json', 'r') as config_file:
        config = json.loads(
            config_file.read().strip()
        )
        try:
            deviceid = config["deviceid"]
            email = config["email"]
            password = config["password"]
        except KeyError:
            logger.critical('Config problem: %s', 'Missing config parameters')
            sys.exit(1)
except IOError:
    logger.critical('Config problem: %s', 'Missing config file')
    sys.exit(1)


api = GooglePlayAPI(deviceid)
api.login(email, password)

logger.info('Conecting to host {}:{}'.format('localhost', '27017'))
client = pymongo.MongoClient("localhost", 27017)
db = client.test

SUB_CAT = (
    'apps_topselling_paid',
    'apps_topselling_free',
    'apps_topgrossing',
    'apps_topselling_new_paid',
    'apps_topselling_new_free'
)

count = 0
offset = 100
logger.info('Using offset {}'.format(offset))

for sub in SUB_CAT:
    index = 0

    while(True):
        try:
            message = api.list('SOCIAL', sub, str(offset), str(index * offset))
            try:
                doc = message.doc[0]
            except IndexError:
                logger.critical(
                    "Slice {}+ failed to fetch for category {} and subcat {}"
                    .format(index * offset, "SOCIAL", sub))
                break

            for c in doc.child:
                logger.debug(
                    'Fetching app id {}, version {} and date {}'.format(
                        c.docid,
                        c.details.appDetails.versionCode,
                        c.details.appDetails.uploadDate
                    ))

                to_insert = obj_to_dict(c)

                db.apps.save(to_insert)

                logger.debug(
                    'Inserted {}'.format(
                        c.docid,
                    ))
                count += 1

        except DecodeError:
            break
        except pymongo.errors.DuplicateKeyError:
            logger.debug("Duplicate key {}".format(c.docid))
            pass
        except Exception:
            raise
        index += 1

logger.info("Fetch process finished. New inserted ids: {}".format(count))
