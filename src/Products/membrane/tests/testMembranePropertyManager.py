#
# MembraneTestCase Membrane
#
from Products.CMFPlone.utils import _createObjectByType
from Products.membrane.config import TOOLNAME
from Products.membrane.interfaces import IMembraneUserAuth
from Products.membrane.interfaces import IMembraneUserProperties
from Products.membrane.tests import base


class MembranePropertyManagerTestBase:
    def _getTargetClass(self):
        from Products.membrane.plugins.propertymanager import MembranePropertyManager

        return MembranePropertyManager

    def _makeOne(self, id="test", *args, **kw):
        return self._getTargetClass()(id=id, *args, **kw)

    def _initExternalProvider(self, mbtool, portal_type):
        mbtool.registerMembraneType(portal_type)
        self.prop_provider = _createObjectByType(
            portal_type, self.portal, "test_prop_provider"
        )


class User:
    def __init__(self, member):
        self.member = member

    def getId(self):
        return IMembraneUserAuth(self.member).getUserId()

    def getUserName(self):
        return self.getId()

    def isGroup(self):
        return False


class Group:
    def __init__(self, group):
        self.group = group

    def getId(self):
        return self.group.getId()

    def getUserName(self):
        return self.getId()

    def isGroup(self):
        return True


class TestMembranePropertyManager(
    base.MembraneTestCase, MembranePropertyManagerTestBase
):
    def setUp(self):
        super().setUp()
        self.portal.pmm = self._makeOne("pmm")
        self.addUser()

    def testGetPropertiesForUserOnUser(self):
        mem_props = IMembraneUserProperties(self.member)
        properties = mem_props.getPropertiesForUser(None)

        self.assertTrue(properties.hasProperty("fullname"))

    def testGetPropertiesForUserFromPropertyManager(self):
        properties = self.portal.pmm.getPropertiesForUser(User(self.member))
        self.assertFalse(properties.hasProperty("id"))
        self.assertTrue(properties.hasProperty("mobilePhone"))

    def testGetMappedPropertyForUserFromPropertyManager(self):
        # The 'title' field should be mapped to the 'fullname' property
        properties = self.portal.pmm.getPropertiesForUser(User(self.member))
        self.assertTrue(properties.hasProperty("fullname"))

    def testGetPropertiesForGroupFromPropertyManager(self):
        self.addGroup()
        group = self.portal.testgroup
        properties = self.portal.pmm.getPropertiesForUser(Group(group))
        self.assertFalse(properties.hasProperty("id"))
        self.assertTrue(properties.hasProperty("title"))
        self.assertTrue(properties.hasProperty("description"))
        self.assertEqual(properties.getProperty("title"), "Test group")
        self.assertEqual(properties.getProperty("description"), "A test group")

    def testGetPropertiesForUser(self):
        userid = IMembraneUserAuth(self.member).getUserId()
        user = self.portal.acl_users.getUserById(userid)
        sheets = user.getOrderedPropertySheets()
        self.assertTrue(
            [
                x.getProperty("fullname")
                for x in sheets
                if x.getProperty("fullname") == "full name"
            ]
        )
        mtool = self.portal.portal_membership
        member = mtool.getMemberById(userid)
        self.assertEqual(member.getProperty("fullname"), "full name")
        self.assertEqual(member.getProperty("ext_editor"), False)

    def testSetPropertiesForUser(self):
        fullname = "null fame"
        userid = IMembraneUserAuth(self.member).getUserId()
        user = self.portal.acl_users.getUserById(userid)
        sheets = user.getOrderedPropertySheets()
        sheet = tuple(sheets)[0]
        sheet.setProperty(user, "fullname", fullname)
        sheet.setProperty(user, "ext_editor", True)
        mbtool = getattr(self.portal, TOOLNAME)
        member = mbtool.getUserObject(user.getUserName())
        self.assertEqual(member.Title(), fullname)
        self.assertEqual(member.getEditor(), True)


class TestMembraneSchemataPropertyManager(
    base.MembraneTestCase, MembranePropertyManagerTestBase
):
    def addUser(self, obj=None):
        if obj is None:
            obj = self.portal
        self.member = _createObjectByType("AlternativeTestMember", obj, "testuser")
        self.member.setUserName("testuser")
        self.member.setPassword("testpassword")
        self.member.setTitle("full name")
        # A property that will be obtained via schemata
        self.member.setHomePhone("555-1212")
        self.member.reindexObject()

    def setUp(self):
        super().setUp()
        self.portal.pmm = self._makeOne("pmm")
        self.addUser()

    def testGetPropertiesForUserOnUser(self):
        mem_props = IMembraneUserProperties(self.member)
        properties = mem_props.getPropertiesForUser(None)
        self.assertTrue(properties.hasProperty("homePhone"))

    def testGetPropertiesForUserFromPropertyManager(self):
        properties = self.portal.pmm.getPropertiesForUser(User(self.member))
        self.assertFalse(properties.hasProperty("id"))
        self.assertTrue(properties.hasProperty("homePhone"))

    def testGetPropertiesForUser(self):
        userid = IMembraneUserAuth(self.member).getUserId()
        user = self.portal.acl_users.getUserById(userid)
        sheets = user.getOrderedPropertySheets()
        self.assertTrue(
            [
                x.getProperty("homePhone")
                for x in sheets
                if x.getProperty("homePhone") == "555-1212"
            ]
        )
        member = self.portal.portal_membership.getMemberById(userid)
        self.assertEqual(member.getProperty("homePhone"), "555-1212")

    def testSetPropertiesForUser(self):
        homePhone = 'phome hone"'
        userid = IMembraneUserAuth(self.member).getUserId()
        user = self.portal.acl_users.getUserById(userid)
        sheets = user.getOrderedPropertySheets()
        tuple(sheets)[0].setProperty(user, "homePhone", homePhone)
        mbtool = getattr(self.portal, TOOLNAME)
        member = mbtool.getUserObject(user.getUserName())
        self.assertEqual(member.getHomePhone(), homePhone)
