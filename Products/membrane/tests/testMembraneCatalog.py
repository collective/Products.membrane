#
# MembraneTestCase Membrane
#

from Acquisition import aq_inner
from Acquisition import aq_parent

from Products.membrane.tests import base
from Products.membrane.config import TOOLNAME
from Products.membrane.catalog import MembraneCatalogProcessor


def wrap(obj):
    """ A method to wrap objects in a PathWrapper class, similar to what
        collective.indexing does.

        The __getattr__ function of the PathWrapper class only gets the wrapped
        instance's attributes if the attributes are not on the PathWrapper
        class or instance.

        This can cause problems in the MembraneCatalogProcessor, which tries to
        get the wrapped instance's 'portal_type' attribute.
    """
    class PathWrapper(obj.__class__):
        portal_type = '' # We explicitly set this class variable here, to test
        # for the case where __getattr__ is not invoked and therefore doesn't
        # get the wrapped object's portal_type (which is what's desired).

        def __init__(self):
            self.__dict__.update(dict(
                context = obj,
                path = obj.getPhysicalPath(),
                REQUEST = getattr(obj, 'REQUEST', None)))

        def __getattr__(self, name):
            return getattr(aq_inner(self.context), name)

    return PathWrapper().__of__(aq_parent(obj))


class TestMembraneCatalogProcessor(base.MembraneTestCase):

    def afterSetUp(self):
        self.mbtool = getattr(self.portal, TOOLNAME)

    def testWrappedObject(self):
        mt = self.mbtool
        self.addUser(username='testuser')
        user = mt.getUserObject('testuser')
        processor = MembraneCatalogProcessor()
        self.assertEqual(len(mt.searchResults(id='testuser')), 1)

        wrapped_user = wrap(user) # See PathWrapper above
        processor.unindex(wrapped_user)
        self.assertEqual(len(mt.searchResults(id='testuser')), 0)

        processor.index(user)
        self.assertEqual(len(mt.searchResults(id='testuser')), 1)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMembraneCatalogProcessor))
    return suite

