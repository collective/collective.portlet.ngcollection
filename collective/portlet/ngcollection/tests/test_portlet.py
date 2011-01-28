from os import path

from zope.component import getUtility, getMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer
from plone.app.portlets.storage import PortletAssignmentMapping

from Products.CMFCore.utils import getToolByName
from Products.Five import zcml
from Products.Five import fiveconfigure

from collective.portlet.ngcollection import ngcollection
from collective.portlet.ngcollection.tests.base import TestCase


class TestPortlet(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def test_portlet_type_registered(self):
        portlet = getUtility(
            IPortletType,
            name='collective.portlet.ngcollection.NGCollection')
        self.assertEquals(portlet.addview,
                          'collective.portlet.ngcollection.NGCollection')

    def test_interfaces(self):
        portlet = ngcollection.Assignment(header=u"title")
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def test_invoke_add_view(self):
        portlet = getUtility(
            IPortletType,
            name='collective.portlet.ngcollection.NGCollection')
        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        addview.createAndAdd(data={'header' : u"test title"})

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0],
                                   ngcollection.Assignment))

    def test_invoke_edit_view(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = ngcollection.Assignment(header=u"title")
        editview = getMultiAdapter((mapping['foo'], request), name='edit')
        self.failUnless(isinstance(editview, ngcollection.EditForm))

    def test_obtain_renderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(IPortletManager, name='plone.rightcolumn',
                             context=self.portal)

        assignment = ngcollection.Assignment(header=u"title")

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, ngcollection.Renderer))


class TestRenderer(TestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))
        #make a collection
        self.collection = self._createType(self.folder, 'Topic', 'collection')

    def _createType(self, context, portal_type, id, **kwargs):
        """Helper method to create a new type
        """
        ttool = getToolByName(context, 'portal_types')
        cat = self.portal.portal_catalog

        fti = ttool.getTypeInfo(portal_type)
        fti.constructInstance(context, id, **kwargs)
        obj = getattr(context.aq_inner.aq_explicit, id)
        cat.indexObject(obj)
        return obj

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.rightcolumn', context=self.portal)

        assignment = assignment or ngcollection.Assignment()
        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)

    def test_render(self):
        r = self.renderer(context=self.portal,
                          assignment=ngcollection.Assignment(header=u"title"))
        r = r.__of__(self.folder)
        r.update()
        output = r.render()
        # TODO: Test output
    
    def test_show_more_label(self):
        # set up our portlet renderer
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST
        mapping['foo'] = ngcollection.Assignment(header=u"title", random=True,
            target_collection='/Members/test_user_1_/collection')
        collectionrenderer = self.renderer(context=None, request=None,
            view=None, manager=None, assignment=mapping['foo'])
        self.assertEquals(collectionrenderer.show_more_label(), 'More&hellip;')
        
        mapping['buz'] = ngcollection.Assignment(header=u"title", random=True,
            target_collection='/Members/test_user_1_/collection',
            show_more_label=u"View more")
        collectionrenderer = self.renderer(context=None, request=None,
            view=None, manager=None, assignment=mapping['buz'])
        self.assertEquals(collectionrenderer.show_more_label(), 'View more')
    
    def test_template(self):
        # test default template
        r = self.renderer(context=self.portal,
                          assignment=ngcollection.Assignment(header=u"title",
                          target_collection='/Members/test_user_1_/collection'))
        r = r.__of__(self.folder)
        r.update()
        output = r.render()
        self.failUnless('portletCollection' in output)
        
        # test assigned custom testing template
        # register portlet templates directory with alternative template
        dir_path = path.join(path.dirname(__file__), 'templates')
        zcml_string = """
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:plone="http://namespaces.plone.org/plone">

  <include package="collective.portlet.ngcollection" file="meta.zcml" />

  <plone:portletTemplates
      interface="collective.portlet.ngcollection.ngcollection.INGCollection"
      directory="%s"
  />

</configure>
        """ % dir_path
        fiveconfigure.debug_mode = True
        zcml.load_string(zcml_string)
        fiveconfigure.debug_mode = False
        
        t_path = path.join(dir_path, 'test.pt')
        t_path = "%s:%s" % (dir_path, 'test.pt')
        r = self.renderer(context=self.portal,
                          assignment=ngcollection.Assignment(header=u"title",
            target_collection='/Members/test_user_1_/collection',
            template=t_path))
        r = r.__of__(self.folder)
        r.update()
        output = r.render()
        self.failUnless('This is a test template!' in output)

class TestCollectionQuery(TestCase):
    """This TestCase was simply copied from plone.portlet.collection portlet
    to ensure we don't break original functionality.
    """

    def afterSetUp(self):
        self.setRoles(('Manager',))
        #make a collection
        self.collection = self._createType(self.folder, 'Topic', 'collection')

    def _createType(self, context, portal_type, id, **kwargs):
        """Helper method to create a new type
        """
        ttool = getToolByName(context, 'portal_types')
        cat = self.portal.portal_catalog

        fti = ttool.getTypeInfo(portal_type)
        fti.constructInstance(context, id, **kwargs)
        obj = getattr(context.aq_inner.aq_explicit, id)
        cat.indexObject(obj)
        return obj

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(IPortletManager,
            name='plone.leftcolumn', context=self.portal)
        assignment = assignment
        return getMultiAdapter((context, request, view, manager, assignment),
            IPortletRenderer)

    def testSimpleQuery(self):
        # set up our collection to search for Folders
        crit = self.folder.collection.addCriterion('portal_type',
            'ATSimpleStringCriterion')
        crit.setValue('Folder')

        # add a few folders
        for i in range(6):
            self.folder.invokeFactory('Folder', 'folder_%s'%i)
            getattr(self.folder, 'folder_%s'%i).reindexObject()

        # the folders are returned by the topic
        collection_num_items = len(self.folder.collection.queryCatalog())
        # We better have some folders
        self.failUnless(collection_num_items >= 6)

        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST
        mapping['foo'] = ngcollection.Assignment(header=u"title",
            target_collection='/Members/test_user_1_/collection')
        collectionrenderer = self.renderer(context=None, request=None,
            view=None, manager=None, assignment=mapping['foo'])

        # we want the portlet to return us the same results as the collection
        self.assertEquals(collection_num_items,
                          len(collectionrenderer.results()))
        
    def testRandomQuery(self):
        # we're being perhaps a bit too clever in random mode with the internals
        # of the LazyMap returned by the collection query, so let's try a bunch
        # of scenarios to make sure they work
        
        # set up our portlet renderer
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST
        mapping['foo'] = ngcollection.Assignment(header=u"title", random=True,
            target_collection='/Members/test_user_1_/collection')
        collectionrenderer = self.renderer(context=None, request=None,
            view=None, manager=None, assignment=mapping['foo'])

        # add some folders
        for i in range(6):
            self.folder.invokeFactory('Folder', 'folder_%s'%i)
            getattr(self.folder, 'folder_%s'%i).reindexObject()

        # collection with no criteria -- should return empty list, without error
        self.assertEqual(len(collectionrenderer.results()), 0)

        # let's make sure the results aren't being memoized
        old_func = self.folder.collection.queryCatalog
        global collection_was_called
        collection_was_called = False
        def mark_collection_called(**kw):
            global collection_was_called
            collection_was_called = True
        self.folder.collection.queryCatalog = mark_collection_called
        collectionrenderer.results()
        self.folder.collection.queryCatalog = old_func
        self.failUnless(collection_was_called)
        
        # collection with simple criterion -- should return 1 (random) folder
        crit = self.folder.collection.addCriterion('portal_type',
            'ATSimpleStringCriterion')
        crit.setValue('Folder')
        self.assertEqual(len(collectionrenderer.results()), 1)
        
        # collection with multiple criteria -- should behave similarly
        crit = self.folder.collection.addCriterion('Creator',
            'ATSimpleStringCriterion')
        crit.setValue('test_user_1_')
        collectionrenderer.results()
        
        # collection with sorting -- should behave similarly
        # (sort is ignored internally)
        self.folder.collection.setSortCriterion('modified', False)
        self.assertEqual(len(collectionrenderer.results()), 1)
        
        # same criteria, now with limit set to 2 -- should return 2 (random)
        # folders
        collectionrenderer.data.limit = 2
        self.assertEqual(len(collectionrenderer.results()), 2)
        
        # make sure there's no error if the limit is greater than the # of
        # results found
        collectionrenderer.data.limit = 10
        self.failUnless(len(collectionrenderer.results()) >= 6)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    suite.addTest(makeSuite(TestCollectionQuery))
    return suite
