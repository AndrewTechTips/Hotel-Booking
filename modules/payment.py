class CreditCard:
    def __init__(self, number, expiration, holder, cvc):
        self.number = str(number)
        self.expiration = str(expiration)
        self.holder = holder.upper().strip()
        self.cvc = str(cvc)

    def validate(self, df_cards_dict):
        card_data = {
            "number": self.number,
            "expiration": self.expiration,
            "holder": self.holder,
            "cvc": self.cvc,
        }

        return card_data in df_cards_dict


class SecureCreditCard(CreditCard):
    def authenticate(self, given_password, df_security_dict):
        if self.number in df_security_dict:
            return df_security_dict[self.number] == given_password

        return False
