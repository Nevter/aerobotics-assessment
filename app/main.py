import markdown
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import requests
import os
from app.orchard_utils import *

app = FastAPI()
app.mount("/assets", StaticFiles(directory="assets"), name="assets")

base_url = "https://sherlock.aerobotics.com/developers"
API_KEY = os.getenv('API_KEY')
HOST_NAME = os.getenv('HOSTNAME')

@app.get("/")
def read_root():
    
    with open('./README.md', 'r') as file:
      readme_md = file.read()

    # Convert the input to HTML
    readme = markdown.markdown(readme_md)

    html_content = f"""
    <html>
        <head>
            <title>Aerobotics Assignment</title>
        </head>
        <body>
            {readme}
        </body>
    </html>
    """

    img_str = f"![img](http://{HOST_NAME}:8000/"
    html_content = html_content.replace("![img](", img_str)

    return HTMLResponse(content=html_content, status_code=200)

@app.get("/orchards/{orchard_id}/missing-trees")
def orchard_missing_trees(orchard_id: int):

    # Print to stdout instead of logging for now
    print(f"Requst to find missing trees in orchard {orchard_id}")

    survey_content = call_aerobotics_api(path="treesurveys/", params={"survey__orchard_id": orchard_id})
    
    print("Retrieved latest orchard survey")

    results = survey_content.json()['results']
    all_trees = [(float(s['latitude']), float(s['longitude'])) for s in results]

    # Get slope and distance between trees on both axes in the orchard
    features = get_orchard_features(all_trees)

    # Find missing trees
    missing_trees = find_missing_trees(all_trees, features)

    # Group missing trees
    missing_tree_groups = find_tree_groups(missing_trees, min_group_size=3, precision=2.5)

    # Find average loc of missing trees
    missing_tree_coords = [find_center_coord(missing_tree_group) for missing_tree_group in missing_tree_groups]

    response = {
        "orchard_id": orchard_id,
        "missing_trees": [{"lat":lat,"lng":lng} for lat,lng in missing_tree_coords]
        }

    print(f"Response: {response}")

    return response

def call_aerobotics_api(path: str, params: dict): 
    return requests.get(
        f"{base_url}/{path}",
        params=params,
        headers={"Authorization": API_KEY, 
                 "accept": "application/json"})