from zope.interface import Interface


class IUserAdder(Interface):
    """
    An interface providing a means of adding a user to a Plone site.
    """
    def addUser(login, password):
        """
        Adds a user with specified id and username.  Any keyword
        arguments are set as properties on the user, if possible.
        """
