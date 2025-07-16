SELECT STRFTIME('%Y-%m-%dT%H:%M:%SZ', MAX("created_at"), '+1 second')
FROM "orders"
;
