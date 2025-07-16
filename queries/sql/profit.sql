SELECT
    "inventory_items"."variant_name" AS "product",
    "inventory_items"."stock",
    COUNT("orders"."variant_id") AS "sales",
    SUM("orders"."price") AS "net",
    SUM("orders"."price") - SUM("orders"."discounted_price") AS "discounts",
    SUM("orders"."fees") AS "fees"
FROM "inventory_items"
INNER JOIN "orders"
    ON  "inventory_items"."variant_id" = "orders"."variant_id"
GROUP BY 1, 2
;
