# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.membrane.at.interfaces import IUserAuthentication
from Products.membrane.at.userrelated import UserRelated
from Products.membrane.interfaces.user import IMembraneUserAuth
from Products.membrane.interfaces.user import IMembraneUserObject
from zope.interface import implements


class Authentication(UserRelated):
    """
    Adapts from IUserAuthProvider to IMembraneUserAuth.
    """
    security = ClassSecurityInfo()

    implements(IMembraneUserAuth)

    #
    #   IAuthenticationPlugin implementation
    #
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
    security.declarePrivate('authenticateCredentials')
