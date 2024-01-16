class LipsgitBaseException(Exception):
    def __init__(self, error_message: str, potential_solution: str):
        super().__init__(
            self._construct_exception_message(error_message, potential_solution)
        )

    @staticmethod
    def _construct_exception_message(
        error_message: str, potential_solution: str
    ) -> str:
        return f"❌{error_message}\n💡{potential_solution}"


class LipsgitConfigNotFoundException(LipsgitBaseException):
    def __init__(self):
        super().__init__(
            "Could not find lipsgit config file", "Please run lipsgit init"
        )
