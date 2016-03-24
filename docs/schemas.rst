REST Services Schemas
*********************


Locations API
=============

.. autoclass:: bingmaps.urls.locations_build_urls.Location

Location By Address
-------------------

.. autoclass:: bingmaps.urls.locations_build_urls.LocationByAddressSchema
   :members: build_query_string

Location By Point
-----------------

.. autoclass:: bingmaps.urls.locations_build_urls.LocationByPointSchema
   :members: build_query_string

Location By Query
-----------------

.. autoclass:: bingmaps.urls.locations_build_urls.LocationByQuerySchema
   :members: build_query_string

Elevations API
==============

.. autoclass:: bingmaps.urls.elevations_build_urls.Elevations

Elevations for latitude and longitude coordinates
-------------------------------------------------

.. autoclass:: bingmaps.urls.elevations_build_urls.Coordinates
   :members: build_query_string

Elevations at equally-spaced locations along a polyline path
------------------------------------------------------------

.. autoclass:: bingmaps.urls.elevations_build_urls.Polyline
   :members: build_query_string

Get offset at a set of latitude and longitude coordinates
---------------------------------------------------------

.. autoclass:: bingmaps.urls.elevations_build_urls.Offset
   :members: build_query_string

Get elevations within an area on the Earth defined as a bounding box
--------------------------------------------------------------------

.. autoclass:: bingmaps.urls.elevations_build_urls.BoundingBox
   :members: build_query_string

Traffic Incidents API
=====================

.. autoclass:: bingmaps.urls.traffic_build_urls.TrafficIncidentsSchema
   :members: build_query_string
