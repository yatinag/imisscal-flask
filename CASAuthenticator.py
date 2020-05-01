import requests
from typing import Optional
from xml.etree import ElementTree

class CASAuthenticator:
    """
    Authenticates a user against the Berkeley CAS
    :author: Sal
    """

    # The CAS endpoint. This should be the same for any application at Berkeley
    __CAS_ENDPOINT = "https://auth.berkeley.edu/cas/"

    # The endpoint that the user is being authorized against. This is used to prevent token redirection/abuse
    # Note that I, Sal, am using my personal OCF account here as a CAS trampoline since Berkeley auth services requires
    # a *.berkeley.edu domain. An OCF trampoline works because it lets us host arbitrary content on a berkeley.edu
    # domain (which already has CAS access!)
    __APP_AUTHORIZATION_ENDPOINT = "https://www.ocf.berkeley.edu/~shusain/cas_redirect.html"

    @staticmethod
    def validate(ticket:str)->Optional[str]:
        """
        Validate a ticket against the Berkeley CAS
        :param ticket: The CAS token
        :return: The UID of the user or None if the user is not valid.
        """

        cas_response = requests.get(CASAuthenticator.__CAS_ENDPOINT + "serviceValidate"
                                    + "?service=" + CASAuthenticator.__APP_AUTHORIZATION_ENDPOINT
                                    + "&ticket=" + ticket)

        if cas_response.status_code != 200:
            print(f"[CASAuthenticator] Bad status response: {cas_response.status_code}")
            return None

        try:
            response = ElementTree.fromstring(cas_response.content)
        except ElementTree.ParseError as ex:
            print(f"[CASAuthenticator] CAS response parse failure:")
            print(ex)
            return None

        error_element = response.find("{http://www.yale.edu/tp/cas}authenticationFailure")
        if error_element is not None:
            error_code = error_element.attrib["code"]
            print(f"[CASAuthenticator] CAS gave an error ({error_code}): {error_element.text}")
            return None

        user_element = response.find("{http://www.yale.edu/tp/cas}authenticationSuccess/{http://www.yale.edu/tp/cas}user")
        if user_element is None:
            return None
        uid = user_element.text
        return uid

    @staticmethod
    def get_authentication_redirect_URL()->str:
        """
        Get the URL to trigger a CAS authorization
        :return: The URL which the user should be redirected to start external CAS authentication
        """
        return CASAuthenticator.__CAS_ENDPOINT + "login?service=" + CASAuthenticator.__APP_AUTHORIZATION_ENDPOINT
