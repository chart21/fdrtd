"""
secure sum example with Simon

four fdrtd servers are needed for this example.
one for each of Alice, Bob, and Charlie.
and an additional one for invitations and synchronizing.
the easiest way is to run them all on localhost:

    pip install fdrtd
    python -m fdrtd.webserver --port=55500 &
    python -m fdrtd.webserver --port=55501 &
    python -m fdrtd.webserver --port=55502 &
    python -m fdrtd.webserver --port=55503 &

then, the three scripts of Alice, Bob, and Charlie may be executed simultaneously.
"""


import representation
from tools.sync import SyncApi


URL_SYNC = "http://localhost:55500"
URL_ALICE = "http://localhost:55501"
URL_BOB = "http://localhost:55502"
URL_CHARLIE = "http://localhost:55503"

SECRET_ALICE = 42.0
NETWORK_ALICE = {'nodes': [URL_ALICE, URL_BOB, URL_CHARLIE], 'myself': 0}  # Alice is no. 0 out of 0, 1, 2.


if __name__ == "__main__":

    api = representation.Api(URL_ALICE)
    api_sync = SyncApi(URL_SYNC)

    microservice = api.create(protocol="Simon")
    task = microservice.create_task(microprotocol="BasicSum", network=NETWORK_ALICE)
    invitation = api.download(task.invite())
    api_sync.send_broadcast(invitation, ["Some", "Shared", "Tokens"])
    task.input(data=SECRET_ALICE)
    task.start()

    result = None
    while result is None:
        result = task.result()
    print(api.download(result))
