import requests
from typing import TYPE_CHECKING, Any, Dict

from ..schemas import FaceAuthResponse
from ..utils import image_to_base64

if TYPE_CHECKING:
    from ..client import BioLogreenClient

class AuthResource:
    """Handles all authentication-related API calls."""

    def __init__(self, client: "BioLogreenClient"):
        self.client = client

    def _post(self, endpoint: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Helper method for making POST requests."""
        headers = {
            "X-API-KEY": self.client.api_key,
            "Content-Type": "application/json"
        }
        url = f"{self.client.base_url}{endpoint}"
        
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code >= 400:
            # Try to get a detailed error message from the API response
            error_detail = response.json().get("detail", response.text)
            raise Exception(f"API Error ({response.status_code}): {error_detail}")
            
        return response.json()

    def signup_with_face(self, image_path: str, custom_fields: Dict[str, Any] = None) -> FaceAuthResponse:
        """
        Registers a new user by their face.

        Args:
            image_path: The local file path to the user's image.
            custom_fields: Optional dictionary of custom data to store.

        Returns:
            A FaceAuthResponse object with the new user's details.
        """
        image_base64 = image_to_base64(image_path)
        payload = {"image_base64": image_base64}
        if custom_fields:
            payload["custom_fields"] = custom_fields
            
        response_data = self._post("/auth/signup-face", payload)
        return FaceAuthResponse(**response_data)

    def login_with_face(self, image_path: str) -> FaceAuthResponse:
        """
        Authenticates an existing user by their face.

        Args:
            image_path: The local file path to the user's image.

        Returns:
            A FaceAuthResponse object with the matched user's details.
        """
        image_base64 = image_to_base64(image_path)
        payload = {"image_base64": image_base64}
        
        response_data = self._post("/auth/login-face", payload)
        return FaceAuthResponse(**response_data)
