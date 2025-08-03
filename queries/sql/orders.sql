SELECT 
    "id",
    "created_at",
    "variant_id",
    "variant_name",
    "price",
    "discounted_price",
    "price" - "discounted_price" AS "discount",
    "fees"
FROM "orders"
;
