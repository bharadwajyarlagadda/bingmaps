from bingmaps.urls import TrafficIncidentsUrl, TrafficIncidentsSchema
from collections import namedtuple
import requests
import json
import xmltodict


class TrafficIncidentsApi(object):
    """Traffic Incidents API class

    This class is used to retrieve the output from the given data from the
    user.
      - First, the data is used to build a URL which is related to the
        Traffic Incidents API.
      - Second, this class helps in retrieving the response from the URL built
      - Third, based on the response, this class helps in retrieving all the
        corresponding output data from the response. Some of the output data
        which this class would be retrieving is:
          - coordinates
          - description
          - congestion
          - detour info
          - road closed info
          - incident id
          - lane info
          - start time of the incident
          - end time of the incident
          - last modified time of the incident
          - severity of the incident
          - type of the incident
          - verification status

    The output from the URL can be either JSON/XML based on the output
    parameter mentioned in the data. Even the output response is 'xml', this
    class helps in converting the xml response to JSON data first and then
    retrieve all the necessary output from it.

    :ivar data: The data that the user will send in to the TrafficIncidentsApi
        to retrieve all the respective output from the response
    :ivar url: The url that gets built based on the user's given data
    :ivar http_protocol: Http protocol for the URL. Can be either of the
        following:
          - http
          - https
    :ivar schema: The schema that gets used to build the URL and the schema
        would be .
    :ivar file_name: The filename that the class can write the JSON response
        to TrafficIncidentsSchema.
          - file_name - 'traffic_incidents'
    :ivar incidents_data: Response from the URL

    Some of the examples are illustrated in Examples page
    """
    def __init__(self, data, http_protocol='http'):
        self.http_protocol = http_protocol
        self.schema = TrafficIncidentsUrl(data,
                                          TrafficIncidentsSchema(),
                                          http_protocol)
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
        """Retrieves the description of the incident/incidents from the output
        response

        Returns:
            description(namedtuple): List of named tuples of descriptions of
            the incident/incidents
        """
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
        """Retrieves the congestion information of the incident/incidents from
        the output response

        Returns:
            congestion(namedtuple): List of named tuples of congestion info of
            the incident/incidents
        """
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
        """Retrieves the detour information of the incident/incidents from
        the output response

        Returns:
            detour_info(namedtuple): List of named tuples of detour info of
            the incident/incidents
        """
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
        """Retrieves the start time of the incident/incidents from the output
        response

        Returns:
            start_time(namedtuple): List of named tuples of start time of the
            incident/incidents
        """
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
        """Retrieves the end time of the incident/incidents from the output
        response

        Returns:
            end_time(namedtuple): List of named tuples of end time of the
            incident/incidents
        """
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
        """Retrieves the incident id/ids of the incident/incidents from the
        output response

        Returns:
            incident_id(namedtuple): List of named tuples of incident id/ids of
            the incident/incidents
        """
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
        """Retrieves the lane info of the incident/incidents from the
        output response

        Returns:
            lane_info(namedtuple): List of named tuples of lane info of the
            incident/incidents
        """
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
        """Retrieves the last modified time stamp of the incident/incidents
        from the output response

        Returns:
            last_modified(namedtuple): List of named tuples of last modified
            time stamp of the incident/incidents
        """
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
        """Retrieves the road closed information for the incident/incidents
        from the output response

        Returns:
            road_closed(namedtuple): List of named tuples of road closed
            information for the incident/incidents
        """
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
        """Retrieves the severity for the incident/incidents from the
        output response

        Returns:
            severity(namedtuple): List of named tuples of severity for the
            incident/incidents
        """
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
        """Retrieves the type of the incident/incidents from the output
        response

        Returns:
            type(namedtuple): List of named tuples of type of the
            incident/incidents
        """
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
        """Retrieves the verification status of the incident/incidents from the
        output response

        Returns:
            verified(namedtuple): List of named tuples of verification status
            of the incident/incidents
        """
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
