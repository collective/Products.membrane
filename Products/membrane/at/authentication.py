# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.membrane.at.interfaces import IUserAuthentication
from Products.membrane.at.userrelated import UserRelated
from Products.membrane.interfaces.user import IMembraneUserAuth
from Products.membrane.interfaces.user import IMembraneUserObject
from zope.interface import implementer


@implementer(IMembraneUserAuth)
class Authentication(UserRelated):
    """
    Adapts from IUserAuthProvider to IMembraneUserAuth.
    """
    security = ClassSecurityInfo()

    #
    #   IAuthenticationPlugin implementation
    #
    @security.private
    def authenticateCredentials(self, credentials):
        login = credentials.get('login')
        password = credentials.get('password')

        if login is None or password is None:
            return None

        # Adapt to IUserAuthentication to provide the actual authentication.
        # If no such adapter (or null-adapter) exists, fail.
        authentication = IUserAuthentication(self.context, None)
        if authentication is None:
            return None

        if authentication.verifyCredentials(credentials):
            info = IMembraneUserObject(self.context, self)
            userid = info.getUserId()
            return userid, login
