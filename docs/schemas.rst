REST Services Schemas
*********************


Locations API
=============

.. autoclass:: bingmaps.urls.locations_build_urls.Location

Location By Address
-------------------

.. autoclass:: bingmaps.urls.locations_build_urls.LocationByAddressSchema
.. autoclass:: bingmaps.urls.locations_build_urls.LocationByAddressQueryString
   :members: build_query_string

Location By Point
-----------------

.. autoclass:: bingmaps.urls.locations_build_urls.LocationByPointSchema
.. autoclass:: bingmaps.urls.locations_build_urls.LocationByPointQueryString
   :members: build_query_string

Location By Query
-----------------

.. autoclass:: bingmaps.urls.locations_build_urls.LocationByQuerySchema
.. autoclass:: bingmaps.urls.locations_build_urls.LocationByQueryString
   :members: build_query_string

Elevations API
==============

.. autoclass:: bingmaps.urls.elevations_build_urls.Elevations

Elevations for latitude and longitude coordinates
-------------------------------------------------

.. autoclass:: bingmaps.urls.elevations_build_urls.CoordinatesSchema
.. autoclass:: bingmaps.urls.elevations_build_urls.Coordinates
   :members: build_query_string

Elevations at equally-spaced locations along a polyline path
------------------------------------------------------------

.. autoclass:: bingmaps.urls.elevations_build_urls.PolylineSchema
.. autoclass:: bingmaps.urls.elevations_build_urls.Polyline
   :members: build_query_string

Get offset at a set of latitude and longitude coordinates
---------------------------------------------------------

.. autoclass:: bingmaps.urls.elevations_build_urls.OffsetSchema
.. autoclass:: bingmaps.urls.elevations_build_urls.Offset
   :members: build_query_string

Get elevations within an area on the Earth defined as a bounding box
--------------------------------------------------------------------

.. autoclass:: bingmaps.urls.elevations_build_urls.BoundingBoxSchema
.. autoclass:: bingmaps.urls.elevations_build_urls.BoundingBox
   :members: build_query_string