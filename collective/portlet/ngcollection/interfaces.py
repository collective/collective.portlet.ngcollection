from zope import interface

class IPortletTemplateManager(interface.Interface):
    """Manages customly registered templates for portlets"""

    def registerDirectory(directory):
        """Add templates to portlet's possible views for rendering"""

    def unregisterDirectory(directory):
        """Remove templates from portlet's possible views for rendering"""

    def hasTemplate(path):
        """Checks if given template is registered"""

    def getTemplate(path, default=None):
        """Returns registered template or default if not registered"""

    def getTemplatesForVocab():
        """Returns list of template pathes and filenames for using them
        in vocabularies"""
