
def test_home_page(app_test_client):
    response = app_test_client.get('/')
    assert response.status_code == 200
    assert b'Enter your zip code:' in response.data

def test_redirect(app_test_client):
    """ This test tests whether the /verify endpoint correctly redirects to zipcode/<zipcode>"""
    response = app_test_client.post('/verify', data={'zip': '12345'})

    assert response.status_code == 302
    assert response.headers['Location'] == '/zipcode/12345'
