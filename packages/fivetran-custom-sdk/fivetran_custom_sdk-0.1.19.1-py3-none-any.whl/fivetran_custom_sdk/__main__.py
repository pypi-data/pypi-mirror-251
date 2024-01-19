import argparse
import importlib.util
import sys

parser = argparse.ArgumentParser()

# Positional
parser.add_argument("project_path", help="Folder path for the connector project")

# Optional (Not all of these are valid with every mutually exclusive option below)
parser.add_argument("--port", "-p", type=int, default=50051, help="Provide port number to run gRPC server")
parser.add_argument("--state", "-s", type=str, default="", help="Provide json state")
parser.add_argument("--config", "-c", type=str, default="", help="Provide json configuration")
parser.add_argument("--key", type=str, default="", help="Provide deploy key")

# Mutually exclusive
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument("--deploy", action="store_true", help="Deploy the connector")
group.add_argument("--debug", action="store_true", help="Debug the connector")
group.add_argument("--run", action="store_true", help="Run the connector")

args = parser.parse_args()

module_name = "custom_connector_code"
spec = importlib.util.spec_from_file_location(module_name, args.filepath)
module = importlib.util.module_from_spec(spec)
sys.modules[module_name] = module
spec.loader.exec_module(module)
connector_object = None
for obj in dir(module):
    if not obj.startswith('__'):  # Exclude built-in attributes
        obj_attr = getattr(module, obj)
        if '<fivetran_custom_sdk.Connector object at' in str(obj_attr):
            connector_object = obj_attr
            break

if not connector_object:
    print("Unable to find connector object")
    sys.exit(1)

# TODO: Read optional args from CLI args or ENV vars

if args.deploy:
    print(f"Deploying connector: {args.project_path}")
    connector_object.deploy(args.deploy_key)
elif args.run:
    print(f"Running connector: {args.project_path}")
    connector_object.run()
elif args.test:
    print(f"Debugging connector: {args.project_path}")
    # TODO: secrets
    # TODO: state
    connector_object.debug(args.port, args.project_path)
else:
    # This should never happen due to required group
    raise NotImplementedError("Unexpected state")