from bingmaps.urls import TrafficIncidentsUrl, TrafficIncidentsSchema
from collections import namedtuple
import requests
import json
import xmltodict


class TrafficIncidentsApi(object):
    def __init__(self, data, http_protocol='http'):
        self.http_protocol = http_protocol
        self.schema = TrafficIncidentsUrl(data,
                                          TrafficIncidentsSchema(),
                                          http_protocol)
        self.file_name = 'traffic_incidents'
        self.incidents_data = None
        self.get_data()

    def build_url(self):
        """Builds the URL for elevations API services based on the data given
        by the user.

        Returns:
            url (str): URL for the elevations API services
        """
        url = '{protocol}/{url}/{rest}/{version}/{restapi}/{rscpath}/' \
              '{query}'.format(protocol=self.schema.protocol,
                               url=self.schema.main_url,
                               rest=self.schema.rest,
                               version=self.schema.version,
                               restapi=self.schema.restApi,
                               rscpath=self.schema.resourcePath,
                               query=self.schema.query)
        return url

    @property
    def response(self):
        """Response from the built URL"""
        return self.incidents_data.text

    @property
    def status_code(self):
        """Status code of the response from the URL"""
        return self.incidents_data.status_code

    def get_data(self):
        """Gets data from the given url"""
        url = self.build_url()
        self.incidents_data = requests.get(url)
        if not self.incidents_data.status_code == 200:
            raise self.incidents_data.raise_for_status()

    def get_resource(self):
        resourceSets = self.response_to_dict()
        try:
            for resource in resourceSets['resourceSets']:
                return [rsc for rsc in resource['resources']]
        except KeyError:
            try:
                resourcesSets = resourceSets['Response']['ResourceSets']
                resourceSet = resourcesSets['ResourceSet']
                if isinstance(resourceSet, dict):
                    return [resourceSet['Resources']]
                elif isinstance(resourceSet, list):
                    return [rsc for rsc in resourceSet['Resources']]
            except KeyError:
                print(KeyError)

    def response_to_dict(self):
        """This method helps in returning the output JSON data from the URL
        and also it helps in converting the XML output/response (string) to a
        JSON object

        Returns:
            data (dict): JSON data from the output/response
        """
        try:
            return json.loads(self.incidents_data.text)
        except Exception:
            return json.loads(json.dumps(xmltodict.parse(
                self.incidents_data.text)))

    @property
    def get_coordinates(self):
        """Retrieves coordinates (latitudes/longitudes) from the output
        JSON/XML response

        Returns:
            coordinates (namedtuple): List of named tuples of coordinates
            (latitudes and longitudes)
        """
        resource_list = self.traffic_incident()
        coordinates = namedtuple('coordinates', ['latitude', 'longitude'])
        if len(resource_list) == 1 and resource_list[0] is None:
            return None
        else:
            try:
                return [coordinates(*resource['point']['coordinates'])
                        for resource in resource_list]
            except (KeyError, TypeError):
                try:
                    if isinstance(resource_list, dict):
                        resource_list = [resource_list]
                    return [coordinates(resource['ToPoint']['Latitude'],
                                        resource['ToPoint']['Longitude'])
                            for resource in resource_list]
                except (KeyError, ValueError) as exc:
                    print(exc)

    def traffic_incident(self):
        resource_list = self.get_resource()
        try:
            for resource in resource_list:
                if isinstance(resource['TrafficIncident'], dict):
                    return [resource['TrafficIncident']]
                elif isinstance(resource['TrafficIncident'], list):
                    return resource['TrafficIncident']
        except (KeyError, TypeError):
            return resource_list

    @property
    def description(self):
        resource_list = self.traffic_incident()
        description = namedtuple('description', 'description')
        if len(resource_list) == 1 and resource_list[0] is None:
            return None
        else:
            try:
                return [description(resource['description'])
                        for resource in resource_list]
            except (KeyError, TypeError):
                try:
                    return [description(resource['Description'])
                            for resource in resource_list]
                except KeyError:
                    return None

    @property
    def congestion(self):
        resource_list = self.traffic_incident()
        congestion = namedtuple('congestion', 'congestion')
        if len(resource_list) == 1 and resource_list[0] is None:
            return None
        else:
            try:
                return [congestion(resource['congestion'])
                        for resource in resource_list]
            except (KeyError, TypeError):
                try:
                    return [congestion(resource['CongestionInfo'])
                            for resource in resource_list]
                except KeyError:
                    return None

    @property
    def detour_info(self):
        resource_list = self.traffic_incident()
        detour_info = namedtuple('detour_info', 'detour_info')
        if len(resource_list) == 1 and resource_list[0] is None:
            return None
        else:
            try:
                return [detour_info(resource['detour'])
                        for resource in resource_list]
            except (KeyError, TypeError):
                try:
                    return [detour_info(resource['detourInfo'])
                            for resource in resource_list]
                except KeyError:
                    return None

    @property
    def start_time(self):
        resource_list = self.traffic_incident()
        start_time = namedtuple('start_time', 'start_time')
        if len(resource_list) == 1 and resource_list[0] is None:
            return None
        else:
            try:
                return [start_time(resource['start'])
                        for resource in resource_list]
            except (KeyError, TypeError):
                return [start_time(resource['StartTimeUTC'])
                        for resource in resource_list]

    @property
    def end_time(self):
        resource_list = self.traffic_incident()
        end_time = namedtuple('end_time', 'end_time')
        if len(resource_list) == 1 and resource_list[0] is None:
            return None
        else:
            try:
                return [end_time(resource['end'])
                        for resource in resource_list]
            except (KeyError, TypeError):
                return [end_time(resource['EndTimeUTC'])
                        for resource in resource_list]

    @property
    def incident_id(self):
        resource_list = self.traffic_incident()
        incident_id = namedtuple('incident_id', 'incident_id')
        if len(resource_list) == 1 and resource_list[0] is None:
            return None
        else:
            try:
                return [incident_id(resource['incidentId'])
                        for resource in resource_list]
            except (KeyError, TypeError):
                return [incident_id(resource['IncidentId'])
                        for resource in resource_list]

    @property
    def lane_info(self):
        resource_list = self.traffic_incident()
        lane_info = namedtuple('lane_info', 'lane_info')
        if len(resource_list) == 1 and resource_list[0] is None:
            return None
        else:
            try:
                return [lane_info(resource['lane'])
                        for resource in resource_list]
            except (KeyError, TypeError):
                try:
                    return [lane_info(resource['LaneInfo'])
                            for resource in resource_list]
                except KeyError:
                    return None

    @property
    def last_modified(self):
        resource_list = self.traffic_incident()
        last_modified = namedtuple('last_modified', 'last_modified')
        if len(resource_list) == 1 and resource_list[0] is None:
            return None
        else:
            try:
                return [last_modified(resource['lastModified'])
                        for resource in resource_list]
            except (KeyError, TypeError):
                return [last_modified(resource['LastModifiedUTC'])
                        for resource in resource_list]

    @property
    def road_closed(self):
        resource_list = self.traffic_incident()
        road_closed = namedtuple('road_closed', 'road_closed')
        if len(resource_list) == 1 and resource_list[0] is None:
            return None
        else:
            try:
                return [road_closed(resource['roadClosed'])
                        for resource in resource_list]
            except (KeyError, TypeError):
                return [road_closed(resource['RoadClosed'])
                        for resource in resource_list]

    @property
    def severity(self):
        resource_list = self.traffic_incident()
        severity = namedtuple('severity', 'severity')
        if len(resource_list) == 1 and resource_list[0] is None:
            return None
        else:
            try:
                return [severity(resource['severity'])
                        for resource in resource_list]
            except (KeyError, TypeError):
                return [severity(resource['Severity'])
                        for resource in resource_list]

    @property
    def type(self):
        resource_list = self.traffic_incident()
        type = namedtuple('type', 'type')
        if len(resource_list) == 1 and resource_list[0] is None:
            return None
        else:
            try:
                return [type(resource['type'])
                        for resource in resource_list]
            except (KeyError, TypeError):
                return [type(resource['Type'])
                        for resource in resource_list]

    @property
    def is_verified(self):
        resource_list = self.traffic_incident()
        verified = namedtuple('verified', 'verified')
        if len(resource_list) == 1 and resource_list[0] is None:
            return None
        else:
            try:
                return [verified(resource['verified'])
                        for resource in resource_list]
            except (KeyError, TypeError):
                return [verified(resource['Verified'])
                        for resource in resource_list]
