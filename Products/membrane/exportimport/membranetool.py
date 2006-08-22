from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.ZCatalog.exportimport import ZCatalogXMLAdapter
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects

from Products.membrane.interfaces import IMembraneTool
from Products.membrane.interfaces import ICategoryMapper
from Products.membrane.config import ACTIVE_STATUS_CATEGORY
from Products.membrane.utils import generateCategorySetIdForType

class MembraneToolXMLAdapter(ZCatalogXMLAdapter):
    """
    Mode im- and exporter for MembraneTool.
    """
    __used_for__ = IMembraneTool

    name = 'membrane_tool'

    def _exportNode(self):
        """
        Export the settings as a DOM node.
        """
        node = ZCatalogXMLAdapter._exportNode(self)
        node.appendChild(self._extractMembraneTypes())

        self._logger.info('MembraneTool settings exported.')
        return node

    def _importNode(self, node):
        """
        Import the settings from the DOM node.
        """
        ZCatalogXMLAdapter._importNode(self, node)

        if self.environ.shouldPurge():
            self._purgeMembraneTypes()

        self._initMembraneTypes(node)
        self._logger.info('MembraneTool settings imported.')

    def _extractMembraneTypes(self):
        cat_map = ICategoryMapper(self.context)
        fragment = self._doc.createDocumentFragment()

        for mtype in self.context.listMembraneTypes():
            # extract the membrane types
            child = self._doc.createElement('membrane-type')
            child.setAttribute('name', mtype)

            # extract the "active" w/f states for the type
            cat_set = generateCategorySetIdForType(mtype)
            states = cat_map.listCategoryValues(cat_set,
                                                ACTIVE_STATUS_CATEGORY)
            for state in states:
                sub = self._doc.createElement('active-workflow-state')
                sub.setAttribute('name', state)
                child.appendChild(sub)

            fragment.appendChild(child)
        return fragment

    def _initMembraneTypes(self, node):
        for child in node.childNodes:
            if child.nodeName != 'membrane-type':
                continue

            # register membrane types
            mtype = str(child.getAttribute('name'))
            if mtype and mtype not in self.context.listMembraneTypes():
                self.context.registerMembraneType(mtype)

            # register "active" workflow states
            cat_map = ICategoryMapper(self.context)
            states = []
            for sub in child.childNodes:
                if sub.nodeName != 'active-workflow-state':
                    continue
                state = str(sub.getAttribute('name'))
                if state and state not in states:
                    states.append(state)
            if states:
                cat_set = generateCategorySetIdForType(mtype)
                cat_map.replaceCategoryValues(cat_set,
                                              ACTIVE_STATUS_CATEGORY,
                                              states)

    def _purgeMembraneTypes(self):
        for mtype in self.context.listMembraneTypes():
            self.context.unregisterMembraneType(mtype)


def importMembraneTool(context):
    """
    Import membrane_tool configuration.
    """
    site = context.getSite()
    tool = getToolByName(site, 'membrane_tool')

    importObjects(tool, '', context)

def exportMembraneTool(context):
    """
    Export membrane_tool configuration.
    """
    site = context.getSite()
    tool = getToolByName(site, 'membrane_tool', None)
    if tool is None:
        logger = context.getLogger("membranetool")
        logger.info("Nothing to export.")
        return

    exportObjects(tool, '', context)
