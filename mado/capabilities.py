from __future__ import annotations

from abc import abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from mado.application_window import Window


class ReadonlyCapable:
    @abstractmethod
    def set_readonly(self) -> None:
        pass
