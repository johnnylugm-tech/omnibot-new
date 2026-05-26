-- FR-16: p95 latency per platform over 30-day window
-- Returns: platform, avg_response_time_ms, p95_response_time_ms
-- SAD.md §2.18 queries/latency.sql

SELECT
    platform,
    ROUND(AVG(response_time_ms), 2) AS avg_response_time_ms,
    PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY response_time_ms) AS p95_response_time_ms
FROM messages
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY platform;
