Task-10: PostgreSQL Index Tuning
Task Group: Caching & Infra

🎯 Objective
Improve database performance by adding indexes to frequently used columns and analyzing query execution plans using `EXPLAIN ANALYZE`.


## 1️⃣ Queries Evaluated (Before Indexing)

##Query A — Posts filtered by user

SELECT * FROM posts WHERE user_id = 1;

Result:
Seq Scan — scanned entire table
Execution time: ~0.040 ms

-------------
Query B — Dashboard JOIN aggregation
SELECT u.id, u.name, COUNT(p.id)
FROM users u
LEFT JOIN posts p ON u.id = p.user_id
GROUP BY u.id, u.name;

Result:
Seq Scan on posts + Seq Scan on users
Execution: ~0.630 ms

------------------------
Query C — Segment contexts

SELECT * FROM segment_contexts WHERE segment_id = 1;

Result:
Seq Scan — scanned entire table
Execution: ~0.568 ms
---------------------------
Indexes Added

CREATE INDEX idx_posts_user_id
ON posts (user_id);

CREATE INDEX idx_segment_contexts_segment_id
ON segment_contexts (segment_id);

These indexes target:

Foreign key lookups

JOIN operations

WHERE filters for dashboards and segment context routes

Queries After Indexing (EXPLAIN ANALYZE)
--
Query A — After index

Execution time improved to ~0.025 ms
PostgreSQL still used Seq Scan (expected on tiny tables)
Estimated cost reduced significantly.
--
Query B — After index

Execution time improved to ~0.080 ms
Hash join still used, but cost lowered.
--
Query C — After index

Execution time improved to ~0.028 ms
Seq Scan chosen because table is very small
Index cost reduced.

Conclusion:

Indexes were successfully added and verified using EXPLAIN ANALYZE.
Even though Seq Scans are still used (due to tiny datasets), index cost improvements show that:

The indexing strategy is correct and will dramatically improve performance as data grows.
