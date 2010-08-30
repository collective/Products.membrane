from Products.CMFCore import permissions as cmfcore_permissions

# Add a new member
ADD_PERMISSION = ADD_MEMBER_PERMISSION = cmfcore_permissions.AddPortalMember
# Add a MemberDataContainer
ADD_MDC_PERMISSION = 'Manage users'
# Register a new member, i.e. create a User object and enable a member
# to log in
REGISTER_PERMISSION = 'membrane: Register member'
# Disable a membership
DISABLE_PERMISSION = 'Manage users'
# Modify the member's ID -- should only happen during preregistration
EDIT_ID_PERMISSION = 'membrane: Edit member id'
# Modify the member's general properties
EDIT_PROPERTIES_PERMISSION = cmfcore_permissions.SetOwnProperties
# Change a member's password
EDIT_PASSWORD_PERMISSION = cmfcore_permissions.SetOwnPassword
# Change a member's roles and domains
EDIT_SECURITY_PERMISSION = 'Manage users'
# Appear in searches
VIEW_PERMISSION = cmfcore_permissions.View
# View a member's roles and domains
VIEW_SECURITY_PERMISSION = 'Manage users'
# View a member's public information
VIEW_PUBLIC_PERMISSION = VIEW_PERMISSION
# View a member's private information
VIEW_OTHER_PERMISSION = EDIT_PROPERTIES_PERMISSION
# Enable password mailing
MAIL_PASSWORD_PERMISSION = cmfcore_permissions.MailForgottenPassword

cmfcore_permissions.setDefaultRoles(REGISTER_PERMISSION, ('Manager',))
