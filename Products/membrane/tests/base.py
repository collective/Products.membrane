from AccessControl.SecurityManagement import newSecurityManager
from Products import membrane
from Products.CMFPlone.tests.PloneTestCase import portal_name
from Products.CMFPlone.tests.PloneTestCase import setupPloneSite
from Products.CMFPlone.tests.PloneTestCase import USELAYER
from Products.CMFPlone.utils import _createObjectByType
from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.membrane import examples
from Products.membrane import tests
from Products.membrane.config import TOOLNAME
from Products.membrane.tests import dummy
from Products.PloneTestCase import layer
from Products.PloneTestCase import ptc
from Products.PloneTestCase.setup import _placefulSetUp
from Testing import ZopeTestCase

import transaction as txn


orig_initialize = membrane.initialize


def initialize(context):
    orig_initialize(context)
    examples.initialize(context)
    tests.initialize(context)

# TODO We are patching the installation here, and should find a better way to
# do this
membrane.initialize = initialize

# Make the boring stuff load quietly
ZopeTestCase.installProduct('membrane')

SiteLayer = layer.PloneSite


ptc.setupPloneSite()


def addUser(obj, username='testuser', title='full name'):
    member = _createObjectByType('TestMember', obj, username)
    member.setUserName(username)
    member.setPassword('testpassword')
    # Title is mapped to the user property fullname using
    # user_property='fullname'
    member.setTitle(title)
    member.setMobilePhone('555-1212')
    member.reindexObject()
    return member


class MembraneProfilesLayer(SiteLayer):

    @classmethod
    def getPortal(cls):
        app = ZopeTestCase.app()
        portal = app._getOb(portal_name)
        _placefulSetUp(portal)
        return portal

    @classmethod
    def setUp(cls):
        fiveconfigure.debug_mode = True
        zcml.load_config('testing.zcml', package=tests)
        fiveconfigure.debug_mode = False

        ZopeTestCase.installPackage('collective.indexing')
        setupPloneSite(extension_profiles=('Products.membrane:default',
                                           'Products.membrane.tests:test'))
        SiteLayer.setUp()
        portal = cls.getPortal()
        mbtool = getattr(portal, TOOLNAME)
        mbtool.registerMembraneType(dummy.TestMember.portal_type)
        mbtool.registerMembraneType(dummy.AlternativeTestMember.portal_type)
        mbtool.registerMembraneType(dummy.TestGroup.portal_type)
        txn.commit()

    @classmethod
    def tearDown(cls):
        pass

    @classmethod
    def testSetUp(cls):
        pass

    @classmethod
    def testTearDown(cls):
        pass


class AddUserLayer(MembraneProfilesLayer):

    @classmethod
    def setUp(cls):
        portal = cls.getPortal()
        app = portal.getPhysicalRoot()
        user = app.acl_users.getUser('portal_owner')
        user = user.__of__(app.acl_users)
        newSecurityManager(app, user)
        addUser(portal)
        txn.commit()

    @classmethod
    def tearDown(cls):
        pass

    @classmethod
    def testSetUp(cls):
        pass

    @classmethod
    def testTearDown(cls):
        pass


class MembraneTestCase(ptc.PloneTestCase):

    if USELAYER:
        layer = MembraneProfilesLayer

    class Session(dict):

        def set(self, key, value):
            self[key] = value

    def _setup(self):
        ptc.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()

    def addGroup(self, obj=None):
        if obj is None:
            obj = self.portal
        self.group = _createObjectByType('TestGroup', obj, 'testgroup')
        self.group.setTitle('Test group')
        self.group.setDescription('A test group')
        self.group.reindexObject()

    def addUser(self, obj=None, username='testuser', title='full name'):
        if obj is None:
            obj = self.portal
        self.member = addUser(obj, username, title)
        self.userid = self.member.getId()


class MembraneUserTestCase(MembraneTestCase):

    layer = AddUserLayer

    def afterSetUp(self):
        self.member = self.portal.testuser
        self.loginAsPortalOwner()
