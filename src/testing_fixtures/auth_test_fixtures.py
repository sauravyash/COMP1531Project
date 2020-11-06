import pytest

import auth
import channels
import other

@pytest.fixture()
def setup_test_interface():
    other.clear()
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    user = auth.auth_login('validemail@gmail.com', 'validpassword')

    return user
