Creating membrane aware content
===============================

.. module:: Products.membrane.interfaces

It is not difficult to extend content types to act as (parts of) users or
groups with membrane. The only thing that is needed is to make sure that
your content is adaptable to one of the membrane interfaces. You can either
make your content type implement the interfaces directly, or register separate
adapters.

Basic user
----------

To expose a content object as a user you must implement the
:py:obj:`IMembraneUserObject` interface. This is a very minimal interface
which membrane uses to find the userid and the login name for a user.
This is a minimal implementation:

.. code-block:: python

   from plone.dexterity.content import Item
   from Products.membrane.interfaces import IMembraneUserAuth
   from plone.uuid.interfaces import IUUID

   class MyContent(Item):
       pass

   class MyContentUser(object):
       def __init__(self, context):
           self.context=context

       def getUserId(self):
           return IUUID(self.context, None)

       def getUserName(self):
           return self.context.login

.. autointerface:: IMembraneUserObject

.. note::

   If you use adapters to implement the membrane interfaces, and you also
   implement one of the other membrane interfaces you do not need to register
   the IMembraneUserObject adapter separately since all other interfaces are
   derived from it. It is recommended to use a MyContentUser-like class as base
   class for all adapters to make sure the getUserId() and getUserName()
   implementations are not duplicated.


Authentication
---------------

If you want a user to be able to login in a site you must add authentication support
to your user content type. This is handled through the :py:obj:`IMembraneUserAuth`
interface. Below is an example for a very basic authentication handler which uses
a plaintext password attribute.

The example below demonstrates a very simple authentication adapter. It uses
the MyContentUser class shown earlier, and uses `five.grok
<http://pypi.python.org/pypi/five.grok>`_ to create the adapter so you do not
need to write any ZCML.

.. code-block:: python

   from plone.dexterity.content import Item
   from five import grok
   from Products.membrane.interfaces import IMembraneUserAuth
   from plone.uuid.interfaces import IUUID

   class MyContent(Item):
       pass

   class MyUserAuthentication(grok.Adapter, MyContentUser):
       grok.context(Content)
       grok.implements(IMembraneUserAuth)

       def authenticateCredentials(self, credentials):
           if self.context.password==credentials["password"]:
               return (self.getUserId(), self.getUserName())
           return None

.. autointerface:: IMembraneUserAuth



User properties
---------------

Every user in a Plone site will be able to use the standard user property support
as provided by PluggableAuthService. Often you want to be able to use a content
object to manage properties for a user, for example to be able to use standard
edit screens to manage certain properties. You can do this by via the
:py:obj:`IMembraneUserProperties` interface.

.. autointerface:: IMembraneUserProperties
