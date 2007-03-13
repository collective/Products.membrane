from Products.membrane.setuphandlers import _doRegisterUserAdderUtility

from utilities import UserAdder

PROFILE_ID = "profile-membrane:examples"
ADDUSER_UTILITY_NAME = "membrane example"

def registerUserAdderUtility(context):
    _doRegisterUserAdderUtility(context, 'membrane-examples-useradder',
                                PROFILE_ID, ADDUSER_UTILITY_NAME,
                                UserAdder())
