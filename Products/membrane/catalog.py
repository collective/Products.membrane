from Acquisition import aq_inner
from Acquisition import aq_parent
from zope.interface import Interface
from zope.interface import providedBy
from zope.app.apidoc.component import getRequiredAdapters
from Products.membrane.interfaces import IUserAuthentication
from Products.membrane.interfaces import IMembraneUserObject
from Products.membrane.interfaces import IGroup
from Products.membrane.interfaces import IMembraneTool
from zope.component import getGlobalSiteManager
from plone.indexer import indexer

@indexer(Interface, IMembraneTool)
def object_implements(obj):
    def getDottedName(iface):
        # have to do this b/c z2->z3 bridges don't play well
        # w/ __identifier__
        return "%s.%s" % (iface.__module__, iface.__name__)
    
    try:
        gsm = getGlobalSiteManager()
        extendors = gsm.adapters._v_lookup._extendors

        def lookup(components, req, result, i, l):
            if i < l:
                for required in req.keys():
                    comps = components.get(required)
                    if comps:
                        lookup(comps, req, result, i+1, l)
            else:
                for iface,a in components.items():
                    if [x for x in a.keys() if not x]: # Filter named adapters, unnamed got u''
                        result[iface] = None

        res = {}
        for iface in providedBy(obj).flattened():
            res[iface] = None
            # Also look for adapters to parent interfaces __sro__
            #for parent in iface.__sro__:
            #    res[parent] = None

        tmp = {}

        adapters = gsm.adapters._adapters
        for i in range(len(adapters)):
            order = adapters[i]
            lookup(order, res, tmp, 0, i)

        res.update(tmp)
        return [getDottedName(h) for h in res.keys()]

    except (AttributeError,IndexError,TypeError,ValueError):
        # Fallback in case there is a problem with the fast version

        res = {}
        for iface in providedBy(obj).flattened():
            res[getDottedName(iface)] = iface
        direct = res.values()
        for iface in direct:
            for adapter_reg in getRequiredAdapters(iface):
                # avoid checking 'named' adapters
                if getattr(adapter_reg, 'name', None):
                    continue
                adaptable_iface = adapter_reg.provided
                adapting_from = [i for i in adapter_reg.required if i is not None]
                skip = False
                if len(adapting_from) > 1:
                    # only support multiadapters that this object can satisfy alone
                    for i in adapting_from:
                        if not i in direct:
                            skip = True
                if adaptable_iface is not None and not skip:
                    res[getDottedName(adaptable_iface)] = adaptable_iface
        return res.keys()




@indexer(Interface, IMembraneTool)
def getUserName(obj):
    obj = IUserAuthentication(obj, None)
    if obj is None:
        return None
    return obj.getUserName()



@indexer(Interface, IMembraneTool)
def getUserId(obj):
    obj = IMembraneUserObject(obj, None)
    if obj is None:
        return None
    return obj.getUserId()



@indexer(Interface, IMembraneTool)
def getGroupId(obj):
    obj = IGroup(obj, None)
    if obj is None:
        return None
    return obj.getGroupId()



@indexer(Interface, IMembraneTool)
def getParentPath(obj):
    """
    Returns the physical path of the parent object.
    """
    return '/'.join(aq_parent(aq_inner(obj)).getPhysicalPath())


