Products.membrane
=================

Overview
--------

membrane is a set of PluggableAuthService (PAS) plug-ins that allow
for the user-related behaviour and data (authentication, properties,
roles, groups, etc.) to be obtained from content within a Plone
site.  It does not actually provide a full member implementation, it
is intended to be a set of tools from which a full implementation
can be constructed.  It is meant to be flexible and pluggable, and
easy to adapt to different deployment scenarios. It is not meant to
be configured through-the-web-only, but to be adapted by filesystem
code.

membrane tries to take a step backwards and re-think some of the
Plone membership-handling. We have tried to make it as simple as
possible, so that grasping and extending it is simple. Hopefully,
simplicity should also make it easier to make sure it is secure.

For information about the "why?" of membrane, and some policies for
helping out, please see 'MANIFESTO.txt'.


Requirements
------------

- Zope 2.9.6
- Plone 2.5.2

Please see docs/INSTALL.txt for installation instructions.


---------
WARNING!!
---------

  Currently, a catalog is used to index the interfaces implemented by
  the objects in the portal.  However, interfaces are specified
  programmatically, either via Python code or ZCML.  Any time Zope is
  restarted, interfaces may have changed, and, if they have, the
  catalog will have become out of date.  Work is under way on a more
  robust interface lookup solution, but for now if you change the
  interfaces implemented on any membrane related type or object, you
  may need to explicitly reindex the 'object_implements' interface on
  the membrane_tool.

