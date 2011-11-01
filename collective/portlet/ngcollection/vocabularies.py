from zope.interface import implements
from zope.component import queryUtility
from zope.component.interfaces import IFactory
from zope.app.container.interfaces import IAdding

try:
    from zope.schema.interfaces import IVocabularyFactory
except ImportError:
    from zope.app.schema.vocabulary import IVocabularyFactory

from zope.schema.vocabulary import SimpleTerm, SimpleVocabulary

from collective.portlet.ngcollection.manager import getPortletTemplateManagers


class PortletTemplates(object):

    implements(IVocabularyFactory)

    def __call__(self, context):
        # we are on an adding form
        if IAdding.providedBy(context):
            # quick and dirty way to have a context on adding form
            # is there some right solution for this?
            factory_name = context.request.getURL().split('/')[-1]
            if factory_name:
                factory = queryUtility(IFactory, name=factory_name)
                if factory is not None:
                    try:
                        context = factory()
                    except Exception, e:
                        # no luck, perhaps factory needs some arguments
                        pass

        items = []
        for manager in getPortletTemplateManagers(context):
            items.extend([SimpleTerm(value, value, title)
                for value, title in manager.getTemplatesForVocab()])
        return SimpleVocabulary(items)
