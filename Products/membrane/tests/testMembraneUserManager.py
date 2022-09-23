from plone.app.testing import login
from plone.app.testing import logout
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.membrane import testing
from Products.membrane.interfaces import IMembraneUserAuth
from Products.membrane.interfaces import IMembraneUserManagement
from Products.membrane.plugins.usermanager import MembraneUserManager
from Products.membrane.tests import base
from Products.membrane.tests.utils import sortTuple
from Products.PlonePAS.interfaces.capabilities import IPasswordSetCapability
from Products.PluggableAuthService.tests.conformance import (  # noqa: E501
    IAuthenticationPlugin_conformance,
)
from Products.PluggableAuthService.tests.conformance import (  # noqa: E501
    IUserEnumerationPlugin_conformance,
)


class MembraneUserManagerTestBase:
    def _getTargetClass(self):
        return MembraneUserManager

    def _makeOne(self, id="test", *args, **kw):
        return self._getTargetClass()(id=id, *args, **kw)


class TestMembraneUserManagerBasics(
    base.MembraneTestCase,
    MembraneUserManagerTestBase,
    IAuthenticationPlugin_conformance,
    IUserEnumerationPlugin_conformance,
):
    # Run the conformance tests
    layer = testing.MEMBRANE_USER_MANAGER_INTEGRATION_TESTING


class TestMembraneUserManagerEnumeration(base.MembraneUserTestCase):

    layer = testing.MEMBRANE_USER_MANAGER_INTEGRATION_TESTING

    def testEnumerateUsersNoArgs(self):
        # If we do not pass any criteria to enumerateUsers, we get all
        # users.
        self.assertEqual(len(self.portal.acl_users.pmm.enumerateUsers()), 1)

    def testEnumerateUsersExtraIndexes(self):
        # You can add keyword arguments for known indexes.
        from persistent.mapping import PersistentMapping
        from Products.membrane.config import QIM_ANNOT_KEY
        from Products.membrane.config import TOOLNAME
        from zope.annotation.interfaces import IAnnotations

        mbtool = getToolByName(self.portal, TOOLNAME)
        annots = IAnnotations(mbtool)
        query_index_map = annots.get(QIM_ANNOT_KEY)
        if query_index_map is None:
            query_index_map = annots[QIM_ANNOT_KEY] = PersistentMapping()
        self.assertTrue("Title" in mbtool.indexes())
        self.assertFalse("title" in query_index_map)
        self.assertEqual(
            len(self.portal.acl_users.pmm.enumerateUsers(title="full name")), 0
        )
        query_index_map["title"] = "Title"
        self.assertEqual(
            len(self.portal.acl_users.pmm.enumerateUsers(title="full name")), 1
        )

    def testEnumerateUsersByLoginNonexisting(self):
        enumusers = self.portal.acl_users.pmm.enumerateUsers
        self.assertEqual(enumusers(login="nonexisting"), ())
        self.assertEqual(enumusers(login="nonexisting", exact_match=True), ())

    def testEnumerateUsersByLogin(self):
        username = self.member.getUserName()
        enumusers = self.portal.acl_users.pmm.enumerateUsers
        self.assertEqual(len(enumusers(login=username, exact_match=True)), 1)
        self.assertEqual(
            len(enumusers(login=username[: len(username) - 1], exact_match=False)), 1
        )
        self.assertEqual(len(enumusers(login=username, exact_match=True)), 1)
        self.assertEqual(
            len(enumusers(login=username, exact_match=True, sort_on="login")), 1
        )
        self.assertEqual(
            len(enumusers(login=username, exact_match=True, sort_on="id")), 1
        )
        self.assertEqual(
            len(enumusers(login=username, exact_match=True, max_results=1)), 1
        )
        self.assertEqual(
            len(enumusers(login=username, exact_match=True, max_results=0)), 0
        )

    def testEnumerateUsersByUserIdNonexisting(self):
        enumusers = self.portal.acl_users.pmm.enumerateUsers
        self.assertEqual(enumusers(id="nonexisting"), ())
        self.assertEqual(enumusers(id="nonexisting", exact_match=True), ())

    def testEnumerateUsersByUserId(self):
        userid = IMembraneUserAuth(self.member).getUserId()
        enumusers = self.portal.acl_users.pmm.enumerateUsers
        self.assertEqual(len(enumusers(id=userid, exact_match=True)), 1)
        self.assertEqual(
            len(enumusers(id=userid[: len(userid) - 1], exact_match=False)), 1
        )
        self.assertEqual(
            len(enumusers(id=userid, exact_match=True, sort_on="login")), 1
        )
        self.assertEqual(len(enumusers(id=userid, exact_match=True, sort_on="id")), 1)
        self.assertEqual(len(enumusers(id=userid, exact_match=True, max_results=1)), 1)
        self.assertEqual(len(enumusers(id=userid, exact_match=True, max_results=0)), 0)

    def testEnumerateUsersExactMatchCaseInsensitive(self):
        enumusers = self.portal.acl_users.pmm.enumerateUsers
        member1 = _createObjectByType("TestMember", self.portal, "Ann")
        member1.setUserName("Ann")
        member1.setPassword("password")
        member1.reindexObject()
        member1_id = IMembraneUserAuth(member1).getUserId()
        member2 = _createObjectByType("TestMember", self.portal, "ann")
        member2.setUserName("ann")
        member2.setPassword("password")
        member2.reindexObject()
        member2_id = IMembraneUserAuth(member2).getUserId()
        queryMember1 = enumusers(id=member1_id, exact_match=True)[0]
        self.assertEqual(queryMember1["id"], member1.getUserName())
        queryMember2 = enumusers(id=member2_id, exact_match=True)[0]
        self.assertEqual(queryMember2["id"], member2.getUserName())

    def test_listMembers(self):
        memship = self.portal.portal_membership
        self.assertEqual(len(memship.listMembers()), 2)
        # A group should not be in the list of members, and should certainly
        # not break the list of members with:
        # AttributeError: 'NoneType' object has no attribute '__of__'
        self.addGroup(self.portal)
        self.assertEqual(len(memship.listMembers()), 2)


class TestMembraneUserManagerAuthentication(base.MembraneUserTestCase):

    layer = testing.MEMBRANE_USER_MANAGER_INTEGRATION_TESTING

    def testAuthenticateOnMember(self):
        credentials = {"login": "norealuser", "password": "norealpassword"}
        userauth = IMembraneUserAuth(self.member)
        authcred = userauth.authenticateCredentials
        self.assertEqual(authcred(credentials), None)
        credentials = {"login": "testuser", "password": "wrongpassword"}
        self.assertEqual(authcred(credentials), None)
        credentials = {"login": "testuser", "password": "testpassword"}
        self.assertEqual(
            authcred(credentials), (userauth.getUserId(), self.member.getUserName())
        )

    def testAuthenticate(self):
        credentials = {"login": "norealuser", "password": "norealpassword"}
        authcred = self.portal.acl_users.pmm.authenticateCredentials
        self.assertEqual(authcred(credentials), None)
        credentials = {"login": "testuser", "password": "wrongpassword"}
        self.assertEqual(authcred(credentials), None)
        credentials = {"login": "testuser", "password": "testpassword"}
        right = (IMembraneUserAuth(self.member).getUserId(), self.member.getUserName())
        self.assertEqual(authcred(credentials), right)

    def testLogin(self):
        login(self.portal, IMembraneUserAuth(self.member).getUserId())

    def testLoginCaseSensitive(self):
        member2 = _createObjectByType(
            "TestMember", self.portal, "TestUser"
        )  # different case
        member2.setUserName("TestUser")
        member2.setPassword("testpassword2")
        member2.reindexObject()
        authcred = self.portal.acl_users.pmm.authenticateCredentials
        credentials = {"login": "testuser", "password": "testpassword"}
        self.assertEqual(
            authcred(credentials),
            (IMembraneUserAuth(self.member).getUserId(), self.member.getUserName()),
        )
        credentials = {"login": "TestUser", "password": "testpassword2"}
        self.assertEqual(
            authcred(credentials),
            (IMembraneUserAuth(member2).getUserId(), member2.getUserName()),
        )


class TestMembraneUserManagerAuthenticationPermissions(base.MembraneUserTestCase):
    """Check if everything works when the user object is private"""

    layer = testing.MEMBRANE_USER_MANAGER_INTEGRATION_TESTING

    def setUp(self):
        super().setUp()
        self.portal.portal_workflow.setDefaultChain("plone_workflow")
        self.portal.portal_workflow.doActionFor(self.member, "hide")

    def testAuthenticate(self):
        logout()
        credentials = {"login": "norealuser", "password": "norealpassword"}
        authcred = self.portal.acl_users.pmm.authenticateCredentials
        self.assertEqual(authcred(credentials), None)
        credentials = {"login": "testuser", "password": "wrongpassword"}
        self.assertEqual(authcred(credentials), None)
        credentials = {"login": "testuser", "password": "testpassword"}
        self.assertEqual(
            authcred(credentials),
            (IMembraneUserAuth(self.member).getUserId(), self.member.getUserName()),
        )

    def testLogin(self):
        logout()
        login(self.portal, IMembraneUserAuth(self.member).getUserId())


class TestUserManagerIntrospectionNoUsers(base.MembraneTestCase):
    def setUp(self):
        super().setUp()
        self.portal.acl_users.pmm = MembraneUserManager(id="pmm")

    def testGetUserIdsNoUsers(self):
        self.assertFalse(self.portal.acl_users.pmm.getUserIds())

    def getUserNamesNoUsers(self):
        self.assertFalse(self.portal.acl_users.pmm.getUserNames())

    def testGetUsersNoUsers(self):
        self.assertFalse(self.portal.acl_users.pmm.getUsers())


class TestUserManagerIntrospectionOneUser(base.MembraneUserTestCase):

    layer = testing.MEMBRANE_USER_MANAGER_INTEGRATION_TESTING

    def testGetUserIdsOneUser(self):
        self.assertEqual(
            self.portal.acl_users.pmm.getUserIds(),
            (IMembraneUserAuth(self.member).getUserId(),),
        )

    def getUserNamesOneUser(self):
        self.assertEqual(
            self.portal.acl_users.pmm.getUserNames(), (self.member.getUserName(),)
        )

    def testGetUsersOneUser(self):
        users = self.portal.acl_users.pmm.getUsers()
        self.assertEqual(
            [x.getId() for x in users], [IMembraneUserAuth(self.member).getUserId()]
        )


class TestUserManagerIntrospectionTwoUsers(base.MembraneUserTestCase):

    layer = testing.MEMBRANE_USER_MANAGER_TWO_USERS_INTEGRATION_TESTING

    def setUp(self):
        super().setUp()
        self.member2 = self.portal.testuser2

    def testGetUserIds(self):
        userids = sortTuple(self.portal.acl_users.pmm.getUserIds())
        correct = sortTuple(
            (
                IMembraneUserAuth(self.member).getUserId(),
                IMembraneUserAuth(self.member2).getUserId(),
            )
        )
        self.assertEqual(userids, correct)

    def testGetUsers(self):
        userids = sortTuple(self.portal.acl_users.pmm.getUserIds())
        correct = sortTuple(
            (
                IMembraneUserAuth(self.member).getUserId(),
                IMembraneUserAuth(self.member2).getUserId(),
            )
        )
        self.assertEqual(userids, correct)


class TestMembraneUserManagerManagement(base.MembraneUserTestCase):

    layer = testing.MEMBRANE_USER_MANAGER_INTEGRATION_TESTING

    def testUserChangePassword(self):
        usermanager = IMembraneUserManagement(self.member)
        userauth = IMembraneUserAuth(self.member)
        authcred = userauth.authenticateCredentials
        # Verify the current credentials
        credentials = {"login": "testuser", "password": "testpassword"}
        self.assertEqual(
            authcred(credentials), (userauth.getUserId(), self.member.getUserName())
        )
        usermanager.doChangeUser("testuser", "pass2")
        credentials = {"login": "testuser", "password": "pass2"}
        self.assertEqual(
            authcred(credentials), (userauth.getUserId(), self.member.getUserName())
        )

    def testUserChangeOtherData(self):
        usermanager = IMembraneUserManagement(self.member)
        usermanager.doChangeUser("testuser", "pass2", mobilePhone="555-1212")
        self.assertEqual(self.member.getMobilePhone(), "555-1212")

    def testUserDeleteUser(self):
        usermanager = IMembraneUserManagement(self.member)
        self.assertTrue("testuser" in self.portal.objectIds())
        usermanager.doDeleteUser("testuser")
        self.assertFalse("testuser" in self.portal.objectIds())
        # login as the new user should fail now
        logout()
        self.assertRaises(ValueError, login, self.portal, "testuser")

    def testChangePassword(self):
        pmm = self.portal.acl_users.pmm
        userauth = IMembraneUserAuth(self.member)
        authcred = pmm.authenticateCredentials
        # Verify the current credentials
        credentials = {"login": "testuser", "password": "testpassword"}
        self.assertEqual(
            authcred(credentials), (userauth.getUserId(), self.member.getUserName())
        )
        pmm.doChangeUser("testuser", "pass2")
        credentials = {"login": "testuser", "password": "pass2"}
        self.assertEqual(
            authcred(credentials), (userauth.getUserId(), self.member.getUserName())
        )

    def testAllowChangePassword(self):
        self.assertTrue(IPasswordSetCapability.providedBy(self.portal.acl_users.pmm))

    def testChangeOtherData(self):
        pmm = self.portal.acl_users.pmm
        pmm.doChangeUser("testuser", "pass2", mobilePhone="555-1212")
        self.assertEqual(self.member.getMobilePhone(), "555-1212")

    def testDeleteUser(self):
        pmm = self.portal.acl_users.pmm
        self.assertTrue("testuser" in self.portal.objectIds())
        pmm.doDeleteUser("testuser")
        self.assertFalse("testuser" in self.portal.objectIds())
        # login as the new user should fail now
        logout()
        self.assertRaises(ValueError, login, self.portal, "testuser")
