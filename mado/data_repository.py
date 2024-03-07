from abc import ABC, abstractmethod
from typing import Sequence, Dict, List

from sqlalchemy import Table, RowMapping, select, update, delete, insert

from mado.db import get_conn


class DataRepository(ABC):
    @abstractmethod
    def fetch_one(self, id_: int) -> RowMapping | Dict[str, any] | None:
        pass

    @abstractmethod
    def fetch_all(self) -> Sequence[RowMapping] | List[Dict[str, any]]:
        pass

    @abstractmethod
    def delete(self, id_: int) -> None:
        pass

    @abstractmethod
    def insert(self, data: Dict[str, any]) -> int:
        pass

    @abstractmethod
    def update(self, id_: int, data: Dict[str, any]) -> None:
        pass


class BasicDataRepository(DataRepository):
    table: Table

    def __init__(self, table: Table) -> None:
        self.table = table

    def fetch_one(self, id_: int) -> RowMapping | None:
        return get_conn().execute(select(self.table).where(self.table.c.id == id_)).mappings().first()

    def fetch_all(self) -> Sequence[RowMapping]:
        return get_conn().execute(select(self.table)).mappings().all()

    def delete(self, id_: int) -> None:
        get_conn().execute(delete(self.table).where(self.table.c.id == id_))
        get_conn().commit()

    def insert(self, data: Dict[str, any]) -> int:
        res = get_conn().execute(insert(self.table).values(data))
        get_conn().commit()

        return res.lastrowid

    def update(self, id_: int, data: Dict[str, any]) -> None:
        get_conn().execute(update(self.table).where(self.table.c.id == id_).values(data))
        get_conn().commit()
