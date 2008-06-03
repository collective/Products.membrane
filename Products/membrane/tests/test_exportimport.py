"""Test the GS export import handlers."""

from Acquisition import aq_base
from Products.CMFCore.utils import getToolByName
from base import MembraneExamplesLayer
from base import MembraneTestCase
from unittest import main
from unittest import makeSuite

class TestMembraneToolExportImport(MembraneTestCase):
    """Test membrane_tool import / export handlers."""
    layer = MembraneExamplesLayer

    def test_useradder(self):
        """
        Simple check to see if the user_adder value is correctly set
        by the GS profile.
        """
        mbtool = getToolByName(self.portal, 'membrane_tool')
        user_adder = getattr(aq_base(mbtool), 'user_adder', None)
        self.assertEqual(user_adder, "membrane_example")

def test_suite():
    return makeSuite(TestMembraneToolExportImport)

if __name__ == "__main__":
    main(defaultTest='test_suite')
