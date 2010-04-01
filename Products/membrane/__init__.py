from AccessControl.Permissions import add_user_folders

from Products.CMFCore.utils import ToolInit

from Products.membrane.config import PROJECTNAME
from Products.membrane.plugins import usermanager, groupmanager, \
     propertymanager, rolemanager, userfactory

from Products.PluggableAuthService import registerMultiPlugin

registerMultiPlugin(usermanager.MembraneUserManager.meta_type)
registerMultiPlugin(groupmanager.MembraneGroupManager.meta_type)
registerMultiPlugin(propertymanager.MembranePropertyManager.meta_type)
registerMultiPlugin(rolemanager.MembraneRoleManager.meta_type)
registerMultiPlugin(userfactory.MembraneUserFactory.meta_type)


def initialize(context):

    context.registerClass(
        usermanager.MembraneUserManager,
        permission=add_user_folders,
        constructors=(usermanager.manage_addMembraneUserManagerForm,
                      usermanager.addMembraneUserManager),
        visibility=None
                          )

    context.registerClass(
        groupmanager.MembraneGroupManager,
        permission=add_user_folders,
        constructors=(groupmanager.manage_addMembraneGroupManagerForm,
                      groupmanager.addMembraneGroupManager),
        visibility=None
        )

    context.registerClass(
        propertymanager.MembranePropertyManager,
        permission=add_user_folders,
        constructors=(propertymanager.manage_addMembranePropertyManagerForm,
                      propertymanager.addMembranePropertyManager),
        visibility=None
        )

    context.registerClass(
        rolemanager.MembraneRoleManager,
        permission=add_user_folders,
        constructors=(rolemanager.manage_addMembraneRoleManagerForm,
                      rolemanager.addMembraneRoleManager),
        visibility=None
        )

    context.registerClass(
        userfactory.MembraneUserFactory,
        permission=add_user_folders,
        constructors=(userfactory.manage_addMembraneUserFactoryForm,
                      userfactory.addMembraneUserFactory),
        visibility=None
        )

    from Products.membrane.tools import membrane
    ToolInit(PROJECTNAME + ' Tool',
             tools=(membrane.MembraneTool, ),
             icon='tool.gif'
             ).initialize(context)
