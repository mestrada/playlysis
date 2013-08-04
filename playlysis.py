"""This script loads the android app's update notes from Google Play
using the stored ids from fetch_ids module
"""

__author__ = "Matias, Nicolas"
__version__ = "0.1"

import logging
import datetime
import StringIO

import pymongo

from helpers import get_n_word_tag_counts

from pytagcloud import create_tag_image, make_tags
# from pytagcloud.lang.counter import get_tag_counts

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
    """get_notes(startdate, enddate)
    This function returns an colection object iterator with
    the updates notes in the soecified time range"""

    return db.updates.find({"dt": {
        "$gte": startdate,
        "$lt": enddate
    }})


def get_tag_cloud(
    startdate,
    enddate,
    n_words=1,
    max_tags=100,
    max_size=80,
    height=900,
    width=600,
    filename='cloud_large.png'
):
    """get_tag_cloud
    This function generates a png file with an image of a tag cloud
    from the collected updates notes between the specified dates
    The required params are the start date and the end date to specify
    a desired time range.
    You can specify a different number of max tags, max tag size or the
    size og the resultant image.
    The filename is optional.
    """

    count = 0
    progress_index = 1
    mem_file = StringIO.StringIO()

    try:
        notes = get_notes(startdate, enddate)
        n_notes = notes.count()

        logger.info("Progress 0 %  of {} notes".format(n_notes))

        for note in notes:
            mem_file.write(note['update_note'])

            if count == int(progress_index * 0.10 * n_notes):
                logger.info("Progress {} %  of {} notes".format(
                    int(100 * (float(count) / n_notes)), n_notes))
                progress_index += 1
            count += 1

        logger.info("Calculating tags")
        tags = make_tags(
            get_n_word_tag_counts(mem_file.getvalue(), n_words),
            maxsize=max_size)

        logger.info("Generating {}".format(filename))

        logger.info("File specs: h={height};w={width}; max_tags={max_tags}; tag_max_size{max_size}".format(
            height=height,
            width=width,
            max_tags=max_tags,
            max_size=max_size
        ))

        create_tag_image(tags[:max_tags], filename, size=(height, width))

        logger.info("{} succesfully created. Procces finished.".format(filename))

    except Exception:
        mem_file.close()
        raise

if __name__ == '__main__':

    startdate = datetime.datetime(2013, 06, 10)
    enddate = datetime.datetime(2013, 06, 11)

    get_tag_cloud(startdate, enddate)
