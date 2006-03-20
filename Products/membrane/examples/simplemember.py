from AccessControl import ClassSecurityInfo, AuthEncoding
from Acquisition import aq_chain, aq_inner

from zope.interface import implements

from Products.CMFCore.utils import getToolByName

from Products.Archetypes.public import BaseSchema, Schema, BaseContent, \
     StringField, StringWidget, registerType

from Products.membrane.interfaces import IUserAuthProvider
from Products.membrane.interfaces import IPropertiesProvider
from Products.membrane.config import PROJECTNAME, TOOLNAME


SimpleSchema = BaseSchema + Schema((
    StringField('userName',
                languageIndependent = 1,
                widget = StringWidget(description = "Username for a person.")
               ),
    StringField('password',
                languageIndependent = 1,
                widget = StringWidget(description = "Password.")
               ),
    StringField('fullname',
                languageIndependent = 1,
                #schemata='userinfo',
                user_property=True,
                widget = StringWidget(description = "Full name.")
               ),
    ))


class SimpleMember(BaseContent):
    """A simple member archetype"""
    schema = SimpleSchema
    _at_rename_after_creation = True

    security = ClassSecurityInfo()

    implements(IUserAuthProvider, IPropertiesProvider)

    #
    # IUserAuthProvider implementation
    # 'getUserName' is auto-generated
    #
    def verifyCredentials(self, credentials):
        login = credentials.get('login')
        password = credentials.get('password')
        if login == self.getUserName() and password == self.getPassword():
            return True
        else:
            return False

    #
    # IUseSchemataProperties implementation
    #
    #security.declarePrivate( 'getUserPropertySchemata' )
    #def getUserPropertySchemata(self):
    #    return ['userinfo']

    #
    # For IGroupsPlugin implementation/Group mixin
    # - should probably use an interface
    #
    #security.declarePrivate( 'getGroupRelationships' )
    #def getGroupRelationships(self):
    #    return ['participatesInProject']


registerType(SimpleMember, PROJECTNAME)
