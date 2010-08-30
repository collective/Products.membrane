Frequently asked questions
==========================

How can I implement membership approval?
----------------------------------------

A common task is to make site membership conditional, for example to only
allow paying users to login. This can easily be implemented by modifying
your :py:obj:Products.membrane.interfaces.IMembraneUserAuth` implementation
to perform extra checks.

The most common approach is to use a custom workflow to manage this. As an
example we can use a simple workflow with two states:

* `unpaid`: initial workflow state, indicates that the user has not paid his
  subscription.
* `paid`: workflow state for users with a valid payment.

You can check the workflow state in your `authenticateCredentials` method. Here
is a basic example:

.. code-block:: python

  from Products.CMFCore.utils import getToolByName

  def authenticateCredentials(self, credentials):
      # Check the workflow to see if the user paid his membership
      wt = getToolByName(self, 'portal_workflow')
      review_state = wt.getInfoFor(self, 'review_state')
      if review_state=='unpaid':
          return None

      # The user paid, so do the normal authentication
      if credentials['password']==self.password:
          return (self.UID, self.login)
      else:
          return None

