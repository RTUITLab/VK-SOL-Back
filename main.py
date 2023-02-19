from fastapi import FastAPI, status, Request, Body, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from models.Event import Event
from models.exchange import Exchange
from models.ticket import Ticket
from pinata import Pinata
import requests
from base64 import b64decode, b64encode
import json
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os.path as path
import os
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder
from secret import Secret
import threading
from fastapi.responses import HTMLResponse

pinata_api_key = "759216f279deb902f362"
pinata_secret_api_key = "be4a3be565d0f7fb22f1771cf703daf0acde0603fc32fe637e21207656b03747"
pinata_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJlZjc5YzJlNC0xZWQ3LTQwODMtOTY2NC1hZjdiY2NmNTY1MDkiLCJlbWFpbCI6InNhc2hhbGV2MjAwMTQ5QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwaW5fcG9saWN5Ijp7InJlZ2lvbnMiOlt7ImlkIjoiRlJBMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfSx7ImlkIjoiTllDMSIsImRlc2lyZWRSZXBsaWNhdGlvbkNvdW50IjoxfV0sInZlcnNpb24iOjF9LCJtZmFfZW5hYmxlZCI6ZmFsc2UsInN0YXR1cyI6IkFDVElWRSJ9LCJhdXRoZW50aWNhdGlvblR5cGUiOiJzY29wZWRLZXkiLCJzY29wZWRLZXlLZXkiOiI3NTkyMTZmMjc5ZGViOTAyZjM2MiIsInNjb3BlZEtleVNlY3JldCI6ImJlNGEzYmU1NjVkMGY3ZmIyMmYxNzcxY2Y3MDNkYWYwYWNkZTA2MDNmYzMyZmU2MzdlMjEyMDc2NTZiMDM3NDciLCJpYXQiOjE2NzY2MjcyOTh9.zK9vnyOf_61DtxMSszIJyGvzcf-OtjdFGZwws-e4uUA"

pinata = Pinata(pinata_api_key, pinata_secret_api_key, pinata_access_token)

async def create_new_event_back(event: Event):
    event.white_list = []
    event.minted = 0
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
    pinata_access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiI5Yzg0MGE3MC0zN2M4LTQ2MzktOWEyYi00ZjA5MDk5NWFjODciLCJlbWFpbCI6ImlseWFtZWRAcm8ucnUiLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGluX3BvbGljeSI6eyJyZWdpb25zIjpbeyJpZCI6IkZSQTEiLCJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MX0seyJpZCI6Ik5ZQzEiLCJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MX1dLCJ2ZXJzaW9uIjoxfSwibWZhX2VuYWJsZWQiOmZhbHNlLCJzdGF0dXMiOiJBQ1RJVkUifSwiYXV0aGVudGljYXRpb25UeXBlIjoic2NvcGVkS2V5Iiwic2NvcGVkS2V5S2V5IjoiM2U5M2YzY2Y4ZWY3ZTRlY2Y2Y2UiLCJzY29wZWRLZXlTZWNyZXQiOiI0NTE2YTlmMjYyZTdhYTNjMDMwNGJjZDM3MjIxOGRhMTc5ZWJhYjNiOTc2NWIxNDMyZWQxYTE0NWFmYzQwOTlmIiwiaWF0IjoxNjc2NzI0MTA4fQ._1Cus09qFl3XteBKL3qyL14-mAA0XH455XBM-uZypSs"
    f.write(f'{{\n	"price": 0,\n	"number": {event.amount},\n	"sellerFeeBasisPoints": 0,\n	"symbol": "TCKT",\n	"isMutable": true,\n	"isSequential": false,\n	"creators": [\n		{{\n			"address": "{solana_addr}",\n			"share": 100\n		}}\n	],\n	"uploadMethod": "pinata",\n	"awsConfig": null,\n	"nftStorageAuthToken": null,\n	"shdwStorageAccount": null,\n	"pinataConfig": {{\n		"jwt": "{pinata_access_token}",\n		"apiGateway": "https://api.pinata.cloud",\n		"contentGateway": "https://gateway.pinata.cloud",\n		"parallelLimit": 1\n	}},\n	"hiddenSettings": null,\n	"retainAuthority": true,\n	"guards": null\n}}\n\n')
    f.close()

    os.system(f'sh -c "cd {base_path} && sugar validate && sugar upload && sugar deploy"')
    # db.events.find_one_and_update({'_id': ObjectId(result_id)}, {'$set': {'cover': f'/img/{result_id}/assets/collection.png'}})

import subprocess
solana_addr = str(subprocess.check_output(['solana', 'address'])).split('\'')[1].split('\\')[0]
print(solana_addr)
print(solana_addr)

app = FastAPI()
UU = []
UU.append(1)
sec = Secret(_time=18,_symbols=8)
check_arr = []
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

@app.get("/api/getQR")
async def getQR(wallet, ticket):
    wallet = "DdzCSCfS8nFypHfWCVoXptvMjVEmcWFEqW3BjUjM5n7H"
    ticket = "3i5ru4Ym1TarxjCoW1Z3akue2S5b31H87nndMjKqQKFD"
    res = requests.post("https://api.hm.ru/key/url/shorten", json={
                                                                    "api_key": "3430dde3-0222-43de-8a6a-dcee8df9af97",
                                                                    "url": f"http://levandrovskiy.ru/api/checkQR?wallet={wallet}&ticket={ticket}&secret={sec.getSec()}"
                                                                    })
    return res.json()['data']['short_url']

@app.get("/api/checkQR")
async def checkQR(wallet, ticket, secret):
    t = ""
    if (secret==sec.getSec()):
        res = requests.get(f"https://api.shyft.to/sol/v1/nft/read_all?network=devnet&address={wallet}", headers={"x-api-key":"-3iYNcRok7Gm4EMl"})
        check_arr = [x["mint"] for x in res.json()["result"]]
        if (ticket in check_arr):
            with open("go.html", "r") as f:
                t = f.read()
            HTMLResponse(content=t, status_code=200)
        else:
            with open("go_away.html", "r") as f:
                t = f.read()
            HTMLResponse(content=t, status_code=200)
    else:
        with open("go_away.html", "r") as f:
                t = f.read()
        return HTMLResponse(content=t, status_code=200)

@app.get("/api/findMint")
async def findMint(wallet, check:bool):
    global check_arr
    if(check == False):
        res = requests.get(f"https://api.shyft.to/sol/v1/nft/read_all?network=devnet&address={wallet}", headers={"x-api-key":"-3iYNcRok7Gm4EMl"})
        check_arr = [{"mint":x["mint"], "owner":x["owner"]} for x in res.json()["result"]]
        return check_arr
    if(check == True):
        res = requests.get(f"https://api.shyft.to/sol/v1/nft/read_all?network=devnet&address={wallet}", headers={"x-api-key":"-3iYNcRok7Gm4EMl"})
        arr = [{"mint":x["mint"], "owner":x["owner"]} for x in res.json()["result"]]
        tt = []
        for x in arr:
            if(not x in check_arr and x["owner"] in check_arr[0]["owner"]):
                tt.append(x)
        if (len(tt) > 0):
            return tt[0]
        else:
            return "No changes"

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
    th = threading.Thread(target=create_new_event_back,args=(event,)).start()
    return ":))))))"


@app.get('/api/event', tags=['events'])
def get_all_events(user_id: str | None = None):
    result = []
    for event in db.events.find():
        event['_id'] = str(event['_id'])
        if (user_id is not None and user_id == event['user_id']) or (user_id is None):
            result.append(event)
    return result


@app.get('/api/event/{id}', tags=['events'])
def get_event_by_id(id: str):
    result = db.events.find_one({'_id': ObjectId(id)})
    result['_id'] = str(result['_id'])
    return result


@app.put('/api/event/{id}/allow/{user_id}', tags=['events'])
def add_to_white_list(id: str, user_id: str):
    result = db.events.find_one({'_id': ObjectId(id)})
    if (len(result['white_list']) < result['amount']):
        result['white_list'].append(user_id)
        db.events.update_one({'_id': ObjectId(id)}, {'$set': {'white_list': result['white_list']}})
    else:
        return HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS)


@app.put('/api/event/{id}/deny/{user_id}', tags=['events'])
def remove_from_white_list(id: str, user_id: str):
    result = db.events.find_one({'_id': ObjectId(id)})
    result['white_list'].remove(user_id)
    db.events.update_one({'_id': ObjectId(id)}, {'$set': {'white_list': result['white_list']}})


@app.post('/api/auth', tags=['auth'], status_code=status.HTTP_201_CREATED)
def create_auth_state(state: str = Body(), address: str = Body()):
    item = {'state': state, 'address': address}
    db.state.insert_one(item).inserted_id


@app.get('/api/auth/{state}', tags=['auth'])
def get_address(state: str):
    result = db.state.find_one_and_delete({'state': state})
    if result is not None:
        return {'address': result['address']}
    else:
        return HTTPException(status_code=404)


@app.get('/api/event', tags=['events'])
def get_all_events(user_id: str | None = None):
    result = []
    for event in db.events.find():
        event['_id'] = str(event['_id'])
        if (user_id is not None and user_id == event['user_id']) or (user_id is None):
            result.append(event)
    return result

@app.get('/api/ticket', tags=['tickets'])
def get_tickets(user_id: str | None = None):
    result = []
    for ticket in db.tickets.find():
        ticket['_id'] = str(ticket['_id'])
        if (user_id is not None and user_id == ticket['user_id']) or (user_id is None):
            result.append(ticket)
    return result

@app.post('/api/ticket', tags=['tickets'])
def create_ticket(ticket: Ticket):
    res = requests.get(f"https://api.shyft.to/sol/v1/nft/read_all?network=devnet&address={ticket.user_id}", headers={"x-api-key":"-3iYNcRok7Gm4EMl"})
    check_arr = [{"mint":x["mint"], "owner":x["owner"]} for x in res.json()["result"]]

    print(check_arr)

    ticket.for_sell = False
    event = db.events.find_one({'_id': ObjectId(ticket.event_id)})
    if event['minted'] >= event['amount']:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if not ticket.user_id in event['white_list']:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    if db.events.find_one({'user_id': ticket.user_id, 'event_id': ObjectId(event['_id'])}) is not None:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    os.system(f'sh -c "cd {back_path}/{ticket.event_id} && sugar mint --receiver {ticket.user_id}"')

    f = open(f'{back_path}/{ticket.event_id}/cache.json')
    data = json.load(f)

    ticket.url = data['items'][str(event['minted'])]['image_link']

    print(data['items'][str(event['minted'])])

    f.close()

    db.events.find_one_and_update({'_id': ObjectId(ticket.event_id)}, {'$set': {"minted": event['minted'] + 1}})

    res = requests.get(f"https://api.shyft.to/sol/v1/nft/read_all?network=devnet&address={ticket.user_id}", headers={"x-api-key":"-3iYNcRok7Gm4EMl"})
    arr = [{"mint":x["mint"], "owner":x["owner"]} for x in res.json()["result"]]
    tt = []
    for x in arr:
        if(not x in check_arr and x["owner"] in check_arr[0]["owner"]):
            tt.append(x)

    print(tt)
    
    if (len(tt) > 0):
        ticket.mint = tt[0]["mint"]
        db.tickets.insert_one(jsonable_encoder(ticket))
        return tt[0]
    else:
        return "No changes"


@app.put('/api/ticket/{id}/sell/{sell_status}', tags=['tickets'])
def set_ticket_for_sell(id: str, sell_status: bool):
    db.tickets.find_one_and_update({'_id': ObjectId(id)}, {'$set': {"for_sell": sell_status}})


@app.get('/api/exchange', tags=['exchange'])
def get_exchanges(user_id: str | None = None):
    result = []
    for exchange in db.exchanges.find():
        exchange['_id'] = str(exchange['_id'])
        if (user_id is not None and (user_id == exchange['users'][0]['id'] or user_id == exchange['users'][1]['id'])) or (user_id is None):
            result.append(exchange)
    return result


@app.post('/api/exchange', tags=['exchange'])
def create_exchange_request(users: Exchange):
    db.exchanges.insert_one(jsonable_encoder(users))


@app.put('/api/exchange/{id}/approve', tags=['exchange'])
def approve_exchange(id: str):
    exchange = db.exchanges.find_one({'_id': ObjectId(id)})

    for ticket in exchange['users'][0]['tickets']:
        new_user = exchange['users'][1]['id']
        db.tickets.find_one_and_update({'_id': ObjectId(ticket)}, {'$set': {'user_id': new_user}})

    for ticket in exchange['users'][1]['tickets']:
        new_user = exchange['users'][0]['id']
        db.tickets.find_one_and_update({'_id': ObjectId(ticket)}, {'$set': {'user_id': new_user}})

    db.exchanges.delete_one({'_id': ObjectId(id)})


@app.put('/api/exchange/{id}/discard', tags=['exchange'])
def discard_exchange(id: str):
    db.exchanges.delete_one({'_id': ObjectId(id)})


t1 = threading.Thread(target=sec.update)
t1.daemon = True
t1.start()