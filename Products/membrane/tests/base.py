# -*- coding: utf-8 -*-
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from Products.CMFPlone.utils import _createObjectByType
from Products.membrane.testing import addUser
from Products.membrane.testing import MEMBRANE_ADD_USER_INTEGRATION_TESTING
from Products.membrane.testing import MEMBRANE_PROFILES_INTEGRATION_TESTING

import unittest


class MembraneTestCase(unittest.TestCase):

    layer = MEMBRANE_PROFILES_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def addGroup(self, obj=None):
        if obj is None:
            obj = self.portal
        self.group = _createObjectByType('TestGroup', obj, 'testgroup')
        self.group.setTitle('Test group')
        self.group.setDescription('A test group')
        self.group.reindexObject()

    def addUser(self, obj=None, username='testuser', title='full name'):
        if obj is None:
            obj = self.portal
        self.member = addUser(obj, username, title)
        self.userid = self.member.getId()


class MembraneUserTestCase(MembraneTestCase):

    layer = MEMBRANE_ADD_USER_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.member = self.portal.testuser
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
