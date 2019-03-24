from typing import Optional, Dict
import abc


class AbstractJikan(abc.ABC):
    def __init__(self,
                 selected_base: Optional[str] = None,
                 use_ssl: bool = True
                 ) -> None: ...

    def anime(self,
              id: int,
              extension: Optional[str] = None,
              page: Optional[int] = None
              ) -> Dict: ...
