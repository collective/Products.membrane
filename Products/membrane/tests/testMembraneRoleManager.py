# -*- coding: utf-8 -*-
#
# MembraneTestCase Membrane
#
from Products.membrane.tests import base

import six
import unittest


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
        if six.PY2:
            self.addUser(self.portal)

    def getUser(self):
        username = self.member.getUserName()
        return self.portal.acl_users.getUser(username)

    @unittest.skipUnless(six.PY2, "Archetypes not supported on Python3")
    def testDefaultRoles(self):
        roles = self.member.getField('roles_').default
        self.failUnless(set(roles) < set(self.getUser().getRoles()))

    @unittest.skipUnless(six.PY2, "Archetypes not supported on Python3")
    def testRolesStayCurrent(self):
        roles = ('Member', 'Reviewer')
        self.failIf(set(roles) < set(self.getUser().getRoles()))
        self.member.setRoles(roles)
        self.failUnless(set(roles) < set(self.getUser().getRoles()))

    @unittest.skipUnless(six.PY2, "Archetypes not supported on Python3")
    def testRolesFromGroup(self):
        self.addGroup()
        role = 'Manager'
        self.failIf(role in self.getUser().getRoles())
        self.group.addReference(self.member)
        self.group.setRoles((role,))
        self.failUnless(role in self.getUser().getRoles())
