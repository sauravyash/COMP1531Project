''' Auth register tests
This file contains all test cases for auth register function.

'''
import auth
import other
import pytest
from error import InputError

# ----- Successful registrations
def test_valid():
    other.clear()
    # Register a user
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')

# ----- Unsuccesful registrations
def test_invalid_email():
    other.clear()
    # Check that an error is raised for invalid email.
    with pytest.raises(InputError):
        result = auth.auth_register('invalidemail.com', '123abc!@#', 'fname', 'lname')

def test_invalid_password():
    other.clear()
    # Check an error is raised for invalid password.
    with pytest.raises(InputError):
        auth.auth_register('validemail@gmail.com', '123', 'fname', 'lname')

def test_empty_password():
    other.clear()
    with pytest.raises(InputError):
        auth.auth_register('validemail@gmail.com', '', 'fname', 'lname')

def test_invalid_fname():
    other.clear()
    # Check that an error is raised for invalid first name.
    with pytest.raises(InputError):
        auth.auth_register('validemail@gmail.com', '123abc!@#', 'invalidfirstnamewhichisgoingtobemorethan50characterslong', 'lname')

def test_invalid_lname():
    other.clear()
    # Check that an error is raised for invalid last name.
    with pytest.raises(InputError):
        auth.auth_register('validemail@gmail.com', '123abc!@#', 'fname', 'invalidlastnamewhichisgoingtobemorethan50characterslong')

def test_empty_first_name():
    other.clear()
    # Check that an error is raised for empty first name.
    with pytest.raises(InputError):
        auth.auth_register('validemail@gmail.com', '123abc!@#', '', 'lname')

def test_empty_last_name():
    other.clear()
    # Check that an error is raised for empty last name.
    with pytest.raises(InputError):
        auth.auth_register('validemail@gmail.com', '123abc!@#', 'fname', '')

def test_already_registered():
    other.clear()
    # Register a user.
    auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
    # Check that user can not be logged in again.
    with pytest.raises(InputError):
        auth.auth_register('validemail@gmail.com', 'validpassword', 'fname', 'fname')
