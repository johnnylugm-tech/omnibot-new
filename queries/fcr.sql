-- FR-16: FCR rate over 30-day window
-- Returns: fcr_rate_pct (0-100)
-- SAD.md §2.18 queries/fcr.sql

SELECT
    ROUND(
        100.0 * COUNT(CASE WHEN first_contact_resolution IS NOT NULL THEN 1 END)
        / NULLIF(COUNT(*), 0),
        2
    ) AS fcr_rate_pct
FROM conversations
WHERE
    scope_type = 'in_scope'
    AND started_at >= NOW() - INTERVAL '30 days';
