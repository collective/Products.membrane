from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.PlonePAS.plugins.ufactory import PloneUserFactory, PloneUser

from Products.Archetypes.config import REFERENCE_CATALOG, UUID_ATTR
from Products.CMFCore.utils import getToolByName

from Products.membrane.interfaces import IMembraneUser
from Products.membrane.interfaces import IMembraneUserFactoryPlugin
from Products.membrane.config import TOOLNAME

from zope.interface import implements

manage_addMembraneUserFactoryForm = PageTemplateFile(
    '../www/MembraneUserFactoryForm', globals(), __name__='manage_addMembraneUserFactoryForm' )

def addMembraneUserFactory( dispatcher, id, title=None, REQUEST=None ):
    """ Add a MembraneUserFactory to a Pluggable Auth Service. """

    pmm = MembraneUserFactory(id, title)
    dispatcher._setObject(pmm.getId(), pmm)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
                                '%s/manage_workspace'
                                '?manage_tabs_message='
                                'MembraneUserFactory+added.'
                            % dispatcher.absolute_url())


class MembraneUserFactory(PloneUserFactory):

    security = ClassSecurityInfo()
    meta_type = 'Membrane User Factory'

    implements(IMembraneUserFactoryPlugin)

    def __init__(self, id, title=''):
        self.id = id
        self.title = title or self.meta_type

    security.declarePrivate('createUser')
    def createUser(self, user_id, name):
        mbtool = getToolByName(self, TOOLNAME)
        # don't create the user unless it's a membrane-based user
        if mbtool.getUserAuthProvider(name, brain=True) is None:
            return None
        if not mbtool.case_sensitive_auth:
            user_id = mbtool.getOriginalUserIdCase(user_id)
        return MembraneUser(user_id, name)

InitializeClass(MembraneUserFactory)


_marker = ['INVALID_VALUE']
class MembraneUser(PloneUser):

    security = ClassSecurityInfo()

    implements(IMembraneUser)

    #
    # Implementing getProperty for convenience
    # This is also implemented by the wrapper
    # from memberdata...
    #
    security.declarePrivate("getProperty")
    def getProperty(self, name, default=_marker):
        """getProperty(self, name) => return property value or
        raise AttributeError
        """
        for sheet in self.getOrderedPropertySheets():
            if sheet.hasProperty(name):
                return sheet.getProperty(name)
        if default is _marker:
            raise AttributeError, name
        else:
            return default

    security.declarePrivate("hasProperty")
    def hasProperty(self, name):
        """hasProperty"""
        for sheet in self.getOrderedPropertySheets():
            if sheet.hasProperty(name):
                True
        return False

    # Helper method for referenceable interface implementation
    def _getMembraneObject(self):
        uid = self.UID()
        if uid is not None:
            refcatalog = getToolByName(self, REFERENCE_CATALOG)
            return refcatalog.lookupObject(uid)

    #
    # IReferenceable - for backwards compatibility with CMFMember
    #
    def getRefs(self, relationship=None):
        """get all the referenced objects for this object"""
        return self._getMembraneObject().getRefs(relationship)

    def getBRefs(self, relationship=None):
        """get all the back referenced objects for this object"""
        return self._getMembraneObject().getBRefs(relationship)

    def getReferences(self, relationship=None):
        """ alias for getRefs """
        return self.getRefs(relationship)

    def getBackReferences(self, relationship=None):
        """ alias for getBRefs """
        return self.getBRefs(relationship)

    def getReferenceImpl(self, relationship=None):
        """ returns the references as objects for this object """
        return self._getMembraneObject().getReferenceImpl(relationship)

    def getBackReferenceImpl(self, relationship=None):
        """ returns the back references as objects for this object """
        return self._getMembraneObject().getBackReferenceImpl(relationship)

    def UID(self):
        """ Unique ID """
        if not hasattr(self, UUID_ATTR):
            setattr(self, UUID_ATTR, self.getProperty('uid', None))
        return getattr(self, UUID_ATTR)

    def reference_url(self):
        """like absoluteURL, but return a link to the object with this UID"""
        return self._getMembraneObject().reference_url()

    def hasRelationshipTo(self, target, relationship=None):
        """test is a relationship exists between objects"""
        return self._getMembraneObject().hasRelationshipTo(target, relationship)

    def addReference(self, target, relationship=None, **kwargs):
        """add a reference to target. kwargs are metadata"""
        return self._getMembraneObject().addReference(target, relationship, **kwargs)

    def deleteReference(self, target, relationship=None):
        """delete a ref to target"""
        return self._getMembraneObject().deleteReference(target, relationship)

    def deleteReferences(self, relationship=None):
        """delete all references from this object"""
        return self._getMembraneObject().deleteReferences(relationship)

    def getRelationships(self):
        """list all the relationship types this object has refs for"""
        return self._getMembraneObject().getRelationships()

InitializeClass(MembraneUser)
