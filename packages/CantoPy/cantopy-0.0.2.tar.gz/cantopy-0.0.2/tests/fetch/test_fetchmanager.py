import pytest
from cantopy.fetch import FetchManager
from cantopy.xenocanto_components import Query

@pytest.fixture
def fetch_manager():
    return FetchManager()


@pytest.fixture
def query():
    return Query(name="common blackbird", q="A")


def test_query_singlepage(fetch_manager: FetchManager, query: Query):
    """Test a single page fetch to the XenoCanto API.

    Parameters
    ----------
    fetch_manager : FetchManager
        An instance of the FetchManager class.
    query : Query
        The Query object to send to the XenoCanto API.
    """

    # Send a simple query
    query_result = fetch_manager.send_query(query)

    # See if the ResultPage object contain the requested information
    assert len(query_result.result_pages) == 1
    assert query_result.result_pages[0].recordings[0].english_name == "Common Blackbird"
    assert query_result.result_pages[0].recordings[0].quality_rating== "A"


def test_query_multipage(fetch_manager: FetchManager, query: Query):
    """Test a multi (3) page fetch to the XenoCanto API.

    Parameters
    ----------
    fetch_manager : FetchManager
        An instance of the FetchManager class.
    query : Query
        The Query object to send to the XenoCanto API.
    """

    # Send a simple query
    query_result = fetch_manager.send_query(query, max_pages=3)

    # See if the ResultPage object contain the requested information
    assert len(query_result.result_pages) == 3
    assert query_result.result_pages[0].recordings[0].english_name == "Common Blackbird"
    assert query_result.result_pages[0].recordings[0].quality_rating == "A"
