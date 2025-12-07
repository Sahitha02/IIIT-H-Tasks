Task Group: Bottleneck Identification
Task 2: Optimize ORM Preloading (Fix N+1 Query Issue)

1. What Was the Performance Problem? (N+1 Queries)
The /users route was slow because it executed:
•	One query to fetch all users
•	N more queries to fetch posts for each user
This means for 10,000 users → 10,001 queries, extremely inefficient.
This was identified in Task 1 and now must be fixed.

2. Approach 
We optimized the /users_optimized route using SQLAlchemy’s eager loading:
User.query.options(selectinload(User.posts)).all()
This changes SQLAlchemy behavior:

Before (slow)
•	Query 1 → load all users
•	Query 2..N → one per user to get their posts

After (optimized)
•	One query → load all users
•	One additional query → load all posts for all users
This reduces query count from N+1 → 2.

What is selectinload?
It tells SQLAlchemy:
“Load related data in batches instead of one-by-one.”
It does this by generating a single IN (...) query for all users' posts.

Why is this faster?
Database engines are optimized for:
•	Fewer queries
•	Larger batch retrieval
•	Efficient joins
So performing 2 big queries is much better than 1000 small queries.

3. Before vs After Comparison (Exact Logs)
Before Optimization (Actual Logs)
SELECT users...
SELECT posts WHERE user_id = 1
SELECT posts WHERE user_id = 2
Total: 3 queries
After Optimization
SELECT users...
SELECT posts WHERE user_id IN (1, 2)
Total: 2 queries
For real-world datasets, this saves thousands of queries.

4. Final Outcome
✔ /users now loads much faster
✔ Database stress reduced
✔ System scales better with large data
✔ Sets the foundation for future dashboard optimizations
