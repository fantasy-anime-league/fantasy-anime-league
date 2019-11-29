from __future__ import annotations

from typing import List, Tuple, TYPE_CHECKING
import io
import http.client
import re
import gzip
import configparser

from fal.orm import Secret, mfalncfm_main
from fal.models import Team, Season, SeasonOfYear, Anime
from .base import Controller

if TYPE_CHECKING:
    from sqlalchemy.orm import Session

httpconn = http.client.HTTPSConnection("myanimelist.net")

config = configparser.ConfigParser()
config.read("config.ini")


class BenchSwaps(Controller):
    MAL_PARAMS = ""

    def get_swaps(
        self,
        session: Session,
        page: int = config.getint("weekly info", "bench-swap-page-start"),
        actions: List[Tuple] = [],
    ) -> List[Tuple]:
        """
        NOTE: copied from old FAL script and converted to Python 3 and uses our modern stack

        Collects swaps for the current week.

        This function accesses the swap thread.

        @param page page identification for threads
        @param actions list of tuples (username, post content)

        @return list of tuples (username, post content = swap)
        """
        header = dict(config.items("myanimelist.net request header"))

        secret_request_headers = (
            session.query(Secret)
            .filter(Secret.context == "myanimelist.net request header")
            .all()
        )
        for row in secret_request_headers:
            header[row.key] = row.value

        httpconn.connect()
        httpconn.request(
            "GET",
            "/forum/?topicid=%s&show=%i"
            % (config.getint("myanimelist", "bench-swap-thread-id"), (page - 1) * 50),
            BenchSwaps.MAL_PARAMS,
            header,
        )
        res = httpconn.getresponse()
        if res.getheader("Content-Encoding") == "gzip":
            response = gzip.GzipFile(fileobj=io.BytesIO(res.read())).read()
        else:
            response = res.read()
        httpconn.close()
        pattern = 'postnum">(\d+).+?row2.+?<strong>(.+?)</strong>.+?row1.+?message\d.+?class="clearfix">(.+?)</div>'
        actions.extend(re.findall(pattern, str(response), re.S))
        if page == config.getint("weekly info", "bench-swap-page-end"):
            return [
                tuple(a[1:])
                for a in actions
                if int(a[0]) >= config.getint("weekly info", "bench-swap-post-start")
                and int(a[0]) <= config.getint("weekly info", "bench-swap-post-end")
            ]
        else:
            return self.get_swaps(session=session, page=page + 1, actions=actions)

    def _execute(self, session: Session, season: Season) -> None:
        post_content_regex = re.compile(r"(.+)\<br /\>.*\\n(.+)")
        for username, post_content in self.get_swaps(session):
            match = post_content_regex.fullmatch(post_content)
            try:
                assert match
            except AssertionError:
                print(f"Unexpected post contents: {post_content}")
                raise
            active, bench = match.group(1, 2)
            team = Team.get_by_name(name=username, season=season, session=session)
            team.bench_swap(
                active_anime=Anime.get_by_name(active, session),
                bench_anime=Anime.get_by_name(bench, session),
                week=self.current_week,
            )
