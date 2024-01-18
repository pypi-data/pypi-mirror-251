import time

import requests

from rockcaptcha.exeptions import RockCaptchaException
from rockcaptcha.helpers import convert_img_to_base64


class RockCaptchaClient:
    def __init__(self, apikey):
        self.apikey = apikey
        self.BASE_URL = "https://api.rockcaptcha.com"

    def get_balance(self):
        r = requests.get(f"{self.BASE_URL}/user/balance?apikey=" + self.apikey)
        if r.status_code == 200:
            data = r.json()
            if data['Code'] == 0:
                return data['Balance']
            else:
                raise RockCaptchaException(f"Error response {r.text}")
        else:
            raise RockCaptchaException("Error " + r.text)

    def get_task_result(self, task_id, timeout, time_sleep, captcha_type=""):
        t_start = time.time()
        while (time.time() - t_start) < timeout:
            r = requests.get(f"{self.BASE_URL}/getresult?apikey=" + self.apikey + "&taskid=" + str(task_id))
            if r.status_code == 200:
                data = r.json()
                if data['Code'] == 0:
                    if data['Status'] == "SUCCESS":
                        if captcha_type == "image2text" or captcha_type == "recaptcha_click":
                            return data["Data"]
                        elif captcha_type == "v3_enterprise":
                            return data["Data"]
                        return data["Data"]["Token"]
                    elif data['Status'] == "ERROR":
                        raise RockCaptchaException(f"Error: {data['Message']}")
                    time.sleep(time_sleep)
                else:
                    raise RockCaptchaException(f"Error {data['Message']}")
            else:
                raise RockCaptchaException(f"Error {r.text}")
        raise RockCaptchaException("TIMEOUT")

    def recaptcha_v2_task_proxy_less(self, site_url, site_key, invisible=False, timeout=180, time_sleep=1):
        try:
            params = {
                "apikey": self.apikey,
                "sitekey": site_key,
                "siteurl": site_url,
                "version": "v2",
                "invisible": str(invisible).lower()
            }
            r = requests.get(
                f"{self.BASE_URL}/recaptchav2",
                params=params
            )
            if r.status_code == 200:
                data = r.json()
                if data['Code'] == 0:
                    task_id = data['TaskId']
                else:
                    raise RuntimeError("Error " + str(data))
            else:
                raise RuntimeError("Error " + r.text)
            return {"code": 0, "token": self.get_task_result(task_id, timeout, time_sleep)}
        except Exception as e:
            return {"code": 1, "message": str(e)}

    def recaptcha_v2_enterprise_task_proxy_less(self, site_url, site_key, s_payload=None, timeout=180, time_sleep=1):
        try:
            params = {
                "apikey": self.apikey,
                "sitekey": site_key,
                "siteurl": site_url,
            }
            if s_payload:
                params["s"] = s_payload
            r = requests.get(
                f"{self.BASE_URL}/recaptchav2_enterprise",
                params=params
            )
            if r.status_code == 200:
                data = r.json()
                if data['Code'] == 0:
                    task_id = data['TaskId']
                else:
                    raise RuntimeError("Error " + str(data))
            else:
                raise RuntimeError("Error " + r.text)
            return {"code": 0, "token": self.get_task_result(task_id, timeout, time_sleep)}
        except Exception as e:
            return {"code": 1, "message": str(e)}

    def recaptcha_v3_task_proxy_less(self, site_url, site_key, page_action, min_score: float = 0.3, timeout=180,
                                     time_sleep=1):
        try:
            params = {
                "apikey": self.apikey,
                "sitekey": site_key,
                "siteurl": site_url,
                "pageaction": page_action,
                "minscore": min_score,
                "version": "v3"
            }
            r = requests.get(
                f"{self.BASE_URL}/recaptchav3",
                params=params
            )
            if r.status_code == 200:
                data = r.json()
                if data['Code'] == 0:
                    task_id = data['TaskId']
                else:
                    raise RuntimeError("Error " + str(data))
            else:
                raise RuntimeError("Error " + r.text)
            return {"code": 0, "token": self.get_task_result(task_id, timeout, time_sleep)}
        except Exception as e:
            return {"code": 1, "message": str(e)}

    def recaptcha_v3_enterprise_task_proxy_less(
            self,
            site_url,
            site_key,
            page_action,
            s_payload=None,
            min_score: float = 0.3,
            timeout=180,
            time_sleep=1
    ):
        try:
            params = {
                "apikey": self.apikey,
                "sitekey": site_key,
                "siteurl": site_url,
                "pageaction": page_action,
                "minscore": min_score
            }
            if s_payload:
                params["s"] = s_payload
            r = requests.get(
                f"{self.BASE_URL}/recaptchav3_enterprise",
                params=params
            )
            if r.status_code == 200:
                data = r.json()
                if data['Code'] == 0:
                    task_id = data['TaskId']
                else:
                    raise RuntimeError("Error " + str(data))
            else:
                raise RuntimeError("Error " + r.text)
            result = self.get_task_result(task_id, timeout, time_sleep, captcha_type="v3_enterprise")
            return {"code": 0, "token": result.get("Token"), "user_agent": result.get("UserAgent")}
        except Exception as e:
            return {"code": 1, "message": str(e)}

    def fun_captcha_task_proxy_less(self, site_url, site_key, timeout=180, time_sleep=3):
        try:
            params = {
                "apikey": self.apikey,
                "sitekey": site_key,
                "siteurl": site_url,
            }
            r = requests.get(
                f"{self.BASE_URL}/funcaptchatokentask",
                params=params
            )
            if r.status_code == 200:
                data = r.json()
                if data['Code'] == 0:
                    task_id = data['TaskId']
                else:
                    raise RuntimeError("Error " + str(data))
            else:
                raise RuntimeError("Error " + r.text)
            return {"code": 0, "token": self.get_task_result(task_id, timeout, time_sleep)}
        except Exception as e:
            return {"code": 1, "message": str(e)}

    def recaptcha_recognition(self, url_list, caption, timeout=60, time_sleep=3):
        try:
            r = requests.post(
                f"{self.BASE_URL}/recognition",
                json={'Image_urls': url_list, 'Caption': caption, "Apikey": self.apikey, "Type": "recaptcha"}
            )
            if r.status_code == 200:
                data = r.json()
                if data['Code'] == 0:
                    task_id = data['TaskId']
                else:
                    raise RuntimeError("Error " + str(data))
            else:
                raise RuntimeError("Error " + r.text)
            return {"code": 0,
                    "token": self.get_task_result(task_id, timeout, time_sleep, captcha_type="recaptcha_click")}
        except Exception as e:
            return {"code": 1, "message": str(e)}

    def image_to_text(self, base64img=None, file=None, timeout=60, time_sleep=1):
        try:
            if base64img is None:
                if file is None:
                    raise RuntimeError("base64img and file is None ")
                else:
                    base64img = convert_img_to_base64(file)
            r = requests.post(
                f"{self.BASE_URL}/recognition", json={
                    'Image': base64img, "Apikey": self.apikey, "Type": "imagetotext"
                })
            if r.status_code == 200:
                data = r.json()
                if data['Code'] == 0:
                    task_id = data['TaskId']
                else:
                    raise RuntimeError("Error " + str(data))
            else:
                raise RuntimeError("Error " + r.text)
            return {"code": 0, "token": self.get_task_result(task_id, timeout, time_sleep, captcha_type="image2text")}
        except Exception as e:
            return {"code": 1, "message": str(e)}
