import sys

from AccessControl import ClassSecurityInfo
from zope.interface import implements

from Products.PlonePAS.sheet import MutablePropertySheet

from Products.membrane.interfaces.user import IMembraneUserProperties
from Products.membrane.at.userrelated import UserRelated


class Properties(UserRelated):
    """
    Adapts from IPropertiesProvider to IMembraneUserProperties,
    returns as properties all AT schema fields marked as
    user_property.  If user_property is a string then that string will
    be used as the property name (in case it is desirable that the
    field name and property differ).
    """
    security = ClassSecurityInfo()

    implements(IMembraneUserProperties)

    illegal_property_ids = ['id']

    def _isPropertyField(self, field):
        """
        Returns 1 if field is a property field, to satisfy
        'filterFields' requirement.
        """
        if hasattr(field, 'user_property') and field.user_property \
           and field.getName() not in self.illegal_property_ids:
            return 1
    security.declarePrivate('_isPropertyField')

    #
    #   IMutablePropertiesPlugin implementation
    #
    def getPropertiesForUser(self, user, request=None):
        """
        Find the fields that have true value for 'user_property' and
        return the values, using user_property value as the property
        name if it is a string.
        """
        properties = {}
        schema = self.context.Schema()
        for field in schema.filterFields(self._isPropertyField):
            # use the accessor if available:
            accessor = field.getAccessor(self.context)
            if accessor is not None:
                value = accessor()
            else:
                value = field.get(self.context)
            user_prop = field.user_property
            prop_name = (isinstance(user_prop, str) and user_prop) or \
                        field.getName()
            properties[prop_name] = value is not None \
                                    and value or ''
        return MutablePropertySheet(self.context.getId(),
                                    **properties)
    security.declarePrivate('getPropertiesForUser')

    def setPropertiesForUser(self, user, propertysheet):
        """
        Find any user property schema fields that match with properties
        on the property sheet and set the field values accordingly.  Have
        to work around impedance diffs btn AT fields and property sheet
        properties.
        """
        properties = dict(propertysheet.propertyItems())
        schema = self.context.Schema()
        for field in schema.filterFields(self._isPropertyField):
            user_prop = field.user_property
            prop_name = (isinstance(user_prop, str) and user_prop) or \
                         field.getName()
            if prop_name in properties:
                value = properties[prop_name]
                try:
                    mutator = field.getMutator(self.context)
                    if mutator is not None:  # skip ComputedFields
                        mutator(value)
                except:  # XXX: investigate which exceptions we care about
                    # relatively safe b/c we're still raising the exception
                    e, m = sys.exc_info()[0:2]
                    msg = """
                    Exception raised when writing %s property:
                    %s: %s
                    """ % (prop_name, e, m)
                    raise ValueError(msg)

    def deleteUser(self, user_id):
        """
        XXX: TODO
        """
        pass


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
        return MutablePropertySheet(self.context.getId(),
                                    **properties)
    security.declarePrivate('getPropertiesForUser')

    def setPropertiesForUser(self, user, propertysheet):
        """
        Find any schema fields from the user property schemata that
        are on the property sheet and set the field values accordingly.
        """
        properties = dict(propertysheet.propertyItems())
        schemata = self.context.Schemata()
        for ups in self.context.getUserPropertySchemata():
            schema = schemata.get(ups, None)
            if schema is not None:
                for field in schema.fields():
                    fieldname = field.getName()
                    if fieldname in properties:
                        value = properties[fieldname]
                    try:
                        field.getMutator(self.context)(value)
                    except:  # XXX: investigate which exceptions we care about
                        # relatively safe b/c we're still raising the exception
                        e, m = sys.exc_info()[0:2]
                        msg = """
                        Exception raised when writing %s property:
                        %s: %s
                        """ % (fieldname, e, m)
                        raise ValueError(msg)

    def deleteUser(self, user_id):
        """
        XXX: TODO
        """
        pass
