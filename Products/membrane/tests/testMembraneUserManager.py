#
# MembraneTestCase Membrane
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

import unittest

from Testing import ZopeTestCase
from Products.membrane.tests import base
from Products.CMFPlone.utils import _createObjectByType

from Products.PluggableAuthService.tests.conformance \
    import IAuthenticationPlugin_conformance
from Products.PluggableAuthService.tests.conformance \
    import IUserEnumerationPlugin_conformance

from Products.membrane.tests.utils import sortTuple
from Products.membrane.interfaces import IMembraneUserAuth
from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.config import TOOLNAME
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.utils import generateCategorySetIdForType
from Products.membrane.utils import getAllWFStatesForType

class MembraneUserManagerTestBase:

    def _getTargetClass( self ):
        from Products.membrane.plugins.usermanager \
            import MembraneUserManager
        return MembraneUserManager

    def _makeOne( self, id='test', *args, **kw ):
        return self._getTargetClass()( id=id, *args, **kw )


class TestMembraneUserManagerBasics( unittest.TestCase
                             , MembraneUserManagerTestBase
                             , IAuthenticationPlugin_conformance
                             , IUserEnumerationPlugin_conformance
                             ):
    # Run the conformance tests
    pass


class TestMembraneUserManagerEnumeration( base.MembraneTestCase
                                        , MembraneUserManagerTestBase):

    def afterSetUp(self):
        self.portal.pmm = self._makeOne('pmm')
        self.addUser()

    def testEnumerateUsersNoArgs(self):
        self.failUnlessEqual(len(self.portal.pmm.enumerateUsers()), 1)        

    def testEnumerateUsersByLoginNonexisting(self):
        enumusers = self.portal.pmm.enumerateUsers
        self.failUnlessEqual(enumusers(login='nonexisting'), ())
        self.failUnlessEqual(enumusers(login='nonexisting', exact_match=True), ())

    def testEnumerateUsersByLogin(self):
        username = self.member.getUserName()
        enumusers = self.portal.pmm.enumerateUsers
        self.failUnlessEqual(len(enumusers(login=username,
                                           exact_match=True)), 1)
        self.failUnlessEqual(len(enumusers(login=username[:len(username)-1],
                                           exact_match=False)), 1)
        self.failUnlessEqual(len(enumusers(login=username,
                                           exact_match=True)), 1)
        self.failUnlessEqual(len(enumusers(login=username,
                                           exact_match=True, sort_on='login')), 1)
        self.failUnlessEqual(len(enumusers(login=username,
                                           exact_match=True, sort_on='id')), 1)
        self.failUnlessEqual(len(enumusers(login=username,
                                           exact_match=True, max_results=1)), 1)
        self.failUnlessEqual(len(enumusers(login=username,
                                           exact_match=True, max_results=0)), 0)

    def testEnumerateUsersByUserIdNonexisting(self):
        enumusers = self.portal.pmm.enumerateUsers
        self.failUnlessEqual(enumusers(id='nonexisting'), ())
        self.failUnlessEqual(enumusers(id='nonexisting', exact_match=True), ())

    def testEnumerateUsersByUserId(self):
        userid = IMembraneUserAuth(self.member).getUserId()
        enumusers = self.portal.pmm.enumerateUsers
        self.failUnlessEqual(len(enumusers(id=userid, exact_match=True)), 1)
        self.failUnlessEqual(len(enumusers(id=userid[:len(userid)-1],
                                           exact_match=False)), 1)
        self.failUnlessEqual(len(enumusers(id=userid,
                                           exact_match=True, sort_on='login')), 1)
        self.failUnlessEqual(len(enumusers(id=userid,
                                           exact_match=True, sort_on='id')), 1)
        self.failUnlessEqual(len(enumusers(id=userid,
                                           exact_match=True, max_results=1)), 1)
        self.failUnlessEqual(len(enumusers(id=userid,
                                           exact_match=True, max_results=0)), 0)


class TestMembraneUserManagerAuthentication(base.MembraneTestCase,
                                            MembraneUserManagerTestBase):
    def afterSetUp(self):
        self.portal.pmm = self._makeOne('pmm')
        self.addUser()

    def testAuthenticateOnMember(self):
        credentials = {'login':'norealuser', 'password':'norealpassword'}
        userauth = IMembraneUserAuth(self.member)
        authcred = userauth.authenticateCredentials
        self.failUnlessEqual(authcred(credentials), None)
        credentials = {'login':'testuser', 'password':'wrongpassword'}
        self.failUnlessEqual(authcred(credentials), None)
        credentials = {'login':'testuser', 'password':'testpassword'}
        self.failUnlessEqual(authcred(credentials), (userauth.getUserId(),
                                                     self.member.getUserName()))

    def testAuthenticate(self):
        credentials = {'login':'norealuser', 'password':'norealpassword'}
        authcred = self.portal.pmm.authenticateCredentials
        self.failUnlessEqual(authcred(credentials), None)
        credentials = {'login':'testuser', 'password':'wrongpassword'}
        self.failUnlessEqual(authcred(credentials), None)
        credentials = {'login':'testuser', 'password':'testpassword'}
        right = (IMembraneUserAuth(self.member).getUserId(),
                 self.member.getUserName())
        self.failUnlessEqual(authcred(credentials), right)

    def testAuthenticateActiveStatesOnly(self):
        mbtool = getattr(self.portal, TOOLNAME)
        wftool = getattr(self.portal, 'portal_workflow')
        authcred = self.portal.pmm.authenticateCredentials
        credentials = {'login':'testuser', 'password':'testpassword'}
        cat_map = ICategoryMapper(mbtool)
        cat_set = generateCategorySetIdForType(self.member.portal_type)
        mem_state = wftool.getInfoFor(self.member, 'review_state')
        right = (IMembraneUserAuth(self.member).getUserId(),
                 self.member.getUserName())
        self.failUnlessEqual(authcred(credentials), right)
        cat_map.removeFromCategory(cat_set, ACTIVE_STATUS_CATEGORY,
                                   mem_state)
        self.failUnlessEqual(authcred(credentials), None)
        cat_map.addToCategory(cat_set, ACTIVE_STATUS_CATEGORY,
                              mem_state)
        self.failUnlessEqual(authcred(credentials), right)

    def testLogin(self):
        self.login(IMembraneUserAuth(self.member).getUserId())


class TestMembraneUserManagerAuthenticationPermissions( base.MembraneTestCase
                                                      , MembraneUserManagerTestBase):
    """Check if everything works when the user object is private"""

    def afterSetUp(self):
        self.portal.pmm = self._makeOne('pmm')
        self.addUser()
        self.portal.portal_workflow.doActionFor(self.member, 'hide')

    def testAuthenticate(self):
        self.logout()
        credentials = {'login':'norealuser', 'password':'norealpassword'}
        authcred = self.portal.pmm.authenticateCredentials
        self.failUnlessEqual(authcred(credentials), None)
        credentials = {'login':'testuser', 'password':'wrongpassword'}
        self.failUnlessEqual(authcred(credentials), None)
        credentials = {'login':'testuser', 'password':'testpassword'}
        self.failUnlessEqual(authcred(credentials),
                             (IMembraneUserAuth(self.member).getUserId(),
                              self.member.getUserName()))

    def testLogin(self):
        self.logout()
        self.login(IMembraneUserAuth(self.member).getUserId())


class TestMembraneUserManagerIntrospection( base.MembraneTestCase
                                          , MembraneUserManagerTestBase):

    def createSecondUser(self):
        self.member2 = _createObjectByType('TestMember', self.portal,
                                           'testuser2')
        self.member2.setUserName('testuser2')
        self.member2.setPassword('testpassword2')
        self.member2.setFullname('full name 2')
        self.member2.reindexObject()

    def afterSetUp(self):
        self.portal.pmm = self._makeOne('pmm')

    def testGetUserIdsNoUsers(self):
        self.failIf(self.portal.pmm.getUserIds())

    def testGetUserIdsOneUser(self):
        self.addUser()
        self.failUnlessEqual(self.portal.pmm.getUserIds(),
                             (IMembraneUserAuth(self.member).getUserId(),))

    def testGetUserIds(self):
        self.addUser()
        self.createSecondUser()
        userids = sortTuple(self.portal.pmm.getUserIds())
        self.failUnlessEqual(userids,
                             sortTuple((IMembraneUserAuth(self.member).getUserId(),
                                        IMembraneUserAuth(self.member2).getUserId())))

    def getUserNamesNoUsers(self):
        self.failIf(self.portal.pmm.getUserNames())

    def getUserNamesOneUser(self):
        self.addUser()
        self.failUnlessEqual(self.portal.pmm.getUserNames(),
                             (self.member.getUserName(),))

    def getUserNames(self):
        self.addUser()
        self.createSecondUser()
        usernames = sortTuple(self.portal.pmm.getUserIds())
        self.failUnlessEqual(userids,
                             sortTuple((self.member.getUserName(),
                                        self.member2.getUserName())))

    def testGetUsersNoUsers(self):
        self.failIf(self.portal.pmm.getUsers())

    def testGetUsersOneUser(self):
        self.addUser()
        users = self.portal.pmm.getUsers()
        self.failUnlessEqual([x.getId() for x in users],
                             [IMembraneUserAuth(self.member).getUserId()])

    def testGetUsers(self):
        self.addUser()
        self.createSecondUser()
        userids = sortTuple(self.portal.pmm.getUserIds())
        self.failUnlessEqual(userids,
                             sortTuple((IMembraneUserAuth(self.member).getUserId(),
                                        IMembraneUserAuth(self.member2).getUserId())))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMembraneUserManagerBasics))
    suite.addTest(makeSuite(TestMembraneUserManagerEnumeration))
    suite.addTest(makeSuite(TestMembraneUserManagerAuthentication))
    suite.addTest(makeSuite(TestMembraneUserManagerAuthenticationPermissions))
    suite.addTest(makeSuite(TestMembraneUserManagerIntrospection))
    return suite

if __name__ == '__main__':
    framework()
