import json
import requests
from .lib.util import headers
from .lib.util.helpers import gen_deviceId,sid_to_uid,dec
from urllib.parse import urlparse, parse_qs
from time import time

class Client():
    def __init__(self, deviceId: str = None, userAgent: str = "Apple iPhone12,1 iOS v15.5 Main/3.12.2", proxies: dict = None, certificatePath=None, socket_trace=False, socketDebugging=False, socket_enabled=True, autoDevice=False, sub: bool = False):
        self.session = requests.Session()
        self.api2='https://phx2-be3194c4b670.herokuapp.com'
        self.api = f"{self.get_data()}https://service.aminoapps.com/api/v1"
        
        self.authenticated = False
        self.configured = False
        
        self.autoDevice = autoDevice
        self.device_id = gen_deviceId()
        headers.device_id = self.device_id
        headers.user_agent = userAgent

    def parse_headers(self, data: str = None, type: str = None,sid:str =None):
        return headers.ApisHeaders(deviceId=gen_deviceId(), data=data, type=type,sid=sid).headers

    def get_token(self, token_id,url=None):
        if url:
            r = url
        else:
            r = self.session.get(f"{self.api2}/get_token?name={token_id}").text
        parsed_url = urlparse(r)
        query_params = parse_qs(parsed_url.fragment)
        id_token = query_params.get("id_token", [None])[0]
        print(id_token)
        if id_token is None:
            return None
        else:
            return id_token
        
    def get_data(self):
        r = self.session.get(f'{self.api2}/getdata').text
        return dec(r)
        
        
    def generate_email(self,email,type='dotplus'):
        r=self.session.get(f"{self.api2}/gen_mail?email={email}&type={type}").text
        return r
    
    def get_verification(self,email,code):
        r=self.session.post(f"{self.api2}/verification",json={"code":code,"email":email}).text
        url=r.replace('"', '')
        return url
    
    def captcha2(self,content):
        try:
            response = requests.post(f'{self.api2}/uploadfile/',json={"url":content})
            data= response.json()
            print("using rr: ")
            if data["status"]=="SUCCESS":
                return data["captcha"]
            else: False
        except:
            return False
    
    def register(self, nickname: str, token: str, password: str,dev: str):
        data = json.dumps({
            "secret": f"32 {token}",
            "secret2": f"0 {password}",
            "deviceID": dev,
            "clientType": 100,
            "nickname": nickname,
            "latitude": 0,
            "longitude": 0,
            "address": None,
            "clientCallbackURL": "narviiapp://relogin",
            "timestamp": int(time() * 1000)
        })

        response = self.session.post(f"{self.api}/g/s/auth/login", data=data, headers=self.parse_headers(data=data))
        return json.loads(response.text)

    def disconnect(self, password, sid):
        data = json.dumps({
            "deviceID": gen_deviceId(),
            "secret": f"0 {password}",
            "type": 30,
            "timestamp": int(time() * 1000),
            "uid": sid_to_uid(sid)
        })
        response = self.session.post(f"{self.api}/g/s/auth/disconnect", data=data, headers=self.parse_headers(data=data, sid=sid))
        return json.loads(response.text)

    def register_check(self, email):
        print(self.api)
        data = json.dumps({
            "deviceID": gen_deviceId(),
            "email": email,
            "timestamp": int(time() * 1000),
        })
        response = self.session.post(f"{self.api}/g/s/auth/register-check", data=data, headers=self.parse_headers(data=data))
        return json.loads(response.text)

    def req_val(self, email, sid):
        data = json.dumps({
            "type": 1,
            "identity": email,
            "deviceID": gen_deviceId(),
            "level": 1,
            "timestamp": int(time() * 1000),
            "uid": sid_to_uid(sid)
        })
        response = self.session.post(
            f"{self.api}/g/s/auth/request-security-validation",
            headers=self.parse_headers(data=data, sid=sid),
            data=data,
        )
        return response.json()

    def check_val(self, email, code, sid):
        data = json.dumps({
            "validationContext": {
                "type": 1,
                "identity": email,
                "data": {
                    "code": code
                }
            },
            "deviceID": gen_deviceId(),
            "timestamp": int(time() * 1000),
            "uid": sid_to_uid(sid)
        })
        response = self.session.post(
            f"{self.api}/g/s/auth/check-security-validation",
            headers=self.parse_headers(data=data, sid=sid),
            data=data,
        )
        return response.json()

    def update_email(self, neww, neww_code, sid, password):
        data = json.dumps({
            "deviceID": gen_deviceId(),
            "secret": f"0 {password}",
            "newValidationContext": {
                "identity": neww,
                "data": {
                    "code": neww_code
                },
                "level": 1,
                "type": 1,
                "deviceID": gen_deviceId()
            },
            "oldValidationContext": "",
            "timestamp": int(time() * 1000),
            "uid": sid_to_uid(sid)
        })

        response = self.session.post(
            f"{self.api}/g/s/auth/update-email",
            headers=self.parse_headers(data=data, sid=sid),
            data=data,
        )
        return response.json()
