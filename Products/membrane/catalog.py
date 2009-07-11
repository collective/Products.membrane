from zope.interface import Interface
from zope.interface import implements
from zope import component

from Acquisition import aq_inner
from Acquisition import aq_parent

from Products.CMFCore.utils import getToolByName

from plone.indexer import indexer
from collective.indexing.interfaces import IIndexQueueProcessor

from Products.membrane.interfaces.user import IMembraneUserObject
from Products.membrane.interfaces.group import IGroup
from Products.membrane.interfaces import membrane_tool

@indexer(Interface, membrane_tool.IMembraneTool)
def object_implements(obj):
    return tuple(
        id_ for id_, iface in
        component.getUtilitiesFor(
            membrane_tool.IMembraneQueryableInterface)
        if iface.getTaggedValue('interface').providedBy(obj)
        or iface.providedBy(obj))


@indexer(Interface, membrane_tool.IMembraneTool)
def getUserName(obj):
    obj = IMembraneUserObject(obj, None)
    if obj is None:
        return None
    return obj.getUserName()


@indexer(Interface, membrane_tool.IMembraneTool)
def getUserId(obj):
    obj = IMembraneUserObject(obj, None)
    if obj is None:
        return None
    return obj.getUserId()


@indexer(Interface, membrane_tool.IMembraneTool)
def getGroupId(obj):
    obj = IGroup(obj, None)
    if obj is None:
        return None
    return obj.getGroupId()


@indexer(Interface, membrane_tool.IMembraneTool)
def getParentPath(obj):
    """
    Returns the physical path of the parent object.
    """
    return '/'.join(aq_parent(aq_inner(obj)).getPhysicalPath())


class MembraneCatalogProcessor(object):
    """Catalog processor to update user objects in the membrane tool.

    This index queue processor acts as a utility that is used by 
    `collective.indexing`_. It makes sure all catalog operations
    on objects providing `IMembraneUserObject` are also reflected
    in the `membrane_tool` catalog.
    """
    implements(IIndexQueueProcessor)

    def index(self, obj, attributes=[]):
        if IMembraneUserObject(obj, None) is None:
            return
        mbtool = getToolByName(obj, "membrane_tool", None)
        if mbtool is not None:
            mbtool.indexObject(obj, attributes or [])

    def reindex(self, obj, attributes=[]):
        if IMembraneUserObject(obj, None) is None:
            return
        mbtool = getToolByName(obj, 'membrane_tool', None)
        if mbtool is not None:
            mbtool.reindexObject(obj, attributes or [])

    def unindex(self, obj):
        if IMembraneUserObject(obj, None) is None:
            return
        mbtool = getToolByName(obj, 'membrane_tool', None)
        if mbtool is not None:
            mbtool.unindexObject(obj)

    def begin(self):
        pass

    def commit(self):
        pass

    def abort(self):
        pass

