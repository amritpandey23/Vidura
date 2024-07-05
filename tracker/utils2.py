import os, json, uuid

def initialize_app(app, app_name="Vidura"):
    config = get_or_initialize_config(app, app_name=app_name)
    example_dates_json = """
    [
        {
            "title": "Birthday",
            "release": "2024",
            "date": "2024-09-23"
        }
    ]
    """
    example_notes_json = """
    [
        {
            "title": "Important Links",
            "content": [
                {
                    "label": "Github",
                    "value": "https://github.com/amritpandey23"
                }
            ]
        }
    ]
    """
    
    if config["db_initialized"] == "false":
        persist_config_json(app, "important_dates", example_dates_json)
        persist_config_json(app, "notes", example_notes_json)
        
    return config

def get_or_initialize_config(app, app_name = "Vidura"):
    config = fetch_config_json(app, "config")
    if config != None and config != "" and config != "{}":
        return json.loads(config)
    
    # start from scratch
    config = fetch_config_json(app, "example.config")
    
    config_dict = json.loads(config)
    
    ## setting site name
    config_dict["SITE_NAME"] = app_name
    
    ## setting database directory
    home_drive = os.environ.get('HOMEDRIVE', '')
    home_path = os.environ.get('HOMEPATH', '')
    db_directory = os.path.join(home_drive, home_path, config_dict["SITE_NAME"])
    os.makedirs(db_directory, exist_ok=True)
    db_directory = db_directory.replace('\\', '/')
    db_path = os.path.join(db_directory, 'site.db').replace('\\', '/')
    config_dict["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{db_path}'
    
    ## setting secret key
    random_uuid = uuid.uuid4()
    random_string = str(random_uuid)
    config_dict["SECRET_KEY"] = random_string
    
    config = json.dumps(config_dict, indent=4)
    
    ## saving content to the file
    persist_config_json(app, "config", config)
    return config_dict

def fetch_config_json(app, config_name):
    """
    Reads the content of a JSON file. If the file doesn't exist, it creates an empty JSON file and returns an empty string.

    :param app: flask app
    :param config_name: The name of the JSON file.
    :return: The content of the JSON file, or an empty string if the file is created.
    """
    if not config_name.endswith(".json"):
        config_name += ".json"

    config_name = os.path.join(app.root_path, "data", config_name)

    if os.path.exists(config_name):
        with open(config_name, "r") as file:
            content = file.read()
            return content if content else "{}"
    else:
        with open(config_name, "w") as file:
            json.dump({}, file)
        return "{}"


def persist_config_json(app, config_name, json_content):
    """
    Validates and saves JSON content to a file. If the file doesn't exist, it creates the file.

    :param app: flask app
    :param json_content: The JSON content to save.
    :param config_name: The name of the JSON file.
    :raises ValueError: If the JSON content is invalid.
    """
    if not config_name.endswith(".json"):
        config_name += ".json"

    config_name = os.path.join(app.root_path, "data", config_name)

    try:
        parsed_content = json.loads(json_content)
    except json.JSONDecodeError as e:
        raise ValueError("Invalid JSON content") from e

    with open(config_name, "w") as file:
        json.dump(parsed_content, file, indent=4)
        
        
def create_or_load_settings(app):
    config = fetch_config_json(app, "site_settings")
    if config == None or config == "" or config == "{}":
        home_drive = os.environ.get('HOMEDRIVE', '')
        home_path = os.environ.get('HOMEPATH', '')

        # Construct the full path to the desired location
        db_directory = os.path.join(home_drive, home_path, 'Vidura')
        os.makedirs(db_directory, exist_ok=True)

        # Ensure that the path uses forward slashes
        db_directory = db_directory.replace('\\', '/')

        # Define the full path to the site.db file
        db_path = os.path.join(db_directory, 'site.db').replace('\\', '/')
        config_dict = {}
        config_dict["SITE_NAME"] = "Vidura"
        config_dict["SECRET_KEY"] = "secret"
        config_dict["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{db_path}'
        config_json = json.dumps(config_dict, indent=4)
        persist_config_json(app, "site_settings", config_json)
        return config_json
    else:
        return config
    
