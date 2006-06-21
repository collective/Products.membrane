Membrane

  Membrane is a member data implementation to be used by
  deployers who don't want nor need community site functionality. It
  may later grow to handle all approaches to members-as-content in
  Plone. It is meant to be flexible and pluggable, and easy to adapt to
  different deployment scenarios. It is not meant to be configured
  through-the-web-only, but to be adapted by filesystem code. 
 
  Membrane tries to take a step backwards and re-think some of the
  Plone membership-handling. We have tried to make it as simple as
  possible, so that grasping and extending it is simple. Hopefully,
  simplicity should also make it easier to make sure it is secure. 
  
  It is the right tool for you if you often find you need to have
  content-objects as members/users, but CMFMember makes your head spin. 
 
  For information about the "why?" of Membrane, and some policies
  helping out, please see 'MANIFESTO.txt'.

---------
WARNING!!
---------

  Currently, a catalog is used to index the interfaces implemented by
  the objects in the portal.  However, interfaces are specified
  programmatically, either via Python code or ZCML.  Any time Zope is
  restarted, interfaces may have changed, and, if they have, the
  catalog will have become out of date.  Work is under way on a more
  robust interface lookup solution, but for now if you change the
  interfaces implemented on any Membrane related object, you should
  explicitly reindex the 'object_implements' interface on the
  membrane_tool.


Credits

  Membrane was created by Plone Solutions.

  Contact "Plone Solutions":http://www.plonesolutions.com/ for support options
  or sponsoring further development.

  Significant refactoring, componentization, and additional work by Rob
  Miller of The Open Planning Project.  (robm -at - openplans <dot> org)

How to test the development version

  The development version has basic functionality to enable you to
  understand the use cases and potential of Membrane better.
  
  Dependencies:
  
  - Zope 2.9.3 or greater

  - Plone 2.5 or greater

Quick Notes:

  membrane is installed via the use of a GenericSetup extension
  profile.  You can either choose the membrane profile to be installed
  at site creation time, or you can use the portal_setup interface.
  If using portal_setup, you'd browse to the properties tab and make
  the 'membrane' profile the active configuration.  Then you click on
  the 'import' tab and click the 'import all steps' button.

  You'll need to also install the 'membrane sample content types'
  extension profile to install the basic sample content types. These
  types are not intended to be used in production, as the use of
  cleartext passwords should clearly indicate.

  Go to a folder somewhere, or simply the root of your Plone site, and
  add a SimpleMember. Enter the username and password, and preferably a
  full name to see that the decorator plugin works.

  Now, try to log in as the user you just added. The full name should
  also show up wherever Plone usually displays full name.
