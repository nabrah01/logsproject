#!/usr/bin/python3
# -*- coding: utf-8 -*-

"""1. What are the most popular three articles of all time? Which articles
have been accessed the most? Present this information  as a sorted list with
the most popular article at the top. Princess Shellfish Marries Prince
Handsome" 1201 views 2. Who are the most popular article authors of all time?
Authors with most page views sorted with the most popular author at the top.
Ursula La Multa - 2304 views 3. On which days did more than 1 percent of
requests lead to errors? The log table has HTTP status codes July 29, 2016 -
2.5 percent of errors

Use psycopg2, views, single sql queries
"""

import psycopg2

DBNAME = "news"
db = psycopg2.connect(dbname=DBNAME)
c = db.cursor()

"""
create view articlelog as
select articles.title, articles.slug, articles.author,
count(log.path) as visits
from log, articles
where log.path like concat('%',articles.slug)
group by articles.title, articles.slug, articles.author
order by visits DESC;
"""


# Q1: Most popular three articles of all time
def question_one():
    query = """select title, visits from articlelog limit 3"""
    c.execute(query)
    questionone = c.fetchall()
    return questionone


# Q2: Most popular article authors of all time
def question_two():
    query = """
    select authors.name, sum(articlelog.visits) as views
    from authors, articlelog
    where articlelog.author = authors.id
    group by authors.name order by views desc
    """
    c.execute(query)
    questiontwo = c.fetchall()
    return questiontwo


# Q3:
'''
create view errorlog as select count(log.status) as status404,
time::timestamp::date from log
where log.status like '404%'
group by time::timestamp::date, status order by time;

create view totalviews as select count(log.status) as totalviews,
time::timestamp::date from log
group by time::timestamp::date  order by time;
'''


def question_three():
    query = """
    select totalviews.time,
    round((errorlog.status404/cast(totalviews.totalviews as numeric)*100), 2)
    as percent
    from errorlog, totalviews
    where errorlog.time = totalviews.time and
    (errorlog.status404/cast(totalviews.totalviews as numeric)*100) > 1.0
    """
    c.execute(query)
    questionthree = c.fetchall()
    return questionthree


def printresults(x, y, z):
    print (y)
    for i in x:
        print ('{} - {} {}'.format(i[0], i[1], z))
    print ()

if __name__ == "__main__":
    results = question_one()
    printresults(
        results,
        "Three most popular articles of all time",
        "views"
        )

    results = question_two()
    printresults(
        results,
        "Most popular article authors of all time",
        "views"
        )

    results = question_three()
    printresults(
        results,
        "Days where >1% of requests led to errors",
        "percent of errors"
        )

    db.close()
