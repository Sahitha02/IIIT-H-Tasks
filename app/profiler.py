from pyinstrument import Profiler

def profile_endpoint(func):
    def wrapper(*args, **kwargs):
        profiler = Profiler()

        # Start recording
        profiler.start()

        result = func(*args, **kwargs)

        # Stop recording
        profiler.stop()

        # Save the report to a file
        report_path = "profiler_report.html"
        with open(report_path, "w") as f:
            f.write(profiler.output_html())

        print(f"Profiler report saved to {report_path}")

        return result

    # Make sure Flask knows this is still the same route function
    wrapper.__name__ = func.__name__
    return wrapper
