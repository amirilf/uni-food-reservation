import requests
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup
from utility.config import PROFILE_URL, PROFILE_IMAGE_URL
from core.account.auth import get_page_or_exception


def get_profile_information(session: requests.Session) -> dict[str, str] | Exception:
    """
    Extract user information including:
        - national_number
        - fullname
        - gender
        - balance
        - phone
        - email
        - faculty
        - degree
        - last_login
    """        

    response = get_page_or_exception(session, PROFILE_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    def get_text_or_default(element_id: str) -> str:
        element = soup.find('label', {'id': element_id})
        return element.get_text(strip=True) if element else ""
    
    user_info = {
        "national_number": get_text_or_default("cphMain_lblNationalCode"),
        "fullname": get_text_or_default("cphMain_lblName"),
        "gender": get_text_or_default("cphMain_lblGender"),
        "phone": get_text_or_default("cphMain_lblMobile"),
        "email": get_text_or_default("cphMain_lblEmail"),
        "faculty": get_text_or_default("cphMain_lblCollege"),
        "degree": get_text_or_default("cphMain_lblGrade"),
        "last_login": get_text_or_default("cphMain_lblLastLogin"),
        "balance": get_text_or_default("lblCredit")
    }

    return user_info

def get_profile_image(sessoin: requests.Session, save: bool = False, path: str = "profile") -> Image.Image | Exception:
    """
    Extract user profile image<br>
    Name parameter could be any path (absolute or relative) and the .png will be added at the end of it.<br>
    
    e.g:
        - `profile` -> `profile.png`
        - `images/profile1` -> `images/profile1.png`
        - `/media/profiles/1` -> `/media/profiles/1.png`
    """

    # no need to handle exception since profile route only returns
    # null content if the session is not authenticated
    content = get_page_or_exception(sessoin, PROFILE_IMAGE_URL).content
    
    if content:
        profile_image = Image.open(BytesIO(content))
        
        if save:
            if profile_image.mode != 'RGB':
                profile_image = profile_image.convert('RGB')
            profile_image.save(path + ".png", format="PNG")

        return profile_image
    else:
        raise Exception("Session is not authenticated.")
