from __future__ import annotations

from abc import abstractmethod
from typing import List, Dict, Optional, Type

from mado.data_repository import DataRepository
from mado.entity.operations import BasicRecordViewer, BasicRecordCreator, BasicRecordManager, RecordManager, \
    RecordCreator, \
    RecordViewer
from mado.form_body import FormBody, FormType


class EntityConfig:
    entity_label: str = "Наименование сущности"
    repository: DataRepository
    table_labels: List[str] = ["Наименование"]
    table_columns: List[str] = ["name"]

    manager: Type[RecordManager] = BasicRecordManager
    creator: Type[RecordCreator] = BasicRecordCreator
    viewer: Type[RecordViewer] = BasicRecordViewer

    def validate_record(self, data: Dict[str, any]) -> Optional[str]:
        return None

    def to_database(self, data: Dict[str, any]) -> Dict[str, any]:
        return data

    def from_database(self, data: Dict[str, any]) -> Dict[str, any]:
        return data

    def process_commit_error(self, err: str) -> str:
        return "Неизвестная ошибка"

    def process_delete_error(self, err: str) -> str:
        if err.startswith("FOREIGN KEY constraint failed"):
            return "Невозможно удалить эту запись, так как от неё зависит запись другой сущности"

    @abstractmethod
    def make_form(self, type_: FormType) -> FormBody:
        pass


class EventConfig(EntityConfig):
    def pre_save(self, data: Dict[str, any]) -> str | None:
        pass

    @abstractmethod
    def make_form(self, type_: FormType) -> FormBody:
        pass
