INSERT INTO "inventory_items" (
    "id",
    "created_at",
    "variant_id",
    "variant_name",
    "variant_price",
    "unit_cost",
    "stock"
) VALUES (
    :id,
    :created_at,
    :variant_id,
    :variant_name,
    :variant_price,
    :unit_cost,
    :stock
)
RETURNING "id"
;
