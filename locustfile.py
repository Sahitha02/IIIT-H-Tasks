from locust import HttpUser, task, between

BASE_URL = "http://127.0.0.1:5000"

# -------------------------------
# Annotator User Simulation
# -------------------------------
class AnnotatorUser(HttpUser):
    wait_time = between(1, 3)  # Wait between requests

    @task
    def open_annotator_dashboard(self):
        self.client.get("/annotator_dashboard")

    @task
    def paginate_annotator_dashboard(self):
        self.client.get("/annotator_dashboard_paginated?page=1&limit=50")


# -------------------------------
# Reviewer User Simulation
# -------------------------------
class ReviewerUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def open_reviewer_dashboard(self):
        self.client.get("/reviewer_dashboard")

    @task
    def open_reviewer_paginated(self):
        self.client.get("/reviewer_dashboard_paginated?page=1&limit=10")


# -------------------------------
# Admin / Validator User Simulation
# -------------------------------
class AdminUser(HttpUser):
    wait_time = between(2, 4)

    @task
    def open_logbook(self):
        self.client.get("/logbook")

    @task
    def validator_dashboard_paginated(self):
        self.client.get("/validator_dashboard_paginated?page=1&limit=50")


# -------------------------------
# Segment Context Testing
# -------------------------------
class SegmentUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def open_segment(self):
        self.client.get("/segment_context_optimized/1")

    @task
    def open_segment_cached(self):
        self.client.get("/segment_context_cached/1")
