import abc


class CollectorConfigValidator(abc.ABC):
    @abc.abstractmethod
    def validate(self, config: dict) -> None:
        """
        raise if not valid, else return None
        """
        raise NotImplementedError

    @abc.abstractmethod
    def is_valid(self, config: dict) -> bool:
        raise NotImplementedError
