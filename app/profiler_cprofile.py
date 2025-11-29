import cProfile
import pstats
import io
from flask import Blueprint, jsonify
from .dashboards import annotator_dashboard, reviewer_dashboard, logbook

profile_bp = Blueprint("profile_bp", __name__)

def run_and_profile(func, filename):
    pr = cProfile.Profile()
    pr.enable()

    func()   # run the endpoint code

    pr.disable()
    s = io.StringIO()
    ps = pstats.Stats(pr, stream=s).sort_stats("tottime")
    ps.print_stats()

    with open(filename, "w") as f:
        f.write(s.getvalue())

    return f"Profiling report saved: {filename}"

@profile_bp.route("/profile_all_dashboards")
def profile_all():
    result1 = run_and_profile(annotator_dashboard, "annotator_profile.txt")
    result2 = run_and_profile(reviewer_dashboard, "reviewer_profile.txt")
    result3 = run_and_profile(logbook, "logbook_profile.txt")

    return jsonify({
        "annotator": result1,
        "reviewer": result2,
        "logbook": result3
    })
