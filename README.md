# Udacity FSND Logs Analysis project

## About

This project analyzes a million row website log for 1 calendar month for a newspaper website and answers three questions based on log data:
-what are the three most popular articles by visits
-which authors are the most popular authors on the website
-when did site errors make up more than 1% of site requests

## To run
### You need to setup/install
-Python 3
-Download [newsdata.sql](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
-Unzip the file and load the data using the command psql -d news -f newsdata.sql

### Create views in the news database

'''
create view articlelog as
select articles.title, articles.slug, articles.author,
count(log.path) as visits
from log, articles
where log.path like concat('%',articles.slug)
group by articles.title, articles.slug, articles.author
order by visits DESC;
'''

'''
create view errorlog as select count(log.status) as status404,
time::timestamp::date from log
where log.status like '404%'
group by time::timestamp::date, status order by time;
'''

'''
create view totalviews as select count(log.status) as totalviews,
time::timestamp::date from log
group by time::timestamp::date  order by time;
'''

Once the views have been created execute "python logs.py" from the command line.