#
# MembraneTestCase Membrane
#

from Products.membrane.tests import base
from Products.membrane.plugins.userfactory import MembraneUser


class MembraneUserFactoryTestBase:

    def _getTargetClass(self):

        from Products.membrane.plugins.userfactory \
            import MembraneUserFactory

        return MembraneUserFactory

    def _makeOne(self, id='test', *args, **kw):

        return self._getTargetClass()(id=id, *args, **kw)


class TestMembraneUserFactory(base.MembraneTestCase,
                              MembraneUserFactoryTestBase):

    def afterSetUp(self):
        self.portal.pmm = self._makeOne('pmm')
        self.addUser()

    def testUserCreation(self):
        username = self.member.getUserName()
        user = self.portal.pmm.createUser(self.userid, username)
        self.failUnless(user)
        self.failUnless(isinstance(user, MembraneUser))

    def testUserCreationFromPAS(self):
        user = self.portal.acl_users.getUserById(self.userid)
        self.failUnless(user)
        self.failUnless(isinstance(user, MembraneUser))

    def testLogin(self):
        self.login(self.userid)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMembraneUserFactory))
    return suite
