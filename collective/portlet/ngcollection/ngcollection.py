import os
from zope import schema
from zope.formlib import form
from zope.interface import implements
from zope.component import queryAdapter

from plone.portlets.interfaces import IPortletDataProvider
from plone.portlet.collection import collection as base
from plone.app.form.widgets.uberselectionwidget import UberSelectionWidget

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


from collective.portlet.ngcollection.manager import getPortletTemplateManagers
from collective.portlet.ngcollection import NGCollectionMessageFactory as _
from collective.portlet.ngcollection.interfaces import IPortletTemplateManager

class INGCollection(base.ICollectionPortlet):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """

    template = schema.Choice(
        title=_(u"Template"),
        description=_(u"Template to use for portlet rendering. If not set "
                      u"then default one will be used."),
        required=False,
        default=u"",
        vocabulary='collective.portlet.ngcollection.PortletTemplates')
    
    show_more_label = schema.TextLine(
        title=_(u"Show More Label"),
        description=_(u"Label for Show More link"),
        default=u"",
        required=False)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(INGCollection)
    
    template = u""
    show_more_label = u""

    def __init__(self, header=u"", target_collection=None, limit=None,
                 random=False, show_more=True, show_dates=False,
                 template=u"", show_more_label=u""):
        super(Assignment, self).__init__(header=header, limit=limit,
            target_collection=target_collection, random=random,
            show_more=show_more, show_dates=show_dates)
        self.template = template
        self.show_more_label = show_more_label


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    _template = ViewPageTemplateFile('ngcollection.pt')
    
    def show_more_label(self):
        return self.data.show_more_label or u"More&hellip;"
    
    def render(self):
        template = self._template
        path = self.data.template
        if path:
            for manager in getPortletTemplateManagers(self.data):
                if manager.hasTemplate(path):
                    if not hasattr(manager.getTemplate(path),'__of__'):
                        return manager.getTemplate(path)(self) # for Plone 4
                    template = manager.getTemplate(path).__of__(self)
                    break
        return template()

class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(INGCollection)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    
    label = _(u"Add NG Collection Portlet")
    description = _(u"This portlet extends standard plone collection portlet "
                    u"with two more extra fields: view_name and "
                    u"show_more_label")

    def create(self, data):
        return Assignment(**data)

class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(INGCollection)
    form_fields['target_collection'].custom_widget = UberSelectionWidget
    
    label = _(u"Edit NG Collection Portlet")
    description = _(u"This portlet extends standard plone collection portlet "
                    u"with two more extra fields: view_name and "
                    u"show_more_label")
