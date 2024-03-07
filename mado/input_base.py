from __future__ import annotations

from abc import abstractmethod

from mado.capabilities import ReadonlyCapable


class InputBase(ReadonlyCapable):
    @abstractmethod
    def get_value(self) -> any:
        raise NotImplementedError

    @abstractmethod
    def set_value(self, value: any):
        raise NotImplementedError

    def set_readonly(self) -> None:
        pass
