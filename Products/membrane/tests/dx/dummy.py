# coding=utf-8
from plone.autoform.interfaces import IFormFieldProvider
from plone.dexterity.content import Container
from plone.dexterity.content import Item
from plone.supermodel import model
from Products.CMFCore.utils import getToolByName
from Products.membrane.interfaces.group import IGroup
from Products.membrane.interfaces.group import IMembraneGroupGroups
from Products.membrane.interfaces.group import IMembraneGroupProperties
from Products.membrane.interfaces.user import IMembraneUserAuth
from Products.membrane.interfaces.user import IMembraneUserChanger
from Products.membrane.interfaces.user import IMembraneUserDeleter
from Products.membrane.interfaces.user import IMembraneUserGroups
from Products.membrane.interfaces.user import IMembraneUserManagement
from Products.membrane.interfaces.user import IMembraneUserObject
from Products.membrane.interfaces.user import IMembraneUserProperties
from Products.membrane.interfaces.user import IMembraneUserRoles
from Products.PlonePAS.sheet import MutablePropertySheet
from zope import schema
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider


@provider(IFormFieldProvider)
class ITestMember(model.Schema):
    roles_ = schema.List(
        value_type=schema.TextLine(default="",),
        title="Roles",
        required=False,
        default=["Member"],
    )

    groups = schema.List(
        value_type=schema.TextLine(default="",),
        title="Groups",
        required=False,
        default=[],
    )


@implementer(
    ITestMember,
    IMembraneUserAuth,
    IMembraneUserChanger,
    IMembraneUserDeleter,
    IMembraneUserGroups,
    IMembraneUserManagement,
    IMembraneUserObject,
    IMembraneUserProperties,
    IMembraneUserRoles,
)
class TestMember(Item):
    """ Pass
    """

    portal_type = "TestMember"
    ext_editor = False

    def getUserId(self):
        return self.getId()

    def getEditor(self):
        return self.ext_editor

    def getGroups(self):
        if IGroup.providedBy(self.aq_parent):
            groups = (self.aq_parent.getGroupId(),)
        else:
            groups = ()
        return groups + tuple(getattr(self, "groups", ()))

    def getMobilePhone(self):
        return getattr(self, "mobilePhone", "")

    def setMobilePhone(self, value):
        self.mobilePhone = value

    def getPassword(self):
        return self.password

    def setPassword(self, value):
        self.password = value

    def getRoles(self):
        return self.roles_

    def setRoles(self, value):
        self.roles_ = value

    def getUserName(self):
        return self.username

    def setUserName(self, value):
        self.username = value

    def doChangeUser(self, login, password, **kwargs):
        self.setPassword(password)
        for key in kwargs:
            setattr(self, key, kwargs[key])

    def doDeleteUser(self, login):
        parent = self.aq_inner.aq_parent
        parent.manage_delObjects([self.getId()])

    def validateProperty(id, value):
        return True

    def getPropertiesForUser(self, user, request=None):
        return MutablePropertySheet(
            self.getId(),
            fullname=self.Title(),
            mobilePhone=self.getMobilePhone(),
            ext_editor=self.getEditor(),
        )

    def setPropertiesForUser(self, user, propertysheet, request=None):
        properties = propertysheet._properties
        for key in properties:
            value = properties[key]
            if key == "fullname":
                key = "title"
            setattr(self, key, value)

    def getGroupsForPrincipal(self, principal):
        return self.getGroups()

    def getRolesForPrincipal(self, principal, request=None):
        roles = list(self.getRoles())
        for groupid in self.groups:
            group = self.aq_parent[groupid]
            roles.extend(group.getRoles())
        return roles

    def authenticateCredentials(self, credentials):
        login = credentials.get("login")
        password = credentials.get("password")
        if login == self.getUserName() and password == self.getPassword():
            return self.getUserId(), login


class AlternativeTestMember(TestMember):
    """ Pass
    """

    portal_type = "AlternativeTestMember"

    def getHomePhone(self):
        return self.homePhone

    def setHomePhone(self, value):
        self.homePhone = value

    def getPropertiesForUser(self, user, request=None):
        return MutablePropertySheet(
            self.getId(),
            fullname=self.Title(),
            homePhone=self.getHomePhone(),
            mobilePhone=self.getMobilePhone(),
            ext_editor=self.getEditor(),
        )


@provider(IFormFieldProvider)
class ITestGroup(model.Schema):
    roles_ = schema.List(
        value_type=schema.TextLine(default="",),
        title="Roles",
        required=False,
        default=["Member"],
    )

    members_ = schema.List(
        value_type=schema.TextLine(default="",),
        title="Members",
        required=False,
        default=[],
    )


@implementer(
    ITestGroup, IGroup, IMembraneGroupProperties, IMembraneGroupGroups,
)
class TestGroup(Container):
    """ Pass
    """

    portal_type = "TestGroup"

    def getGroupId(self):
        return self.getId()

    def getGroupName(self):
        return self.getId()

    def getGroupMembers(self):
        return tuple(self) + tuple(self.members_)

    def getPropertiesForUser(self, user, request=None):
        return MutablePropertySheet(
            self.getId(), title=self.Title(), description=self.Description(),
        )

    def addReference(self, value):
        self.members_ = [value.getUserId()]
        user = self.aq_parent[value.getUserId()]
        groups = user.groups or []
        groups.append(self.getGroupId())
        user.groups = groups
        user.reindexObject()
        self.reindexObject()

    def setMembers(self, memberuids):
        mbtool = getToolByName(self, "membrane_tool")
        brains = mbtool(UID=memberuids)
        for brain in brains:
            self.addReference(brain.getObject())

    def getRoles(self):
        return self.roles_

    def setRoles(self, value):
        self.roles_ = value

    def getGroupsForPrincipal(self, principal):
        return (self.getGroupId(),)


class IUserPropertiesProvider(Interface):
    """
    """


@implementer(IUserPropertiesProvider)
class TestPropertyProvider(Item):
    """
    Tests externally provided properties w/ properties coming from
    schemata
    """

    portal_type = "TestPropertyProvider"

    def getUserName(self):
        # We must implement IMembraneUserObject. We cheat a bit and do not
        # provide the right login.
        return None

    def getUserPropertySchemata(self):
        return ("userinfo",)


class ISchemataPropertiesProvider(Interface):
    def getUserPropertySchemata():
        """
        Returns a sequence of schemata names to be used for determining
        user properties.
        """


@implementer(ISchemataPropertiesProvider)
class TestAlternatePropertyProvider(Item):
    """
    Tests externally provided properties w/ properties coming from
    schemata
    """

    portal_type = "TestAlternatePropertyProvider"

    def getUserName(self):
        # We must implement IMembraneUserObject. We cheat a bit and do not
        # provide the right login.
        return None

    def getUserPropertySchemata(self):
        return ("userinfo",)
