from auth import auth_register
from auth import auth_logout
from auth import auth_login

'''
Elements of securely storing passwords, and returning intelligent tokens, are not required for iteration 1. You can simply store passwords plainly, and tokens can just be a user's "ID" or "email" (up to you). We will discuss ways to improve the quality and methods of these capabilities in iteration 2.
'''

result = auth.auth_register('validemail@gmail.com', '123abc!@#', 'Hayden', 'Everest')
auth.auth_login('validemail@gmail.com', '123abc!@#') # Expect to work since we registered
