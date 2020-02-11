# coding=utf-8
import six


if six.PY2:
    from Products.membrane.tests.at.dummy import AlternativeTestMember  # noqa: E501, F401
    from Products.membrane.tests.at.dummy import TestAlternatePropertyProvider  # noqa: E501, F401
    from Products.membrane.tests.at.dummy import TestGroup  # noqa: F401
    from Products.membrane.tests.at.dummy import TestMember  # noqa: F401
    from Products.membrane.tests.at.dummy import TestPropertyProvider  # noqa: E501, F401
else:
    from Products.membrane.tests.dx.dummy import AlternativeTestMember  # noqa: E501, F401
    from Products.membrane.tests.dx.dummy import TestAlternatePropertyProvider  # noqa: E501, F401
    from Products.membrane.tests.dx.dummy import TestGroup  # noqa: F401
    from Products.membrane.tests.dx.dummy import TestMember  # noqa: F401
    from Products.membrane.tests.dx.dummy import TestPropertyProvider  # noqa: E501, F401
