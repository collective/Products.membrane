from Products.Archetypes.ReferenceEngine import Reference


class UserRelatedRelation(Reference):
    """
    Relationship object btn user auth providers and any related providers
    (e.g. properties, groups, roles, etc.)
    """
    relationship = "User Related Relation"
