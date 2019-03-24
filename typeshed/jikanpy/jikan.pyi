from typing import Optional, Dict

from jikanpy.abstractjikan import AbstractJikan


class Jikan(AbstractJikan):
    def season(self, year: int, season: str) -> Dict: ...

    def user(self,
             username: str,
             request: Optional[str] = None,
             argument: Optional[str] = None,
             page: Optional[int] = None
             ) -> Dict: ...
