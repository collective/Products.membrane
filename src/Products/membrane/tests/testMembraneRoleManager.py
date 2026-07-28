#
# MembraneTestCase Membrane
#
from Products.membrane.tests import base


class MembraneRoleManagerTestBase:
    def _getTargetClass(self):
        from Products.membrane.plugins.rolemanager import MembraneRoleManager

        return MembraneRoleManager

    def _makeOne(self, id="test", *args, **kw):
        return self._getTargetClass()(id=id, *args, **kw)


class TestMembraneRoleManagerPlugin(base.MembraneTestCase, MembraneRoleManagerTestBase):
    def setUp(self):
        super().setUp()
        self.addUser(self.portal)

    def getUser(self):
        username = self.member.getUserName()
        return self.portal.acl_users.getUser(username)

    def testDefaultRoles(self):
        roles = self.member.roles_
        self.assertTrue(set(roles) < set(self.getUser().getRoles()))

    def testRolesStayCurrent(self):
        self.assertSetEqual(set(self.getUser().getRoles()), {"Member", "Authenticated"})
        roles = ("Member", "Reviewer")
        self.member.setRoles(roles)
        self.assertSetEqual(
            set(self.getUser().getRoles()), {"Authenticated"} | set(roles)
        )

    def testRolesFromGroup(self):
        self.addGroup()
        role = "Manager"
        self.assertFalse(role in self.getUser().getRoles())
        self.group.addReference(self.member)
        self.group.setRoles((role,))
        self.assertTrue(role in self.getUser().getRoles())
