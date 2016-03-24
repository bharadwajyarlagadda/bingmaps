REST Services
*************


Locations API
=============

Location By Address API
-----------------------

.. autoclass:: bingmaps.apiservices.LocationByAddress
   :inherited-members:

Location By Point API
---------------------

.. autoclass:: bingmaps.apiservices.LocationByPoint
   :inherited-members:
   :members: build_url

Location By Query API
---------------------

.. autoclass:: bingmaps.apiservices.LocationByQuery
   :inherited-members:


Elevations API
==============

.. autoclass:: bingmaps.apiservices.ElevationsApi
   :members: build_url, get_data, status_code, response_to_dict, elevations,
             zoomlevel, to_json_file, response

Traffic Incidents API
=====================

.. autoclass:: bingmaps.apiservices.TrafficIncidentsApi
   :members: build_url, status_code, response, response_to_dict,
             get_coordinates, description, congestion, detour_info, start_time,
             end_time, incident_id, lane_info, last_modified, road_closed,
             severity, type, is_verified