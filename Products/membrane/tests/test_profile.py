"""Test the generic setup profile."""

from unittest import main, makeSuite

from Products.CMFCore.utils import getToolByName

from base import MembraneTestCase


class TestProfile(MembraneTestCase):
    """Test the generic setup profile."""

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
        setup_tool.runImportStepFromProfile('profile-Products.membrane.tests:test',
                                            'membranetool')


def test_suite():
    return makeSuite(TestProfile)

if __name__ == "__main__":
    main(defaultTest='test_suite')
