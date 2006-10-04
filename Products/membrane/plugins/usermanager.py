# Copyright 2005 Plone Solutions
# info@plonesolutions.com

import copy
from AccessControl import ClassSecurityInfo
from AccessControl.SecurityManagement import getSecurityManager
from App.class_init import default__class_init__ as InitializeClass
from OFS.Cache import Cacheable
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from zope.interface import implements

from Products.CMFCore.utils import getToolByName

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import createViewName
from Products.PluggableAuthService.interfaces.plugins \
    import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins \
    import IUserEnumerationPlugin

from Products.PlonePAS.interfaces.plugins import IUserIntrospection
from Products.PlonePAS.interfaces.plugins import IUserManagement

from Products.membrane.config import TOOLNAME
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.interfaces import IMembraneUserAuth
from Products.membrane.interfaces import IMembraneUserManagement
from Products.membrane.interfaces import IMembraneUserChanger
from Products.membrane.interfaces import IUserAuthProvider
from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.interfaces import IUserAuthentication
from Products.membrane.utils import generateCategorySetIdForType

manage_addMembraneUserManagerForm = PageTemplateFile(
    '../www/MembraneUserManagerForm', globals(), __name__='manage_addMembraneUserManagerForm' )


def addMembraneUserManager( dispatcher, id, title=None, REQUEST=None ):
    """ Add a MembraneUserManager to a Pluggable Auth Service. """

    pmm = MembraneUserManager(id, title)
    dispatcher._setObject(pmm.getId(), pmm)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
                                '%s/manage_workspace'
                                '?manage_tabs_message='
                                'MembraneUserManager+added.'
                            % dispatcher.absolute_url())


class MembraneUserManager(BasePlugin, Cacheable):
    """ PAS plugin for managing contentish members in Plone.
    """
    meta_type = 'Membrane User Manager'

    security = ClassSecurityInfo()

    implements(IAuthenticationPlugin,
               IUserEnumerationPlugin,
               IUserIntrospection,
               IUserManagement
               )

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title

    #
    #   IAuthenticationPlugin implementation
    #
    security.declarePrivate('authenticateCredentials')
    def authenticateCredentials(self, credentials):
        """ See IAuthenticationPlugin.

        o We expect the credentials to be those returned by
          ILoginPasswordExtractionPlugin.
        """
        login = credentials.get('login')
        password = credentials.get('password')

        if login is None or password is None:
            return None

        # We can't depend on security when authenticating the user,
        # or we'll get stuck in loops
        mbtool = getToolByName(self, TOOLNAME)
        member = mbtool.getUserAuthProvider(login)
        if member is None:
            return None
        # Check workflow state is active
        wftool = getToolByName(self, 'portal_workflow')
        review_state = wftool.getInfoFor(member, 'review_state')
        wfmapper = ICategoryMapper(mbtool)
        cat_set = generateCategorySetIdForType(member.portal_type)
        if not wfmapper.isInCategory(cat_set, ACTIVE_STATUS_CATEGORY,
                                     review_state):
            return None
        # Delegate to member object
        member = IMembraneUserAuth(member)
        return member.authenticateCredentials(credentials)


    #
    #   IUserEnumerationPlugin implementation
    #
    security.declarePrivate( 'enumerateUsers' )
    def enumerateUsers( self
                      , id=None
                      , login=None
                      , exact_match=False
                      , sort_by=None
                      , max_results=None
                      , **kw
                      ):
        """ See IUserEnumerationPlugin.
        """
        user_info = []
        plugin_id = self.getId()
        view_name = createViewName('enumerateUsers', id or login)

        if isinstance( id, str ):
            id = [ id ]

        if isinstance( login, str ):
            login = [ login ]

        # Look in the cache first...
        keywords = copy.deepcopy(kw)
        keywords.update( { 'id' : id
                         , 'login' : login
                         , 'exact_match' : exact_match
                         , 'sort_by' : sort_by
                         , 'max_results' : max_results
                         }
                       )
        cached_info = self.ZCacheable_get( view_name=view_name
                                         , keywords=keywords
                                         , default=None
                                         )
        if cached_info is not None:
            return tuple(cached_info)

        mbtool = getToolByName(self, TOOLNAME)
        query = {}

        # Note: ZCTextIndex doesn't allow 'contains' searches AFAICT,
        #       so we use 'starts with'.
        if login:
            query['getUserName'] = exact_match and login or \
                                   ['%s*' % l for l in login]

        elif id:
            query['getUserId'] = exact_match and id or \
                                 ['%s*' % i for i in id]

        if sort_by is not None:
            if sort_by == 'login':
                query['sort_on'] = 'getUserName'
            if sort_by == 'id':
                query['sort_on'] = 'getUserId'

        query['object_implements'] = {'query': (IMembraneUserAuth.__identifier__,
                                                IUserAuthProvider.__identifier__,
                                                IUserAuthentication.__identifier__),
                                      'operator': 'and'}

        members = mbtool.unrestrictedSearchResults(**query)

        if max_results is not None:
            members = members[:max_results]

        for m in members:
            member = m._unrestrictedGetObject()
            authentication = IUserAuthentication(member)
            username = authentication.getUserName()
            authprovider = IUserAuthProvider(member)
            uid = authprovider.UID()
            userid = IMembraneUserAuth(member).getUserId()
            # XXX need to ask object for the edit URL, must adhere to an
            #     interface so we know we can stay within contract
            info = { 'id': userid
                     , 'login' : username
                     , 'pluginid': plugin_id
                     , 'editurl': '%s/base_edit' % member.absolute_url()
                     , 'uid': uid
                     }
            user_info.append(info)

        # Put the computed value into the cache
        self.ZCacheable_set(user_info, view_name=view_name, keywords=keywords)

        return tuple( user_info )


    #
    #   IUserIntrospection implementation
    #
    security.declarePrivate('getUserIds')
    def getUserIds(self):
        """
        Return a list of user ids
        """
        mbtool = getToolByName(self, TOOLNAME)
        uSR = mbtool.unrestrictedSearchResults
        users = uSR(object_implements=IMembraneUserAuth.__identifier__)
        return tuple([u.getUserId for u in users])

    security.declarePrivate('getUserNames')
    def getUserNames(self):
        """
        Return a list of usernames
        """
        mbtool = getToolByName(self, TOOLNAME)
        uSR = mbtool.unrestrictedSearchResults
        users = uSR(object_implements=IUserAuthProvider.__identifier__)
        return tuple([u.getUserName for u in users])

    security.declarePrivate('getUsers')
    def getUsers(self):
        """
        Return a list of users

        XXX DON'T USE THIS, it will kill performance
        """
        uf = getToolByName(self, 'acl_users')
        return tuple([uf.getUserById(x) for x in self.getUserIds()])

    #
    # IMembraneUserChanger implementation
    #
    def doChangeUser(self, login, password, **kwargs):
        mbtool = getToolByName(self, TOOLNAME)
        uSR = mbtool.unrestrictedSearchResults
        users = uSR(object_implements=IMembraneUserChanger.__identifier__,
                    getUserName=login)
        if users:
            user = users[0]._unrestrictedGetObject()
            IMembraneUserChanger(user).doChangeUser(login, password,
                                                       **kwargs)
        else:
            raise RuntimeError, 'User does not exist: %s'%login

    #
    # IUserManagement implementation
    #
    def doDeleteUser(self, login):
        mbtool = getToolByName(self, TOOLNAME)
        uSR = mbtool.unrestrictedSearchResults
        users = uSR(object_implements=IMembraneUserManagement.__identifier__,
                    getUserName=login)
        if users:
            user = users[0]._unrestrictedGetObject()
            IMembraneUserManagement(user).doDeleteUser(login)
        else:
            raise RuntimeError, 'User does not exist: %s'%login

    def doAddUser(self, login, password):
        """This is highly usecase dependent and will need to be implemented
        independently"""
        raise NotImplementedError


InitializeClass( MembraneUserManager )
