from Products.membrane.interfaces import IMembraneTool
from Products.GenericSetup.utils import XMLAdapterBase
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects
from Products.CMFCore.utils import getToolByName

class MembraneToolXMLAdapter(XMLAdapterBase):
    """
    Mode im- and exporter for MembraneTool.
    """
    __used_for__ = IMembraneTool

    def _exportNode(self):
        """
        Export the settings as a DOM node.
        """
        node = self._getObjectNode('object')
        node.appendChild(self._extractMembraneTypes())

        self._logger.info('MembraneTool settings exported.')
        return node

    def _importNode(self, node):
        """
        Import the settings from the DOM node.
        """
        if self.environ.shouldPurge():
            self._purgeMembraneTypes()

        self._initMembraneTypes(node)
        self._logger.info('MembraneTool settings imported.')

    def _extractMembraneTypes(self):
        fragment = self._doc.createDocumentFragment()
        for mtype in self.context.listMembraneTypes():
            child = self._doc.createElement('membrane-type')
            child.setAttribute('name', mtype)
            fragment.appendChild(child)
        return fragment

    def _initMembraneTypes(self, node):
        for child in node.childNodes:
            if child.nodeName != 'membrane-type':
                continue

            mtype = str(child.getAttribute('name'))
            if mtype and mtype not in self.context.listMembraneTypes():
                self.context.registerMembraneType(mtype)

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
