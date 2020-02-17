# -*- coding: utf-8 -*-
#
# MembraneTestCase Membrane
#

from Products.CMFPlone.utils import _createObjectByType
from Products.membrane.interfaces import IMembraneUserAuth
from Products.membrane.interfaces import IMembraneUserGroups
from Products.membrane.tests import base
from Products.membrane.tests.utils import sortTuple
from Products.PluggableAuthService.tests.conformance import IGroupEnumerationPlugin_conformance  # noqa: E501
from Products.PluggableAuthService.tests.conformance import IGroupsPlugin_conformance  # noqa: E501

import unittest


class MembraneGroupManagerTestBase:

    def _getTargetClass(self):

        from Products.membrane.plugins.groupmanager \
            import MembraneGroupManager

        return MembraneGroupManager

    def _makeOne(self, id='test', *args, **kw):

        return self._getTargetClass()(id=id, *args, **kw)

    def createGroupAndUsers(self):
        self.addGroup(self.portal)
        self.addUser(self.group)

        self.member2 = _createObjectByType(
            'TestMember', self.portal, 'testmember')
        self.member2.setUserName('testmember')
        self.member2.setPassword('testpassword')
        self.member2.setTitle('Member 2')
        self.member2.reindexObject()


class TestMembraneGroupManagerBasics(unittest.TestCase,
                                     MembraneGroupManagerTestBase,
                                     IGroupsPlugin_conformance,
                                     IGroupEnumerationPlugin_conformance):
    # Run the conformance tests
    pass


class TestMembraneGroupManager(base.MembraneTestCase,
                               MembraneGroupManagerTestBase):

    def setUp(self):
        super(TestMembraneGroupManager, self).setUp()
        self.portal.pmm = self._makeOne('pmm')

    def testGroupMembership(self):
        self.createGroupAndUsers()
        group = self.portal.testgroup
        member = group.testuser  # We need acquisition to be correct
        mem_auth = IMembraneUserAuth(member)
        mem_grps = IMembraneUserGroups(member)
        member2 = self.member2
        mem2_auth = IMembraneUserAuth(member2)
        mem2_grps = IMembraneUserGroups(member2)
        self.failUnlessEqual(group.getGroupMembers(),
                             (mem_auth.getUserId(),))
        self.failUnlessEqual(mem_grps.getGroupsForPrincipal(mem_grps),
                             (group.getId(),))
        self.group.setMembers([member2.UID()])
        self.failUnlessEqual(sortTuple(group.getGroupMembers()),
                             sortTuple([mem2_auth.getUserId(),
                                        mem_auth.getUserId()]))
        self.failUnlessEqual(mem2_grps.getGroupsForPrincipal(mem2_grps),
                             (group.getId(),))


class TestMembraneGroupManagerSelectedGroups(base.MembraneTestCase,
                                             MembraneGroupManagerTestBase):

    def addUser(self, obj=None):
        if obj is None:
            obj = self.portal
        self.member = _createObjectByType('AlternativeTestMember',
                                          obj, 'testuser')
        self.member.setUserName('testuser')
        self.member.setPassword('testpassword')
        self.member.setTitle('full name')
        self.member.reindexObject()

    def setUp(self):
        super(TestMembraneGroupManagerSelectedGroups, self).setUp()
        self.portal.pmm = self._makeOne('pmm')

    def testGroupMembership(self):
        self.createGroupAndUsers()
        group = self.portal.testgroup
        member = group.testuser  # We need acquisition to be correct
        mem_auth = IMembraneUserAuth(member)
        mem_grps = IMembraneUserGroups(member)
        member2 = self.member2
        mem2_auth = IMembraneUserAuth(member2)
        mem2_grps = IMembraneUserGroups(member2)
        self.failUnlessEqual(group.getGroupMembers(),
                             (mem_auth.getUserId(),))
        self.failUnlessEqual(mem_grps.getGroupsForPrincipal(mem_grps),
                             (group.getId(),))
        self.group.setMembers([member2.UID()])
        self.failUnlessEqual(sortTuple(group.getGroupMembers()),
                             sortTuple([mem2_auth.getUserId(),
                                        mem_auth.getUserId()]))
        self.failUnlessEqual(
            mem2_grps.getGroupsForPrincipal(mem2_grps), (group.getId(),))


class TestMembraneGroupManagerEnumeration(base.MembraneTestCase,
                                          MembraneGroupManagerTestBase):

    def setUp(self):
        super(TestMembraneGroupManagerEnumeration, self).setUp()
        self.portal.pmm = self._makeOne('pmm')

    def testEnumerateGroupsNoArgs(self):
        self.createGroupAndUsers()
        self.failUnlessEqual(len(self.portal.pmm.enumerateGroups()), 1)

    def testEnumerateGroupsByTitleNonexisting(self):
        self.createGroupAndUsers()
        enumgrps = self.portal.pmm.enumerateGroups
        self.failUnlessEqual(enumgrps(title='nonexisting'), ())
        self.failUnlessEqual(
            enumgrps(title='nonexisting', exact_match=True), ())

    def testEnumerateGroupsByTitle(self):
        self.createGroupAndUsers()
        enumgrps = self.portal.pmm.enumerateGroups
        self.failUnlessEqual(len(enumgrps(title=self.group.Title(),
                                          exact_match=True)), 1)
        self.failUnlessEqual(len(enumgrps(
            title=self.group.Title()[:len(self.group.Title()) - 1],
            exact_match=False)), 1)
        self.failUnlessEqual(len(enumgrps(title=self.group.Title(),
                                          exact_match=True,
                                          sort_on='title')), 1)
        self.failUnlessEqual(len(enumgrps(title=self.group.Title(),
                                          exact_match=True, sort_on='id')), 1)
        self.failUnlessEqual(len(enumgrps(title=self.group.Title(),
                                          exact_match=True, max_results=1)), 1)
        self.failUnlessEqual(len(enumgrps(title=self.group.Title(),
                                          exact_match=True, max_results=0)), 0)

    def testEnumerateGroupsByIdNonexisting(self):
        self.createGroupAndUsers()
        enumgrps = self.portal.pmm.enumerateGroups
        self.failUnlessEqual(enumgrps(id='nonexisting'), ())
        self.failUnlessEqual(enumgrps(id='nonexisting', exact_match=True), ())

    def testEnumerateGroupsById(self):
        self.createGroupAndUsers()
        enumgrps = self.portal.pmm.enumerateGroups
        self.failUnlessEqual(len(enumgrps(id=self.group.getGroupName(),
                                          exact_match=True)), 1)
        self.failUnlessEqual(len(enumgrps(
            id=self.group.getGroupName()[:len(self.group.getGroupName()) - 1],
            exact_match=False)), 1)
        self.failUnlessEqual(len(enumgrps(id=self.group.getGroupName(),
                                          exact_match=True,
                                          sort_on='title')), 1)
        self.failUnlessEqual(len(enumgrps(id=self.group.getGroupName(),
                                          exact_match=True, sort_on='id')), 1)
        self.failUnlessEqual(len(enumgrps(id=self.group.getGroupName(),
                                          exact_match=True, max_results=1)), 1)
        self.failUnlessEqual(len(enumgrps(id=self.group.getGroupName(),
                                          exact_match=True, max_results=0)), 0)

    def testEnumerateGroupsWithSimilarIds(self):
        self.createGroupAndUsers()
        """ ensure that enumerating groups while exact_match==True returns only
            exact matches for a given id
        """
        # add a new group with a similar id
        self.newgroup = _createObjectByType(
            'TestGroup', self.portal, 'testgroup-2')
        self.newgroup.setTitle('New Test group')
        self.newgroup.setDescription('A test group')
        self.newgroup.reindexObject()

        enumgrps = self.portal.pmm.enumerateGroups
        # only an exact match should be found when exact_match==True
        self.failUnlessEqual(len(enumgrps(id=self.group.getGroupName(),
                                          exact_match=True)), 1)
        self.failUnlessEqual(len(enumgrps(id=self.group.getGroupName(),
                                          exact_match=False)), 2)


class TestMembraneGroupIntrospection(base.MembraneTestCase,
                                     MembraneGroupManagerTestBase):

    # Test IGroupIntrospection

    def setUp(self):
        super(TestMembraneGroupIntrospection, self).setUp()
        self.portal.pmm = self._makeOne('pmm')

    def testGetGroupIdsNoGroups(self):
        self.failIf(self.portal.pmm.getGroupIds())

    def testGetGroupIds(self):
        self.addGroup(self.portal)
        groupids = self.portal.pmm.getGroupIds()
        self.failUnlessEqual(groupids, (self.group.getGroupId(),))

        group2 = _createObjectByType('TestGroup', self.portal, 'testgroup2')
        group2.setTitle('Test group 2')
        group2.reindexObject()
        groupids = self.portal.pmm.getGroupIds()
        self.failUnlessEqual(sortTuple(groupids),
                             sortTuple((self.group.getGroupId(),
                                        group2.getGroupId())))

    def testGroupMembersNoMembers(self):
        self.addGroup(self.portal)
        self.failIf(self.portal.pmm.getGroupMembers(self.group.getGroupId()))

    def testGroupMembers(self):
        self.createGroupAndUsers()
        pmm = self.portal.pmm
        self.failUnlessEqual(pmm.getGroupMembers(self.group.getGroupId()),
                             (self.userid,))

    def testGetGroupByIdNoGroup(self):
        g = self.portal.pmm.getGroupById('nonexisting')
        self.failIf(g)

    def testGetGroupById(self):
        from Products.PlonePAS.plugins.group import PloneGroup
        self.createGroupAndUsers()
        group = self.portal.pmm.getGroupById(self.group.getGroupId())
        self.failUnless(group)
        self.failUnless(isinstance(group, PloneGroup))

    def testGetGroupsNoGroups(self):
        self.failIf(self.portal.pmm.getGroups())

    def testGetGroups(self):
        self.createGroupAndUsers()
        groups = self.portal.pmm.getGroups()
        self.failUnless(groups)
        self.failUnlessEqual(len(groups), 1)
        self.failUnlessEqual(groups[0].getId(), self.group.getGroupId())
