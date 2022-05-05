from typing import List

from fastapi_dream_core.application_dependencies.application_dependencies_abc import ApplicationDependenciesABC
from fastapi_dream_core.routes.health.health_schemas import DependencyHealthCheckSchema
from fastapi_dream_core.utils.singleton_meta import SingletonMeta


class ApplicationDependencyException(Exception):
    pass


class Readiness(metaclass=SingletonMeta):

    __dependencies: List[ApplicationDependenciesABC] = []

    def add_dependency(self, dependency: ApplicationDependenciesABC):
        if not isinstance(dependency, ApplicationDependenciesABC):
            raise ApplicationDependencyException(f"Readiness.add_dependency expected ApplicationDependenciesABC")

        self.__dependencies.append(dependency)

    def ready(self) -> List[DependencyHealthCheckSchema]:
        return [
            DependencyHealthCheckSchema(
                name=str(dependency),
                ready=dependency.readiness()
            )
            for dependency in self.__dependencies
        ]
