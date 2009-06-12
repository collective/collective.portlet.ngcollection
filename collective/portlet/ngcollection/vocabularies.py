from zope import component
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.interface import implements
from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from collective.portlet.ngcollection.manager import getPortletTemplateManagers
from collective.portlet.ngcollection.interfaces import IPortletTemplateManager
from collective.portlet.ngcollection import NGCollectionMessageFactory as _

class PortletTemplates(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        # TODO: how to make this vocabulary work while object is being
        #       created, container but not portlet assignment is as
        #       context at that moment
        items = []
        for manager in getPortletTemplateManagers(context):
            items.extend([SimpleTerm(value, value, title)
                for value, title in manager.getTemplatesForVocab()])
        return SimpleVocabulary(items)
