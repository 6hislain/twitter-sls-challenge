# Twitter SLS Challenge

SLS Energy coding challenge

## Requirements

- python 3
- code editor: vscode
- web browser: chrome
- database: postgres

## Installation

- git clone `https://github.com/6hislain/twitter-sls-challenge`
- cd `twitter-sls-challenge`
- pip install > requirements.txt
- edit file `twitter_sls_challenge\settings.py` line `81 - 85` to connect to your database
- python manage.py migrate
- python manage.py runserver

### Load dataset into database

- put the `query2_ref.txt` file in this project (root) folder
- python manage.py split_file ./query2_ref.txt ./data
- python manage.py load_data ./data
