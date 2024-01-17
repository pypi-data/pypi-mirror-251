
from typing import Protocol

class PbarProtocol(Protocol):
    
    def update(self, value: float | int):
        pass