from Acquisition import aq_parent, aq_inner
from Products.membrane.utils import getCurrentUserAdder
import base


class TestUserAdder(base.MembraneTestCase):
    """
    Tests the IUserAdder utility that is included in the 'example'
    profile.
    """

    def afterSetUp(self):
        super(TestUserAdder, self).afterSetUp()

        from Products.PluggableAuthService.interfaces.plugins import \
             IUserAdderPlugin

        setup_tool = self.portal.portal_setup
        setup_tool.runAllImportStepsFromProfile(
            'profile-Products.membrane:examples')
        plugins = self.portal.acl_users.plugins
        plugins.movePluginsUp(IUserAdderPlugin, ['membrane_users'])

    def testUserFolderCreatesUser(self):
        uf = self.portal.acl_users
        userid = 'test_utility'
        pwd = 'secret'
        self.loginAsPortalOwner()
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


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestUserAdder))
    return suite
