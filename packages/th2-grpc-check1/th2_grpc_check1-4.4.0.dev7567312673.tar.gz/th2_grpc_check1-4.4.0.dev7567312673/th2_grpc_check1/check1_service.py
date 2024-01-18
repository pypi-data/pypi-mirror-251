from . import check1_pb2_grpc as importStub

class Check1Service(object):

    def __init__(self, router):
        self.connector = router.get_connection(Check1Service, importStub.Check1Stub)

    def createCheckpoint(self, request, timeout=None, properties=None):
        return self.connector.create_request('createCheckpoint', request, timeout, properties)

    def submitCheckRule(self, request, timeout=None, properties=None):
        return self.connector.create_request('submitCheckRule', request, timeout, properties)

    def submitCheckSequenceRule(self, request, timeout=None, properties=None):
        return self.connector.create_request('submitCheckSequenceRule', request, timeout, properties)

    def submitNoMessageCheck(self, request, timeout=None, properties=None):
        return self.connector.create_request('submitNoMessageCheck', request, timeout, properties)

    def waitForResult(self, request, timeout=None, properties=None):
        return self.connector.create_request('waitForResult', request, timeout, properties)

    def multiSubmitRules(self, request, timeout=None, properties=None):
        return self.connector.create_request('multiSubmitRules', request, timeout, properties)