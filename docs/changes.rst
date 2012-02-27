Changelog
=========

2.1.3 (2012-02-27)
------------------

- Bugfix. The catalog processor called by collective.indexing doesn't unindex users
  from the membrane_tool. [jcbrand]


2.1.2 (2011-12-16)
------------------

- Fixed problem that occurs after upgrading the SearchableText index
  of the membrane_tool, which happens after upgrading to membrane 2.0
  or to Plone 4: the membrane_tool catalog would be empty.  Now we
  refresh the membrane_tool catalog when we upgrade the index.  If
  this has already happened to you, it should work to just go to the
  membrane_tool, then the Advanced tab, and click on 'Update Catalog.'
  [maurits]


2.1.1, 29 November, 2011
------------------------

- Made the getUserObject method private for better security.
  Use ``portal_membership.getMemberInfo(user_id)`` when you need something
  similar in a skin script or template.  Or ``@@pas_member`` on Plone 4.0+.
  Problem reported by Richard Mitchell, thanks!
  [maurits]


2.1.0, 15 November, 2011
------------------------

- Restored compatibility with collective.indexing 1.8 or earlier.
  [maurits]

- Added a normalizer lexicon that does case normalization.
  getUserId and getUserName are the only places where case sensitivity
  makes sense in searches. Title and SearchableText needs normalization.
  [tesdal]

- Fixed a bug where only user objects and not groups would be
  indexed if collective.indexing could be imported.
  Also added a missing check of of portal_type against listMembraneTypes
  before performing re/un/indexing.
  [tesdal]

- Add compatibility with collective.indexing 2.0a1.
  [hannosch]


2.0.2, 26 April, 2011
---------------------

- In the unindexObject patch when collective.indexing is used, when
  the object is no membrane object, try to unwrap it, as it may be a
  PathWrapper around the object, wrapped by collective.indexing.
  Without this, stale brains may be left in the membrane_tool catalog,
  at least when using dexterity objects as members.
  [maurits]

- Changed the test setup so the tests also work on Plone 4.1, next to
  Plone 4.0 and 3.3.
  [maurits]


2.0.1, March 11, 2011
---------------------

- Add an upgrade step to handle cases where meta_type for the SearchableText
  step has been rewritten to "Broken Because Product is Gone" which would cause
  the 2.0 upgrade step to not migrate the index.
  [cah190]


2.0, March 9, 2011
------------------

- Add an upgrade step to migrate from membrane 1.1 releases.
  [cah190]


2.0b2, September 20, 2010
-------------------------

- Fix username/userid error in the PAS users plugin: doChangeUser takes a
  userid as parameter, not a username.
  [wichert]


2.0b1, August 31, 2010
----------------------

- Apply the collective.indexing profile when it is available.
  [maurits]

- Removed the dependency on collective.indexing >= 1.1 as it was added
  to allow non-Archetypes content to be used, but it is giving
  problems with some normal Archetypes content.  If you add
  collective.indexing to your buildout yourself, we still use it and
  register our own catalog queue processor with it.  Please install it
  in your Plone Site yourself.
  [maurits]

- Bug fix: when asked to return a maximum number of users, convert
  max_results to an integer.
  [maurits]

- Remove deprecated workflow state category set status mapper. This should be
  implemented using a workflow based test in an IMembraneUserAuth
  implementation, not in the core Membrane code.
  [rossp, wichert]

- Fix performance problems with the object_implements index using
  marker interfaces registered as utilities. [rossp]

  The object_implements index used to use the ZCA to find out not only
  what interfaces an object provided, but what interfaces an object
  could be adapted to out to the second order (adapting two objects).
  Providing this degree of magical awareness proved to be a large
  performance problem.

- Remove BBB method to migrate the list of membrane types from
  archetypes_tool to membrane_tool. [rossp]

- Use ZCTextIndex for the SearchableText index. This fixes problems with
  unicode data.
  [wichert]

- Modify the property plugin to handle property adapters returning
  None and pure dictionaries. Even though the PAS interface does not allow
  it this is common behaviour.
  [wichert]

- Use collective.indexing to update the membrane_tool catalog data. This
  allows non-Archetypes content to be used.
  [wichert]

- Refactor PAS plugins to only depend on the generic interfaces. This
  removes the dependency on Archetypes.
  [wichert]

- Use `plone.indexer`_ to manager indexable attribuets.
  [wichert]

- Update GenericSetup import handler to gracefully handle sites without a
  membrane_tool installed.
  [wichert]

- Improve package description, RESTify the changelog.
  [wichert]

- Move GenericSetup profile and step registration to zcml.
  [wichert]

.. _plone.indexer: http://pypi.python.org/pypi/plone.indexer


1.1b5 Released March 23, 2009
-----------------------------

- Fix git based release problem, now using setuptools-git
  [hannosch]



1.1b4 Released March 20, 2009
-----------------------------

- Tested with Plone 3.0-3.2 [rossp]

- Add a warning about upcoming changes to object_implements
  [rossp]

- Deprecate the category mapper support [rossp]

- Deprecate AT assumptions [rossp]

- Provide the offending login name when more than one match
  [witsch]

- Fix AttributeError bug when the search term is None [claytron]

- Distinguish btn substring matches and case-insensitive matches
  for userid and username when supporting case-insensitive logins
  [rafrombrc]
  
- Only use the membrane user factory plug-in for users for whom
  membrane provides authentication.
  [rafrombrc]


1.1b3 Released July 23, 2008
----------------------------

- Fix issue with retrieving unnamed user adders.
  [witsch]

- Remove counter again as the membrane tool inherits from Plone's
  catalog tool, which already has support for a counter.  Keep the
  test and caching helper, though. :)
  [witsch]


1.1b2 Released July 22, 2008
----------------------------

- Add a counter to the membrane tool which can be used as a cache key as
  well as a convenience helper for quickly memoizing adapters and tools.
  [witsch]

- Have rolemanager and groupmanager search for exact userids.
  [mj]


1.1b1 Released May 22, 2008
---------------------------

- Initial egg release.
  [rafrombrc]


- removed deprecation messages in Plone 3.0 (Zope 2.10): Import of
  zope.app.annotation turned into zope.annotation 
  [jensens]


1.0b1
-----

- Introduced IUserChanger interface to separate the password
  changing from the user addition and deletion portions of
  IUserManagement. [rafrombrc]

- Completed general implementation of roles, groups, properties
  plugins. [rafrombrc, jhammel, rmarianski]


0.3
---

- Added a IUserManagement interface (from PlonePAS) to the
  usermanager.  It will be available to implementations that
  provide the corresponding IMembraneUserManagement interface
  directly or through adaptation.  This allows thing like
  PasswordResetTool to work.

- Renamed package to 'membrane' from 'Membrane' to reflect current
  standard python naming conventions. [rafrombrc]

- Major refactoring to use Zope 3 component engine to glue
  together all the pieces.  Mix-ins have been converted to
  adapters, providers are defined by implementation of specific
  interfaces. [rafrombrc]


0.2-alpha
---------

- Made Title in membrane_tool a ZCTextIndex too, so that
  enumerateGroups() of membrane_groups works without exact_match.

- getUserName and getUserId indexes in membrane_tool are now of
  type ZCTextIndex, allowing us to do exact_match=False queries in
  MembraneUserManager.enumerateUsers.

  PluggableAuthService.enumerateUsers recommends treating id and
  login as "contains" search tokens, but with our text index we
  can only do "starts with" searches.  However, that's much better
  than returning () for every call that has "exact_match=False".
  [dpunktnpunkt]

