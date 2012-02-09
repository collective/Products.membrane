from zope.interface import Interface
from zope.interface import implements
from zope import component

from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent

from Products.CMFCore.utils import getToolByName

from plone.indexer import indexer

from Products.membrane.interfaces.user import IMembraneUserObject
from Products.membrane.interfaces.group import IGroup
from Products.membrane.interfaces import membrane_tool
from Products.membrane.config import USE_COLLECTIVE_INDEXING
if USE_COLLECTIVE_INDEXING:
    from collective.indexing.interfaces import IIndexQueueProcessor


@indexer(Interface, membrane_tool.IMembraneTool)
def object_implements(obj):
    """Catalog indexer which returns a list of all interfaces implementing
    :py:obj:`IMembraneQueryableInterface`. This boils down to the list of
    supported membrane behaviours for an object..
    """
    return tuple(
        id_ for id_, iface in
        component.getUtilitiesFor(
            membrane_tool.IMembraneQueryableInterface)
        if iface(obj, None) is not None)


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
    `collective.indexing`_. It makes sure all catalog operations on objects
    providing :py:obj:`IMembraneUserObject` are also reflected
    in the `membrane_tool` catalog.
    """
    if USE_COLLECTIVE_INDEXING:
        implements(IIndexQueueProcessor)

    def index(self, obj, attributes=[]):
        if IMembraneUserObject(obj, None) is None and IGroup(obj, None) is None:
            return
        mbtool = getToolByName(obj, "membrane_tool", None)
        if mbtool is not None:
            # Verify that the portal_type is part of the catalog map
            if getattr(obj, 'portal_type') in mbtool.listMembraneTypes():
                mbtool.indexObject(obj, attributes or [])

    def reindex(self, obj, attributes=[]):
        if IMembraneUserObject(obj, None) is None and IGroup(obj, None) is None:
            return
        mbtool = getToolByName(obj, 'membrane_tool', None)
        if mbtool is not None:
            if getattr(obj, 'portal_type') in mbtool.listMembraneTypes():
                mbtool.reindexObject(obj, attributes or [])

    def unindex(self, obj):
        if aq_base(obj).__class__.__name__ == 'PathWrapper':
            # Could be a PathWrapper object from collective.indexing.
            obj = obj.context

        if IMembraneUserObject(obj, None) is None and IGroup(obj, None) is None:
            return
        mbtool = getToolByName(obj, 'membrane_tool', None)
        if mbtool is not None:
            if getattr(obj, 'portal_type') in mbtool.listMembraneTypes():
                mbtool.unindexObject(obj)

    def begin(self):
        pass

    def commit(self):
        pass

    def abort(self):
        pass
