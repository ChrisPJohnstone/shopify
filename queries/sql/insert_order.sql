INSERT INTO "orders" (
    "id",
    "created_at",
    "variant_id",
    "variant_name",
    "price",
    "discounted_price",
    "fees"
) VALUES (
    :id,
    :created_at,
    :variant_id,
    :variant_name,
    :price,
    :discounted_price,
    :fees
)
RETURNING "id"
;
