BEGIN;
--
-- Create model Post
--
CREATE TABLE "blog_post" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "title" varchar(150) NOT NULL UNIQUE, "text" text NOT NULL, "published_date" datetime NOT NULL);
COMMIT;
