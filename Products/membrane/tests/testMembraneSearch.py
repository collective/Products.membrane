import os, sys
import unittest

from Testing import ZopeTestCase
from Products.membrane.tests import base
from Products.CMFPlone.utils import _createObjectByType

from Products.membrane.tests.utils import sortTuple
from Products.membrane.tests import testMembraneUserManager
from Products.membrane.interfaces import IMembraneUserAuth


class TestMembraneSearch(base.MembraneTestCase,
                         testMembraneUserManager.MembraneUserManagerTestBase):
    def afterSetUp(self):
        self.portal.pmm = self._makeOne('pmm')
        self.addUser()

    def testSimpleMemberSearch(self):
        mtool = self.portal.portal_membership
        mems = mtool.searchForMembers(login=self.member.getUserName())
        user_auth = IMembraneUserAuth(self.member)
        self.failUnless(len(mems) == 1 and mems[0] ==
                        mtool.getMemberById(user_auth.getUserId()))

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMembraneSearch))
    return suite
