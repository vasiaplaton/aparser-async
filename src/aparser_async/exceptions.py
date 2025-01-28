__all__ = ('AParserError', 'AParserReqError', 'AParserRequestNotSuccess')


class AParserError(Exception):
    """Any error, base exception"""


class AParserReqError(AParserError):
    """Network request error"""


class AParserRequestNotSuccess(AParserError):
    """Request not success, aparaser returned success != 1"""
