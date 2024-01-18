RockCaptcha package for Python
=
[Rockcaptcha.com](https://rockcaptcha.com) package for Python3

Rockcaptcha solve recaptchaV2, recaptchaV3, funcaptcha, imageToText very fast and cheap

# Install

```bash
pip install rockcaptcha
```

# Usage

## create client

```python
from rockcaptcha import RockCaptchaClient

APIKEY = "<EXAMPLE API KEY>"
client = RockCaptchaClient(apikey=APIKEY)
```

## Recaptcha v2:

```python
result = client.recaptcha_v2_task_proxy_less(site_url="SITE_URL", site_key="SITE_KEY", invisible=False)
if result["code"] == 0:  # task success:
    print(result["token"])
else:  # error
    print(result["message"])
```

## Recaptcha v2 enterprise:

```python

result = client.recaptcha_v2_enterprise_task_proxy_less(site_url="SITE_URL", site_key="SITE_KEY")
if result["code"] == 0:  # task success:
    print(result["token"])
else:  # error
    print(result["message"])
```

## Recaptcha v3:

```python
result = client.recaptcha_v3_task_proxy_less(site_url="SITE_URL", site_key="SITE_KEY",
                                             page_action="PAGE_ACTION")
if result["code"] == 0:  # task success:
    print(result["token"])
else:  # error
    print(result["message"])
```

## Recaptcha v3 enterprise:

```python
result = client.recaptcha_v3_enterprise_task_proxy_less(site_key="SITE_KEY",
                                                        site_url="SITE_URL",
                                                        page_action="PAGE_ACTION")
if result["code"] == 0:  # task success:
    print(result.get('token'))
    print(result.get('user_agent'))
else:  # error
    print(result["message"])
```

## Recaptcha recognition

```python
url_list = ['']
caption = 'cars'
result = client.recaptcha_recognition(url_list=url_list, caption=caption)
if result["code"] == 0:  # task success:
    print(result["token"])
else:  # error
    print(result["message"])
```

## Image2text

```python

result = client.image_to_text(file="/path/to/example-file.jpg")
if result["code"] == 0:  # task success:
    print(result["token"])
else:  # error
    print(result["message"])
```

## Funcaptcha

```python
site_key = "2CB16598-CB82-4CF7-B332-5990DB66F3AB"
site_url = "https://twitter.com/"
result = client.fun_captcha_task_proxy_less(site_url, site_key)
if result["code"] == 0:  # task success:
    print(result["token"])
else:  # error
    print(result["message"])
```
