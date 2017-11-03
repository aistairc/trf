import shutil


def check_executable(executable: str):
    location = shutil.which(executable)
    if location is None:
        print('`{0}` is not found on your PATH.\n'
              'Make sure that `{0}` is installed on your system '
              'and available on the PATH.'.format(executable))
        sys.exit(1)
    else:
        pass
