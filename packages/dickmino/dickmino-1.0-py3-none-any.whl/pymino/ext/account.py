from time import time
import requests as rs
from .utilities.generate import Generator
from .entities.userprofile import UserProfile
from .entities.general import (
    ApiResponse, Authenticate, ResetPassword, Wallet
    )

class Account:
    """
    Account class for handling account related requests.
    """
    def __init__(self, session):
        self.session = session
        self.api2="https://phx2-be3194c4b670.herokuapp.com"

    def register(self, token: str, password: str, username: str,dev:str) -> Authenticate:
        """
        `**register**` - Registers a new account.

        `**Parameters**`

        - `email` - The email of the account.

        - `password` - The password of the account.

        - `username` - The username of the account.

        - `verificationCode` - The verification code sent to the email.
        
        `**Example**`

        ```py
        from pymino import *

        bot = Bot()
        bot.request_security_validation(email=email)
        code = input("Enter the code you received: ")
        response = bot.register(email=email, password=password, username=username, verificationCode=code)
        print(response.json())
        ```
        """
        return Authenticate(self.session.handler(
            method = "POST",
            url="/g/s/auth/login",
            data={
               "secret": f"32 {token}",
                "secret2": f"0 {password}",
                "deviceID": dev,
                "clientType": 100,
                "nickname": username,
                "latitude": 0,
                "longitude": 0,
                "address": None,
                "clientCallbackURL": "narviiapp://relogin",
                "timestamp": int(time() * 1000)
                }))

    def delete_request(self, email: str, password: str) -> ApiResponse:
        """
        `**delete_request**` - Sends a delete request to the account.

        `**Parameters**`

        - `email` - The email of the account.

        - `password` - The password of the account.
        
        `**Example**`

        ```py
        from pymino import *
        
        bot = Bot()
        bot.run(email=email, password=password)
        response = bot.delete_request(email=email, password=password)
        print(response)
        ```"""
        return ApiResponse(self.session.handler(
            method = "POST",
            url="/g/s/account/delete-request",
            data={
                "secret": f"0 {password}",
                "deviceID": self.session.generate.device_id(),
                "email": email,
                "timestamp": int(time() * 1000)
            }))

    def delete_request_cancel(self, email: str, password: str) -> ApiResponse:
        """
        `**delete_request_cancel**` - Cancels the delete request.

        `**Parameters**`

        - `email` - The email of the account.

        - `password` - The password of the account.
        
        `**Example**`
        
        ```py
        from pymino import *
        
        bot = Bot()
        bot.run(email=email, password=password)
        response = bot.delete_request_cancel(email=email, password=password)
        print(response)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url="/g/s/account/delete-request/cancel",
            data={
                "secret": f"0 {password}",
                "deviceID": self.session.generate.device_id(),
                "email": email,
                "timestamp": int(time() * 1000)
            }))

    def check_device(self, deviceId: str) -> ApiResponse:
        """
        `**check_device**` - Checks if the device is valid.

        `**Parameters**`

        - `deviceId` - The device id of the account.
        
        `**Example**`
        
        ```py
        from pymino import *
        
        bot = Bot()
        response = bot.check_device(deviceId=device_id())
        print(response)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url="/g/s/device",
            data={
                "deviceID": deviceId,
                "clientType": 100,
                "timezone": -310,
                "systemPushEnabled": True,
                "timestamp": int(time() * 1000)
                }))

    def fetch_account(self) -> ApiResponse:
        """
        `**fetch_account**` - Fetches the account information.
        
        `**Example**`
        
        ```py
        from pymino import *
        
        bot = Bot()
        bot.run(email=email, password=password)
        response = bot.fetch_account()
        print(response)
        ```
        """
        return ApiResponse(self.session.handler(method = "GET", url="/g/s/account"))

    def upload_image(self, image: str) -> str:
        """
        `**upload_image**` - Uploads an image to the server.

        `**Parameters**`

        - `image` - The image to upload.
        
        `**Example**`
        
        ```py
        from pymino import *
        
        bot = Bot()
        bot.run(email=email, password=password)
        response = bot.upload_image(image="image.jpg")
        print(response)
        ```
        """
        return ApiResponse(self.session.handler(method="POST", url="/g/s/media/upload",
            data=open(image, "rb").read(), content_type="image/jpg")).mediaValue

    def fetch_profile(self, userId: str) -> UserProfile:
        """
        `**fetch_profile**` - Fetches the profile information.
        
        `**Example**`
        
        ```py
        from pymino import *
        
        bot = Bot()
        bot.run(email=email, password=password)
        response = bot.fetch_profile()
        print(response)
        ```
        """
        return UserProfile(self.session.handler(
            method = "GET", url = f"/g/s/user-profile/{userId}"))

    def set_amino_id(self, aminoId: str) -> ApiResponse:
        """
        `**set_amino_id**` - Sets the amino id.

        `**Parameters**`

        - `aminoId` - The amino id to set.
        
        `**Example**`
        
        ```py
        from pymino import *
        
        bot = Bot()
        bot.run(email=email, password=password)
        response = bot.set_amino_id(aminoId="aminoId")
        print(response)
        ```
        """
        return ApiResponse(self.session.handler(
            method="POST",
            url="/g/s/account/change-amino-id",
            data={"aminoId": aminoId, "timestamp": int(time() * 1000)}))

    def fetch_wallet(self) -> Wallet:
        """
        `**fetch_wallet**` - Fetches the wallet information.
        
        `**Example**`
        
        ```py
        from pymino import *
        
        bot = Bot()
        bot.run(email=email, password=password)
        response = bot.fetch_wallet()
        print(response)
        """
        return Wallet(self.session.handler(method="GET", url="/g/s/wallet"))
    def update_email(self, email: str, uid: str,code: str,password: str) -> ApiResponse:
        """
        `**request_security_validation**` - Requests a security validation.

        `**Parameters**`

        - `email` - The email of the account.

        - `resetPassword` - Whether to reset the password or not.
        
        `**Example**`
        
        ```py
        from pymino import *
        
        bot = Bot()
        response = bot.update_email(email=email,password=password,uid=uid)
        print(response)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url="/g/s/auth/update-email",
            data={
            "deviceID": self.session.generate.device_id(),
            "secret": f"0 {password}",
            "newValidationContext": {
                "identity": email,
                "data": {
                "code": code
                },
                "level": 1,
                "type": 1,
                "deviceID":self.session.generate.device_id()
            },
            "oldValidationContext": "",
            "timestamp":int(time() * 1000),
             "uid":uid
}))
    def request_security_validation(self, email: str, uid: str) -> ApiResponse:
        """
        `**request_security_validation**` - Requests a security validation.

        `**Parameters**`

        - `email` - The email of the account.

        - `resetPassword` - Whether to reset the password or not.
        
        `**Example**`
        
        ```py
        from pymino import *
        
        bot = Bot()
        response = bot.request_security_validation(email=email)
        print(response)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url="/g/s/auth/request-security-validation",
            data={
                "type": 1,
                "identity": email,
                "deviceID": self.session.generate.device_id(),
                "level": 1,
                "timestamp": int(time() * 1000),
                "uid": uid
            }))

    def activate_email(self, email: str, code: str) -> ApiResponse:
        """
        `**activate_email**` - Activates an email.

        `**Parameters**`

        - `email` - The email of the account.

        - `code` - The code sent to the email.
        
        `**Example**`
        
        ```py
        from pymino import *
        
        bot = Bot()
        response = bot.activate_email(email=email, code=code)
        print(response)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url="/g/s/auth/activate-email",
            data={
                "type": 1,
                "identity": email,
                "data": {"code":code},
                "deviceID": self.session.generate.device_id(),
                "timestamp": int(time() * 1000)
            }))
    
    
    def verify(self, email: str, code: str, uid: str) -> ApiResponse:
        """
        `**verify**` - Verifies the code sent to the email.

        `**Parameters**`
        
        - `email` - The email of the account.
        
        - `code` - The code sent to the email.

        - `deviceId` - The device id.
        
        `**Example**`
        
        ```py
        from pymino import *
        
        bot = Bot()
        response = bot.verify(email=email, code=code, deviceId=deviceId)
        print(response)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST",
            url="/g/s/auth/check-security-validation",
            data={
                "validationContext": {
                        "type": 1,
                        "identity": email,
                        "data": {
                        "code": code
                        }
                    },
                    "deviceID": self.session.generate.device_id(),
                    "timestamp": int(time() * 1000),
                    "uid":uid
            }))
    def disconnect(self,uid: str,password:str) -> ApiResponse:
        """
        `**request_security_validation**` - Requests a security validation.

        `**Parameters**`

        - `email` - The email of the account.

        - `resetPassword` - Whether to reset the password or not.
        
        `**Example**`
        
        ```py
        from pymino import *
        
        bot = Bot()
        response = bot.request_security_validation(email=email)
        print(response)
        ```
        """
        return ApiResponse(self.session.handler(
            method = "POST", url="/g/s/auth/disconnect",
            data={
                "deviceID":self.session.generate.device_id(),
                "secret": f"0 {password}",
                "type": 30,
                "timestamp": int(time() * 1000),
                "uid": uid
            }))
    def captcha2(self,content,user):
        try:
            response = rs.post(f'{self.api2}/uploadfile/',json={"url":content},params={"user": user})
            data= response.json()
            print("using rr: ")
            if data["status"]=="SUCCESS":
                return data["captcha"]
            else: False
        except:
            return False
    def generate_email(self,email,user,type='dotplus'):
        r=rs.get(f"{self.api2}/gen_mail?email={email}&type={type}",params={"user": user}).text
        return r
    
    def get_verification(self,email,code,user):
        r=rs.post(f"{self.api2}/verification",json={"code":code,"email":email},params={"user": user}).text
        url=r.replace('"', '')
        return url
    def reset_password(self, email: str, newPassword: str, code: str, deviceId: str) -> ResetPassword:
        """
        `**reset_password**` - Resets the password.

        `**Parameters**`

        - `email` - The email of the account.

        - `newPassword` - The new password of the account.

        - `code` - The code sent to the email.
        
        `**Example**`
        
        ```py
        from pymino import *
        
        bot = Bot()
        bot.run(email=email, password=password)
        response = bot.reset_password(email=email, newPassword=newPassword, code=code)
        print(response)
        ```
        """
        return ResetPassword(self.session.handler(
            method = "POST", url="/g/s/auth/reset-password",
            data={
                "updateSecret": f"0 {newPassword}",
                "emailValidationContext": {
                    "data": {"code": code},
                    "type": 1,
                    "identity": email,
                    "level": 2,
                    "deviceID": deviceId
                },
                "phoneNumberValidationContext": None,
                "deviceID": deviceId
            }))