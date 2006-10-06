#
# MembraneTestCase Membrane
#

import os, sys

from zope.interface import Interface

from Testing import ZopeTestCase
from Products.membrane.tests import base
from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.config import TOOLNAME
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.utils import generateCategorySetIdForType

def resolveInterface(dotted_name):
    parts = dotted_name.split('.')
    m_name = '.'.join(parts[:-1])
    k_name = parts[-1]
    module = __import__(m_name, globals(), locals(), [k_name])
    klass = getattr(module, k_name)
    if not issubclass(klass, Interface):
        raise ValueError, '%r is not a valid Interface.' % dotted_name
    return klass

class TestMembraneTool(base.MembraneTestCase):

    def afterSetUp(self):
        pass

    def testMembraneTypeRegistration(self):
        mt = getattr(self.portal, TOOLNAME)
        pt = 'TestMember'
        self.failUnless(pt in mt.listMembraneTypes())
        mt.unregisterMembraneType(pt)
        self.failIf(pt in mt.listMembraneTypes())
        mt.registerMembraneType(pt)
        self.failUnless(pt in mt.listMembraneTypes())

    def testObjectImplements(self):
        from Products.membrane.tools.membrane import object_implements
        mt = getattr(self.portal, TOOLNAME)
        interface_ids = object_implements(mt, self.portal)
        for iid in interface_ids:
            iface = resolveInterface(str(iid))
            try:
                iface(mt)
            except TypeError:
                self.fail("Can't adapt to %s" % iid)

    def testStatusCategoriesAreInitialized(self):
        mt = getattr(self.portal, TOOLNAME)
        cat_map = ICategoryMapper(mt)
        for pt in ['TestMember', 'TestGroup']:
            cat_set = generateCategorySetIdForType(pt)
            self.failUnless(cat_map.hasCategorySet(cat_set))
            self.failUnless(cat_map.hasCategory(cat_set,
                                                ACTIVE_STATUS_CATEGORY))
            wft = getattr(self.portal, 'portal_workflow')
            chain = wft.getChainForPortalType(pt)
            for wfid in chain:
                wf = getattr(wft, wfid)
                states = wf.states.objectIds()
                for state in states:
                    self.failUnless(cat_map.isInCategory(cat_set,
                                                         ACTIVE_STATUS_CATEGORY,
                                                         state))

    def testStatusCategoriesGetCleared(self):
        mt = getattr(self.portal, TOOLNAME)
        pt = 'TestMember'
        cat_map = ICategoryMapper(mt)
        cat_set = generateCategorySetIdForType(pt)
        self.failUnless(cat_map.hasCategorySet(cat_set))
        mt.unregisterMembraneType(pt)
        self.failIf(cat_map.hasCategorySet(cat_set))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMembraneTool))
    return suite
