from airflow.decorators import task

@task(task_id="print_the_context")
def print_context(ds=None, **kwargs):
    """Print the Airflow context and ds variable from the context."""
    print(kwargs)
    print(ds)
    return "Whatever you return gets printed in the logs"

run_this = print_context()