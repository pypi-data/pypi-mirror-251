import docker
import grpc
import inspect
import json
import os

from concurrent import futures
from docker.types import Mount

from .protos import common_pb2
from .protos import connector_sdk_pb2
from .protos import connector_sdk_pb2_grpc


DOCKER_IMAGE_NAME = "it5t/fivetran-sdk-connector-tester"
DOCKER_IMAGE_VERSION = "024.0118.003"
DOCKER_CONTAINER_NAME = "fivetran_connector_tester"


def upsert(table: str, data):
    __yield_check(inspect.stack())

    # TODO: Map to appropriate data types, not just string

    mapped_data = {}
    for key in data.keys():
        mapped_data[key] = common_pb2.ValueType(string=str(data[key]))

    record = connector_sdk_pb2.Record(
        table_name=table,
        type="UPSERT",
        data=mapped_data
    )

    return connector_sdk_pb2.UpdateResponse(
        operation=connector_sdk_pb2.Operation(record=record))


def update(table: str, modified: dict, schema_name: str = None):
    __yield_check(inspect.stack())
    # TODO


def delete(table: str, primary_key: set, schema_name: str = None):
    __yield_check(inspect.stack())
    # TODO


def truncate(table: str, schema_name: str = None):
    __yield_check(inspect.stack())
    # TODO


def checkpoint(state: dict):
    __yield_check(inspect.stack())
    return connector_sdk_pb2.UpdateResponse(
             operation=connector_sdk_pb2.Operation(checkpoint=connector_sdk_pb2.Checkpoint(
                 state_json=json.dumps(state))))


def __yield_check(stack):
    called_method = stack[0].function
    calling_code = stack[1].code_context[0]
    if f"{called_method}(" in calling_code:
        if 'yield' not in calling_code:
            print(f"ERROR: Please add 'yield' to '{called_method}' operation on line {stack[1].lineno} in file '{stack[1].filename}'")
            os._exit(1)
    else:
        # This should never happen
        raise RuntimeError(f"Unable to find '{called_method}' function in stack")


class Connector(connector_sdk_pb2_grpc.ConnectorServicer):
    def __init__(self, update, schema=None):
        self.schema_method = schema
        self.update_method = update

        self.configuration = None
        self.state = None
        self.tables = {}


    # Call this method to deploy the connector to Fivetran platform
    def deploy(self, deploy_key):
        print("This feature is under development")


    # Call this method to run the connector in production
    def serve(self, port: int = 50051):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        connector_sdk_pb2_grpc.add_ConnectorServicer_to_server(self, server)
        server.add_insecure_port("[::]:" + str(port))
        server.start()
        print("Connector started, listening on " + str(port))
        return server


    # This method starts both the server and the local testing environment
    def debug(self, port: int = 50051, project_path: str = os.getcwd(), state: str = None, configuration: str = None) -> bool:
        if configuration: self.configuration = json.loads(configuration)
        if state: self.state = json.loads(state)

        docker_client = docker.from_env()
        server = self.serve()
        # server.wait_for_termination()  # Uncomment this to run the tester manually

        image = f"{DOCKER_IMAGE_NAME}:{DOCKER_IMAGE_VERSION}"
        result = docker_client.images.list(image)
        if not result:
            # Pull the image from docker hub if it is missing
            docker_client.images.pull(DOCKER_IMAGE_NAME, DOCKER_IMAGE_VERSION)

        error = False
        try:
            for container in docker_client.containers.list(all=True):
                if container.name == DOCKER_CONTAINER_NAME:
                    if container.status == "running":
                        container.stop()
                    else:
                        container.remove()
                    break

            working_dir = os.path.join(project_path, "files")
            try:
                os.mkdir(working_dir)
            except FileExistsError:
                pass

            container = docker_client.containers.run(
                image=image,
                name=DOCKER_CONTAINER_NAME,
                command="--custom-sdk=true",
                mounts=[Mount("/data", working_dir, read_only=False, type="bind")],
                network="host",
                remove=True,
                detach=True,
                environment=["GRPC_HOSTNAME=host.docker.internal"])

            for line in container.attach(stdout=True, stderr=True, stream=True):
                msg = line.decode("utf-8")
                print(msg, end="")
                if ("Exception in thread" in msg) or ("SEVERE:" in msg):
                    error = True

        finally:
            server.stop(grace=2.0)
            return (not error)

    # -- Methods below override ConnectorServicer methods
    def ConfigurationForm(self, request, context):
        if not self.configuration:
            self.configuration = {}

        # Not going to use the tester's configuration file
        return common_pb2.ConfigurationFormResponse()


    def Test(self, request, context):
        return None


    def Schema(self, request, context):
        if self.schema_method:
            response = self.schema_method(self.configuration)

            for entry in response:
                if 'table' not in entry:
                    print("ERROR: Entry missing table name: " + entry)
                    os._exit(1)

                table_name = entry['table']

                if table_name in self.tables:
                    print("ERROR: Table already defined: " + table_name)
                    os._exit(1)

                table = common_pb2.Table(name=table_name)
                columns = {}

                if "primary_key" not in entry:
                    print("ERROR: Table requires at least one primary key: " + table_name)
                    os._exit(1)

                for pkey_name in entry["primary_key"]:
                    column = columns[pkey_name] if pkey_name in columns \
                                                else common_pb2.Column(name=pkey_name)
                    column.primary_key = True
                    columns[pkey_name] = column

                if "columns" in entry:
                    for column_name in entry["columns"]:
                        column = columns[column_name] if column_name in columns \
                                                      else common_pb2.Column(name=column_name)

                        # TODO: Map column types entry['columns'][column_name] to common_pb2.Column

                        if column_name in entry["primary_key"]:
                            column.primary_key = True

                        columns[column_name] = column

                table.columns.extend(columns.values())
                self.tables[table_name] = table

            return connector_sdk_pb2.SchemaResponse(without_schema=common_pb2.TableList(tables=self.tables.values()))

        else:
            return connector_sdk_pb2.SchemaResponse(schema_response_not_supported=True)


    def Update(self, request, context):
        state = self.state if self.state else json.loads(request.state_json)

        try:
            for resp in self.update_method(configuration=self.configuration, state=state):
                yield resp
        except TypeError as e:
            if str(e) != "'NoneType' object is not iterable":
                raise e
