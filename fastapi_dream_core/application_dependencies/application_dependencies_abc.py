from abc import ABC


class ApplicationDependenciesABC(ABC):

    def readiness(self) -> bool:
        """Not Implemented"""
