# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Acquisition import aq_chain
from Acquisition import aq_inner
from Products.membrane.at.userrelated import UserRelated
from Products.membrane.interfaces.group import IGroup
from Products.membrane.interfaces.user import IMembraneUserGroups
from zope.interface import implementer


@implementer(IMembraneUserGroups)
class Groups(UserRelated):
    """
    Adapts from IGroupsProvider to IMembraneUserGroups, gets groups
    from acquisition and backrefs
    """
    security = ClassSecurityInfo()

    #
    #   IGroupsPlugin implementation
    #
    @security.private
    def getGroupsForPrincipal(self, principal, request=None):
        groups = {}
        # Get all BRefs that implement IGroup - slightly expensive
        for obj in self.context.getBRefs():
            group = IGroup(obj, None)
            if group is not None:
                groups[group.getGroupId()] = 1
        for parent in aq_chain(aq_inner(self.context)):
            group = IGroup(parent, None)
            if group is not None:
                groups[group.getGroupId()] = 1
        return tuple(groups.keys())


@implementer(IMembraneUserGroups)
class SelectedGroups(UserRelated):
    """
    Adapts from ISelectedGroupsProvider to IMembraneUserGroups; gets groups
    from acquisition and backrefs w/ a specific relationship.
    """
    security = ClassSecurityInfo()

    def __init__(self, context):
        self.context = context

    #
    #   IGroupsPlugin implementation
    #
    @security.private
    def getGroupsForPrincipal(self, principal, request=None):
        groups = {}
        for relationship in self.context.getGroupRelationships():
            groups.update(dict.fromkeys([g.getUserId() for g in
                                         self.context.getBRefs(relationship)]))
        for parent in aq_chain(aq_inner(self.context)):
            group = IGroup(parent, None)
            if group is not None:
                groups[group.getGroupId()] = 1
        return tuple(groups.keys())
