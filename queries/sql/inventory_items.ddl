CREATE TABLE IF NOT EXISTS "inventory_items" (
    "id"            TEXT        NOT NULL,
    "created_at"    TIMESTAMP   NOT NULL,
    "variant_id"    TEXT        NOT NULL,
    "variant_name"  TEXT        NOT NULL,
    "variant_price" REAL        NOT NULL,
    "unit_cost"     REAL        NOT NULL,
    "stock"         INTEGER     NOT NULL
)
;
