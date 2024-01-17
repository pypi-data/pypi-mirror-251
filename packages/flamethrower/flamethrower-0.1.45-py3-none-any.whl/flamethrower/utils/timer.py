import time
from contextlib import contextmanager
from flamethrower.shell.printer import Printer
from flamethrower.containers.container import container

@contextmanager
def execution_time():
    printer: Printer = container.printer()
    start_time = time.time()
    try:
        yield
    finally:
        end_time = time.time()
        mins, secs = divmod(end_time - start_time, 60)
        if mins:
            printer.print_light_green(f'\nThis run took {int(mins)}m {secs:.1f}s 🚀')
        else:
            printer.print_light_green(f'\nThis run took {secs:.1f}s 🚀')

# Example usage
if __name__ == "__main__":
    with execution_time():
        time.sleep(1)  # Code to time goes here.
