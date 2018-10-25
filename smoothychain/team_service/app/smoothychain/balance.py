from copy import deepcopy
from collections import defaultdict
from .exceptions import NegativeBalance


def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance


@singleton
class Balance:
    def __init__(self):
        self._balance = defaultdict(float)

    def check_changes(self, changes, force=False):
        diff = deepcopy(self._balance)
        if not force:
            for change in changes:
                if diff[change["pubkey"]] + change["amount"] < 0:
                    raise NegativeBalance
                diff[change["pubkey"]] += change["amount"]

    def commit(self, changes, force=False):
        self.check_changes(changes, force=force)
        for change in changes:
            self._balance[change["pubkey"]] += change["amount"]

    def get_balance(self, pubkey):
        if pubkey in self._balance:
            return self._balance[pubkey]
        else:
            return 0
