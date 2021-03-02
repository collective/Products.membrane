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

Since version 5.0: Plone 5.2.
Since version 4.0: Plone 5.1.
Version 3.0: Plone 4.3 or 5.0.  We only test with Python 2.7.
For older Plone versions, please use Products.membrane branch 2.1.x.

If you create a membrane type based on Archetypes, then you must first install Archetypes, then membrane.
This is needed so new users are properly indexed by the membrane tool.
The canonical implementation of such a membrane type for Plone is ``Products.remember``.

If you create a membrane type based on dexterity on Plone 4 or Plone 5.0, then you must add ``collective.indexing`` to the eggs of your Plone instance. On Plone 5.1 you should no longer add ``collective.indexing`` to the eggs.
The canonical implementation of such a membrane type for Plone is ``dexterity.membrane``.


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
