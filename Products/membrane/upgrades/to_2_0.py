# coding=utf-8
from Acquisition import aq_get
from logging import getLogger
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.UnicodeSplitter.splitter import I18NNormalizer
from Products.CMFPlone.UnicodeSplitter.splitter import Splitter
from Products.ZCTextIndex.interfaces import IZCTextIndex
from Products.ZCTextIndex.ZCTextIndex import PLexicon


logger = getLogger(__name__)


def update_lexicon(context):
    mbtool = getToolByName(context, "membrane_tool")
    if "plone_lexicon" not in mbtool:
        mbtool.plone_lexicon = PLexicon(
            "plone_lexicon", "", Splitter(), I18NNormalizer(),
        )
    for index_id in (
        "getGroupId",
        "getUserId",
        "getUserName",
        "SearchableText",
        "Title",
    ):
        index = mbtool.Indexes.get(index_id)
        if IZCTextIndex.providedBy(index):
            index.lexicon_id = "plone_lexicon"
            logger.info("Reindex membrane catalog index: %r", index_id)
            mbtool.manage_clearIndex([index_id])
            mbtool.reindexIndex(index_id, aq_get(context, "REQUEST", None))
