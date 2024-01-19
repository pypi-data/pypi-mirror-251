import requests
import base64
import json
from PIL import Image as PilImage
import io
# from ..config import base_url, api_token

base_url = "https://dev-aicloud-gateway.logicplum.com/api/v2"
api_token = "i6DmueJGRHw1UYVcyKXmjSprOEWDRtCC7oqxJKuKzz7wXcAHHO9UPUQLlWt23AHx"

def display_response(res_type, response):
    if res_type == 'base64':
        return response
    else:
        # Check if the response is bytes (for 'image' type)
        if isinstance(response, bytes) and (response.startswith(b'\x89PNG') or response.startswith(b'\xff\xd8\xff\xe0')):
            # Open the image
            image = PilImage.open(io.BytesIO(response))
            
            # Convert image to RGB mode if it has an alpha channel
            if image.mode == 'RGBA':
                image = image.convert('RGB')

            # Display the image
            return image
        else:
            # Handle the case when response is not bytes as expected for 'image' type
            response_dict = json.loads(response.decode('utf-8'))
            return response_dict

def roc_plot(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/roc"
    headers = {"Authorization":client_token}
    response = requests.post(url, data=data,headers=headers)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()


def advanced_lift_chart(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/advanced-lift-chart"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()


def advanced_feature_impact(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/advanced-feature-impact"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()


def partial_dependency(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/partial-dependency"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()




def residual(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/residual"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()



def predict_vs_actual(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/predict-vs-actual"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()


def word_cloud(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/wordcloud"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()


def confusion_matrix(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/confusion-matrix"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()


def get_allColumns(deployment_id,client_token):
    url = f"{base_url}/plot/dataset-columns//{deployment_id}"
    headers = {"Authorization":client_token}
    response = requests.get(url,headers=headers)
    return response.json()

def prediction_distribution(deployment_id,res_type,client_token):
    data = {
    "deployment_id": deployment_id,
    "res_type" : res_type 
    }
    url = f"{base_url}/plot/prediction-distribution"
    headers = {"Authorization":client_token}
    # Send the POST request
    response = requests.post(url, data=data,headers=headers)
    if data.get('res_type') == 'image':
        return response.content
    return response.json()

a = roc_plot("ff424a1a-acab-40eb-8987-41c13cfc4f19","base64","eyJuYW1lIjoiYWFiYiIsImVtYWlsIjoiYWFjY0B5b3BtYWlsLmNvbSJ9:1rGbLp:OOBiKlbYKo98hqXYSIc5U13Ls7CGE9bkbJHTtdRglPE")
print(a)