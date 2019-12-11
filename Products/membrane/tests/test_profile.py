# -*- coding: utf-8 -*-
"""Test the generic setup profile."""

from .base import MembraneTestCase
from Products.CMFCore.utils import getToolByName

import six
import unittest


class TestProfile(MembraneTestCase):
    """Test the generic setup profile."""

    @unittest.skipUnless(six.PY2, "Archetypes not supported on Python3")
    def test_archetypetool(self):
        """
        Check interaction with archetypetool.xml

        If archetypetool.xml registers a type for the catalog map
        and membranetool.xml is run after archetypetool.xml, then
        membranetool.xml still needs to register the types with the
        status map.

        This problem only surfaces when the archetypetool step is run
        before the membranetool step and since the order is
        unpredictable this test exposes the bug.

        """
        attool = getToolByName(self.portal, 'archetype_tool')
        catalog_map = getattr(attool, 'catalog_map', {})
        if 'TestMember' not in catalog_map:
            catalog_map['TestMember'] = ('portal_catalog',
                                         'membrane_tool')
        setup_tool = getToolByName(self.portal, 'portal_setup')
        setup_tool.runImportStepFromProfile(
            'profile-Products.membrane.tests:test',
            'membranetool')
