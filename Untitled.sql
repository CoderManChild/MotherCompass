CREATE TABLE "users" (
  "id" integer PRIMARY KEY,
  "full_name" text,
  "email" text,
  "username" text,
  "role" text
);

CREATE TABLE "mothers" (
  "id" integer PRIMARY KEY,
  "user_id" integer UNIQUE,
  "public_or_private" bool,
  "opt_in_ads" bool,
  "prev_chlidren" integer,
  "expect_or_deliver" bool,
  "DOB" date,
  "provider_id" integer UNIQUE
);

CREATE TABLE "providers" (
  "id" integer PRIMARY KEY,
  "user_id" integer UNIQUE,
  "address" text,
  "license_number" text
);

CREATE TABLE "posts" (
  "id" integer PRIMARY KEY,
  "title" text,
  "body" text,
  "user_id" integer
);

CREATE TABLE "comments" (
  "id" integer PRIMARY KEY,
  "body" text,
  "user_id" integer,
  "post_id" integer
);

COMMENT ON COLUMN "users"."role" IS 'Mother or Doctor, one-to-one';

COMMENT ON COLUMN "mothers"."user_id" IS 'do not duplicate fields from users table';

COMMENT ON COLUMN "mothers"."public_or_private" IS 'choose whether we want this';

COMMENT ON COLUMN "mothers"."opt_in_ads" IS 'yes or no';

COMMENT ON COLUMN "mothers"."prev_chlidren" IS 'number of children';

COMMENT ON COLUMN "mothers"."DOB" IS 'default to first of month if expected, say that on client-facing view';

COMMENT ON COLUMN "mothers"."provider_id" IS 'this means can only chat with the single associated provider';

COMMENT ON COLUMN "posts"."body" IS 'Content of the post';

COMMENT ON COLUMN "posts"."user_id" IS 'Creator of post';

COMMENT ON COLUMN "comments"."body" IS 'Content of the post';

COMMENT ON COLUMN "comments"."user_id" IS 'Creator of post';

COMMENT ON COLUMN "comments"."post_id" IS 'Post id, assuming no comments to comments';

ALTER TABLE "mothers" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "mothers" ADD FOREIGN KEY ("provider_id") REFERENCES "providers" ("id");

ALTER TABLE "providers" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "posts" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "comments" ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "comments" ADD FOREIGN KEY ("post_id") REFERENCES "posts" ("id");
