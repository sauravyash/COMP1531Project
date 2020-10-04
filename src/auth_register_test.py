import auth
import other
import pytest
from error import InputError

#Successful registrations
def test_valid():
    other.clear()
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')

#Unsuccesful registrations
def test_invalid_email():
    other.clear()
    with pytest.raises(InputError) as e:
        result = auth.auth_register('invalidemail.com', '123abc!@#', 'fname', 'lname')
        print(result)

def test_invalid_password():
    other.clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', '123', 'fname', 'lname')

def test_empty_password():
    other.clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', '', 'fname', 'lname')

def test_invalid_fname():
    other.clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', '123abc!@#', 'invalidfirstnamewhichisgoingtobemorethan50characterslong', 'lname')

def test_invalid_lname():
    other.clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', '123abc!@#', 'fname', 'invalidlastnamewhichisgoingtobemorethan50characterslong')

def test_empty_first_name():
    other.clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', '123abc!@#', '', 'lname')

def test_empty_last_name():
    other.clear()
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', '123abc!@#', 'fname', '')

def test_already_registered():
    other.clear()
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
