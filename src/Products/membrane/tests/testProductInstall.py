#
# MembraneTestCase Membrane
#
from Products.membrane.config import TOOLNAME
from Products.membrane.tests import base
from zope.location.interfaces import ISite


class TestProductInstall(base.MembraneTestCase):
    def testExampleTypesInstall(self):
        setup_tool = self.portal.portal_setup
        setup_tool.runAllImportStepsFromProfile("profile-Products.membrane.tests:test")
        typeslist = ["TestMember", "TestGroup"]
        for t in typeslist:
            self.assertTrue(
                t in self.portal.portal_types.objectIds(),
                "%s content type not installed" % t,
            )

    def testTestTypesInstall(self):
        typeslist = ["TestMember", "AlternativeTestMember", "TestGroup"]
        for t in typeslist:
            self.assertTrue(
                t in self.portal.portal_types.objectIds(),
                "%s content type not installed" % t,
            )

    def testToolInstall(self):
        self.assertTrue(TOOLNAME in self.portal.objectIds())

    def testSiteManagerInstall(self):
        self.assertTrue(ISite.providedBy(self.portal))
