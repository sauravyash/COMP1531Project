#from auth import auth_register
import auth
import pytest
from error import InputError

#Successful registrations
def test_valid():
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')

#Unsuccesful registrations
def test_invalidemail():
    with pytest.raises(InputError) as e:
        result = auth.auth_register('invalidemail.com', '123abc!@#', 'fname', 'lname')
        print(result)

def test_invalidpassword():
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail2@gmail.com', '123', 'fname', 'lname')

def test_invalidfname():
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail3@gmail.com', '123abc!@#', 'invalidfirstnamewhichisgoingtobemorethan50characterslong', 'lname')

def test_invalidlname():
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail4@gmail.com', '123abc!@#', 'fname', 'invalidlastnamewhichisgoingtobemorethan50characterslong')

def test_alreadyregistered():
    with pytest.raises(InputError) as e:
        auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
