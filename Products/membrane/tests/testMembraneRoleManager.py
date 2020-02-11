# -*- coding: utf-8 -*-
#
# MembraneTestCase Membrane
#
from Products.membrane.tests import base

import six


class MembraneRoleManagerTestBase:

    def _getTargetClass(self):
        from Products.membrane.plugins.rolemanager \
            import MembraneRoleManager
        return MembraneRoleManager

    def _makeOne(self, id='test', *args, **kw):
        return self._getTargetClass()(id=id, *args, **kw)


class TestMembraneRoleManagerPlugin(base.MembraneTestCase,
                                    MembraneRoleManagerTestBase):

    def setUp(self):
        super(TestMembraneRoleManagerPlugin, self).setUp()
        self.addUser(self.portal)

    def getUser(self):
        username = self.member.getUserName()
        return self.portal.acl_users.getUser(username)

    def testDefaultRoles(self):
        if six.PY2:
            roles = self.member.getField('roles_').default
        else:
            roles = self.member.roles_
        self.failUnless(set(roles) < set(self.getUser().getRoles()))

    def testRolesStayCurrent(self):
        self.assertSetEqual(set(self.getUser().getRoles()), {"Member", "Authenticated"})
        roles = ('Member', 'Reviewer')
        self.member.setRoles(roles)
        self.assertSetEqual(set(self.getUser().getRoles()), {"Authenticated"} | set(roles))

    def testRolesFromGroup(self):
        self.addGroup()
        role = 'Manager'
        self.failIf(role in self.getUser().getRoles())
        self.group.addReference(self.member)
        self.group.setRoles((role,))
        self.failUnless(role in self.getUser().getRoles())
