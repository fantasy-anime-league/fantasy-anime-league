import pytest

from fal.controllers.ptw_counter import PTWEntry


@pytest.fixture
def ptw_fixture():
    return [PTWEntry('One Punch Man Season 2', 34134, '311,499'),
            PTWEntry('Shingeki no Kyojin Season 3 Part 2', 38524, '98,614')]
