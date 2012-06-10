from datetime import datetime

import psycopg2

from os.path import exists
from os import makedirs
import os

import urlparse

urlparse.uses_netloc.append('postgres')
url = urlparse.urlparse(os.environ.get('DATABASE_URL',"postgres://herokuflask@localhost/herokudb"))

db = "dbname=%s user=%s password=%s host=%s " % (url.path[1:], url.username, url.password, url.hostname)

schema = "schema.sql"

def open_database_connection():
    #return psycopg2.connect('dbname=herokudb user=herokuflask')
    return psycopg2.connect(db)

def connect_db():
    return open_database_connection()

def init_db():
    conn = open_database_connection()
    with open(schema) as s:
        c = conn.cursor()

        c.execute(s.read())
        conn.commit()
    conn.close()

def get_latest_post():
    conn = connect_db()
    c = conn.cursor()
    c.execute( """
                select post_id
                from
                Post
                order by
                post_date DESC
                limit 1;
                """)
    id_record = c.fetchone()
    post_id = id_record[0]
    post_id = int(post_id)
    conn.close()
    return Post(post_id)
 


class Post:

    def __init__(self,post_id=None):
        if not post_id:
            self.post_date = datetime.now()
            self.title = "This is the title"
            self.caption = "The caption"
            self.post_id = None
            self.image_data = ""
        else:
            conn = connect_db()
            c = conn.cursor()
            c.execute("""select post_id,post_date,title,caption
                        from Post 
                        where post_id = (%s)""", (post_id,))

            post_id,post_date,title,caption = c.fetchone()
            self.post_id = post_id
            self.post_date = post_date
            self.title = title
            self.caption = caption
            conn.close()
                

    def save(self):
        if self.post_id is None:
            conn = connect_db()
            c = conn.cursor()
            c.execute("""insert into post 
                            (post_date,title,caption,image_data)
                            VALUES
                            (%s,%s,%s,%s);
                            """,(self.post_date, self.title, self.caption,self.image_data))
            conn.commit()
            conn.close()

    def show(self):
        conn = connect_db()
        c = conn.cursor()
        c.execute("select post_id,post_date,title,caption from Post order by post_date")
        r = c.fetchall() #rows
        posts = [(i,d,t,com) for i,d,t,com in r]

        conn.close()
        return posts

