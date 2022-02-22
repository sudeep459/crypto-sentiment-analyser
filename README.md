# An Api for crypto sentiment analysis

The App folder contains the Api, whereas the script folder has the file for scraping data from web.
These two are to be executed seperately.

How do I get set up?
Summary of set up
	Run the fast-api service using app.main.py file
		pip install -r requirements.txt
		uvicorn app.main:app --host 0.0.0.0 --port 8000
	(or) Use docker files
	For Script cronjob
		Fill db details in config.py
		cd script
		pip install -r requirements.txt
		python script.py - runs everyday at 9:00 PM
