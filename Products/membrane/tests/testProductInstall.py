#
# MembraneTestCase Membrane
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.membrane.tests import base
from Products.membrane.config import TOOLNAME
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import setSecurityManager

class TestProductInstall(base.MembraneTestCase):

    def afterSetUp(self):
        pass

    def testExampleTypesInstall(self):
        setup_tool = self.portal.portal_setup
        setup_tool.setImportContext('profile-membrane:examples')
        setup_tool.runAllImportSteps()
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


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestProductInstall))
    return suite

if __name__ == '__main__':
    framework()
