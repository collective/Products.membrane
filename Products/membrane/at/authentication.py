from AccessControl import ClassSecurityInfo
from zope.interface import implements

from Products.membrane.interfaces import IMembraneUserAuth
from Products.membrane.interfaces import IUserAuthentication
from userrelated import UserRelated


class Authentication(UserRelated):
    """
    Adapts from IUserAuthProvider to IMembraneUserAuth.
    """
    security = ClassSecurityInfo()

    implements(IMembraneUserAuth)

    #
    #   IAuthenticationPlugin implementation
    #
    security.declarePrivate('authenticateCredentials')
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
            userid = self.getUserId()
            return userid, login
