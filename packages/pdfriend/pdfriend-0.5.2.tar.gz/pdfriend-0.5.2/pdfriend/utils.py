import traceback

def print_unexpected_exception(exception: Exception, debug: bool = False):
    print("unexpected error occured:")
    if debug:
        traceback.print_exception(exception)
    else:
        print(exception)

