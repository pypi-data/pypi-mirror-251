from AcodisApiHandler._acodis_logger import *
from AcodisApiHandler.acodis_error import *
from AcodisApiHandler.acodis_handler import *
from AcodisApiHandler.acodis_parser import *
from AcodisApiHandler._version import get_git_version

__all__ = ['AcodisApiHandler', 'extract_tags', 'AcodisError', 'AcodisApiError', 'AcodisAuthError', 'AcodisParsingError']

if __name__ == '__main__':
    print("version is: " + get_git_version())