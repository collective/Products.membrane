from Testing import ZopeTestCase
#from Products.membrane import examples
from Products.membrane.tests import dummy
from Products.membrane.config import TOOLNAME

from Products.GenericSetup import EXTENSION, profile_registry

from Products.CMFPlone.utils import _createObjectByType
from Products.CMFPlone.interfaces import IPloneSiteRoot

# Make the boring stuff load quietly
ZopeTestCase.installProduct('membrane')

try:
    from Products.PlonePAS.tests.PlonePASTestCase import PlonePASTestCase
except ImportError:
    from Products.PlonePAS.tests.PloneTestCase \
            import PloneTestCase as PlonePASTestCase

from Products.membrane.interfaces import IMembraneUserAuth

profile_registry.registerProfile('test',
                                 'membrane',
                                 'Testing extension profile for membrane',
                                 'profiles/test',
                                 'membrane',
                                 EXTENSION,
                                 for_=IPloneSiteRoot)

class MembraneTestCase(PlonePASTestCase):

    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PlonePASTestCase._setup(self)
        setup_tool = self.portal.portal_setup
        setup_tool.setImportContext('profile-membrane:default')
        setup_tool.runAllImportSteps()
        setup_tool.setImportContext('profile-membrane:test')
        setup_tool.runAllImportSteps()
        mbtool = getattr(self.portal, TOOLNAME)
        mbtool.registerMembraneType(dummy.TestMember.portal_type)
        mbtool.registerMembraneType(dummy.AlternativeTestMember.portal_type)
        mbtool.registerMembraneType(dummy.TestGroup.portal_type)
                                       
        self.app.REQUEST['SESSION'] = self.Session()

    def addUser(self, obj=None):
        if obj is None:
            obj = self.portal
        self.member = _createObjectByType('TestMember', obj, 'testuser')
        self.member.setUserName('testuser')
        self.member.setPassword('testpassword')
        self.member.setFullname('full name')
        self.member.reindexObject()
        self.userid = IMembraneUserAuth(self.member).getUserId()

    def addGroup(self, obj=None):
        if obj is None:
            obj = self.portal
        self.group = _createObjectByType('TestGroup', obj, 'testgroup')
        self.group.setTitle('Test group')
        self.group.reindexObject()
