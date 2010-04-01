#
# MembraneTestCase Membrane
#

from Products.CMFPlone.utils import _createObjectByType

from Products.membrane.interfaces import IMembraneUserAuth
from Products.membrane.interfaces import IMembraneUserProperties
from Products.membrane.config import TOOLNAME
from Products.membrane.at.relations import UserRelatedRelation
import base
from dummy import TestPropertyProvider
from dummy import TestAlternatePropertyProvider


class MembranePropertyManagerTestBase:

    def _getTargetClass(self):
        from Products.membrane.plugins.propertymanager \
            import MembranePropertyManager
        return MembranePropertyManager

    def _makeOne(self, id='test', *args, **kw):
        return self._getTargetClass()(id=id, *args, **kw)

    def _initExternalProvider(self, mbtool, portal_type):
        mbtool.registerMembraneType(portal_type)
        self.prop_provider = _createObjectByType(portal_type,
                                                 self.portal,
                                                 'test_prop_provider')


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


class TestMembranePropertyManager(base.MembraneTestCase,
                                  MembranePropertyManagerTestBase):

    def afterSetUp(self):
        self.portal.pmm = self._makeOne('pmm')
        self.addUser()

    def testGetPropertiesForUserOnUser(self):
        mem_props = IMembraneUserProperties(self.member)
        properties = mem_props.getPropertiesForUser(None)

        self.failUnless(properties.hasProperty('fullname'))

    def testGetPropertiesForUserFromPropertyManager(self):
        properties = self.portal.pmm.getPropertiesForUser(User(self.member))
        self.failIf(properties.hasProperty('id'))
        self.failUnless(properties.hasProperty('mobilePhone'))

    def testGetMappedPropertyForUserFromPropertyManager(self):
        # The 'title' field should be mapped to the 'fullname' property
        properties = self.portal.pmm.getPropertiesForUser(User(self.member))
        self.failUnless(properties.hasProperty('fullname'))

    def testGetPropertiesForGroupFromPropertyManager(self):
        self.addGroup()
        group = self.portal.testgroup
        properties = self.portal.pmm.getPropertiesForUser(Group(group))
        self.failIf(properties.hasProperty('id'))
        self.failUnless(properties.hasProperty('title'))
        self.failUnless(properties.hasProperty('description'))
        self.failUnlessEqual(properties.getProperty('title'), 'Test group')
        self.failUnlessEqual(
            properties.getProperty('description'), 'A test group')

    def testGetPropertiesForUser(self):
        userid = IMembraneUserAuth(self.member).getUserId()
        user = self.portal.acl_users.getUserById(userid)
        sheets = user.getOrderedPropertySheets()
        self.failUnless([x.getProperty('fullname') for x in sheets
                         if x.getProperty('fullname') == 'full name'])
        mtool = self.portal.portal_membership
        member = mtool.getMemberById(userid)
        self.failUnlessEqual(member.getProperty('fullname'), 'full name')

    def testGetPropertiesFromExternalProvider(self):
        value = 'foo'
        mbtool = getattr(self.portal, TOOLNAME)
        self._initExternalProvider(mbtool, TestPropertyProvider.portal_type)
        self.prop_provider.setExtraProperty(value)
        self.member.addReference(self.prop_provider,
                                 relationship=UserRelatedRelation.relationship)
        self.prop_provider.reindexObject()

        userid = IMembraneUserAuth(self.member).getUserId()
        user = self.portal.acl_users.getUserById(userid)
        sheets = user.getOrderedPropertySheets()
        self.failUnless([x.getProperty('extraProperty') for x in sheets
                         if x.getProperty('extraProperty') == value])
        mtool = self.portal.portal_membership
        member = mtool.getMemberById(userid)
        self.failUnlessEqual(member.getProperty('extraProperty'), value)

    def testSetPropertiesForUser(self):
        fullname = 'null fame'
        userid = IMembraneUserAuth(self.member).getUserId()
        user = self.portal.acl_users.getUserById(userid)
        sheets = user.getOrderedPropertySheets()
        sheets[0].setProperty(user, 'fullname', fullname)
        mbtool = getattr(self.portal, TOOLNAME)
        member = mbtool.getUserObject(user.getUserName())
        self.assertEqual(member.Title(), fullname)


class TestMembraneSchemataPropertyManager(base.MembraneTestCase,
                                          MembranePropertyManagerTestBase):

    def addUser(self, obj=None):
        if obj is None:
            obj = self.portal
        self.member = _createObjectByType('AlternativeTestMember', obj,
                                          'testuser')
        self.member.setUserName('testuser')
        self.member.setPassword('testpassword')
        self.member.setTitle('full name')
        # A property that will be obtained via schemata
        self.member.setHomePhone('555-1212')
        self.member.reindexObject()

    def afterSetUp(self):
        self.portal.pmm = self._makeOne('pmm')
        self.addUser()

    def testGetPropertiesForUserOnUser(self):
        mem_props = IMembraneUserProperties(self.member)
        properties = mem_props.getPropertiesForUser(None)
        self.failUnless(properties.hasProperty('homePhone'))

    def testGetPropertiesForUserFromPropertyManager(self):
        properties = self.portal.pmm.getPropertiesForUser(User(self.member))
        self.failIf(properties.hasProperty('id'))
        self.failUnless(properties.hasProperty('homePhone'))

    def testGetPropertiesForUser(self):
        userid = IMembraneUserAuth(self.member).getUserId()
        user = self.portal.acl_users.getUserById(userid)
        sheets = user.getOrderedPropertySheets()
        self.failUnless([x.getProperty('homePhone') for x in sheets
                         if x.getProperty('homePhone') == '555-1212'])
        member = self.portal.portal_membership.getMemberById(userid)
        self.failUnlessEqual(member.getProperty('homePhone'), '555-1212')

    def testGetPropertiesFromExternalProvider(self):
        wrongvalue = 'foo'
        rightvalue = 'bar'
        mbtool = getattr(self.portal, TOOLNAME)
        self._initExternalProvider(mbtool,
                                   TestAlternatePropertyProvider.portal_type)
        self.prop_provider.setExtraProperty(wrongvalue)
        self.prop_provider.setExtraPropertyFromSchemata(rightvalue)
        self.member.addReference(self.prop_provider,
                                 relationship=UserRelatedRelation.relationship)
        self.prop_provider.reindexObject()

        userid = IMembraneUserAuth(self.member).getUserId()
        user = self.portal.acl_users.getUserById(userid)
        sheets = user.getOrderedPropertySheets()
        self.failUnless([x.getProperty('extraPropertyFromSchemata')
                         for x in sheets
                         if x.getProperty('extraPropertyFromSchemata') \
                         == rightvalue])

        mtool = self.portal.portal_membership
        member = mtool.getMemberById(userid)
        self.failUnlessEqual(member.getProperty('extraPropertyFromSchemata'),
                             rightvalue)
        self.failIf(member.hasProperty('extraProperty'))

    def testSetPropertiesForUser(self):
        homePhone = 'phome hone"'
        userid = IMembraneUserAuth(self.member).getUserId()
        user = self.portal.acl_users.getUserById(userid)
        sheets = user.getOrderedPropertySheets()
        sheets[0].setProperty(user, 'homePhone', homePhone)
        mbtool = getattr(self.portal, TOOLNAME)
        member = mbtool.getUserObject(user.getUserName())
        self.assertEqual(member.getHomePhone(), homePhone)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMembranePropertyManager))
    suite.addTest(makeSuite(TestMembraneSchemataPropertyManager))
    return suite
