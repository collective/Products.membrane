from Acquisition import aq_base
from persistent.mapping import PersistentMapping

from zope.annotation.interfaces import IAnnotations

from Products.CMFCore.utils import getToolByName
from Products.GenericSetup.ZCatalog.exportimport import ZCatalogXMLAdapter
from Products.GenericSetup.utils import exportObjects
from Products.GenericSetup.utils import importObjects

from Products.membrane.interfaces import IMembraneTool
from Products.membrane.config import QIM_ANNOT_KEY


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
        node.appendChild(self._extractQueryIndexMap())
        node.appendChild(self._extractUserAdder())

        self._logger.info('MembraneTool settings exported.')
        return node

    def _importNode(self, node):
        """
        Import the settings from the DOM node.
        """
        ZCatalogXMLAdapter._importNode(self, node)

        if self.environ.shouldPurge():
            self._purgeMembraneTypes()
            self._purgeQueryIndexMap()

        self._initMembraneTypes(node)
        self._initQueryIndexMap(node)
        self._initUserAdder(node)
        self._logger.info('MembraneTool settings imported.')

    def _extractMembraneTypes(self):
        fragment = self._doc.createDocumentFragment()

        for mtype in self.context.listMembraneTypes():
            # extract the membrane types
            child = self._doc.createElement('membrane-type')
            child.setAttribute('name', mtype)

            fragment.appendChild(child)
        return fragment

    def _extractQueryIndexMap(self):
        fragment = self._doc.createDocumentFragment()
        annots = IAnnotations(self.context)
        query_index_map = annots.get(QIM_ANNOT_KEY)
        if query_index_map is not None:
            child = self._doc.createElement('query_index_map')

            for key, value in query_index_map.items():
                sub = self._doc.createElement('index')
                sub.setAttribute('name', key)
                inner = self._doc.createTextNode(value)
                sub.appendChild(inner)
                child.appendChild(sub)

            fragment.appendChild(child)
        return fragment

    def _extractUserAdder(self):
        fragment = self._doc.createDocumentFragment()
        user_adder = getattr(aq_base(self.context), 'user_adder', None)
        if user_adder:
            child = self._doc.createElement('user-adder')
            child.setAttribute('name', user_adder)
            fragment.appendChild(child)
        return fragment

    def _initMembraneTypes(self, node):
        for child in node.childNodes:
            if child.nodeName != 'membrane-type':
                continue

            # register membrane types if they're not listed in the
            # catalog map or in the status map
            mtype = str(child.getAttribute('name'))
            if mtype and \
                   mtype not in self.context.listMembraneTypes():
                self.context.registerMembraneType(mtype)

    def _initQueryIndexMap(self, node):
        for child in node.childNodes:
            if child.nodeName != 'query_index_map':
                continue

            annots = IAnnotations(self.context)
            query_index_map = annots.get(QIM_ANNOT_KEY)
            if query_index_map is None:
                query_index_map = annots[QIM_ANNOT_KEY] = PersistentMapping()

            for sub in child.childNodes:
                if sub.nodeName != 'index':
                    continue
                key = str(sub.getAttribute('name'))
                value = ''
                for inner in sub.childNodes:
                    if inner.nodeType == inner.TEXT_NODE:
                        value = str(inner.nodeValue)
                        break
                if value:
                    query_index_map[key] = value

    def _initUserAdder(self, node):
        for child in node.childNodes:
            if child.nodeName != 'user-adder':
                continue
            user_adder = child.getAttribute('name')
            self.context.user_adder = user_adder

    def _purgeMembraneTypes(self):
        for mtype in self.context.listMembraneTypes():
            self.context.unregisterMembraneType(mtype)

    def _purgeQueryIndexMap(self):
        annots = IAnnotations(self.context)
        if annots.get(QIM_ANNOT_KEY) is not None:
            del annots[QIM_ANNOT_KEY]


def importMembraneTool(context):
    """
    Import membrane_tool configuration.
    """
    site = context.getSite()
    tool = getToolByName(site, 'membrane_tool', None)

    if tool is not None:
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
