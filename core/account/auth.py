import requests
from core.captcha.solve import solve_in_byte
from core.utility.variables import LOGIN_URL, CAPTCHA_URL, AUTH_SESSION_HEADER
from bs4 import BeautifulSoup

def login(username: str, password: str) -> requests.Session:
        
    # set session
    session = requests.Session()
    session.headers.update(AUTH_SESSION_HEADER)
    
    # get & solve captcha
    captcha_result = solve_in_byte(session.get(CAPTCHA_URL).content)

    # set form data to post
    form_data = {
        'txtUsername': username,
        'txtPassword': password,
        'txtCaptcha': captcha_result,
        '__EVENTTARGET': "btnLogin",
    }

    # authenticate using data
    response = session.post(LOGIN_URL, data=form_data)
    
    # check for errors 
    soup = BeautifulSoup(response.content, 'html.parser')
    error_label = soup.find('label', {'id': 'lblLoginError'})
    if error_label:
        raise Exception(error_label.get_text(strip=True))
    
    return session


def session_expired(session: requests.Session = None) -> bool:
    return False
