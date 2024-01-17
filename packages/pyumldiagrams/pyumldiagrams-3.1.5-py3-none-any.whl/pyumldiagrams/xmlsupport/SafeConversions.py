
from logging import Logger
from logging import getLogger


class SafeConversions:
    def __init__(self):
        self.logger: Logger = getLogger(__name__)

    def _stringToBoolean(self, strBoolValue: str) -> bool:

        self.logger.debug(f'{strBoolValue=}')
        try:
            if strBoolValue is not None:
                if strBoolValue in [True, "True", "true", 1, "1"]:
                    return True
        except (ValueError, Exception) as e:
            self.logger.error(f'_stringToBoolean error: {e}')

        return False

    def _stringToInteger(self, x: str):
        if x is not None and x != '':
            return int(x)
        else:
            return 0
