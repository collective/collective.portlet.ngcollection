from setuptools import setup, find_packages
import os

version = '1.2'

setup(name='collective.portlet.ngcollection',
      version=version,
      description="Extends plone collection portlet in order to allow assigning different views for each newly created portlet through it's edit form",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone portlet collection',
      author='Quintagroup',
      author_email='support@quintagroup.com',
      url='http://dev.plone.org/collective/browser/collective.portlet.ngcollection',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.portlet'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target=plone
      """,
      )
