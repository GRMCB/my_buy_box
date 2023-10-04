from unittest.mock import patch

def test_healthcheck(app_test_client):
    with patch(app_test_client.get) as mock_query:
        # Set up the mock object to return the desired data
        mock_query.return_value = [(1,)]

        """ This test tests whether the /health endpoint returns Healthy"""
        response = mock_query('/health')

    assert "Data Collector app is Healthy" in response.text