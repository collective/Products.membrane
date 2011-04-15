from AccessControl.SecurityManagement import newSecurityManager
import transaction as txn
from Testing import ZopeTestCase

from Products.Five import zcml
from Products.Five import fiveconfigure

from Products.CMFPlone.utils import _createObjectByType

from Products.PloneTestCase.setup import _placefulSetUp
from Products.PloneTestCase import layer
from Products.CMFPlone.tests.PloneTestCase import (portal_name,
                                                   USELAYER,
                                                   setupPloneSite)

# TODO Patch the installation here, should find a better way to do
# this
from Products import membrane
from Products.membrane import tests
from Products.membrane import examples

orig_initialize = membrane.initialize


def initialize(context):
    orig_initialize(context)
    examples.initialize(context)
    tests.initialize(context)

membrane.initialize = initialize

# Make the boring stuff load quietly
ZopeTestCase.installProduct('membrane')

SiteLayer = layer.PloneSite

try:
    from Products.PlonePAS.tests.base import (
        TestCase as PlonePASTestCase)
    PlonePASTestCase  # pyflakes
except ImportError:
    # BBB Plone 3
    from Products.PlonePAS.tests.PlonePASTestCase import (
        PlonePASTestCase)

from Products.membrane.tests import dummy
from Products.membrane.config import TOOLNAME


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


class MembraneTestCase(PlonePASTestCase):

    if USELAYER:
        layer = MembraneProfilesLayer

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PlonePASTestCase._setup(self)
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
