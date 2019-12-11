# -*- coding: utf-8 -*-
from plone.app.testing import login
from Products.membrane.plugins.userfactory import MembraneUser
from Products.membrane.tests import base

import six
import unittest


class MembraneUserFactoryTestBase:

    def _getTargetClass(self):

        from Products.membrane.plugins.userfactory \
            import MembraneUserFactory

        return MembraneUserFactory

    def _makeOne(self, id='test', *args, **kw):

        return self._getTargetClass()(id=id, *args, **kw)


class TestMembraneUserFactory(base.MembraneTestCase,
                              MembraneUserFactoryTestBase):

    def setUp(self):
        super(TestMembraneUserFactory, self).setUp()
        self.portal.pmm = self._makeOne('pmm')
        if six.PY2:
            self.addUser()

    @unittest.skipUnless(six.PY2, "Archetypes not supported on Python3")
    def testUserCreation(self):
        username = self.member.getUserName()
        user = self.portal.pmm.createUser(self.userid, username)
        self.failUnless(user)
        self.failUnless(isinstance(user, MembraneUser))

    @unittest.skipUnless(six.PY2, "Archetypes not supported on Python3")
    def testUserCreationFromPAS(self):
        user = self.portal.acl_users.getUserById(self.userid)
        self.failUnless(user)
        self.failUnless(isinstance(user, MembraneUser))

    @unittest.skipUnless(six.PY2, "Archetypes not supported on Python3")
    def testLogin(self):
        login(self.portal, self.userid)
