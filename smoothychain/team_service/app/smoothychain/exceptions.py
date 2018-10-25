class AbstractException(Exception):
    pass


class NotValidTransaction(AbstractException):
    pass


class NegativeBalance(AbstractException):
    pass


class NotValidBlock(AbstractException):
    pass


class NotEnoughMoney(AbstractException):
    pass


class WrongSignature(AbstractException):
    pass


class TooMuchCode(AbstractException):
    pass


class WrongType(AbstractException):
    pass


class WrongDifficulty(AbstractException):
    pass
