from abc import abstractmethod, ABC


class DbContext(ABC):
    @abstractmethod
    async def ensure_created(self):
        """
        Ensures that the database for the context exists.

        :return:
        """

    @abstractmethod
    async def ensure_deleted(self):
        """
        Ensures that the database for the context does not exist.

        :return:
        """
