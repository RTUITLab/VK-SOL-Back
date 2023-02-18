import uvicorn
from fastapi import FastAPI, File, UploadFile, status, Header, Request, Depends, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from models.Event import Event
from pinata import Pinata
import requests
from base64 import b64decode, b64encode
import pymongo
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os.path as path
import os
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder

pinata_api_key = "759216f279deb902f362"
pinata_secret_api_key = "be4a3be565d0f7fb22f1771cf703daf0acde0603fc32fe637e21207656b03747"
pinata_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJlZjc5YzJlNC0xZWQ3LTQwODMtOTY2NC1hZjdiY2NmNTY1MDkiLCJlbWFpbCI6InNhc2hhbGV2MjAwMTQ5QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImlkIjoiRlJBMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfSx7ImlkIjoiTllDMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiI3NTkyMTZmMjc5ZGViOTAyZjM2MiIsInNjb3BlZEtleVNlY3JldCI6ImJlNGEzYmU1NjVkMGY3ZmIyMmYxNzcxY2Y3MDNkYWYwYWNkZTA2MDNmYzMyZmU2MzdlMjEyMDc2NTZiMDM3NDciLCJpYXQiOjE2NzY2MjcyOTh9.zK9vnyOf_61DtxMSszIJyGvzcf-OtjdFGZwws-e4uUA"

pinata = Pinata(pinata_api_key, pinata_secret_api_key, pinata_access_token)

import subprocess
solana_addr = str(subprocess.check_output(['solana', 'address'])).split('\'')[1].split('\\')[0]
print(solana_addr)
print(solana_addr)

app = FastAPI()
UU = []
UU.append(1)

URL = "https://9302-193-41-142-48.ngrok.io"

back_path = path.abspath(path.join(__file__, "../")
                         ).replace("\\", "/") + '/zero_images'
pwd = back_path+"/"
app.mount("/img", StaticFiles(directory=back_path), name="img")

DB_URL = os.getenv('DB_URL', 'localhost')
client = MongoClient(f'mongodb://{DB_URL}:27017/')
db = client['back']

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api")
async def getAll():
    # response = pinata.pin_file("IMG_0816-222.png")
    print(back_path+" !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


@app.get("/api/createFolder")
async def createFolder(path):
    if (os.path.exists(back_path+"/"+path)):
        return "Lox"
    else:
        os.mkdir(back_path+"/"+path)
        return back_path+"/"+path


@app.get("/api/ngrog")
async def setNgrogUrl(url=""):
    URL = url
    return requests.get(URL+"/robots.txt").status_code


@app.get("/api/allPined")
async def getAllPined():
    response = pinata.get_pins()
    return response


@app.get("/api/txt2img")
async def getTxt2Img(text="pixel Cat", steps="20", load: bool = False, filename="foo.png"):
    res = requests.post(URL+'/sdapi/v1/txt2img', headers={
                        "Content-Type": 'application/json'}, json={"prompt": text, "steps": steps})
    if (load == False):
        with open(pwd+filename, "wb") as f:
            f.write(b64decode(res.json()["images"][0]))
        return FileResponse(pwd+filename)
    else:
        response = pinata.pin_file(pwd+filename)
        return {"URL": "https://gateway.pinata.cloud/ipfs/"+response['data']['IpfsHash'], "IMG": res.json()["images"][0]}


@app.get("/api/img2img")
async def getImg2Img(init_image=None, mask=None, text="a poster of a stadium with a blue light shining on it's side and the words RAMMSTEIN on it, a poster, international typographic style", steps="30", load: bool = False, filename="foo.png"):
    if (init_image == None):
        with open(pwd+"Ramm.jpg", "rb") as f:
            img1 = f.read()
            UU[0] = b64encode(img1).decode()
    if (mask == None):
        with open(pwd+"Ramm_mask_wb.jpg", "rb") as f:
            img1 = f.read()
            YY = b64encode(img1).decode()
    res = requests.post(URL+'/sdapi/v1/img2img', headers={"Content-Type": 'application/json'}, json={
        "init_images": UU,
        "mask_blur": 4,
        "prompt": text,
        "mask": YY,
        "negative_prompt": "ugly",
        "steps": steps,
        "inpaint_full_res_padding": 0,
        "inpainting_mask_invert": 0,
        "inpainting_fill": 1,
        "sd_model_checkpoint": "realisticVisionV12_v12inpainting.ckpt [5f929c741f]",
        "denoising_strength": 0.50,
        "cfg_scale": 19,
        "sampler_index": "DPM++ 2S a",
        "inpainting_mask_weight": 1,
        "initial_noise_multiplier": 1,
        "img2img_color_correction": False,
        "img2img_fix_steps": False,
        "img2img_background_color": "#000000",
        "include_init_images": True})
    with open(pwd+filename, "wb") as f:
        f.write(b64decode(res.json()["images"][0]))
    if (load == False):
        return FileResponse(pwd+filename)
    else:
        response = pinata.pin_file(pwd+filename)
        return {"URL": "https://gateway.pinata.cloud/ipfs/"+response['data']['IpfsHash'], "IMG": res.json()["images"][0]}


@app.post("/api/img2img")
async def getImg2Imgpost(request: Request, load: bool = False, filename="foo.png"):
    item = await request.json()
    res = requests.post(URL+'/sdapi/v1/img2img', headers={"Content-Type": 'application/json'}, json={
        "init_images": item['init_image'],
        "mask_blur": 4,
        "prompt": item["text"],
        "mask": item["mask"],
        "negative_prompt": "ugly",
        "steps": item["steps"],
        "inpaint_full_res_padding": 0,
        "inpainting_mask_invert": 0,
        "inpainting_fill": 1,
        "sd_model_checkpoint": "realisticVisionV12_v12inpainting.ckpt [5f929c741f]",
        "denoising_strength": 0.50,
        "cfg_scale": 19,
        "sampler_index": "DPM++ 2S a",
        "inpainting_mask_weight": 1,
        "initial_noise_multiplier": 1,
        "img2img_color_correction": False,
        "img2img_fix_steps": False,
        "img2img_background_color": "#000000",
        "include_init_images": True})
    with open(pwd+filename, "wb") as f:
        f.write(b64decode(res.json()["images"][0]))
    if (load == False):
        return FileResponse(pwd+filename)
    else:
        response = pinata.pin_file(pwd+filename)
        return {"URL": "https://gateway.pinata.cloud/ipfs/"+response['data']['IpfsHash'], "IMG": res.json()["images"][0]}


@app.post("/api/saveData")
async def saveData(request: Request, db_name="files_meta"):
    item = await request.json()
    posts = db[db_name]
    post_id = posts.insert_one(item).inserted_id
    return {"name": str(post_id)}

@app.put("/api/putData")
async def putData(request: Request, db_name="files_meta"):
    return "comming soon"

@app.delete("/api/delData")
async def delData(request: Request, db_name="files_meta"):
    item = await request.json()
    posts = db[db_name]
    if "_id" in item:
        item["_id"] = ObjectId(item["_id"])
    posts.delete_one(item)
    arr = []
    element = posts.find({})
    for document in element:
        print(document)
        document["_id"] = str(document["_id"])
        arr.append(document)
    return {"size": len(arr), 'data': arr}

@app.get("/api/unPin")
async def unPin(id):
    response = pinata.unpin_file(id)
    return response


@app.get("/api/getData")
async def getData(db_name="files_meta", id=None):
    if id == None:
        posts = db[db_name]
        arr = []
        element = posts.find({})
        for document in element:
            print(document)
            document["_id"] = str(document["_id"])
            arr.append(document)
        return {"size": len(arr), 'data': arr}
    else:
        id = ObjectId(id)
        posts = db[db_name]
        element = posts.find_one({'_id': id})
        element["_id"] = str(element["_id"])
        return element


@app.get('/api/folderContent', name="Allow to get folders and files in directory")
async def getFiles(path=""):
    """Allow to get folders and files in directory"""
    arr = []
    if not os.path.exists(back_path):
        return "Lox"

    for entry in os.scandir(back_path + path):
        status = -1
        if entry.is_dir():
            t = 'dir'
        elif entry.is_file():
            t = 'file'
            if entry.name.split('.')[-1] == 'svs':
                # posts = db['files_meta']
                # resp = posts.find_one({'path': path+'/'+entry.name})
                # print(resp)
                # if not resp == None:
                #     status = resp['status']
                status = 100

        elif entry.is_symlink():
            t = 'link'
        else:
            t = 'unknown'

        if entry.name.isdigit():
            arr.append({'name': "Папка "+entry.name,
                       'type': t, 'status': status})
        else:
            arr.append({'name': entry.name, 'type': t, 'status': status})
    return arr


@app.post('/api/event', tags=['events'])
async def create_new_event(event: Event):
    # Save to database
    event.white_list = []
    jsonable_event = jsonable_encoder(event)
    result_id = str(db.events.insert_one(jsonable_event).inserted_id)

    # Create images for solana
    base_path = back_path + '/' + result_id
    base_path_assets = base_path + '/assets'
    os.mkdir(base_path)
    os.mkdir(base_path_assets)

    for i in range(event.amount):
        f = open(f'{base_path_assets}/{i}.json', "a")
        f.write(f'{{\n	"name": "Ticket {i}",\n	"symbol": "TCKT",\n	"description": "Collection of {event.amount} tickets",\n	"image": "{i}.png",\n	"attributes": [],\n	"properties": {{\n		"files": [\n			{{\n				"uri": "{i}.png",\n				"type": "image/png"\n			}}\n		]\n	}}\n}}\n')
        f.close()

        await getTxt2Img(text=event.name, steps="20", load=False, filename=f"{result_id}/assets/{i}.png")

    # Create collection cover
    f = open(f'{base_path_assets}/collection.json', "a")
    f.write(f'{{\n	"name": "Tickets Collection",\n	"symbol": "TCKT",\n	"description": "Collection of {event.amount} tickets",\n	"image": "collection.png",\n	"attributes": [],\n	"properties": {{\n		"files": [\n			{{\n				"uri": "collection.png",\n				"type": "image/png"\n			}}\n		]\n	}}\n}}\n')
    f.close()
    await getTxt2Img(text=f'{event.name} collection', steps="20", load=False, filename=f"{result_id}/assets/collection.png")

    # Create collection config
    f = open(f'{base_path}/config.json', "a")
    pinata_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI0ZThiYzgyMy00OTBjLTQ0M2ItYWUyZi00MzkwYjg2NGQ0NjgiLCJlbWFpbCI6IjBpbHlhQGJrLnJ1IiwiZW1haWxfdmVyaWZpZWQiOnRydWUsInBpbl9wb2xpY3kiOnsicmVnaW9ucyI6W3siaWQiOiJGUkExIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9LHsiaWQiOiJOWUMxIiwiZGVzaXJlZFJlcGxpY2F0aW9uQ291bnQiOjF9XSwidmVyc2lvbiI6MX0sIm1mYV9lbmFibGVkIjpmYWxzZSwic3RhdHVzIjoiQUNUSVZFIn0sImF1dGhlbnRpY2F0aW9uVHlwZSI6InNjb3BlZEtleSIsInNjb3BlZEtleUtleSI6IjA5ODY3MmIwMGRiNWE4MGFmY2Q4Iiwic2NvcGVkS2V5U2VjcmV0IjoiZDJiYzBhNmFmZmY0MGEwNTdkNzc4OGU1ZDRmMjllYzg1YzhjNmE5Y2M5MDgzNmM3YTE2ODkxYjAyZDRmZTA4NiIsImlhdCI6MTY3NjY0NDQ0Mn0.2EVkLNwR5z1ctyUib0q0q42lXmi4V2ow2MZtWXAxH58"
    f.write(f'{{\n	"price": 0,\n	"number": {event.amount},\n	"sellerFeeBasisPoints": 0,\n	"symbol": "TCKT",\n	"isMutable": true,\n	"isSequential": false,\n	"creators": [\n		{{\n			"address": "{solana_addr}",\n			"share": 100\n		}}\n	],\n	"uploadMethod": "pinata",\n	"awsConfig": null,\n	"nftStorageAuthToken": null,\n	"shdwStorageAccount": null,\n	"pinataConfig": {{\n		"jwt": "{pinata_access_token}",\n		"apiGateway": "https://api.pinata.cloud",\n		"contentGateway": "https://gateway.pinata.cloud",\n		"parallelLimit": 1\n	}},\n	"hiddenSettings": null,\n	"retainAuthority": true,\n	"guards": null\n}}\n\n')
    f.close()

    # Publish collection
    os.system(f'sh -c "cd {base_path} && sugar validate && sugar upload && sugar deploy"')

    db.events.find_one_and_update({'_id': ObjectId(result_id)}, {'$set': {'cover': f'/img/{result_id}/assets/collection.png'}})

    return {"id": str(result_id)}


@app.get('/api/event', tags=['events'])
def get_all_events() -> list[Event]:
    result = []
    for event in db.events.find():
        event['_id'] = str(event['_id'])
        result.append(event)
    return result


@app.get('/api/event/{id}', tags=['events'])
def get_event_by_id(id: str):
    result = db.events.find_one({'_id': ObjectId(id)})
    result['_id'] = str(result['_id'])
    return result


