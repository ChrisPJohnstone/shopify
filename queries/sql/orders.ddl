CREATE TABLE IF NOT EXISTS "orders" (
    "id"                TEXT        NOT NULL,
    "created_at"        TIMESTAMP   NOT NULL,
    "variant_id"        TEXT        NOT NULL,
    "variant_name"      TEXT        NOT NULL,
    "price"             REAL        NOT NULL,
    "discounted_price"  REAL        NOT NULL,
    "fees"              REAL        NOT NULL
)
;
