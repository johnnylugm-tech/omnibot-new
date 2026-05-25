"""Phase 1 ODD SQL queries — FCR rate, p95 latency per platform, knowledge source distribution.

SRS.md §FR-16:
  "Provide Phase 1 ODD SQL queries: FCR rate, p95 latency per platform,
   knowledge source distribution"
"""

ODD_QUERIES = {
    "fcr": """
        SELECT
            COUNT(*) AS total,
            SUM(CASE WHEN first_contact_resolution THEN 1 ELSE 0 END) AS fcr,
            ROUND(
                SUM(CASE WHEN first_contact_resolution THEN 1 ELSE 0 END) * 100.0
                / NULLIF(COUNT(*), 0), 2
            ) AS fcr_rate_pct
        FROM conversations
        WHERE started_at > NOW() - INTERVAL '30 days'
          AND scope_type = 'in_scope'
          AND first_contact_resolution IS NOT NULL
    """,
    "latency": """
        SELECT
            platform,
            AVG(response_time_ms) AS avg_latency_ms,
            PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY response_time_ms) AS p95_latency_ms
        FROM conversations
        WHERE started_at > NOW() - INTERVAL '30 days'
          AND response_time_ms IS NOT NULL
        GROUP BY platform
    """,
    "knowledge_hits": """
        SELECT
            knowledge_source,
            COUNT(*) AS total,
            AVG(confidence_score) AS avg_confidence
        FROM messages
        WHERE role = 'assistant'
          AND created_at > NOW() - INTERVAL '7 days'
          AND knowledge_source IS NOT NULL
        GROUP BY knowledge_source
    """,
}
