def login_client(client, username="user_SA", password="test1234"):
    assert client.login(
        username=username, password=password
    ), "Login échoué dans les tests"
    return client
