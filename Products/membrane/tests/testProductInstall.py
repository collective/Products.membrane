# -*- coding: utf-8 -*-
#
# MembraneTestCase Membrane
#
from Products.membrane.config import TOOLNAME
from Products.membrane.tests import base
from zope.location.interfaces import ISite

import six


class TestProductInstall(base.MembraneTestCase):

    def testExampleTypesInstall(self):
        setup_tool = self.portal.portal_setup
        if six.PY2:
            setup_tool.runAllImportStepsFromProfile(
                'profile-Products.membrane:examples')
            typeslist = ['SimpleMember', 'SimpleGroup']
        else:
            setup_tool.runAllImportStepsFromProfile(
                'profile-Products.membrane.tests:test')
            typeslist = ['TestMember', 'TestGroup']
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
