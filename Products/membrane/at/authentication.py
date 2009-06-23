from AccessControl import ClassSecurityInfo
from zope.interface import implements

from Products.CMFCore import utils

from Products.membrane.interfaces.user import IMembraneUserObject
from Products.membrane.interfaces.user import IMembraneUserAuth
from Products.membrane.interfaces.categorymapper import ICategoryMapper
from Products.membrane.utils import generateCategorySetIdForType
from Products.membrane import config
from Products.membrane.at.interfaces import IUserAuthentication
from Products.membrane.at.userrelated import UserRelated


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

        # Check workflow state is active
        wftool = utils.getToolByName(self.context, 'portal_workflow')
        review_state = wftool.getInfoFor(self.context, 'review_state')

        mbtool = utils.getToolByName(self.context, config.TOOLNAME)
        wfmapper = ICategoryMapper(mbtool)
        cat_set = generateCategorySetIdForType(
            self.context.portal_type)

        if not wfmapper.isInCategory(
            cat_set, config.ACTIVE_STATUS_CATEGORY, review_state):
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
