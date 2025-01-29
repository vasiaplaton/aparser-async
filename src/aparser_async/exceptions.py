__all__ = ('AParserError', 'AParserReqError', 'AParserRequestNotSuccess', 'AParserTimeoutError')


class AParserError(Exception):
    """Any error, base exception"""


class AParserReqError(AParserError):
    """Network request error"""


class AParserRequestNotSuccess(AParserError):
    """Request not success, aparaser returned success != 1"""


class AParserTimeoutError(AParserError):
    """Timeout error"""
