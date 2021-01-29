import json


class Endpoint(object):
    """ REST-Endpoint with or without credentials """

    def __init__(self, url, details, user=None, pw=None):
        self.url = url
        self.details = details
        self.requests_params = {'url': self.url}
        if (user is not None) and (pw is not None):
            self.creds = (user, pw)
            self.requests_params['auth'] = self.creds


class Route(object):
    """ Broker and topic with a list of endpoints as destinations """

    def __init__(self, broker, topic):
        self.broker = broker
        self.topic = topic
        self.endpoints = []


def read_config(path):
    """read the given config file and return a list of broker, topic, endpoint triplets
    """
    with open(path) as json_data:
        config = json.load(json_data)
        return config['routes']
        # TODO: use db connectstring to read config from db


class Config(object):

    def __init__(self, path='config.json'):
        pairs = read_config(path)
        route_merger = {}
        for pair in pairs:
            broker = pair['broker']
            protocol_in = pair['protocol_in']
            protocol_out = pair['protocol_out']
            topic = pair['topic']
            key = broker + 'justmakingsure' + topic
            route_merger[key] = route_merger.get(key, Route(broker=broker, topic=topic))
            details = {
                'broker': broker,
                'endpoint': pair['endpoint'],
                'topic': topic,
                'protocol_in': protocol_in,
                'protocol_out': protocol_out
            }
            endpoint = Endpoint(url=pair['endpoint'],
                                details=details,
                                pw=pair.get('endpoint_pw', None))
            route_merger[key].endpoints.append(endpoint)
        self.routes = [r for r in route_merger.values()]
