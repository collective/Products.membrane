#
# MembraneTestCase Membrane
#

from Products.membrane.tests import base
from Products.CMFPlone.utils import _createObjectByType

from Products.membrane.plugins.userfactory import MembraneUser


class MembraneUserFactoryTestBase:

    def _getTargetClass( self ):

        from Products.membrane.plugins.userfactory \
            import MembraneUserFactory

        return MembraneUserFactory

    def _makeOne( self, id='test', *args, **kw ):

        return self._getTargetClass()( id=id, *args, **kw )


class TestMembraneUserFactory( base.MembraneTestCase
                             , MembraneUserFactoryTestBase):

    def afterSetUp(self):
        self.portal.pmm = self._makeOne('pmm')
        self.addUser()

    def testUserCreation(self):
        username = self.member.getUserName()
        user = self.portal.pmm.createUser(self.userid, username)
        self.failUnless(user)
        self.failUnless(isinstance(user, MembraneUser))

    def testUserCreationFromPAS(self):
        user = self.portal.acl_users.getUserById(self.userid)
        self.failUnless(user)
        self.failUnless(isinstance(user, MembraneUser))

    def testLogin(self):
        self.login(self.userid)


class TestMembraneUserReferenceable( base.MembraneTestCase
                                   , MembraneUserFactoryTestBase):

    def afterSetUp(self):
        self.portal.pmm = self._makeOne('pmm')
        self.addUser()

    def testUID(self):
        user = self.portal.acl_users.getUserById(self.userid)
        self.failUnlessEqual(user.getProperty('uid'), self.member.UID())
        self.failUnlessEqual(user.UID(), self.member.UID())

    def testGetMembraneObject(self):
        user = self.portal.acl_users.getUserById(self.userid)
        self.failUnlessEqual(user._getMembraneObject(), self.member)

    def testAddAndGetRefs(self):
        user = self.portal.acl_users.getUserById(self.userid)
        folder = _createObjectByType('Folder', self.portal, 'document')

        user.addReference(folder)

        self.failUnless(user.hasRelationshipTo(folder))
        self.failUnless(self.member.hasRelationshipTo(folder))

        refs = user.getRefs()
        self.failUnlessEqual(refs, self.member.getRefs())
        self.failUnlessEqual(len(refs), 1)

        self.failUnlessEqual(refs, user.getReferences())

        ref = refs[0]
        self.failUnlessEqual(ref, folder)

        brefs = folder.getBRefs()
        self.failUnlessEqual(len(brefs), 1)

        bref = brefs[0]
        self.failUnlessEqual(bref, self.member)

        refimpl = user.getReferenceImpl()
        self.failUnless(refimpl)
        self.failUnlessEqual(refimpl, self.member.getReferenceImpl())

        brefimpl = folder.getBackReferenceImpl()
        self.failUnless(brefimpl)
        
        self.failUnlessEqual(user.reference_url(), self.member.reference_url())

        user.deleteReference(folder)
        self.failIf(user.getRefs())
        self.failIf(self.member.getRefs())
        

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestMembraneUserFactory))
    suite.addTest(makeSuite(TestMembraneUserReferenceable))
    return suite
