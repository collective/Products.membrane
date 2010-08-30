#
# MembraneTestCase Membrane
#

import transaction as txn
from Products.CMFPlone.utils import _createObjectByType

from Products.PlonePAS.interfaces.capabilities import IPasswordSetCapability

from Products.PluggableAuthService.tests.conformance \
    import IAuthenticationPlugin_conformance
from Products.PluggableAuthService.tests.conformance \
    import IUserEnumerationPlugin_conformance

from Products.membrane.tests.utils import sortTuple
from Products.membrane.interfaces import IMembraneUserAuth
from Products.membrane.interfaces import IMembraneUserManagement
from Products.membrane.plugins.usermanager import MembraneUserManager
from Products.membrane.tests import base


class MembraneUserManagerLayer(base.AddUserLayer):
    @classmethod
    def setUp(cls):
        portal = cls.getPortal()
        portal.acl_users.pmm = MembraneUserManager(id='pmm')
        txn.commit()

    @classmethod
    def tearDown(cls):
        pass

    @classmethod
    def testSetUp(cls):
        pass

    @classmethod
    def testTearDown(cls):
        pass


class MembraneUserManagerTwoUsersLayer(MembraneUserManagerLayer):
    @classmethod
    def setUp(cls):
        portal = cls.getPortal()
        member = _createObjectByType('TestMember', portal,
                                     'testuser2')
        member.setUserName('testuser2')
        member.setPassword('testpassword2')
        member.setTitle('full name 2')
        member.reindexObject()
        txn.commit()

    @classmethod
    def tearDown(cls):
        pass

    @classmethod
    def testSetUp(cls):
        pass

    @classmethod
    def testTearDown(cls):
        pass


class MembraneUserManagerTestBase:
    def _getTargetClass(self):
        return MembraneUserManager

    def _makeOne(self, id='test', *args, **kw):
        return self._getTargetClass()(id=id, *args, **kw)


class TestMembraneUserManagerBasics(base.MembraneTestCase,
                                    MembraneUserManagerTestBase,
                                    IAuthenticationPlugin_conformance,
                                    IUserEnumerationPlugin_conformance):
    # Run the conformance tests
    layer = MembraneUserManagerLayer


class TestMembraneUserManagerEnumeration(base.MembraneUserTestCase):

    layer = MembraneUserManagerLayer

    def testEnumerateUsersNoArgs(self):
        self.failUnlessEqual(
            len(self.portal.acl_users.pmm.enumerateUsers()), 1)

    def testEnumerateUsersByLoginNonexisting(self):
        enumusers = self.portal.acl_users.pmm.enumerateUsers
        self.failUnlessEqual(enumusers(login='nonexisting'), ())
        self.failUnlessEqual(
            enumusers(login='nonexisting', exact_match=True), ())

    def testEnumerateUsersByLogin(self):
        username = self.member.getUserName()
        enumusers = self.portal.acl_users.pmm.enumerateUsers
        self.failUnlessEqual(len(enumusers(login=username,
                                           exact_match=True)), 1)
        self.failUnlessEqual(len(enumusers(login=username[:len(username) - 1],
                                           exact_match=False)), 1)
        self.failUnlessEqual(len(enumusers(login=username,
                                           exact_match=True)), 1)
        self.failUnlessEqual(len(enumusers(
            login=username, exact_match=True, sort_on='login')), 1)
        self.failUnlessEqual(len(enumusers(login=username,
                                           exact_match=True, sort_on='id')), 1)
        self.failUnlessEqual(len(enumusers(
            login=username, exact_match=True, max_results=1)), 1)
        self.failUnlessEqual(len(enumusers(
            login=username, exact_match=True, max_results=0)), 0)

    def testEnumerateUsersByUserIdNonexisting(self):
        enumusers = self.portal.acl_users.pmm.enumerateUsers
        self.failUnlessEqual(enumusers(id='nonexisting'), ())
        self.failUnlessEqual(enumusers(id='nonexisting', exact_match=True), ())

    def testEnumerateUsersByUserId(self):
        userid = IMembraneUserAuth(self.member).getUserId()
        enumusers = self.portal.acl_users.pmm.enumerateUsers
        self.failUnlessEqual(len(enumusers(id=userid, exact_match=True)), 1)
        self.failUnlessEqual(len(enumusers(id=userid[:len(userid) - 1],
                                           exact_match=False)), 1)
        self.failUnlessEqual(len(enumusers(
            id=userid, exact_match=True, sort_on='login')), 1)
        self.failUnlessEqual(len(enumusers(id=userid,
                                           exact_match=True, sort_on='id')), 1)
        self.failUnlessEqual(len(enumusers(
            id=userid, exact_match=True, max_results=1)), 1)
        self.failUnlessEqual(len(enumusers(
            id=userid, exact_match=True, max_results=0)), 0)

    def testEnumerateUsersExactMatchCaseInsensitive(self):
        enumusers = self.portal.acl_users.pmm.enumerateUsers
        member1 = _createObjectByType('TestMember', self.portal, 'Ann')
        member1.setUserName('Ann')
        member1.setPassword('password')
        member1.reindexObject()
        member1_id = IMembraneUserAuth(member1).getUserId()
        member2 = _createObjectByType('TestMember', self.portal, 'ann')
        member2.setUserName('ann')
        member2.setPassword('password')
        member2.reindexObject()
        member2_id = IMembraneUserAuth(member2).getUserId()
        queryMember1 = enumusers(id=member1_id, exact_match=True)[0]
        self.failUnlessEqual(queryMember1['id'], member1.getUserName())
        queryMember2 = enumusers(id=member2_id, exact_match=True)[0]
        self.failUnlessEqual(queryMember2['id'], member2.getUserName())


class TestMembraneUserManagerAuthentication(base.MembraneUserTestCase):

    layer = MembraneUserManagerLayer

    def testAuthenticateOnMember(self):
        credentials = {'login': 'norealuser', 'password': 'norealpassword'}
        userauth = IMembraneUserAuth(self.member)
        authcred = userauth.authenticateCredentials
        self.failUnlessEqual(authcred(credentials), None)
        credentials = {'login': 'testuser', 'password': 'wrongpassword'}
        self.failUnlessEqual(authcred(credentials), None)
        credentials = {'login': 'testuser', 'password': 'testpassword'}
        self.failUnlessEqual(authcred(credentials),
                             (userauth.getUserId(), self.member.getUserName()))

    def testAuthenticate(self):
        credentials = {'login': 'norealuser', 'password': 'norealpassword'}
        authcred = self.portal.acl_users.pmm.authenticateCredentials
        self.failUnlessEqual(authcred(credentials), None)
        credentials = {'login': 'testuser', 'password': 'wrongpassword'}
        self.failUnlessEqual(authcred(credentials), None)
        credentials = {'login': 'testuser', 'password': 'testpassword'}
        right = (IMembraneUserAuth(self.member).getUserId(),
                 self.member.getUserName())
        self.failUnlessEqual(authcred(credentials), right)

    def testLogin(self):
        self.login(IMembraneUserAuth(self.member).getUserId())

    def testLoginCaseSensitive(self):
        member2 = _createObjectByType('TestMember', self.portal,
                                     'TestUser')  # different case
        member2.setUserName('TestUser')
        member2.setPassword('testpassword2')
        member2.reindexObject()
        authcred = self.portal.acl_users.pmm.authenticateCredentials
        credentials = {'login': 'testuser', 'password': 'testpassword'}
        self.failUnlessEqual(authcred(credentials),
                             (IMembraneUserAuth(self.member).getUserId(),
                              self.member.getUserName()))
        credentials = {'login': 'TestUser', 'password': 'testpassword2'}
        self.failUnlessEqual(authcred(credentials),
                             (IMembraneUserAuth(member2).getUserId(),
                              member2.getUserName()))


class TestMembraneUserManagerAuthenticationPermissions(
    base.MembraneUserTestCase):
    """Check if everything works when the user object is private"""

    layer = MembraneUserManagerLayer

    def afterSetUp(self):
        base.MembraneUserTestCase.afterSetUp(self)
        self.portal.portal_workflow.doActionFor(self.member, 'hide')

    def testAuthenticate(self):
        self.logout()
        credentials = {'login': 'norealuser', 'password': 'norealpassword'}
        authcred = self.portal.acl_users.pmm.authenticateCredentials
        self.failUnlessEqual(authcred(credentials), None)
        credentials = {'login': 'testuser', 'password': 'wrongpassword'}
        self.failUnlessEqual(authcred(credentials), None)
        credentials = {'login': 'testuser', 'password': 'testpassword'}
        self.failUnlessEqual(authcred(credentials),
                             (IMembraneUserAuth(self.member).getUserId(),
                              self.member.getUserName()))

    def testLogin(self):
        self.logout()
        self.login(IMembraneUserAuth(self.member).getUserId())


class TestUserManagerIntrospectionNoUsers(base.MembraneTestCase):

    def afterSetUp(self):
        self.portal.acl_users.pmm = MembraneUserManager(id='pmm')

    def testGetUserIdsNoUsers(self):
        self.failIf(self.portal.acl_users.pmm.getUserIds())

    def getUserNamesNoUsers(self):
        self.failIf(self.portal.acl_users.pmm.getUserNames())

    def testGetUsersNoUsers(self):
        self.failIf(self.portal.acl_users.pmm.getUsers())


class TestUserManagerIntrospectionOneUser(base.MembraneUserTestCase):

    layer = MembraneUserManagerLayer

    def testGetUserIdsOneUser(self):
        self.failUnlessEqual(self.portal.acl_users.pmm.getUserIds(),
                             (IMembraneUserAuth(self.member).getUserId(),))

    def getUserNamesOneUser(self):
        self.failUnlessEqual(self.portal.acl_users.pmm.getUserNames(),
                             (self.member.getUserName(),))

    def testGetUsersOneUser(self):
        users = self.portal.acl_users.pmm.getUsers()
        self.failUnlessEqual([x.getId() for x in users],
                             [IMembraneUserAuth(self.member).getUserId()])


class TestUserManagerIntrospectionTwoUsers(base.MembraneUserTestCase):

    layer = MembraneUserManagerTwoUsersLayer

    def afterSetUp(self):
        base.MembraneUserTestCase.afterSetUp(self)
        self.member2 = self.portal.testuser2

    def testGetUserIds(self):
        userids = sortTuple(self.portal.acl_users.pmm.getUserIds())
        correct = sortTuple(
            (IMembraneUserAuth(self.member).getUserId(),
             IMembraneUserAuth(self.member2).getUserId())
            )
        self.failUnlessEqual(userids, correct)

    def testGetUsers(self):
        userids = sortTuple(self.portal.acl_users.pmm.getUserIds())
        correct = sortTuple(
            (IMembraneUserAuth(self.member).getUserId(),
             IMembraneUserAuth(self.member2).getUserId())
            )
        self.failUnlessEqual(userids, correct)


class TestMembraneUserManagerManagement(base.MembraneUserTestCase):

    layer = MembraneUserManagerLayer

    def testUserChangePassword(self):
        usermanager = IMembraneUserManagement(self.member)
        userauth = IMembraneUserAuth(self.member)
        authcred = userauth.authenticateCredentials
        # Verify the current credentials
        credentials = {'login': 'testuser', 'password': 'testpassword'}
        self.failUnlessEqual(authcred(credentials),
                             (userauth.getUserId(), self.member.getUserName()))
        usermanager.doChangeUser('testuser', 'pass2')
        credentials = {'login': 'testuser', 'password': 'pass2'}
        self.failUnlessEqual(authcred(credentials),
                             (userauth.getUserId(), self.member.getUserName()))

    def testUserChangeOtherData(self):
        usermanager = IMembraneUserManagement(self.member)
        usermanager.doChangeUser('testuser', 'pass2', mobilePhone='555-1212')
        self.failUnlessEqual(self.member.getMobilePhone(), '555-1212')

    def testUserDeleteUser(self):
        usermanager = IMembraneUserManagement(self.member)
        self.failUnless('testuser' in self.portal.objectIds())
        usermanager.doDeleteUser('testuser')
        self.failIf('testuser' in self.portal.objectIds())
        # login as the new user should fail now
        self.logout()
        self.assertRaises(AttributeError, self.login, 'testuser')

    def testChangePassword(self):
        pmm = self.portal.acl_users.pmm
        userauth = IMembraneUserAuth(self.member)
        authcred = pmm.authenticateCredentials
        # Verify the current credentials
        credentials = {'login': 'testuser', 'password': 'testpassword'}
        self.failUnlessEqual(authcred(credentials),
                             (userauth.getUserId(), self.member.getUserName()))
        pmm.doChangeUser('testuser', 'pass2')
        credentials = {'login': 'testuser', 'password': 'pass2'}
        self.failUnlessEqual(authcred(credentials),
                             (userauth.getUserId(), self.member.getUserName()))

    def testAllowChangePassword(self):
        self.failUnless(
            IPasswordSetCapability.providedBy(self.portal.acl_users.pmm))

    def testChangeOtherData(self):
        pmm = self.portal.acl_users.pmm
        pmm.doChangeUser('testuser', 'pass2', mobilePhone='555-1212')
        self.failUnlessEqual(self.member.getMobilePhone(), '555-1212')

    def testDeleteUser(self):
        pmm = self.portal.acl_users.pmm
        self.failUnless('testuser' in self.portal.objectIds())
        pmm.doDeleteUser('testuser')
        self.failIf('testuser' in self.portal.objectIds())
        # login as the new user should fail now
        self.logout()
        self.assertRaises(AttributeError, self.login, 'testuser')


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMembraneUserManagerBasics))
    suite.addTest(makeSuite(TestMembraneUserManagerEnumeration))
    suite.addTest(makeSuite(TestMembraneUserManagerAuthentication))
    suite.addTest(makeSuite(TestMembraneUserManagerAuthenticationPermissions))
    suite.addTest(makeSuite(TestUserManagerIntrospectionNoUsers))
    suite.addTest(makeSuite(TestUserManagerIntrospectionOneUser))
    suite.addTest(makeSuite(TestUserManagerIntrospectionTwoUsers))
    suite.addTest(makeSuite(TestMembraneUserManagerManagement))
    return suite
