from zope.interface import implements

from Products.CMFCore.utils import getToolByName

from Products.membrane.interfaces.user import IMembraneUserObject


class UserIdProvider(object):
    """
    Adapts from SimpleMember to IMembraneUserObject.  Uses a massaged path to
    the member object instead of the UID.
    """
    implements(IMembraneUserObject)

    def __init__(self, context):
        self.context = context

    def getUserId(self):
        purl = getToolByName(self.context, 'portal_url')
        rel_url = purl.getRelativeUrl(self.context)
        return rel_url.replace('/', '-')

    def getUserName(self):
        return self.context.getUserName()
