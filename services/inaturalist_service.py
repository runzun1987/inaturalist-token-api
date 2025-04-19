import requests
from bs4 import BeautifulSoup


from services.mongodb import post_token_mongodb


def fetch_inaturalist_token(email: str, password: str) -> str:
    from main import Token
    session = requests.Session()

    # Step 1: Retrieve the CSRF token
    login_url = "https://www.inaturalist.org/login"
    resp = session.get(login_url)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    token_input = soup.find("input", {"name": "authenticity_token"})
    if not token_input or not token_input.get("value"):
        raise RuntimeError("CSRF token not found.")
    csrf_token = token_input["value"]

    # Step 2: Submit login form
    payload = {
        "utf8": "✓",
        "authenticity_token": csrf_token,
        "user[email]": email,
        "user[password]": password,
        "user[remember_me]": "0",
        "commit": "Log In",
    }
    headers = {
        "Referer": login_url,
        "User-Agent": "python-requests/2.x",
    }
    login_resp = session.post("https://www.inaturalist.org/session", data=payload, headers=headers)
    login_resp.raise_for_status()
    if "sign out" not in login_resp.text.lower():
        raise RuntimeError("Login failed. Check your credentials.")

    # Step 3: Retrieve API token
    token_resp = session.get("https://www.inaturalist.org/users/api_token", headers={"Accept": "application/json"})
    token_resp.raise_for_status()
    api_token = token_resp.json().get("api_token")
    if not api_token:
        raise RuntimeError("API token not found.")

    try:
        token = Token(value=api_token)
        post_token_mongodb(token)
    except Exception as e:
       print(e)


    return api_token
