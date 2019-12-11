# -*- coding: utf-8 -*-
"""Test the GS export import handlers."""

from .base import MembraneTestCase
from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName

import six
import unittest


class TestMembraneToolExportImport(MembraneTestCase):
    """Test membrane_tool import / export handlers."""

    def setUp(self):
        super(TestMembraneToolExportImport, self).setUp()

    @unittest.skipUnless(six.PY2, "Archetypes not supported on Python3")
    def test_useradder(self):
        """
        Simple check to see if the user_adder value is correctly set
        by the GS profile.
        """
        setup_tool = self.portal.portal_setup
        setup_tool.runAllImportStepsFromProfile(
            'profile-Products.membrane:examples')
        plugins = self.portal.acl_users.plugins
        from Products.PluggableAuthService.interfaces.plugins import \
            IUserAdderPlugin
        plugins.movePluginsUp(IUserAdderPlugin, ['membrane_users'])
        mbtool = getToolByName(self.portal, 'membrane_tool')
        user_adder = getattr(aq_base(mbtool), 'user_adder', None)
        self.assertEqual(user_adder, "membrane_example")
