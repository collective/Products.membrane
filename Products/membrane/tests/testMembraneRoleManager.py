#
# MembraneTestCase Membrane
#

from Products.membrane.tests import base


class MembraneRoleManagerTestBase:

    def _getTargetClass(self):
        from Products.membrane.plugins.rolemanager \
            import MembraneRoleManager
        return MembraneRoleManager

    def _makeOne(self, id='test', *args, **kw):
        return self._getTargetClass()(id=id, *args, **kw)


class TestMembraneRoleManagerPlugin(base.MembraneTestCase,
                                    MembraneRoleManagerTestBase):

    def afterSetUp(self):
        self.addUser(self.portal)

    def getUser(self):
        username = self.member.getUserName()
        return self.portal.acl_users.getUser(username)

    def testDefaultRoles(self):
        roles = self.member.getField('roles_').default
        self.failUnless(set(roles) < set(self.getUser().getRoles()))

    def testRolesStayCurrent(self):
        roles = ('Member', 'Reviewer')
        self.failIf(set(roles) < set(self.getUser().getRoles()))
        self.member.setRoles(roles)
        self.failUnless(set(roles) < set(self.getUser().getRoles()))

    def testRolesFromGroup(self):
        self.addGroup()
        role = 'Manager'
        self.failIf(role in self.getUser().getRoles())
        self.group.addReference(self.member)
        self.group.setRoles((role,))
        self.failUnless(role in self.getUser().getRoles())


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMembraneRoleManagerPlugin))
    return suite
