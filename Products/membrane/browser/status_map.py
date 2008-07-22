from Products.Five import BrowserView

from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.utils import generateCategorySetIdForType
from Products.membrane.utils import getAllWFStatesForType
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

class StatusMapView(BrowserView):
    """
    ZMI page for managing membrane type "active" status mappings.
    """

    template = ZopeTwoPageTemplateFile('status_map.pt')

    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.cat_map = ICategoryMapper(context)

    def __call__(self):
        types = self.request.get('types', [])
        for portal_type in types:
            states = self.request.get("%s_active_states" % portal_type, [])
            cat_set = generateCategorySetIdForType(portal_type)
            self.cat_map.replaceCategoryValues(cat_set,
                                               ACTIVE_STATUS_CATEGORY,
                                               states)
        return self.template()

    def allStatesForType(self, portal_type):
        return getAllWFStatesForType(self.context, portal_type)

    def activeStatesForType(self, portal_type):
        cat_set = generateCategorySetIdForType(portal_type)
        return self.cat_map.listCategoryValues(cat_set,
                                               ACTIVE_STATUS_CATEGORY)
