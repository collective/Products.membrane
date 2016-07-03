#
# MembraneTestCase Membrane
#
from zope.location.interfaces import ISite
from Products.membrane.config import TOOLNAME
import base


class TestProductInstall(base.MembraneTestCase):

    def testExampleTypesInstall(self):
        setup_tool = self.portal.portal_setup
        setup_tool.runAllImportStepsFromProfile(
            'profile-Products.membrane:examples')
        typeslist = ['SimpleMember', 'SimpleGroup']
        for t in typeslist:
            self.failUnless(t in self.portal.portal_types.objectIds(),
                            '%s content type not installed' % t)

    def testTestTypesInstall(self):
        typeslist = ['TestMember', 'AlternativeTestMember', 'TestGroup']
        for t in typeslist:
            self.failUnless(t in self.portal.portal_types.objectIds(),
                            '%s content type not installed' % t)

    def testToolInstall(self):
        self.failUnless(TOOLNAME in self.portal.objectIds())

    def testSiteManagerInstall(self):
        self.failUnless(ISite.providedBy(self.portal))
