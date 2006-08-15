from AccessControl import ClassSecurityInfo
from zope.interface import implements

from Products.CMFCore.utils import getToolByName

from Products.membrane.interfaces import IMembraneUserProperties
from userrelated import UserRelated


class Properties(UserRelated):
    """
    Adapts from IPropertiesProvider to IMembraneUserProperties, returns
    as properties all AT schema fields marked as user_property.  If
    user_property is a string then that string will be used as the property
    name (in case it is desirable that the field name and property differ).
    """
    security = ClassSecurityInfo()

    implements(IMembraneUserProperties)

    #
    #   IPropertiesPlugin implementation
    #
    security.declarePrivate('getPropertiesForUser')
    def getPropertiesForUser(self, user, request=None):
        illegal_ids = ['id']
        properties = {}
        schema = self.context.Schema()
        for field in schema.fields():
            if hasattr(field, 'user_property') and \
                   field.getName() not in illegal_ids:
                value = field.get(self.context)
                user_prop = field.user_property
                prop_name = (isinstance(user_prop, str) and user_prop) or \
                            field.getName()
                properties[prop_name] = value is not None \
                                              and value or ''
        return properties


class SchemataProperties(UserRelated):
    """
    Adapts from ISchemataPropertiesProvider to
    IMembraneUserProperties.  Gets properties from the specified
    schematas
    """
    security = ClassSecurityInfo()

    implements(IMembraneUserProperties)

    #
    #   IPropertiesPlugin implementation
    #
    security.declarePrivate( 'getPropertiesForUser' )
    def getPropertiesForUser(self, user, request=None ):
        illegal_ids = ['id']
        properties = {}
        schemata = self.context.Schemata()
        for ups in self.context.getUserPropertySchemata():
            schema = schemata.get(ups, None)
            if schema is not None:
                for field in schema.fields():
                    if field.getName() not in illegal_ids:
                        value = field.get(self.context)
                        properties[field.getName()] = \
                                value is not None and value or ''
        return properties
