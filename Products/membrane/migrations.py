import logging

from Products.CMFCore.utils import getToolByName

logger = logging.getLogger('Products.membrane')


def _upgradeSearchableTextIndex(context, setup_tool, membrane_tool):
    # Delete the old index, import membranetool so it will be
    # recreated.  Then we should reindex it, but since the import
    # clears all other indexes as well, we refresh the complete
    # catalog.  Note that this only updates existing items in the
    # catalog and does not go hunting for new members.
    membrane_tool.delIndex('SearchableText')
    setup_tool.runImportStepFromProfile('profile-Products.membrane:default',
                                        'membranetool')
    #membrane_tool.reindexIndex('SearchableText', None)
    logger.info("Refreshing membrane_tool catalog...")
    membrane_tool.refreshCatalog()


def from_1_1_to_2_0(context):
    membrane_tool = getToolByName(context, 'membrane_tool')
    setup_tool = getToolByName(context, 'portal_setup')
    registry = setup_tool.getImportStepRegistry()

    # remove membrane-sitemanager import step
    if u'membrane-sitemanager' in registry.listSteps():
        handler = registry.getStepMetadata(u'membrane-sitemanager')['handler']
        if handler == 'Products.membrane.setuphandlers.initSiteManager':
            if registry.getStepMetadata(u'membrane-sitemanager')['invalid']:
                registry.unregisterStep(u'membrane-sitemanager')

    # if SearchableText is still a TextIndex, we need to drop the
    # index, import the correct index, then reindex
    if 'SearchableText' in membrane_tool.Indexes:
        if membrane_tool.Indexes['SearchableText'].meta_type == 'TextIndex':
            _upgradeSearchableTextIndex(context, setup_tool, membrane_tool)


def from_2_0_to_2_0_1(context):
    membrane_tool = getToolByName(context, 'membrane_tool')
    setup_tool = getToolByName(context, 'portal_setup')

    # in newer Plones the meta_type is rewritten to "Broken Because
    # Product is Gone" so we test and upgrade the index, if necessary
    if 'SearchableText' in membrane_tool.Indexes:
        meta_type = membrane_tool.Indexes['SearchableText'].meta_type
        if meta_type == 'Broken Because Product is Gone':
            _upgradeSearchableTextIndex(context, setup_tool, membrane_tool)
