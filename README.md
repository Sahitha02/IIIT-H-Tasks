Task-6: Async Logging Queue  
Task Group: API Optimization

Objective
Move the `log_action` function out of the main HTTP request flow and execute it asynchronously in a background worker using a Redis-backed task queue. This improves API performance by making logging non-blocking.

---

What Was Implemented:

1. Added Dramatiq (Windows-friendly task queue)
Since RQ and Celery rely on `os.fork()`, which is not supported on Windows, Dramatiq was chosen as the async queue system.


