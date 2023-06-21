import openai
import requests
from crud import get_user
from loader import SECRET_KEY
from loader import session, logger, OPENAPI_TOKEN


def check_user_password(user_input: str) -> bool:
    """
    Checks user password.
    Args:
        user_input: Provided password.

    Returns:
        True if match else False.
    """
    
    return user_input == SECRET_KEY


def make_verified(user_id: int) -> None:
    """
    Sets the 'is_verified' flag for user.
    Args:
        user_id: User ID.

    Returns:
        None.
    """
    
    user = get_user(user_id)
    user.is_verified = True
    session.add(user)
    session.commit()


def send_question(question: str) -> str:
    """
    Performs the request to OpenAi API.
    Args:
        question: User question as a string.

    Returns:
        An OpenAI answer or error message.
    """
    
    openai.api_key = OPENAPI_TOKEN
    response = openai.Completion.create(
        prompt=question,
        model="text-davinci-003",
        max_tokens=500,
        n=1
    )
    if response:

        return response.choices[0].text.strip()
    else:
        return "Oops, something went wrong."


def get_tokens() -> int | str:
    """
    Performs the request to OpenAi API to check account balance in tokens.

    Returns:
        Tokens left or error string.
    """

    url = "https://api.openai.com/v1/dashboard/billing/subscription"
    headers = {"Authorization": f"Bearer {OPENAPI_TOKEN}"}
    request = requests.get(url, headers=headers)
    if request.status_code == 200:
        response = request.json()
        return response["hard_limit"]
    else:
        "Some problems with receiving information from OpenAi server. Try again later."


def get_help_text() -> str:
    """
    Generates help text.
    Returns:
        Help text.
    """

    return "This bot acts as a proxy layer for ChatGTP. You will need a password to work. " \
           "Use the /start command to get started."

