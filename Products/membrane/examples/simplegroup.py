# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo

from zope.interface import implements

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.public import BaseSchema, Schema, BaseFolder
from Products.Archetypes.public import ReferenceField, ReferenceWidget
from Products.Archetypes.public import LinesField, MultiSelectionWidget
from Products.Archetypes.public import registerType
from Products.Archetypes.public import DisplayList

from Products.membrane.interfaces import user as user_ifaces
from Products.membrane.interfaces.group import IGroup
from Products.membrane.config import PROJECTNAME, TOOLNAME
from Products.membrane.utils import getFilteredValidRolesForPortal

SimpleSchema = BaseSchema + Schema((

    ReferenceField(
        name='manager',
        relationship='managesProject',
        allowed_types=('SimpleMember',),
        vocabulary='listUsers',
        languageIndependent=1,
        widget=ReferenceWidget(
            label='Group manager',
            description='The manager of this project.'
        ),
    ),

    ReferenceField(
        name="members",
        relationship='participatesInProject',
        multiValued=1,
        languageIndependent=1,
        allowed_types=('SimpleMember',),
        vocabulary='listUsers',
        widget=ReferenceWidget(
            label='Associated group members',
            description='''\
Members of this group that are really from other groups''',
        ),
    ),

    LinesField(
        # not 'roles' b/c 'validate_roles' exists; stoopid Archetypes
        name="roles_",
        accessor='getRoles',
        languageIndependent=1,
        vocabulary='getRoleSet',
        multiValued=1,
        widget=MultiSelectionWidget(
            label="Roles",
            description="Roles that members of this group should receive.",
        ),
    ),
))


class SimpleGroup(BaseFolder):
    """A simple group archetype"""
    schema = SimpleSchema
    _at_rename_after_creation = True

    implements(IGroup)

    security = ClassSecurityInfo()

    def getGroupName(self):
        return self.getId()

    #####################################################
    # IGroup implementation
    # NOTE: Title() and getRoles() are autogenerated
    #####################################################
    def getGroupId(self):
        return self.getId()

    def getGroupMembers(self):
        # All references and all subobjects that are members
        members = dict.fromkeys(
            [user_ifaces.IMembraneUserAuth(m).getUserId() for m in
             self.getRefs('participatesInProject')])
        mt = getToolByName(self, TOOLNAME)
        usr = mt.unrestrictedSearchResults
        for m in usr(
                object_implements=(
                    user_ifaces.IMembraneUserAuthAvail.__identifier__),
                path='/'.join(self.getPhysicalPath())):
            members[m.getUserId] = 1
        return tuple(members.keys())

    def listUsers(self):
        """
        Return a DisplayList of users
        """
        catalog = getToolByName(self, TOOLNAME)

        results = catalog(object_implements=(
            user_ifaces.IMembraneUserAuthAvail.__identifier__))
        value = []
        for r in results:
            key = r.getUserName is not None and \
                r.getUserName.strip() or r.getUserId
            value.append((key.lower(), (r.UID, key)))
        value.sort()
        value = [r for throwaway, r in value]
        value.insert(0, ('', '<no reference>'))
        return DisplayList(value)

    getRoleSet = getFilteredValidRolesForPortal

registerType(SimpleGroup, PROJECTNAME)
