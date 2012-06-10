drop table if exists post;
create table post (
        post_id SERIAL,
        post_date TIMESTAMP,
        title VARCHAR(80),
        caption VARCHAR(80),
        image_data BYTEA,
        PRIMARY KEY (post_id)
);
