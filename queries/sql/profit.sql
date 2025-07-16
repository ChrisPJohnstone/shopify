WITH "data" AS (
    SELECT
        "inventory_items"."variant_name" AS "product",
        "inventory_items"."variant_price" AS "price",
        "inventory_items"."unit_cost" AS "cost",
        "inventory_items"."stock",
        COUNT("orders"."variant_id") AS "sales"
    FROM "inventory_items"
    INNER JOIN "orders"
        ON  "inventory_items"."variant_id" = "orders"."variant_id"
    GROUP BY 1, 2, 3, 4
)

SELECT
    "data"."product",
    "data"."price",
    "data"."cost",
    "data"."stock",
    "data"."sales",
    ("data"."price" - "data"."cost") * "data"."sales" AS "profit"
FROM "data"
;
