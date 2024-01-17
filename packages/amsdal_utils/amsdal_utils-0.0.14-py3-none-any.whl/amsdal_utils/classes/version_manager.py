from pydantic import BaseModel

from amsdal_utils.utils.singleton import Singleton


class ClassVersion(BaseModel):
    class_name: str
    version: str
    is_latest: bool


class ClassVersionManager(metaclass=Singleton):
    def __init__(self) -> None:
        self._class_versions: list[ClassVersion] = []

    def register_class_version(
        self,
        class_name: str,
        version: str,
        *,
        is_latest: bool,
        unregister_previous_versions: bool = True,
    ) -> None:
        _registered_class_version = next(
            (
                class_version
                for class_version in self._class_versions
                if class_version.class_name == class_name and class_version.version == version
            ),
            None,
        )

        if _registered_class_version:
            return

        if unregister_previous_versions:
            self._class_versions = [
                class_version for class_version in self._class_versions if class_version.class_name != class_name
            ]
        elif is_latest:
            for class_version in self._class_versions:
                if class_version.class_name == class_name and class_version.is_latest:
                    class_version.is_latest = False

        self._class_versions.append(
            ClassVersion(
                class_name=class_name,
                version=version,
                is_latest=is_latest,
            ),
        )

    def clear_versions(self) -> None:
        self._class_versions.clear()

    def get_class_versions(self, class_name: str) -> list[ClassVersion]:
        return [class_version for class_version in self._class_versions if class_version.class_name == class_name]

    def get_latest_class_version(self, class_name: str) -> ClassVersion:
        return next(
            (
                class_version
                for class_version in self._class_versions
                if class_version.class_name == class_name and class_version.is_latest
            ),
        )
