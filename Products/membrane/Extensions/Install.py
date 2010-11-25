PLUGIN_IDS = [
    'membrane_users',
    'membrane_groups',
    'membrane_roles',
    'membrane_properties',
    'membrane_user_factory',
    ]

def uninstall(self, portal, reinstall=False):
    portal.acl_users.manage_delObjects(PLUGIN_IDS)
    portal_setup = portal.portal_setup
    toolset = portal_setup.getToolsetRegistry()
    del toolset._required['membrane_tool']
    portal_setup.getImportStepRegistry().unregisterStep('membranetool')
    portal_setup.getExportStepRegistry().unregisterStep('membranetool')
    portal.manage_delObjects(['membrane_tool'])
    portal_setup._p_changed = True
