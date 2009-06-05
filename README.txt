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

So to avoid having some odd conditions in your collection portlet's template
NGCollection extends standard plone collection portlet with view_name field.
View name is a name of some traversable object which will be called without any
parameters to retrieve html output.

Thus view can be a content object, a skins template, a zope3 browser view or
any other zope traversable object. This view can count on a 'view' binding
variable which is a reference to portlet renderer.

Apart from the 'view_name' field NGCollection portlet also adds 'more_label'
field. This field is here to override default collection's portlet
'Show more...' link text with some custom one entered by user.
