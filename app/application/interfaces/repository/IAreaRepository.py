from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.entities import Area

class IAreaRepository(ABC):

    @abstractmethod
    def opteberAreaPorId(self, idArea:int) -> Area:
        pass