from zope.interface import implementedBy
from zope import component

from collective.portlet.ngcollection import manager
from collective.portlet.ngcollection.interfaces import IPortletTemplateManager

def handler(directory, interface, package):
    gsm = component.getGlobalSiteManager()

    # check if a portlet template manager already exists
    factories = set(factory for name, factory in gsm.adapters.lookupAll(
        (interface,), IPortletTemplateManager))

    # if factory is available on the interface bases of the interface we
    # discard it and register a new manager specialized to the interface
    base_factories = set(factory for name, factory in gsm.adapters.lookupAll(
        (implementedBy(interface.__bases__),), IPortletTemplateManager))

    dirkey = manager.getDirKey(package, directory)
    try:
        factory = factories.difference(base_factories).pop()
    except KeyError:
        factory = manager.PortletTemplateManagerFactory()
        component.provideAdapter(
            factory, (interface,), IPortletTemplateManager, name=dirkey)

    factory(interface).registerDirectory(directory, package)

   
def portletTemplatesDirective(_context, directory, interface):
    package = _context.package
    _context.action(
        discriminator = ('portletTemplates', directory, interface, package),
        callable = handler,
        args = (directory, interface, package ))
