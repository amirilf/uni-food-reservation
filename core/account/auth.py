import requests
from bs4 import BeautifulSoup
from core.captcha.solve import solve_in_byte
from utility.config import LOGIN_URL, CAPTCHA_URL, AUTH_SESSION_HEADER, PROFILE_URL


def get_page_or_exception(session: requests.Session, url: str) -> requests.Response:
    """
    Fetch a page using the authenticated session. Raise an exception if the session is not authenticated.
    """

    response = session.get(url)
    response.raise_for_status()

    if response.url == url:
        return response
    elif response.url == LOGIN_URL:
        raise Exception("Session is not authenticated.")
    raise Exception("Error while fetching `" + url + "`.")

def login(username: str, password: str) -> requests.Session:
    """
    Authenticate the user and return the session. Raise an exception for any login errors.
    """
    
    session = requests.Session()
    session.headers.update(AUTH_SESSION_HEADER)
    
    captcha_result = solve_in_byte(session.get(CAPTCHA_URL).content)

    form_data = {
        'txtUsername': username,
        'txtPassword': password,
        'txtCaptcha': captcha_result,
        '__EVENTTARGET': "btnLogin",
    }

    response = session.post(LOGIN_URL, data=form_data)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    error_label = soup.find('label', {'id': 'lblLoginError'})
    if error_label:
        raise Exception(error_label.get_text(strip=True))

    return session

def logout(session: requests.Session) -> bool:
    """
    Log out the user. Return True if successful.
    """
    
    try:
        response = get_page_or_exception(session, PROFILE_URL)
    except Exception:
        return True  # Session is already expired
    
    soup = BeautifulSoup(response.content, 'html.parser')
    viewstate = soup.find('input', {'name': '__VIEWSTATE'})['value']
        
    form_data = {
        '__EVENTTARGET': 'ctl00$logout',
        '__VIEWSTATE': viewstate,
    }

    return session.post(PROFILE_URL, data=form_data).url == LOGIN_URL

def session_checker(session: requests.Session | None) -> bool:
    
    if not session:
        return False
    
    try:
        get_page_or_exception(session, PROFILE_URL)
        return True
    except:
        return False
    