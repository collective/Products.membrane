# -*- coding: utf-8 -*-
#
# MembraneTestCase Membrane
#
from Products.CMFCore.indexing import wrap
from Products.membrane.catalog import MembraneCatalogProcessor
from Products.membrane.config import TOOLNAME
from Products.membrane.tests import base


class TestMembraneCatalogProcessor(base.MembraneTestCase):

    def setUp(self):
        super(TestMembraneCatalogProcessor, self).setUp()
        self.mbtool = getattr(self.portal, TOOLNAME)

    def testWrappedObject(self):
        mt = self.mbtool
        self.addUser(username='testuser')
        user = mt.getUserObject('testuser')
        processor = MembraneCatalogProcessor()
        self.assertEqual(len(mt.searchResults(id='testuser')), 1)

        wrapped_user = wrap(user)
        processor.unindex(wrapped_user)
        self.assertEqual(len(mt.searchResults(id='testuser')), 0)

        processor.index(user)
        self.assertEqual(len(mt.searchResults(id='testuser')), 1)
