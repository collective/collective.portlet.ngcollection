import os
import re

from zope.interface import implements
from zope.component import getGlobalSiteManager

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.portlet.ngcollection.interfaces import IPortletTemplateManager
from collective.portlet.ngcollection import migration

from Products.CMFCore.FSMetadata import FSMetadata

osjoin = os.path.join

def getDirKey(package, directory):
    if package is not None:
        packpath = package.__path__[0]
        reldir = directory[len(packpath):].strip('/\\')
        # bind-out from OS separators
        '/'.join(reldir.split(os.sep))
        return "%s-%s" % (package.__name__, reldir)
    else:
        return directory

def getTemplateKey(dirkey, filename):
    return ":".join([dirkey, filename])

class PortletTemplateManagerFactory(object):
    def __init__(self):
        self.manager = PortletTemplateManager()

    def __call__(self, layer):
        return self.manager


class PortletTemplateManager(object):
    implements(IPortletTemplateManager)

    def __init__(self):
        self._templates = {}

    def registerDirectory(self, directory, package):
        """See interface"""
        dirkey = getDirKey(package, directory)
        for filename in os.listdir(directory):
            if len(filename) > 3 and filename.endswith('.pt'):
                path = osjoin(directory, filename)
                tmplkey = getTemplateKey(dirkey, filename)
                metadata = FSMetadata(path)
                metadata.read()
                properties = metadata.getProperties()
                title = properties.get('title', filename[:-3])
                self._templates[tmplkey] = (title.decode('utf-8'),
                                        ViewPageTemplateFile(path))
                migration.add_to_migration_map(tmplkey, path)

    def unregisterDirectory(self, directory, package):
        """See interface"""
        # HOOK: Generate remove key by passing directory key with
        #       EMPTY FILE NAME to getTemplateKey function
        rmkey = getTemplateKey(getDirKey(package, directory), "")
        for path, template in self.templates.items():
            if path.startswith(rmkey):
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
        if migration.DO_MIGRATE:
            migration.migrate(obj, adapter)
        yield adapter

