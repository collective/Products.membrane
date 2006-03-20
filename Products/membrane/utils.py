from config import STATUS_CATEGORY_SET

def generateCategorySetIdForType(portal_type):
    return "_".join((portal_type, STATUS_CATEGORY_SET))
