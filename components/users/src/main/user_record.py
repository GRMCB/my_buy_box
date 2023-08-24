from search_parameters import SearchParameters

class UserRecord:
    def __init__(self, user_id: str, zip_code: str, redfin_search_parameters: RedfinSearchParameters):
        self.user_id = user_id
        self.zip_code = zip_code
        self.redfin_search_parameters = redfin_search_parameters
