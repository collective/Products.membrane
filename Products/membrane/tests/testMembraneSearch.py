from Products.membrane.tests import base
from Products.membrane.tests import testMembraneUserManager
from Products.membrane.interfaces import IMembraneUserAuth


class TestMembraneSearch(base.MembraneTestCase,
                         testMembraneUserManager.MembraneUserManagerTestBase):
    def afterSetUp(self):
        self.portal.pmm = self._makeOne('pmm')
        self.addUser()

    def testSimpleMemberSearch(self):
        uf = self.portal.acl_users
        mems = uf.searchUsers(login=self.member.getUserName())
        user_auth = IMembraneUserAuth(self.member)
        self.failUnless(len(mems) == 1 and
                        mems[0]['userid'] == user_auth.getUserId())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMembraneSearch))
    return suite
