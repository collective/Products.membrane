Overview
========

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

For announcement, help, or to keep up with development discussions,
see the poorly named "remember" list:

http://www.openplans.org/projects/remember/lists/remember/

Vision
======

membrane is a product to enable users as content in Plone sites, in
collaboration with PlonePAS. The name gives you an idea of the intended
complexity and amount of code.

membrane won't be the only member handling product in your site, instead it
should enable us to easily plug in products that enable default Plone member
policy, or more exotic setups in corporate intranets. This means that to get
the default Plone behaviour you will need something else in addition to
membrane.


Requirements
============

- Plone 3.3 or better


WARNING!!
=========

  Currently, a catalog is used to index the interfaces implemented by
  the objects in the portal.  However, interfaces are specified
  programmatically, either via Python code or ZCML.  Any time Zope is
  restarted, interfaces may have changed, and, if they have, the
  catalog will have become out of date.  Work is under way on a more
  robust interface lookup solution, but for now if you change the
  interfaces implemented on any membrane related type or object, you
  may need to explicitly reindex the 'object_implements' interface on
  the membrane_tool.

