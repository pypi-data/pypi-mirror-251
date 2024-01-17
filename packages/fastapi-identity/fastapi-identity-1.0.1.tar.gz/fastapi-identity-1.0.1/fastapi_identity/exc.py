class ArgumentNoneError(ValueError):
    def __init__(self, name: str):
        super().__init__("Value '%s' cannot be None." % name)


class NotSupportedException(Exception):
    pass


class InvalidOperationException(Exception):
    pass
