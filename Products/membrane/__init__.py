import warnings

from AccessControl.Permissions import add_user_folders

from Products.CMFCore.utils import ContentInit, ToolInit
from Products.CMFCore.permissions import AddPortalContent as ADD_CONTENT_PERMISSION

warnings.warn(
    'Products.membrane - The Archetypes assumptions may be removed as'
    'soon as version 1.2', DeprecationWarning)
from Products.Archetypes import process_types
from Products.Archetypes.public import listTypes

from Products.PluggableAuthService import registerMultiPlugin

from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.GenericSetup import EXTENSION, profile_registry

from Products.membrane.config import PROJECTNAME
from Products.membrane.plugins import usermanager, groupmanager, \
     propertymanager, rolemanager, userfactory

registerMultiPlugin(usermanager.MembraneUserManager.meta_type)
registerMultiPlugin(groupmanager.MembraneGroupManager.meta_type)
registerMultiPlugin(propertymanager.MembranePropertyManager.meta_type)
registerMultiPlugin(rolemanager.MembraneRoleManager.meta_type)
registerMultiPlugin(userfactory.MembraneUserFactory.meta_type)


def initialize(context):

    import examples
    examples            # make pyflakes happy

    content_types, constructors, ftis = process_types(listTypes(PROJECTNAME),
                                                      PROJECTNAME)

    ContentInit(
        PROJECTNAME + ' Content',
        content_types = content_types,
        permission = ADD_CONTENT_PERMISSION,
        extra_constructors = constructors,
        fti = ftis,
        ).initialize(context)

    context.registerClass(usermanager.MembraneUserManager,
                          permission = add_user_folders,
                          constructors = (usermanager.manage_addMembraneUserManagerForm,
                                          usermanager.addMembraneUserManager),
                          visibility = None
                          )

    context.registerClass(groupmanager.MembraneGroupManager,
                          permission = add_user_folders,
                          constructors = (groupmanager.manage_addMembraneGroupManagerForm,
                                          groupmanager.addMembraneGroupManager),
                          visibility = None
                          )

    context.registerClass(propertymanager.MembranePropertyManager,
                          permission = add_user_folders,
                          constructors = (propertymanager.manage_addMembranePropertyManagerForm,
                                          propertymanager.addMembranePropertyManager),
                          visibility = None
                          )

    context.registerClass(rolemanager.MembraneRoleManager,
                          permission = add_user_folders,
                          constructors = (rolemanager.manage_addMembraneRoleManagerForm,
                                          rolemanager.addMembraneRoleManager),
                          visibility = None
                          )

    context.registerClass(userfactory.MembraneUserFactory,
                          permission = add_user_folders,
                          constructors = (userfactory.manage_addMembraneUserFactoryForm,
                                          userfactory.addMembraneUserFactory),
                          visibility = None
                          )

    from Products.membrane.tools import membrane
    ToolInit(PROJECTNAME+ ' Tool',
             tools = (membrane.MembraneTool, ),
             icon = 'tool.gif'
             ).initialize(context)

    profile_registry.registerProfile('default',
                                     'membrane',
                                     'Extension profile for membrane',
                                     'profiles/default',
                                     'membrane',
                                     EXTENSION,
                                     for_=IPloneSiteRoot)

    profile_registry.registerProfile('examples',
                                     'membrane sample content types',
                                     'Sample types extension profile for membrane',
                                     'profiles/examples',
                                     'membrane',
                                     EXTENSION,
                                     for_=IPloneSiteRoot)
