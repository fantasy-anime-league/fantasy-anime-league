from fal.models import PlanToWatch
from fal.clients.mfalncfm_main import session_scope

import pytest

from datetime import date


@pytest.mark.parametrize(
    "date,ptw_counts", [(date(2019, 3, 6), {34134: 311499, 38524: 98614})]
)
def test_query_ptw(date, ptw_counts):
    with session_scope(True) as session:
        query = (
            session.query(PlanToWatch)
            .filter(PlanToWatch.date == date)
            .filter(PlanToWatch.anime_id.in_(ptw_counts.keys()))
        )
        ptw_entries = query.all()
        assert len(ptw_entries) == 2
        for ptw_entry in ptw_entries:
            assert ptw_entry.anime_id in ptw_counts.keys()
            assert ptw_entry.date == date
            assert ptw_entry.count == ptw_counts[ptw_entry.anime_id]
