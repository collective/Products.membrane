from zope.component import getUtilitiesFor

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile

from Products.membrane.interfaces import IUserAdder


class FormControllerView(BrowserView):
    """
    A (super) quick-n-dirty prototype of what a FormController-like
    abstract view class might look like.  This is NOT ultimately
    intended to live w/in the membrane product, but this is such an
    initial prototype that I don't think it should be used by anybody
    else.  Consider yourself warned...  :-)
    """
    def __call__(self):
        if not self.request.get('submitted'):
            return self.template()
        errors = self._validate()
        if errors:
            return self.template(errors=errors)
        errors = self._control()
        if errors:
            return self.template(errors=errors)
        return self.template()

    def _validate(self):
        """
        performs validation and returns an errors dictionary
        """
        return {}

    def _control(self):
        """
        performs the actions after a successful validation, returns
        errors dictionary
        """
        return {}


class MembraneTypesView(FormControllerView):
    """
    ZMI page for managing the membrane types.
    """
    template = ZopeTwoPageTemplateFile('membrane_types.pt')

    def _control(self):
        """
        Specify the membrane types.
        """
        new_mem_types = set(self.request.get('membrane_types', []))
        old_mem_types = set(self.context.listMembraneTypes())
        for portal_type in old_mem_types.difference(new_mem_types):
            self.context.unregisterMembraneType(portal_type)
        for portal_type in new_mem_types.difference(old_mem_types):
            self.context.registerMembraneType(portal_type)

        user_adder = self.request.get('user_adder', self.context.user_adder)
        self.context.user_adder = user_adder

    def availableAdders(self):
        """
        Return the set of available IUserAdder utilities.
        """
        adders = getUtilitiesFor(IUserAdder)
        return [adder[0] for adder in adders]
