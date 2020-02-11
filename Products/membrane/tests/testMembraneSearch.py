# -*- coding: utf-8 -*-
from Products.membrane.interfaces import IMembraneUserAuth
from Products.membrane.tests import base
from Products.membrane.tests import testMembraneUserManager


class TestMembraneSearch(base.MembraneTestCase,
                         testMembraneUserManager.MembraneUserManagerTestBase):

    def setUp(self):
        super(TestMembraneSearch, self).setUp()
        self.portal.pmm = self._makeOne('pmm')
        self.addUser()

    def testSimpleMemberSearch(self):
        uf = self.portal.acl_users
        mems = uf.searchUsers(login=self.member.getUserName())
        user_auth = IMembraneUserAuth(self.member)
        self.failUnless(len(mems) == 1 and
                        mems[0]['userid'] == user_auth.getUserId())

    def testFullnameMemberSearch(self):
        uf = self.portal.acl_users
        mems = uf.searchUsers(fullname=self.member.Title())
        user_auth = IMembraneUserAuth(self.member)
        self.failUnless(len(mems) == 1 and
                        mems[0]['userid'] == user_auth.getUserId())
