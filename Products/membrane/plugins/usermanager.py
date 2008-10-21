# Copyright 2005 Plone Solutions
# info@plonesolutions.com

# Copyright 2006 The Open Planning Project
# robm <at> openplans -dot- org

import copy
from AccessControl import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass
from OFS.Cache import Cacheable
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.ZCTextIndex.ZCTextIndex import ZCTextIndex

from zope.interface import implements
from zope.annotation.interfaces import IAnnotations

from Products.CMFCore.utils import getToolByName

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import createViewName

from Products.membrane.config import TOOLNAME
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.config import QIM_ANNOT_KEY
from Products.membrane.interfaces import IMembraneUserManagerPlugin
from Products.membrane.interfaces import IMembraneUserAuth
from Products.membrane.interfaces import IMembraneUserChanger
from Products.membrane.interfaces import IMembraneUserDeleter
from Products.membrane.interfaces import IUserAuthProvider
from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.interfaces import IUserAuthentication
from Products.membrane.utils import generateCategorySetIdForType
from Products.membrane.utils import getCurrentUserAdder
from Products.membrane.utils import queryMembraneTool
from Products.membrane.utils import findImplementations


manage_addMembraneUserManagerForm = PageTemplateFile(
    '../www/MembraneUserManagerForm',
    globals(), __name__='manage_addMembraneUserManagerForm' )


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

    implements(IMembraneUserManagerPlugin)

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

        mbtool = getToolByName(self, TOOLNAME)
        query = {}

        # allow arbitrary indexes to be passed in to the catalog query
        query_index_map = IAnnotations(mbtool).get(QIM_ANNOT_KEY)
        if query_index_map is not None:
            for keyword in kw.keys():
                if keyword in query_index_map:
                    index_name = query_index_map[keyword]
                    search_term = kw[keyword]
                    if search_term is not None:
                        if not exact_match:
                            index = mbtool.Indexes[index_name]
                            if type(index) == ZCTextIndex:
                                # split, glob, join
                                sep = search_term.strip().split()
                                sep = ["%s*" % val for val in sep]
                                search_term = ' '.join(sep)
                        query[index_name] = search_term

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

        # Note: ZCTextIndex doesn't allow 'contains' searches AFAICT,
        #       so we use 'starts with'.
        if login:
            if exact_match:
                query['exact_getUserName'] = login
            else:
                query['getUserName'] = ['%s*' % l for l in login]

        elif id:
            if exact_match:
                query['exact_getUserId'] = id
            else:
                query['getUserId'] = ['%s*' % i for i in id]

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
        users = findImplementations(self, IMembraneUserAuth)
        return tuple([u.getUserId for u in users])

    security.declarePrivate('getUserNames')
    def getUserNames(self):
        """
        Return a list of usernames
        """
        users = findImplementations(self, IUserAuthProvider)
        return tuple([u.getUserName for u in users])

    security.declarePrivate('getUsers')
    def getUsers(self):
        """
        Return a list of users

        XXX DON'T USE THIS, it will kill performance
        """
        uf = getToolByName(self, 'acl_users')
        return tuple([uf.getUserById(x) for x in self.getUserIds()])

    def _getUserChanger(self, login):
        return queryMembraneTool(
            self,
            object_implements=IMembraneUserChanger.__identifier__,
            getUserName=login)

    #
    # IUserManagement implementation
    # (including IMembraneUserChanger implementation)
    #
    def doChangeUser(self, login, password, **kwargs):
        users = self._getUserChanger(login)
        if users:
            user = users[0]._unrestrictedGetObject()
            IMembraneUserChanger(user).doChangeUser(login, password,
                                                    **kwargs)
        else:
            raise RuntimeError, 'No adapter found for user: %s'%login

    def doDeleteUser(self, login):
        users = queryMembraneTool(self,
                                  object_implements=IMembraneUserDeleter.__identifier__,
                                  getUserName=login)
        if users:
            user = users[0]._unrestrictedGetObject()
            IMembraneUserDeleter(user).doDeleteUser(login)
        else:
            raise RuntimeError, 'No adapter found for user: %s'%login

    def doAddUser(self, login, password):
        """
        This is highly usecase dependent, so it delegates to a local
        utility
        """
        adder = getCurrentUserAdder(self)
        if adder is not None:
            adder.addUser(login, password)
            return True
        else:
            raise(NotImplemented, "IUserAdder utility not available")

    def allowPasswordSet(self, login):
        """
        Check if we have access to set the password.
        We can verify this by checking if we can adapt to an IUserChanger
        """
        return bool(self._getUserChanger(login))

    def allowDeletePrincipal(self, login):
        """
        Check to see if the user can be deleted by trying to adapt
        to an IMembraneUserDeleter
        """
        return bool(queryMembraneTool(self,
                                      object_implements=IMembraneUserDeleter.__identifier__,
                                      getUserName=login))
        

InitializeClass( MembraneUserManager )
