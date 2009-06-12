from zope.interface import Interface
from zope.configuration import fields

from collective.portlet.ngcollection import NGCollectionMessageFactory as _

class IPortletTemplatesDirective(Interface):
    """Directive which registers a directory with templates for the given
    portlet type."""

    directory = fields.Path(
        title=u"Path to directory",
        required=True)

    interface = fields.GlobalInterface(
        title=_(u"Portlet type interface"),
        description=_(u"Should correspond to the public interface "
                      u"of the portlet assignment"),
        required=True)
