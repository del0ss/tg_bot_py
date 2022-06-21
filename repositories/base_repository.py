from abc import ABC, abstractmethod


class AbstractRepository(ABC):
    @abstractmethod
    def getUser(self, tg_id):
        pass

    @abstractmethod
    def getPhone(self, phone):
        pass

    @abstractmethod
    def updateTgId(self, phone, tg_id):
        pass

    @abstractmethod
    def insertAttempt(self, tg_id):
        pass

    @abstractmethod
    def attempt(self, tg_id):
        pass

    @abstractmethod
    def deleteAttempt(self, tg_id):
        pass

    @abstractmethod
    def insertSpamList(self, tg_id, time):
        pass

    @abstractmethod
    def getSpamList(self, tg_id):
        pass

    @abstractmethod
    def deleteUserFromSpamList(self, tg_id):
        pass
