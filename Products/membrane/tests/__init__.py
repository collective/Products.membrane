# -*- coding: utf-8 -*-
"""
Initialising code for Products.membrane.tests product.
See also testing.zcml and the profile directory.
"""
import six


def initialize(context):

    if not six.PY2:
        return

    from Products.Archetypes.public import listTypes
    from Products.Archetypes.public import process_types
    from Products.CMFCore.permissions import AddPortalContent
    from Products.CMFCore.utils import ContentInit
    from Products.membrane.config import PROJECTNAME

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME), PROJECTNAME)

    ContentInit(
        PROJECTNAME + ' Content',
        content_types=content_types,
        permission=AddPortalContent,
        extra_constructors=constructors,
        fti=ftis,
    ).initialize(context)
