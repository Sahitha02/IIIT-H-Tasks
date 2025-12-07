Task Group: Bottleneck Identification
Task 1: Identify N+1 Query Issues

1. Problem Summary
The project had N+1 query problems in endpoints that loaded users and their posts.
What is N+1?
•	The system first queried all users (1 query)
•	Then for each user, it queried their posts (N queries)
•	Total = 1 + N queries, which becomes slow when data grows.
This causes:
•	Slow dashboards
•	Multiple repeated database hits
•	Poor scaling when records increase

2. Approach :
Enabled SQLAlchemy query logging
We turned on:
SQLALCHEMY_ECHO = True
This printed all SQL queries to the terminal.

Hit the endpoint:
GET /users
Observed actual SQL logs
1.	Query to load all users
2.	Separate queries for each user's posts:
SELECT posts ... WHERE user_id = 1
SELECT posts ... WHERE user_id = 2
This confirmed an N+1 issue.

•	It executed three queries instead of one (for small data)
•	Would run thousands with large data

3. Technical Explanation
In SQLAlchemy, this happens when:
user.posts
is accessed without eager-loading strategies (joinedload or selectinload).
The ORM lazily loads related records → triggers many SELECT calls.
This is one of the most common performance bottlenecks in Python + Flask + SQLAlchemy systems.

4. Before Optimization – Query Count
Step	Query
Load users	SELECT * FROM users
Load posts for user 1	SELECT * FROM posts WHERE user_id = 1
Load posts for user 2	SELECT * FROM posts WHERE user_id = 2
Total queries for 2 users = 3
For 10 users = 11
For 10,000 users = 10,001 queries → extremely slow
This proves an N+1 query problem.
6. Final Outcome
✔Successfully identified the N+1 problem
✔ Verified with SQL logs
