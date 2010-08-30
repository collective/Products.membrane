Creating membrane aware content
===============================

.. module:: Products.membrane.interfaces

It is not difficult to extend content types to act as (parts of) users or
groups with membrane. The only thing that is needed is to make sure that
your content is adaptable to one of the membrane interfaces. You can either
make your content type implement the interfaces directly, or register separate
adapters.

Base adapter
------------

All adapters must implement the :py:obj:`IMembraneUserObject` interface. This interface
specifies methods to get the userid and login name for a user object. Membrane needs
this to be able to identify the relevant user.

.. code-black:: python

   from plone.dexterity.content import Item
   from Products.membrane.interfaces import IMembraneUserAuth
   from plone.uuid.interfaces import IUUID

   class MyUser(Item):
       pass

   class BaseUserObject(object):
       def __init__(self, context):
           self.context=context

       def getUserId(self):
           return IUUID(self.context, None)

       def getUserName(self):
           return self.context.login

.. autointerface:: IMembraneUserObject


Authentication
---------------

If you want a user to be able to login in a site you must add authentication support
to your user content type. This is handled through the :py:obj:`IMembraneUserAuth`
interface. Below is an example for a very basic authentication handler which users
a plaintext password attribute. This uses the `BaseUserObject` class shown above.

.. code-black:: python

   from plone.dexterity.content import Item
   from five import grok
   from Products.membrane.interfaces import IMembraneUserAuth
   from plone.uuid.interfaces import IUUID

   class MyUser(Item):
       pass

   class MyUserAuthentication(grok.Adapter, BaseUserObject):
       grok.context(MyUser)
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
