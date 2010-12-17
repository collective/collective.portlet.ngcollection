import os

from zope.interface import implements
from zope.component import getGlobalSiteManager

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.portlet.ngcollection.interfaces import IPortletTemplateManager

from Products.CMFCore.FSMetadata import FSMetadata

class PortletTemplateManagerFactory(object):
    def __init__(self):
        self.manager = PortletTemplateManager()

    def __call__(self, layer):
        return self.manager

class PortletTemplateManager(object):
    implements(IPortletTemplateManager)

    def __init__(self):
        self._templates = {}

    def registerDirectory(self, directory):
        """See interface"""
        for filename in os.listdir(directory):
            if len(filename) > 3 and filename.endswith('.pt'):
                path = "%s/%s" % (directory, filename)
                metadata = FSMetadata(path)
                metadata.read()
                properties = metadata.getProperties()
                title = properties.get('title', filename[:-3])
                self._templates[path] = (title.decode('utf-8'),
                                         ViewPageTemplateFile(path))

    def unregisterDirectory(self, directory):
        """See interface"""
        for path, template in self.templates.items():
            del self._templates[path]

    def hasTemplate(self, path):
        """See interface"""
        return self._templates.has_key(path)

    def getTemplate(self, path, default=None):
        """See interface"""
        if self.hasTemplate(path):
            return self._templates[path][1]
        else:
            return default

    def getTemplatesForVocab(self):
        """See interface"""
        return [(path, item[0]) for path, item in self._templates.items()]


def getPortletTemplateManagers(obj):
    """Yields found for obj adapters to IPortletTemplateManager.
    
    obj could ba an object as well as an interface.
    """
    gsm = getGlobalSiteManager()
    for name, adapter in gsm.getAdapters((obj,), IPortletTemplateManager):
        yield adapter
