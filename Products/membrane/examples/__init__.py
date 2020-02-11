# -*- coding: utf-8 -*-
import six


def initialize(context):
    if not six.PY2:
        return
    from Products.Archetypes import process_types
    from Products.Archetypes.public import listTypes
    from Products.CMFCore.permissions import AddPortalContent as ADD_CONTENT_PERMISSION  # noqa: 5401
    from Products.CMFCore.utils import ContentInit
    from Products.membrane.config import PROJECTNAME
    from Products.membrane.examples import simplegroup  # noqa: F401
    from Products.membrane.examples import simplemember  # noqa: F401

    content_types, constructors, ftis = process_types(
        listTypes(PROJECTNAME), PROJECTNAME)

    ContentInit(
        PROJECTNAME + ' Content',
        content_types=content_types,
        permission=ADD_CONTENT_PERMISSION,
        extra_constructors=constructors,
        fti=ftis,
    ).initialize(context)
