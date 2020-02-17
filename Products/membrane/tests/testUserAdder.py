# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Acquisition import aq_parent
from plone.app.testing import login
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from plone.app.testing import TEST_USER_NAME
from Products.membrane.tests import base
from Products.membrane.utils import getCurrentUserAdder

import six


class TestUserAdder(base.MembraneTestCase):
    """
    Tests the IUserAdder utility that is included in the 'example'
    profile.
    """

    def setUp(self):
        super(TestUserAdder, self).setUp()
        from Products.PluggableAuthService.interfaces.plugins import \
            IUserAdderPlugin
        setup_tool = self.portal.portal_setup
        if six.PY2:
            setup_tool.runAllImportStepsFromProfile(
                'profile-Products.membrane:examples')
        else:
            setup_tool.runAllImportStepsFromProfile(
                'profile-Products.membrane.tests:test')
        plugins = self.portal.acl_users.plugins
        plugins.movePluginsUp(IUserAdderPlugin, ['membrane_users'])

    def testUserFolderCreatesUser(self):
        uf = self.portal.acl_users
        userid = 'test_utility'
        pwd = 'secret'
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)
        uf._doAddUser(userid, pwd, [], [])
        self.failUnless(userid in self.portal.objectIds())
        req = self.portal.REQUEST
        self.failIf(uf.authenticate(userid, pwd, req) is None)

    def testAcquisition(self):
        plugin = self.portal.acl_users.membrane_users
        adder = getCurrentUserAdder(plugin)
        # We should have request
        self.failIf(getattr(aq_inner(adder), 'REQUEST', None) is None)
        # Our parent should be the plugin
        self.failUnless(aq_parent(adder) is plugin)
