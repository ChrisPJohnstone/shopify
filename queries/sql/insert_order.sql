INSERT INTO "orders" (
    "id",
    "created_at",
    "variant_id",
    "variant_name"
) VALUES (
    :id,
    :created_at,
    :variant_id,
    :variant_name
)
RETURNING "id"
;
