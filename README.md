# Playlysis
# Google Play parser & analizer.

# External Libraries
* [GooglePlayApi](https://github.com/egirault/googleplay-api)

# Requirements
* [Python 2.7+](http://www.python.org)
* [Requests](https://github.com/kennethreitz/requests)
* [PyMongo](https://github.com/mongodb/mongo-python-driver)
* [lxml](https://github.com/lxml/lxml/)
* [pytagcloud](https://github.com/atizo/PyTagCloud)

# Database
We are using MongoDB for storage.
## Collections
* apps: This collections stores the application's IDs.
		```
		{
			"_id" : ObjectId("51983e8c8c65f2e78e8c7e09"),
			"appid" : "com.facebook.katana",
			"details" : {
				"appDetails" : {
					"versionCode" : "204208",
					"installationSize" : 18804498,
					"numDownloads" : "100,000,000+",
					"packageName" : "com.facebook.katana",
					"uploadDate" : "May 17, 2013"
				}
			},
			"detailsUrl" : "details?doc=com.facebook.katana",
			"shareUrl" : "https://play.google.com/store/apps/details?id=com.facebook.katana",
			"purchaseDetailsUrl" : "details?doc=com.facebook.katana",
			"backendDocid" : "com.facebook.katana",
			"docType" : 1,
			"backendId" : 3,
			"title" : "Facebook",
			"creator" : "Facebook"
		}
		```
* updates: This collections stores the update notes.
		```
			{
				"_id" : ObjectId("51982aa0a8d4f42d5253d80f"),
				"uploaded" : "May 17, 2013",
				"update_note" : "What's in this version:• Send stickers to make your messages more fun• Delete unwanted comments from your posts• Get directions, check in, call businesses and more right from the top of Facebook Pages",
				"appid" : "com.facebook.katana",
				"version" : "Varies with device",
				"published" : "May 17, 2013",
				"versionCode" : "204208",
				"dt" : ISODate("2013-05-19T01:28:00.823Z")
			}
		```

## Indexes
*appid index:
*db.apps.ensureIndex({"appid":1}, {unique: true})

*update notes index:
**db.updates.ensureIndex({"appid":1, "published"}, {unique: true})



# Usage
## Fetch IDs
	$ python fetch_ids.py
	2013-05-20 13:52:17,737 - INFO - Conecting to host localhost:27017
	2013-05-20 13:52:17,738 - INFO - Using offset 100
	.
	.
	.

## Fetch update Notes
	$ python play_parser.py
	2013-05-20 13:53:35,225 - INFO - Conecting to host localhost:27017
	2013-05-20 13:53:35,227 - INFO - Progress 0 %  of 1631 apps
	2013-05-20 13:53:35,230 - INFO - Waiting for 1.0 seconds
	.
	.
	.

## Fetch update Notes
	$ python playlysis.py
	2013-05-20 13:53:35,225 - INFO - Conecting to host localhost:27017

TODO Add logging and documentation to playlysis
TODO Add a web interface

