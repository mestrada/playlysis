import time
import random
import re
import StringIO

from operator import itemgetter

from pytagcloud.lang.stopwords import StopWords

def get_attr(obj, attr_list):
    attr = obj
    try:
        for key in attr_list:
            attr = attr_list.__getattribute__(key)
        return attr
    except Exception:
        return None


def obj_to_dict(obj):
    out_dict = {
        "details": {
            "appDetails": {
                "versionCode": None,
                "installationSize": None,
                "numDownloads": None,
                "packageName": None,
                "uploadDate": None
            }
        },
        "offer": {
            "micros": None,
            "currencyCode": None,
            "formattedAmount": None,
            "convertedPrice": {
                "micros": None,
                "currencyCode": None,
            }
        },
        "aggregateRating": {
            "type": None,
            "starRating": None,
            "ratingsCount": None,
            "oneStarRatings": None,
            "twoStarRatings": None,
            "threeStarRatings": None,
            "fourStarRatings": None,
            "fiveStarRatings": None,
            "commentCount": None
        },
        "detailsUrl": None,
        "shareUrl": None,
        "purchaseDetailsUrl": None,
        "backendDocid": None,
        "docType": None,
        "backendId": None,
        "title": None,
        "creator": None
    }

    out_dict["appid"] = obj.docid

    out_dict["details"]['appDetails']['versionCode'] = get_attr(obj, 'details.appDetails.versionCode'.split('.'))
    out_dict["details"]['appDetails']['installationSize'] = get_attr(obj, 'details.appDetails.installationSize'.split('.'))
    out_dict["details"]['appDetails']['numDownloads'] = get_attr(obj, 'details.appDetails.numDownloads'.split('.'))
    out_dict["details"]['appDetails']['packageName'] = get_attr(obj, 'details.appDetails.packageName'.split('.'))
    out_dict["details"]['appDetails']['uploadDate'] = get_attr(obj, 'details.appDetails.uploadDate'.split('.'))

    out_dict["offer"]['micros'] = get_attr(obj, 'offer.micros'.split('.'))
    out_dict["offer"]['currencyCode'] = get_attr(obj, 'offer.currencyCode'.split('.'))
    out_dict["offer"]['formattedAmount'] = get_attr(obj, 'offer.formattedAmount'.split('.'))
    out_dict["offer"]['convertedPrice']['micros'] = get_attr(obj, 'offer.convertedPrice.micros'.split('.'))
    out_dict["offer"]['convertedPrice']['currencyCode'] = get_attr(obj, 'offer.convertedPrice.currencyCode'.split('.'))

    out_dict["aggregateRating"]["type"] = get_attr(obj, 'aggregateRating.type'.split('.'))
    out_dict["aggregateRating"]["starRating"] = get_attr(obj, 'aggregateRating.starRating'.split('.'))
    out_dict["aggregateRating"]["ratingsCount"] = get_attr(obj, 'aggregateRating.ratingsCount'.split('.'))
    out_dict["aggregateRating"]["oneStarRatings"] = get_attr(obj, 'aggregateRating.oneStarRatings'.split('.'))
    out_dict["aggregateRating"]["twoStarRatings"] = get_attr(obj, 'aggregateRating.twoStarRatings'.split('.'))
    out_dict["aggregateRating"]["threeStarRatings"] = get_attr(obj, 'aggregateRating.threeStarRatings'.split('.'))
    out_dict["aggregateRating"]["fourStarRatings"] = get_attr(obj, 'aggregateRating.fourStarRatings'.split('.'))
    out_dict["aggregateRating"]["fiveStarRatings"] = get_attr(obj, 'aggregateRating.fiveStarRatings'.split('.'))
    out_dict["aggregateRating"]["commentCount"] = get_attr(obj, 'aggregateRating.commentCount'.split('.'))

    out_dict["detailsUrl"] = get_attr(obj, 'detailsUrl'.split('.'))
    out_dict["shareUrl"] = get_attr(obj, 'shareUrl'.split('.'))
    out_dict["purchaseDetailsUrl"] = get_attr(obj, 'purchaseDetailsUrl'.split('.'))
    out_dict["backendDocid"] = get_attr(obj, 'backendDocid'.split('.'))
    out_dict["title"] = get_attr(obj, 'title'.split('.'))
    out_dict["creator"] = get_attr(obj, 'creator'.split('.'))

    return out_dict


def wait(logger=None):
    secs = float(2) / random.randint(1, 4)

    if logger:
        logger.debug("Waiting for {} seconds".format(secs))

    time.sleep(secs)


def lookup(dictionary, key_stack, obj):
    # attr_list = filter(lambda x: '__' not in x, attr_list)
    if not key_stack:
        key_stack = []

    if isinstance(dictionary, dict):
        for key in dictionary:
            lookup(dictionary[key], key_stack.append(key), obj)
    else:
        attr = obj
        # set_dict = {}
        for key in key_stack:
            attr = attr.__getattribute__(key)
        dictionary = attr


def get_n_word_tag_counts(text, n):
    """
    Search tags in a given text. The language detection is based on stop lists.
    This implementation is inspired by https://github.com/jdf/cue.language. Thanks Jonathan Feinberg.
    """

    regexp = r"[\w']+"

    for _ in xrange(1, n):
        regexp += r" [\w']+"

    words = map(lambda x:x.lower(), re.findall(r"[\w']+", text, re.UNICODE))
    
    s = StopWords()
    s.load_language(s.guess(words))
    
    aux_file = StringIO.StringIO()
    
    for word in words:
        if s.is_stop_word(word):
            words.remove(word)
        else:
            aux_file.write(word + ' ')

    words = map(
        lambda x:x.lower(),
        re.findall(regexp, aux_file.getvalue(), re.UNICODE)
        )

    aux_file.flush()
    aux_file.close()

    counted = {}
    
    for word in words:
        if not s.is_stop_word(word) and len(word) > 1:
            if counted.has_key(word):
                counted[word] += 1
            else: 
                counted[word] = 1
      
    return sorted(counted.iteritems(), key=itemgetter(1), reverse=True)
