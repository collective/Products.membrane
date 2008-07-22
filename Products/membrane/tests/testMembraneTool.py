#
# MembraneTestCase Membrane
#

from zope.interface import Interface

from Products.membrane.tests import base
from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.config import TOOLNAME
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.utils import generateCategorySetIdForType
from Products.membrane.utils import membraneCacheKey

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
        self.mbtool = getattr(self.portal, TOOLNAME)

    def testMembraneTypeRegistration(self):
        mt = self.mbtool
        pt = 'TestMember'
        self.failUnless(pt in mt.listMembraneTypes())
        mt.unregisterMembraneType(pt)
        self.failIf(pt in mt.listMembraneTypes())
        mt.registerMembraneType(pt)
        self.failUnless(pt in mt.listMembraneTypes())

    def testObjectImplements(self):
        from Products.membrane.tools.membrane import object_implements
        mt = self.mbtool
        interface_ids = object_implements(mt, self.portal)
        for iid in interface_ids:
            iface = resolveInterface(str(iid))
            try:
                iface(mt)
            except TypeError:
                self.fail("Can't adapt to %s" % iid)

    def testStatusCategoriesAreInitialized(self):
        mt = self.mbtool
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
        mt = self.mbtool
        pt = 'TestMember'
        cat_map = ICategoryMapper(mt)
        cat_set = generateCategorySetIdForType(pt)
        self.failUnless(cat_map.hasCategorySet(cat_set))
        mt.unregisterMembraneType(pt)
        self.failIf(cat_map.hasCategorySet(cat_set))

    def testGetUserAuthProviderForEmptyString(self):
        # see http://plone.org/products/membrane/issues/7
        mt = self.mbtool
        self.addUser()
        self.addUser(username='testuser2')
        mt.getUserAuthProvider('')
        # test passes if above call doesn't raise AssertionError

    def testCaseSensitivityIsHonored(self):
        mt = self.mbtool
        self.addUser()
        self.failUnless(mt.getUserAuthProvider('TESTUSER') is None)
        self.failIf(mt.getUserAuthProvider('testuser') is None)

        mt.case_sensitive_auth = False
        self.failIf(mt.getUserAuthProvider('TESTUSER') is None)
        self.failIf(mt.getUserAuthProvider('testuser') is None)

    def testGetOriginalUserIdCase(self):
        mt = self.mbtool
        self.addUser()
        case_test = 'TeStUsEr'
        orig_id = mt.getOriginalUserIdCase(case_test)
        self.failUnless(orig_id == case_test.lower())

    def testCatalogCounter(self):
        mt = self.mbtool
        self.assertEqual(mt.getCatalogCount(), 0)
        last = mt.getCatalogCount()
        self.addUser()
        self.failUnless(mt.getCatalogCount() > last)
        last = mt.getCatalogCount()
        self.addUser(username='testuser2')
        self.failUnless(mt.getCatalogCount() > last)
        last = mt.getCatalogCount()
        self.portal.manage_delObjects('testuser2')
        self.failUnless(mt.getCatalogCount() > last)

    def testCacheKey(self):
        method = lambda: 42
        class MockAdapter:
            pass
        adapter = MockAdapter()
        adapter.context = self.mbtool
        path = '/'.join(self.mbtool.getPhysicalPath())
        self.assertEqual(membraneCacheKey(method, adapter), (path, 0))
        last = membraneCacheKey(method, adapter)
        self.addUser()
        self.failUnless(membraneCacheKey(method, adapter) > last)
        last = membraneCacheKey(method, adapter)
        self.addUser(username='testuser2')
        self.failUnless(membraneCacheKey(method, adapter) > last)
        last = membraneCacheKey(method, adapter)
        self.portal.manage_delObjects('testuser2')
        self.failUnless(membraneCacheKey(method, adapter) > last)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMembraneTool))
    return suite
