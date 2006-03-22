
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from zope.interface import implements
from zope.app.annotation.interfaces import IAttributeAnnotatable

from Testing import ZopeTestCase

from Products.membrane.interfaces import ICategoryMapper

#ZopeTestCase.installProduct('Five')
#ZopeTestCase.installProduct('membrane')

class Foo(object):
    """
    Dummy class for testing category mapper.
    """
    implements(IAttributeAnnotatable)
    
class TestCategoryMapper(ZopeTestCase.ZopeTestCase):

    def afterSetUp(self):
        self.obj = Foo()
        self.cat_map = ICategoryMapper(self.obj)

    def testAddCategorySet(self):
        cat_set = 'category_set'
        self.cat_map.addCategorySet(cat_set)
        self.failUnless(self.cat_map.hasCategorySet(cat_set))
        self.failUnless(cat_set in self.cat_map.listCategorySets())

    def testDelCategorySet(self):
        cat_set = 'category_set'
        self.cat_map.addCategorySet(cat_set)
        self.failUnless(self.cat_map.hasCategorySet(cat_set))
        self.cat_map.delCategorySet(cat_set)
        self.failIf(self.cat_map.hasCategorySet(cat_set))
        self.failUnless(len(self.cat_map.listCategorySets()) == 0)

    def testAddCategory(self):
        cat_set1 = 'category_set1'
        cat_set2 = 'category_set2'
        cat = 'category'
        self.cat_map.addCategorySet(cat_set1)
        self.cat_map.addCategorySet(cat_set2)
        self.cat_map.addCategory(cat_set1, cat)
        self.failUnless(self.cat_map.hasCategory(cat_set1, cat))
        self.failIf(self.cat_map.hasCategory(cat_set2, cat))

    def testMissingCatSetRaisesError(self):
        self.assertRaises(KeyError, self.cat_map.addToCategory,
                          self.cat_map, 'category_set', 'category')
        self.assertRaises(KeyError, self.cat_map.removeFromCategory,
                          self.cat_map, 'category_set', 'category')
        
    def testMissingCategoryRaisesError(self):
        cat_set = 'category_set'
        self.cat_map.addCategorySet(cat_set)
        self.assertRaises(KeyError, self.cat_map.addToCategory,
                          self.cat_map, cat_set, 'category')
        self.assertRaises(KeyError, self.cat_map.removeFromCategory,
                          self.cat_map, cat_set, 'category')

    def testAddToCategory(self):
        cat_set = 'category_set'
        cat1 = 'category1'
        cat2 = 'category2'
        datum1 = 'datum1'
        datum2 = 'datum2'
        self.cat_map.addCategorySet(cat_set)
        self.cat_map.addCategory(cat_set, cat1)
        self.cat_map.addCategory(cat_set, cat2)
        self.cat_map.addToCategory(cat_set, cat1, datum1)
        self.failUnless(self.cat_map.isInCategory(cat_set, cat1, datum1))
        self.failIf(self.cat_map.isInCategory(cat_set, cat1, datum2))
        self.failIf(self.cat_map.isInCategory(cat_set, cat2, datum1))

        self.cat_map.addToCategory(cat_set, cat1, datum2)
        self.failUnless(self.cat_map.isInCategory(cat_set, cat1, datum1))
        self.failUnless(self.cat_map.isInCategory(cat_set, cat1, datum2))
        self.failUnless(set([datum1, datum2]) == \
                        set(self.cat_map.listCategoryValues(cat_set, cat1)))

    def testRemoveFromCategory(self):
        cat_set = 'category_set'
        cat = 'category'
        datum1 = 'datum1'
        datum2 = 'datum2'
        self.cat_map.addCategorySet(cat_set)
        self.cat_map.addCategory(cat_set, cat)
        self.cat_map.addToCategory(cat_set, cat, datum1)
        self.cat_map.addToCategory(cat_set, cat, datum2)
        self.failUnless(set([datum1, datum2]) == \
                        set(self.cat_map.listCategoryValues(cat_set, cat)))

        self.cat_map.removeFromCategory(cat_set, cat, datum1)
        self.failIf(self.cat_map.isInCategory(cat_set, cat, datum1))
        self.failUnless(self.cat_map.isInCategory(cat_set, cat, datum2))
        self.failUnless(set([datum2]) == \
                        set(self.cat_map.listCategoryValues(cat_set, cat)))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestCategoryMapper))
    return suite

if __name__ == '__main__':
    framework()

