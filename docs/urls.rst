API Services URLs
*****************

Most of the URLs used as part of the API services will be unstructured URLs

Locations API
=============

Location By Address
-------------------

.. autoclass:: bingmaps.urls.locations_build_urls.LocationByAddressUrl
   :inherited-members:

Location By Point
-----------------

.. autoclass:: bingmaps.urls.locations_build_urls.LocationByPointUrl
   :inherited-members:

Location By Query
-----------------

.. autoclass:: bingmaps.urls.locations_build_urls.LocationByQueryUrl
   :inherited-members:


Elevations API
==============

.. autoclass:: bingmaps.urls.elevations_build_urls.ElevationsUrl
   :members: protocol, main_url, rest, version, restApi, resourcePath, query

Traffic Incidents API
=====================

.. autoclass:: bingmaps.urls.traffic_build_urls.TrafficIncidentsUrl
   :members: protocol, main_url, rest, version, restApi, resourcePath, query