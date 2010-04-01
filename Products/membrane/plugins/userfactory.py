from AccessControl import ClassSecurityInfo
from App.class_init import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from Products.PlonePAS.plugins.ufactory import PloneUserFactory, PloneUser

from Products.CMFCore.utils import getToolByName

from Products.membrane.interfaces.user import IMembraneUser
from Products.membrane.interfaces.plugins import IMembraneUserFactoryPlugin
from Products.membrane.config import TOOLNAME

from zope.interface import implements

manage_addMembraneUserFactoryForm = PageTemplateFile(
    '../www/MembraneUserFactoryForm', globals(),
    __name__='manage_addMembraneUserFactoryForm' )


def addMembraneUserFactory(dispatcher, id, title=None, REQUEST=None):
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

    def createUser(self, user_id, name):
        mbtool = getToolByName(self, TOOLNAME)
        # don't create the user unless it's a membrane-based user
        if mbtool.getUserObject(user_id=user_id, brain=True) is None:
            return None
        if not mbtool.case_sensitive_auth:
            user_id = mbtool.getOriginalUserIdCase(user_id)
        return MembraneUser(user_id, name)
    security.declarePrivate('createUser')

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
    def getProperty(self, name, default=_marker):
        """getProperty(self, name) => return property value or
        raise AttributeError
        """
        for sheet in self.getOrderedPropertySheets():
            if sheet.hasProperty(name):
                return sheet.getProperty(name)
        if default is _marker:
            raise AttributeError(name)
        else:
            return default
    security.declarePrivate("getProperty")

    def hasProperty(self, name):
        """hasProperty"""
        for sheet in self.getOrderedPropertySheets():
            if sheet.hasProperty(name):
                True
        return False
    security.declarePrivate("hasProperty")


InitializeClass(MembraneUser)
