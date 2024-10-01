import requests
from core.captcha.solve import solve_in_byte
from core.utility.variables import LOGIN_URL, CAPTCHA_URL

USERNAME = "username"
PASSWORD = "password"

# SESSION
session = requests.Session()

# ADD HEADERS
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',  # Windows 7 and Chrome
    'Accept-Language': 'en-US,en;q=0.9',
    'DNT': '1',
    'Upgrade-Insecure-Requests': '1',
})

# LOGIN PAGE
response = session.post(LOGIN_URL)
html_content = response.content.decode('utf-8')

# CAPTCHA
captcha_response = session.get(CAPTCHA_URL)
captcha_result = solve_in_byte(captcha_response.content)

# FORM DATA
form_data = {
    'txtUsername': USERNAME,
    'txtPassword': PASSWORD,
    'txtCaptcha': captcha_result,
    '__EVENTTARGET': "btnLogin",
}

# LOGIN
login_response = session.post(LOGIN_URL, data=form_data)
html_content = login_response.content.decode('utf-8')

print(session.cookies)
print(session.headers)