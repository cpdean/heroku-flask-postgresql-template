import unittest
import db
import os
import datetime

os.environ['DATABASE_URL'] = "postgres://herokuflask@localhost/herokudb"

class TestDatabase(unittest.TestCase):
    
    def setUp(self):
        db.init_db()

    def injectSeveralPosts(self,n):
        for i in range(n):
            p = db.Post()
            p.title = "injected"
            p.save()


    def test_connect(self):
        c = db.connect_db()
        cur = c.cursor()
        # ensure the post table is there
        cur.execute("select exists(select * from information_schema.tables where table_name=%s)", ('post',))
        self.assertEqual(cur.fetchone()[0],True)

    def test_make_post(self):
        p = db.Post()
        p.title = "PostTitle"
        p.caption = "Postcaption"
        p.save()
        new_p = db.get_latest_post()

        self.assertEqual(new_p.title,p.title)
        self.assertEqual(new_p.caption,p.caption)

    def test_date_datatype(self):
        now = datetime.datetime.now()
        p = db.Post()
        p.post_date = now
        p.save()
        new_p = db.get_latest_post()

        self.assertEqual(new_p.post_date,p.post_date)

    def test_show_posts(self):
        self.injectSeveralPosts(10)
        posts = db.Post().show()
        self.assertEquals(len(posts),10)

        

if __name__ == '__main__':
    unittest.main()
