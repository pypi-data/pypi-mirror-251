from cloudeasy.github.session import Session


class User(Session):

    def get_user_profile(self):
        return self.get("user")

    def list_user_emails(self):
        return self.get("user/emails")

    def list_user_public_emails(self):
        return self.get("user/public_emails")
