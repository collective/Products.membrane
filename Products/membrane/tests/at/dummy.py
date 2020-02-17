# -*- coding: utf-8 -*-
from AccessControl import ClassSecurityInfo
from Products.Archetypes.public import BaseContent
from Products.Archetypes.public import BaseFolder
from Products.Archetypes.public import BaseSchema
from Products.Archetypes.public import BooleanField
from Products.Archetypes.public import DisplayList
from Products.Archetypes.public import LinesField
from Products.Archetypes.public import ReferenceField
from Products.Archetypes.public import registerType
from Products.Archetypes.public import Schema
from Products.Archetypes.public import StringField
from Products.CMFCore.utils import getToolByName
from Products.membrane.at.interfaces import IGroupAwareRolesProvider
from Products.membrane.at.interfaces import IGroupPropertiesProvider
from Products.membrane.at.interfaces import IGroupsProvider
from Products.membrane.at.interfaces import ISchemataPropertiesProvider
from Products.membrane.at.interfaces import ISelectedGroupsProvider
from Products.membrane.at.interfaces import IUserAuthentication
from Products.membrane.at.interfaces import IUserAuthProvider
from Products.membrane.at.interfaces import IUserPropertiesProvider
from Products.membrane.at.interfaces import IUserRoles
from Products.membrane.config import PROJECTNAME
from Products.membrane.config import TOOLNAME
from Products.membrane.interfaces import group as group_ifaces
from Products.membrane.interfaces import user as user_ifaces
from zope.interface import implementer


GROUP_RELATIONSHIP = 'participatesInProject'

group = BaseSchema.copy() + Schema((
    ReferenceField(
        name='manager',
        relationship='managesProject',
        allowed_types=('Member', 'TestMember',),
        vocabulary='listUsers',
        languageIndependent=1),
    ReferenceField(
        name="members",
        relationship=GROUP_RELATIONSHIP,
        multiValued=1,
        languageIndependent=1,
        allowed_types=('Member', 'TestMember',),
        vocabulary='listUsers',),
    LinesField(
        name="roles_",
        accessor='getRoles',
        mutator='setRoles',
    ),
))

# Make the group title and description user properties
group['title'].user_property = True
group['description'].user_property = True


@implementer(group_ifaces.IGroup, IGroupPropertiesProvider)
class TestGroup(BaseFolder):
    """A group archetype for testing"""
    schema = group

    security = ClassSecurityInfo()

    def getGroupName(self):
        return self.getId()

    def getGroupId(self):
        return self.getId()

    def getGroupMembers(self):
        # All references and all subobjects that are members
        mems = self.getRefs(GROUP_RELATIONSHIP)
        mem_dict = dict.fromkeys(
            [user_ifaces.IMembraneUserAuth(m).getUserId()
             for m in mems])
        mbtool = getToolByName(self, TOOLNAME)
        mems = mbtool.unrestrictedSearchResults(
            object_implements=(
                user_ifaces.IMembraneUserAuth.__identifier__),
            path='/'.join(self.getPhysicalPath()))
        for m in mems:
            mem_dict[m.getUserId] = 1
        return tuple(mem_dict.keys())

    def listUsers(self):
        """
        Return a DisplayList of users
        """
        catalog = getToolByName(self, TOOLNAME)
        results = catalog(
            object_implements=(
                user_ifaces.IMembraneUserAuth.__identifier__))

        value = []
        for r in results:
            key = r.getUserName is not None and r.getUserName.strip() \
                or r.getUserId
            value.append((key.lower(), (r.UID, key)))
        value.sort()
        value = [r for throwaway, r in value]
        value.insert(0, ('', '<no reference>'))
        return DisplayList(value)


registerType(TestGroup, PROJECTNAME)


user = BaseSchema + Schema((
    StringField('userName',
                languageIndependent=1,),
    StringField('password',
                languageIndependent=1,),
    StringField('title',
                languageIndependent=1,
                user_property='fullname',
                accessor='Title'),
    StringField('mobilePhone',
                languageIndependent=1,
                user_property=True,),
    StringField('homePhone',
                languageIndependent=1,
                schemata='userinfo',),
    LinesField('roles_',
               languageIndependent=1,
               accessor='getRoles',
               mutator='setRoles',
               default=('Member',)),
    BooleanField('editor',
                 languageIndependent=1,
                 user_property='ext_editor',
                 default=False),
))

extra = BaseSchema + Schema((
    StringField('extraProperty',
                user_property=True,),
    StringField('extraPropertyFromSchemata',
                schemata='userinfo',),
))


class BaseMember:
    schema = user
    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    # use the object id as our userid

    def getUserId(self):
        return self.getId()

    # getUserName is autogenerated

    def verifyCredentials(self, credentials):
        login = credentials.get('login')
        password = credentials.get('password')
        if self.getUserName() == login and self.getPassword() == password:
            return True

    # IMembraneUserManagement methods

    def doChangeUser(self, login, password, **kwargs):
        self.setPassword(password)
        if kwargs:
            self.edit(**kwargs)

    # IMembraneUserDeleter method

    def doDeleteUser(self, login):
        parent = self.aq_inner.aq_parent
        parent.manage_delObjects([self.getId()])


@implementer(
    IUserAuthProvider,
    IUserAuthentication,
    IUserPropertiesProvider,
    IGroupsProvider,
    IGroupAwareRolesProvider,
    IUserRoles,
    user_ifaces.IMembraneUserChanger,
    user_ifaces.IMembraneUserManagement,
    user_ifaces.IMembraneUserDeleter
)
class TestMember(BaseMember, BaseContent):
    """A member archetype for testing"""


registerType(TestMember, PROJECTNAME)


@implementer(
    IUserAuthProvider,
    IUserAuthentication,
    ISchemataPropertiesProvider,
    ISelectedGroupsProvider
)
class AlternativeTestMember(BaseMember, BaseContent):
    """A member archetype for testing"""

    security = ClassSecurityInfo()

    # For IPropertiesPlugin implementation/Property mixin
    @security.private
    def getUserPropertySchemata(self):
        return ['userinfo']

    # For IGroupsPlugin implementation/Group mixin
    @security.private
    def getGroupRelationships(self):
        return [GROUP_RELATIONSHIP]


registerType(AlternativeTestMember, PROJECTNAME)


@implementer(IUserPropertiesProvider)
class TestPropertyProvider(BaseContent):
    """Tests externally provided properties"""
    schema = extra
    _at_rename_after_creation = True
    security = ClassSecurityInfo()

    def getUserName(self):
        # We must implement IMembraneUserObject. We cheat a bit and do not
        # provide the right login.
        return None


registerType(TestPropertyProvider, PROJECTNAME)


@implementer(ISchemataPropertiesProvider)
class TestAlternatePropertyProvider(BaseContent):
    """
    Tests externally provided properties w/ properties coming from
    schemata
    """
    schema = extra
    _at_rename_after_creation = True
    security = ClassSecurityInfo()

    def getUserName(self):
        # We must implement IMembraneUserObject. We cheat a bit and do not
        # provide the right login.
        return None

    def getUserPropertySchemata(self):
        return ('userinfo',)


registerType(TestAlternatePropertyProvider, PROJECTNAME)
