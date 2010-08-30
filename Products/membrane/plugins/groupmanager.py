# Copyright 2005 Plone Solutions
# info@plonesolutions.com

import logging
from AccessControl import ClassSecurityInfo
from App.class_init import default__class_init__ as InitializeClass
from OFS.Cache import Cacheable
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from zope.interface import implements

from Products.CMFCore.utils import getToolByName

from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from Products.PluggableAuthService.utils import createViewName
from Products.PluggableAuthService.PluggableAuthService \
    import _SWALLOWABLE_PLUGIN_EXCEPTIONS

from Products.PluggableAuthService.interfaces.plugins \
     import IGroupEnumerationPlugin
from Products.PluggableAuthService.interfaces.plugins \
    import IPropertiesPlugin
from Products.PluggableAuthService.interfaces.plugins \
    import IRolesPlugin

from Products.membrane.interfaces import group as group_ifaces
from Products.membrane.interfaces import user as user_ifaces
from Products.membrane.interfaces.plugins import IMembraneGroupManagerPlugin
from Products.membrane.config import TOOLNAME
from Products.membrane.utils import findMembraneUserAspect

# XXX REMOVE WHEN REFACTORING
from Acquisition import aq_base
from Products.PlonePAS.plugins.group import PloneGroup

manage_addMembraneGroupManagerForm = PageTemplateFile(
    '../www/MembraneGroupManagerForm', globals(),
    __name__='manage_addMembraneGroupManagerForm' )


def addMembraneGroupManager(dispatcher, id, title=None, REQUEST=None):
    """ Add a MembraneGroupManager to a Pluggable Auth Service. """

    pmm = MembraneGroupManager(id, title)
    dispatcher._setObject(pmm.getId(), pmm)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
                                '%s/manage_workspace'
                                '?manage_tabs_message='
                                'MembraneGroupManager+added.'
                            % dispatcher.absolute_url())


class MembraneGroupManager(BasePlugin, Cacheable):
    """
    PAS plugin for managing contentish groups in Plone.
    """
    meta_type = 'Membrane Group Manager'

    security = ClassSecurityInfo()

    implements(IMembraneGroupManagerPlugin)

    def __init__(self, id, title=None):
        self._id = self.id = id
        self.title = title

    #
    #   IGroupsPlugin implementation
    #
    def getGroupsForPrincipal(self, principal, request=None):
        groups = {}
        providers = findMembraneUserAspect(
            self, user_ifaces.IMembraneUserGroups,
            exact_getUserId=principal.getId())
        for provider in providers:
            pgroups = dict.fromkeys(provider.getGroupsForPrincipal(principal))
            groups.update(pgroups)
        return tuple(groups.keys())
    security.declarePrivate('getGroupsForPrincipal')

    #
    #   IGroupEnumerationPlugin implementation
    #
    def enumerateGroups(self,
                        id=None,
                        title=None,
                        exact_match=False,
                        sort_by=None,
                        max_results=None,
                        **kw
                        ):
        """
        See IGroupEnumerationPlugin.
        Quite similar to enumerateUsers, but searches for groups
        and uses title instead of login
        """
        group_info = []
        plugin_id = self.getId()

        if isinstance(id, str):
            id = [id]

        if isinstance(title, str):
            title = [title]

        mbtool = getToolByName(self, TOOLNAME)
        query = {}

        if id:
            if exact_match:
                query['exact_getGroupId'] = id
            else:
                query['getGroupId'] = ['%s*' % i for i in id if i]

        elif title:
            query['Title'] = exact_match and title or \
                             ['%s*' % t for t in title if t]

        if sort_by is not None:
            if sort_by == 'title':
                query['sort_on'] = 'Title'
            if sort_by == 'id':
                query['sort_on'] = 'getGroupId'

        query['object_implements'
              ] = group_ifaces.IGroup.__identifier__

        groups = mbtool.unrestrictedSearchResults(**query)

        i = 0
        for g in groups:
            obj = g._unrestrictedGetObject()
            group = group_ifaces.IGroup(obj, None)
            if group is None:
                continue

            if max_results is not None and i >= max_results:
                break
            i += 1
            # XXX WE NEED TO ASK THE GROUP ITSELF WHERE ITS EDIT
            # SCREENS ARE
            info = {'id': group.getGroupId(),
                    'pluginid': plugin_id,
                    'properties_url': '%s/base_edit' % obj.absolute_url(),
                    'members_url': '%s/base_edit' % obj.absolute_url(),
                     }

            group_info.append(info)

        return tuple(group_info)
    security.declarePrivate('enumerateGroups')

    #
    #   IGroupsPlugin implementation
    #
    def getGroupById(self, group_id, default=None):
        plugins = self.acl_users._getOb('plugins')

        group_id = self._verifyGroup(plugins, group_id=group_id)
        title = None

        if not group_id:
            return default

        return self._findGroup(plugins, group_id, title)

    def getGroups(self):
        return map(self.getGroupById, self.getGroupIds())

    def getGroupIds(self):
        mbtool = getToolByName(self, TOOLNAME)
        groups = mbtool.unrestrictedSearchResults(
            object_implements=group_ifaces.IGroup.__identifier__)
        return tuple([g.getGroupId for g in groups])

    def getGroupMembers(self, group_id):
        groupmembers = {}
        groups = findMembraneUserAspect(self, group_ifaces.IGroup,
                                        exact_getGroupId=group_id)
        for group in groups:
            groupmembers.update(dict.fromkeys(group.getGroupMembers()))
        return tuple(groupmembers.keys())

    # XXXXXXXXXXXXXXXXXXXXXXXXXX REMOVE FROM HERE IF POSSIBLE

    # [optilude] svn.plone.org/svn/collective/borg/tests/test_department.py
    # exercises (and found NameErrors in) this, coming from
    # portal_groups.getGroupById()

    #################################
    # group wrapping mechanics

    def _createGroup(self, plugins, group_id, name):
        """ Create group object. For users, this can be done with a
        plugin, but I don't care to define one for that now. Just uses
        PloneGroup.  But, the code's still here, just commented out.
        This method based on PluggableAuthervice._createUser
        """

        #factories = plugins.listPlugins(IUserFactoryPlugin)

        #for factory_id, factory in factories:

        #    user = factory.createUser(user_id, name)

        #    if user is not None:
        #        return user.__of__(self)

        return PloneGroup(group_id, name).__of__(self)
    security.declarePrivate('_createGroup')

    def _findGroup(self, plugins, group_id, title=None, request=None):
        """ group_id -> decorated_group
        This method based on PluggableAuthService._findGroup
        """

        # See if the group can be retrieved from the cache
        view_name = '_findGroup-%s' % group_id
        keywords = {'group_id': group_id, 'title': title}
        group = self.ZCacheable_get(view_name=view_name
                                  , keywords=keywords
                                  , default=None
                                 )

        if group is None:

            group = self._createGroup(plugins, group_id, title)

            propfinders = plugins.listPlugins(IPropertiesPlugin)
            for propfinder_id, propfinder in propfinders:

                data = propfinder.getPropertiesForUser(group, request)
                if data:
                    group.addPropertysheet(propfinder_id, data)

            groups = self.acl_users._getGroupsForPrincipal(
                group, request, plugins=plugins)
            group._addGroups(groups)

            rolemakers = plugins.listPlugins(IRolesPlugin)

            for rolemaker_id, rolemaker in rolemakers:

                roles = rolemaker.getRolesForPrincipal(group, request)

                if roles:
                    group._addRoles(roles)

            group._addRoles(['Authenticated'])

            # Cache the group if caching is enabled
            base_group = aq_base(group)
            if getattr(base_group, '_p_jar', None) is None:
                self.ZCacheable_set(base_group
                                   , view_name=view_name
                                   , keywords=keywords
                                  )

        return group.__of__(self)
    security.declarePrivate('_findGroup')

    def _verifyGroup(self, plugins, group_id=None, title=None):

        """ group_id -> boolean
        This method based on PluggableAuthService._verifyUser
        """
        criteria = {}

        if group_id is not None:
            criteria['id'] = group_id
            criteria['exact_match'] = True

        if title is not None:
            criteria['title'] = title

        if criteria:
            view_name = createViewName('_verifyGroup', group_id or title)
            cached_info = self.ZCacheable_get(view_name=view_name
                                             , keywords=criteria
                                             , default=None
                                            )

            if cached_info is not None:
                return cached_info

            enumerators = plugins.listPlugins(IGroupEnumerationPlugin)

            for enumerator_id, enumerator in enumerators:
                try:
                    info = enumerator.enumerateGroups(**criteria)

                    if info:
                        id = info[0]['id']
                        # Put the computed value into the cache
                        self.ZCacheable_set(id
                                           , view_name=view_name
                                           , keywords=criteria
                                           )
                        return id

                except _SWALLOWABLE_PLUGIN_EXCEPTIONS:
                    logger = logging.getLogger('membrane')
                    logger.debug(
                        'GroupEnumerationPlugin %s error' % enumerator_id,
                        exc_info=True)

        return 0
    security.declarePrivate('_verifyGroup')
    # XXXXXXXXXXXXXXXXXXXXXXXXXX REMOVE TO HERE

InitializeClass(MembraneGroupManager)
