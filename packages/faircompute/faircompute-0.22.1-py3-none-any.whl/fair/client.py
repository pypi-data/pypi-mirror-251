import random
import os
import sys
from time import sleep
from typing import Sequence, Union, Optional
from urllib.parse import quote_plus

import requests

POLL_TIMEOUT = 0.1


class ClustersClient:
    def __init__(self, client: 'FairClient'):
        self.client = client
        self.endpoint_address = os.path.join(client.server_address, 'clusters')

    def create(self, cluster_name: str, public: bool):
        json = {
            'name': cluster_name,
            'public': public,
            'version': 'V021',
        }
        return self.client._make_request('post', url=f"{self.endpoint_address}/create", json=json)

    def remove(self, cluster_name: str):
        json = {
            'name': cluster_name,
            'version': 'V021',
        }
        return self.client._make_request('post', url=f"{self.endpoint_address}/remove", json=json)

    def list(self):
        return self.client._make_request('post', url=f"{self.endpoint_address}/list").json()["clusters"]


class ClusterNodesClient:
    def __init__(self, client: 'FairClient', cluster_name: str):
        self.client = client
        self.endpoint_address = os.path.join(client.server_address, 'clusters', cluster_name, 'nodes')

    def list(self):
        return self.client._make_request('post', url=f"{self.endpoint_address}/list").json()["nodes"]

    def add(self, name: str, node_id: str):
        json = {
            'name': name,
            'node_id': node_id,
            'version': 'V021',
        }
        return self.client._make_request('post', url=f"{self.endpoint_address}/add", json=json)

    def remove(self, name: str):
        json = {
            'name': name,
            'version': 'V021',
        }
        return self.client._make_request('post', url=f"{self.endpoint_address}/remove", json=json)

    def rename(self, name_or_id: str, new_name: str):
        node = next(node for node in self.list() if node['name'] == name_or_id or node['id'] == name_or_id)
        self.remove(node['name'])
        self.add(new_name, node['id'])


class ClusterClient:
    def __init__(self, client: 'FairClient', cluster_name: str):
        self.client = client
        self.cluster_name = cluster_name

    @property
    def nodes(self) -> ClusterNodesClient:
        return ClusterNodesClient(self.client, self.cluster_name)


class FairClient:
    def __init__(self,
                 server_address='https://faircompute.com:8000',
                 user_email: Optional[str] = None,
                 user_password: Optional[str] = None):
        self.token = None
        self.server_address = os.path.join(server_address, 'api/v0')
        if user_email is None:
            user_email = os.environ.get('FAIRCOMPUTE_USER_EMAIL')
        if user_password is None:
            user_password = os.environ.get('FAIRCOMPUTE_USER_PASSWORD')
        self.authenticate(user_email, user_password)

    def authenticate(self, user_email: str, user_password: str):
        url = f'{self.server_address}/auth/login'
        json = {"email": user_email, "password": user_password, "version": "V018"}
        resp = requests.post(url, json=json)
        if not resp.ok:
            raise Exception(f"Error! status: {resp.status_code}")
        self.token = resp.json()["token"]

    def _make_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }

    def _make_request(self, method, url, **kwargs) -> requests.Response:
        response = requests.request(method, url, headers=self._make_headers(), **kwargs)
        if not response.ok:
            raise Exception(f"{response.reason}: {response.text}")
        return response

    def run(self,
            image: str,
            command: Sequence[str] = tuple(),
            ports: Sequence[tuple[int, int]] = tuple(),
            volumes: Sequence[tuple[str, str]] = tuple(),
            runtime: str = 'docker',
            network: str = 'bridge',
            cluster_name: str = 'default',
            node_name: Optional[str] = None,
            detach: bool = False):
        if node_name is None or node_name == 'any':
            nodes = self.cluster().nodes.list()
            if len(nodes) == 0:
                raise Exception(f"No nodes found")
            node_name = random.choice(nodes)['name']
        return self._run_program(cluster_name, node_name, image, command, ports=ports, runtime=runtime,
                                 network=network, volumes=volumes, detach=detach)

    def _run_program(self,
                     cluster_name: str,
                     node_name: str,
                     image: str,
                     command: Sequence[str] = tuple(),
                     ports: Sequence[tuple[int, int]] = tuple(),
                     volumes: Sequence[tuple[str, str]] = tuple(),
                     runtime: str = 'docker',
                     network: str = 'bridge',
                     detach: bool = False):
        commands = [
            {
                'type': 'Create',
                'container_desc': {
                    'image': image,
                    'runtime': runtime,
                    'ports': [[{"port": host_port, "ip": 'null'}, {"port": container_port, "protocol": "Tcp"}] for (host_port, container_port) in ports],
                    'command': command,
                    'host_config': {
                        'network_mode': network
                    }
                },
            },
            *[
                {
                    'type': 'CopyInto',
                    'container_id': '$0',
                    'bucket_id': (1 << 64) - 1,
                    'remote_key': remote_path,  # we use remote_path as key to reference the file in the bucket
                                                # key is an arbitrary string
                    'local_path': remote_path
                }
                for _, remote_path in volumes
            ],
            {
                'type': 'Start',
                'container_id': '$0',
            },
        ]
        if not detach:
            commands.append({
                'type': 'Wait',
                'container_id': '$0',
            })

        resp = self.put_program(cluster_name, node_name, commands)
        program_id = resp['program_id']
        bucket_id = resp['bucket_id']

        for local_path, remote_path in volumes:
            with open(local_path) as f:
                data = f.read()
                self.put_file_data(bucket_id=bucket_id, file_name=remote_path, data=data)
                self.put_file_eof(bucket_id=bucket_id, file_name=remote_path)

        # upload stdin (empty for now)
        self.put_file_eof(bucket_id, '#stdin')

        # wait for program to get scheduled
        while True:
            program_info = self.get_program_info("default", node_name, program_id)
            if program_info['status'] in ('Queued', 'NotResponding'):
                sleep(POLL_TIMEOUT)
            elif program_info['status'] in ('Processing', 'Completed'):
                break
            else:
                raise RuntimeError("Unexpected program status: {}".format(program_info['status']))

        if detach:
            return program_info
        else:
            self._poll_output(bucket_id)

            # wait for job to complete
            while True:
                job = self.get_program_info(cluster_name, node_name, program_id)
                if job['status'] == 'Completed':
                    break
                else:
                    sleep(POLL_TIMEOUT)

            # get result
            return self.get_program_result(cluster_name, node_name, program_id)

    def _poll_output(self, bucket_id: int):
        # print stdout and stderr
        stdout_data = self.get_file_data(bucket_id, '#stdout')
        stderr_data = self.get_file_data(bucket_id, '#stderr')
        while stdout_data is not None or stderr_data is not None:
            data_received = False
            if stdout_data:
                try:
                    data = next(stdout_data)
                    if data:
                        sys.stdout.write(data.decode('utf-8'))
                        data_received = True
                except StopIteration:
                    stdout_data = None
            if stderr_data:
                try:
                    data = next(stderr_data)
                    if data:
                        sys.stderr.write(data.decode('utf-8'))
                        data_received = True
                except StopIteration:
                    stderr_data = None

            if not data_received:
                sleep(POLL_TIMEOUT)

    def put_program(self,
                    cluster_name: str,
                    node_name: str,
                    commands: Sequence[dict]):
        json = {
            'version': 'V018',
            'commands': commands,
        }
        return self._make_request('put', url=f"{self.server_address}/clusters/{cluster_name}/nodes/{node_name}/programs", json=json).json()

    def get_program_info(self, cluster_name: str, node_name: str, program_id: int):
        return self._make_request('get', url=f"{self.server_address}/clusters/{cluster_name}/nodes/{node_name}/programs/{program_id}/info").json()

    def get_file_data(self, bucket_id: int, file_name: str):
        session = requests.Session()
        with session.get(url=f"{self.server_address}/buckets/{bucket_id}/{quote_plus(file_name)}", headers=self._make_headers(), stream=True) as resp:
            for line in resp.iter_lines():
                yield line

    def put_file_data(self, bucket_id: int, file_name: str, data: Union[str, bytes]):
        return self._make_request('put', url=f"{self.server_address}/buckets/{bucket_id}/{quote_plus(file_name)}", data=data)

    def put_file_eof(self, bucket_id: int, file_name: str):
        return self._make_request('put', url=f"{self.server_address}/buckets/{bucket_id}/{quote_plus(file_name)}/eof")

    def get_program_result(self, cluster_name: str, node_name: str, program_id: int):
        resp = self._make_request('get', url=f"{self.server_address}/clusters/{cluster_name}/nodes/{node_name}/programs/{program_id}/result").json()
        return resp['result'][-1]['Ok']['exit_code']

    def cluster(self, name: str = 'default') -> ClusterClient:
        return ClusterClient(self, name)

    @property
    def clusters(self) -> ClustersClient:
        return ClustersClient(self)
