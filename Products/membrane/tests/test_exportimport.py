"""Test the GS export import handlers."""

from Acquisition import aq_base
from base import MembraneTestCase
from Products.CMFCore.utils import getToolByName


class TestMembraneToolExportImport(MembraneTestCase):
    """Test membrane_tool import / export handlers."""

    def setUp(self):
        super(TestMembraneToolExportImport, self).setUp()

        from Products.PluggableAuthService.interfaces.plugins import \
            IUserAdderPlugin

        setup_tool = self.portal.portal_setup
        setup_tool.runAllImportStepsFromProfile(
            'profile-Products.membrane:examples')
        plugins = self.portal.acl_users.plugins
        plugins.movePluginsUp(IUserAdderPlugin, ['membrane_users'])

    def test_useradder(self):
        """
        Simple check to see if the user_adder value is correctly set
        by the GS profile.
        """
        mbtool = getToolByName(self.portal, 'membrane_tool')
        user_adder = getattr(aq_base(mbtool), 'user_adder', None)
        self.assertEqual(user_adder, "membrane_example")
