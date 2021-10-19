from fdrtd.server.bus import Bus
from fdrtd.server.discovery import discover_microservices


class TestInterface:

    def __init__(self):
        self.bus = Bus()
        microservices = discover_microservices("../fdrtd", self.bus)
        self.bus.set_microservices(microservices)

    def post(self, *path, body=None):
        if len(path) == 1:
            if path[0] == 'representations':
                response = self.bus.create_representation(body)
                return {'type': 'uuid', 'uuid': response}, 200 

    def put(self, *path, body=None):
        if len(path) == 1:
            if path[0] == 'representations':
                response = self.bus.upload_representation(body)
                return {'type': 'uuid', 'uuid': response}, 200

    def patch(self, *path, body=None):
        if len(path) == 2:
            if path[0] == 'representation':
                response = self.bus.call_representation(path[1], body)
                if response is None:
                    return {'type': 'none'}, 200
                return {'type': 'uuid', 'uuid': response}, 200

    def get(self, *path):
        if len(path) == 1:
            if path[0] == 'representations':
                response = self.bus.list_representations()
                return {'type': 'list', 'list': response}, 200
        if len(path) == 2:
            if path[0] == 'representation':
                response = self.bus.download_representation(path[1])
                return {'type': 'object', 'object': response}, 200
        if len(path) == 3:
            if path[0] == 'representation':
                uuid = self.bus.create_attribute(path[1], path[2], public=True)
                return {'type': 'uuid', 'uuid': uuid}, 200

    def delete(self, *path):
        if len(path) == 2:
            if path[0] == 'representation':
                self.bus.release_representation(path[1])
                return {'type': 'none'}, 200

