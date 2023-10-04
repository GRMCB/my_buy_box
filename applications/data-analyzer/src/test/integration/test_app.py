def test_healthcheck(app_test_client):
    """ This test tests whether the /health endpoint returns Healthy"""
    response = app_test_client.post('/health')

    assert "Data Analyzer app is Healthy" in response.text