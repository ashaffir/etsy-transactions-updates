import my_pkce
from config import ETSY_X_API_KEY


class CODEGEN:
    def __init__(self):
        self.code_verifier = my_pkce.generate_code_verifier(length=32)
        self.code_challenge = my_pkce.get_code_challenge(self.code_verifier)
        self.state = "dkflre"
        self.client_id = ETSY_X_API_KEY
        self.file_path = ""

    def listing_code_generator(self):
        scope = "listings_r"
        full_url = f"https://www.etsy.com/oauth/connect?response_type=code&redirect_uri=http://localhost:8000/oauth/redirect&scope={scope}&client_id={self.client_id}&state={self.state}&code_challenge={self.code_challenge}&code_challenge_method=S256"

        return full_url

    def user_code_generator(self):
        scope = "email_r"
        full_url = f"https://www.etsy.com/oauth/connect?response_type=code&redirect_uri=http://localhost:8000/oauth/redirect&scope={scope}&client_id={self.client_id}&state={self.state}&code_challenge={self.code_challenge}&code_challenge_method=S256"

        return full_url

    def transactions_generator(self):
        scope = "transactions_w"
        full_url = f"https://www.etsy.com/oauth/connect?response_type=code&redirect_uri=http://localhost:8000/oauth/redirect&scope={scope}&client_id={self.client_id}&state={self.state}&code_challenge={self.code_challenge}&code_challenge_method=S256"
        return full_url
