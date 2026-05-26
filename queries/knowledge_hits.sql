-- FR-16: Knowledge source distribution over 7-day window
-- Returns: source (rule/escalate), hit_count
-- SAD.md §2.18 queries/knowledge_hits.sql

SELECT
    source,
    COUNT(*) AS hit_count
FROM messages
WHERE
    role = 'assistant'
    AND created_at >= NOW() - INTERVAL '7 days'
GROUP BY source
ORDER BY hit_count DESC;
