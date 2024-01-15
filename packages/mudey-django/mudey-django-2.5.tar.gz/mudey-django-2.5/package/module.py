import argparse
import subprocess
import pathlib
from pathlib import Path





# The directory containing this file
BASE_DIR = pathlib.Path(__file__).parent.parent




def start(file_path, args):
    subprocess.run(["python", Path(BASE_DIR / file_path ), args.app_name, args.model_name])


    
def make_project(args):
    print(f"Executing create:project command for {args.project_name}")
    # generate_entity()
    subprocess.run(["python", 
                    Path(BASE_DIR / "package/create_django_project.py" ), 
                    args.project_name])
    
def make_app(args):
    print(f"Executing create:app command for app: {args.app_name}.")
    # generate_entity()
    subprocess.run(["python", 
                    Path(BASE_DIR / "package/generate_django_app.py" ), 
                    args.app_name])
    
def make_entity(args):
    print(f"Executing make:entity command for app: {args.app_name} and model: {args.model_name}.")
    # generate_entity()
    start("package/model_generator.py", args)
    start("package/view_generator.py", args)
    start("package/template_generator.py", args)

def make_form(args):
    print(f"Executing make:form command for app: {args.app_name} and model: {args.model_name}")
    start("package/form_generator.py", args)

def make_view(args):
    print(f"Executing make:view command for app: {args.app_name} and model: {args.model_name}")
    start("package/view_generator.py", args)
    start("package/template_generator.py", args)
    
def make_model(args):
    print(f"Executing make:model command for app: {args.app_name} and model: {args.model_name}")
    start("package/model_generator.py", args)

def make_entity_crud(args):
    print(f"Executing make:crud command for app: {args.app_name} and model: {args.model_name}.")
    start("package/from_generator.py", args)
    start("package/view_generator.py", args)
    start("package/template_generator.py", args)
    
def make_service(args):
    print(f"Executing make:service command for app: {args.app_name} and service: {args.service_name}.")
 
    subprocess.run(["python", 
                    Path(BASE_DIR / "package/ecommerce_generator.py" ), 
                    args.app_name, args.service_name])

def main():
    parser = argparse.ArgumentParser(description="Custom CLI for performing tasks")
    subparsers = parser.add_subparsers()

    entity_parser = subparsers.add_parser("create:project", help="Create an django project")
    entity_parser.add_argument("project_name", help="Name of the project")
    entity_parser.set_defaults(func=make_project)
    
    entity_parser = subparsers.add_parser("create:app", help="Create an django application")
    entity_parser.add_argument("app_name", help="Name of the app")
    entity_parser.set_defaults(func=make_app)

    entity_parser = subparsers.add_parser("make:entity", help="Create an entity")
    entity_parser.add_argument("app_name", help="Name of the app")
    entity_parser.add_argument("model_name", help="Name of the model")
    entity_parser.set_defaults(func=make_entity)

    form_parser = subparsers.add_parser("make:form", help="Create a form")
    form_parser.add_argument("app_name", help="Name of the app")
    form_parser.add_argument("model_name", help="Name of the model")
    form_parser.set_defaults(func=make_form)
    
    model_parser = subparsers.add_parser("make:model", help="Create a model")
    model_parser.add_argument("app_name", help="Name of the app")
    model_parser.add_argument("model_name", help="Name of the model")
    model_parser.set_defaults(func=make_model)
    
    view_parser = subparsers.add_parser("make:view", help="Create a view")
    view_parser.add_argument("app_name", help="Name of the app")
    view_parser.add_argument("model_name", help="Name of the model")
    view_parser.set_defaults(func=make_view)

    entity_crud_parser = subparsers.add_parser("make:crud", help="Create CRUD for an entity")
    entity_crud_parser.add_argument("app_name", help="Name of the app")
    entity_crud_parser.add_argument("model_name", help="Name of the model")
    entity_crud_parser.set_defaults(func=make_entity_crud)
    
    service_parser = subparsers.add_parser("make:service", help="Generate a Django e-commerce services")
    service_parser.add_argument("app_name", help="Name of the app")
    service_parser.add_argument("service_name", help="Name of the service")
    service_parser.set_defaults(func=make_service)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)


if __name__ == "__main__":
    main()