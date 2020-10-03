import auth
import other
import pytest
from error import InputError

#Successful registrations
def test_valid():
    other.clear()
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')

#Unsuccesful registrations
def test_invalidemail():
    other.clear()
    with pytest.raises(InputError) as e:
        result = auth.auth_register('invalidemail.com', '123abc!@#', 'fname', 'lname')
        print(result)

def test_invalidpassword():
    other.clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', '123', 'fname', 'lname')

def test_invalidfname():
    other.clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', '123abc!@#', 'invalidfirstnamewhichisgoingtobemorethan50characterslong', 'lname')

def test_invalidlname():
    other.clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', '123abc!@#', 'fname', 'invalidlastnamewhichisgoingtobemorethan50characterslong')

def test_nofirstname():
    other.clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', '123abc!@#', '', 'lname')

def test_nolastname():
    other.clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', '123abc!@#', 'fname', '')

def test_alreadyregistered():
    other.clear()
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
