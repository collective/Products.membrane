from Products.CMFCore.utils import getToolByName

def from_1_1_to_2_0(context):
    setup_tool = getToolByName(context, 'portal_setup')
    membrane_tool = getToolByName(context, 'membrane_tool')

    registry = setup_tool.getImportStepRegistry()

    # remove membrane-sitemanager import step
    if u'membrane-sitemanager' in registry.listSteps() and registry.getStepMetadata(u'membrane-sitemanager')['handler'] == 'Products.membrane.setuphandlers.initSiteManager' and registry.getStepMetadata(u'membrane-sitemanager')['invalid']:
        registry.unregisterStep(u'membrane-sitemanager')
        
    # if SearchableText is still a TextIndex, we need to drop the index, import the correct index, then reindex
    if 'SearchableText' in membrane_tool.Indexes and membrane_tool.Indexes['SearchableText'].meta_type == 'TextIndex':
        membrane_tool.delIndex('SearchableText')
        setup_tool.runImportStepFromProfile('profile-Products.membrane:default', 'membranetool')
        membrane_tool.reindexIndex('SearchableText', None)

