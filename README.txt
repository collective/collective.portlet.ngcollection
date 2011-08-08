Introduction
============

This package provides portlet which extends plone collection portlet in order
to allow assigning different views for each newly created portlet through it's
edit form.

This is often required to have many collection portlets displaying different
information in different places. Plone portlets provide us with portletRenderer
directive which in general is really usefull, but it's not an option because it
overrides portlet renderer globally thus allowing to have only one template at
a time.

Thus to avoid having some odd conditions in your collection portlet's template
NGCollection extends standard plone collection portlet with a template field
where you can select template to use from available templates.

Apart from the 'template' field NGCollection portlet also adds
'show_more_label' field. This field is here to override default collection's
portlet 'More...' link text with some custom one entered by user.


Portlet Templates
-----------------

In order to register new alternative templates for your portlet this package
provides portletTemplates directive::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:plone="http://namespaces.plone.org/plone">

      <include package="collective.portlet.ngcollection" file="meta.zcml" />

      <plone:portletTemplates
          interface="path.to.some.portlet.assignment.Interface"
          directory="alternative_templates"
          />

    </configure>

In this example we register templates contained inside alternative_templates
folder as alternative templates available for path.to.some.portlet.assignment.
Interface portlet. Thus you'll be able to select one of them on portlet edit
form via Plone interface.

You can register more than one directory for your portlet.

This idea with registering directories with custom templates was highly inspired
by z3c.jbot package.

Contributors
------------

 * Vitaliy Podoba
 * Roman Kozlovskiy
 * Volodymyr Cherepanyak

