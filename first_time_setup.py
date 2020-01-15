import sys
import os


def get_python_version():
    version_info=sys.version_info
    assert version_info>=(3,8) "Application requires python interpreter v3.8, please rerun with the correct version"
def main():
    # verify system version
    print("Checking python interpreter version")
    get_python_version()

if __name__=="__main__":
    main()