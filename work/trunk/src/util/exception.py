# !/usr/bin/python
# -*- conding: utf-8 unicode -*
# vim: tabstop=4 shiftwidth=4 softtabstop=4

class HandleError(Exception):
    """
    Raised when bad parameters,or command is not found
    """
    pass

class CommitError(Exception):
    """
    Raised when command run error
    """
    pass

class ExistsInDB(Exception):
    pass

class NotFoundInDB(Exception):
    pass

class ExistsInSys(Exception):
    pass

class NotFoundInSys(Exception):
    pass
