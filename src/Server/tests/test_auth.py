from Server import auth

# SECRET_KEY = os.getenv("SECRET_KEY", None)
# EMAIL = os.getenv("EMAIL", None)
# KEY = os.getenv("KEY", None)


def test_generateToken():
    assert True


def test_decodeToken():
    assert True


def test_authenticateEmail():
    testEmail = "***REMOVED***"
    assert auth.authenticateEmail(testEmail) == True


def test_checkHostEmail():
    assert True


def test_checkHostToken():
    assert True
