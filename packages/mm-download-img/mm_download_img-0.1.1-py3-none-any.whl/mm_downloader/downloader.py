import requests
import cv2
import os

def get_s3_path(path):
    url = f"https://s.mservice.io/internal/wedjat-portal/v1/pending/get-public-image-link?imagePath={path}"
    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)
    image_url = response.json()['data']['link']
    return image_url

def download(filename, path):
    """

    Args:
        filename (str): saved filename
        path (str): image s3 path
    """
    if os.path.isfile(filename):
            print("File existed")
    else:
        print("Start request for image", path)
        image_url = get_s3_path(path)
            
        try:
            r = requests.get(image_url, allow_redirects=True, timeout=10)
        except requests.ConnectionError as e:
            print("OOPS!! Connection Error Image API")
            return
        except requests.Timeout as e:
            print("OOPS!! Timeout Error Image API")
            return
        except requests.RequestException as e:
            print("OOPS!! General Error")
            return
        if r != "":
            open(filename, "wb").write(r.content)
            try:
                a = cv2.imread(filename).shape
                if len(a) != 3:
                    print("OOPS!! An image is error -> Delete")
                    os.system(f"rm -rf {filename}")
            except Exception as e:
                print(e)
                print("OOPS!! An image is error -> Delete")
                os.system(f"rm -rf {filename}")


        
