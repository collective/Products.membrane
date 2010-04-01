PROJECTNAME = 'membrane'
TOOLNAME = 'membrane_tool'

GLOBALS = globals()

FILTERED_ROLES = ('Anonymous', 'Authenticated')

QIM_ANNOT_KEY = 'Products.membrane.query_index_map'

try:
    import collective.indexing
    collective.indexing  # pyflakes
except ImportError:
    USE_COLLECTIVE_INDEXING = False
else:
    USE_COLLECTIVE_INDEXING = True
