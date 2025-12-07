Task Group: Bottleneck Identification
Task 3: Profile Slow Endpoints

1. What Was the Goal?
Some routes in the system (annotator dashboard, reviewer dashboard, logbook) felt slow because:
•	They do heavy computations
•	They loop through large lists
•	They execute many SQL queries

2. Approach
Installed Pyinstrument Profiler
Enabled Flask’s built-in performance profiler:
app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir="profiler_output")
Now every request generates a performance profile.
Triggered slow endpoints manually:
/annotator_dashboard
/reviewer_dashboard
/logbook
Generated detailed profiling reports
For each endpoint, we produced a .prof file that shows:
•	Function call time
•	Number of calls
•	Time spent in loops
•	SQL time
•	CPU time

3. Technical Explanation
Profiling is the process of measuring performance inside your code.
The profiler records:
•	How many times each function runs
•	How long each function takes
•	How much CPU time each loop consumes
•	Which lines are bottlenecks
This is essential BEFORE doing any optimization.
It answers:
“Where is the system actually slow?”

4. Observations (Actual Results)
When I ran the profiler, I saw:
Annotator Dashboard
•	Heavy loop: for i in range(20000)
•	Most time spent in CPU arithmetic
•	No DB queries involved
Reviewer Dashboard
•	Several SQL queries
•	ORM lazy-loading contributing to overhead
Logbook
•	Expensive loop: for i in range(50000)
•	Sleep delay (time.sleep(0.1))
•	CPU-bound + artificial delay

5. Final Outcome
✔Profiling integrated into the project
✔ Detailed performance metrics generated
✔ Identified slow code paths with evidence

