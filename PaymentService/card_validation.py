
from pydantic import BaseModel, conint

class aCreditCard(BaseModel):
    cardNumber = str
    expirationMonth = conint(ge=1, le=12)
    expirationYear = int
    cvc = conint(ge=100, le=999)

class CreditCard:
    def __init__(self, cardNumber, expirationMonth, expirationYear, cvc) -> None:
        self.cardNumber = cardNumber
        self.expirationMonth = expirationMonth
        self.expirationYear = expirationYear
        self.cvc = cvc



class CardValidator:
    def __init__(self, credit_card: CreditCard) -> None:
        self.credit_card = credit_card
    
    def validate_card_number(self):

        #Access card number and change all values to integers
        pan = [int(i) for i in self.credit_card[::-1]]
        for i in pan:
            pan[i] = int(pan[i])

        #1=True, Other=False
        for i in range(1,len(pan),2):
            pan[i] *= 2
            if pan[i] > 9:
                pan[i] -= 9
        credit_sum = sum(pan)
        if credit_sum%10 == 0:
            return 1
        else:
            return 0

    def validate_expiration(self):
        if self.credit_card.expirationMonth < 1 or self.credit_card.expirationMonth > 12:
            return 0
        if len(self.credit_card.expirationYear) != 4:
            return 0
        
        return 1
    
    def validate_cvc(self):
        if len(self.credit_card.cvc) != 3:
            return 0
        
        return 1
    
    def validate_card(self):
        #If all validator function have return one we can conclude that all attributes of the card are validated
        pan_result = self.validate_card_number()
        expiration_result = self.validate_expiration()
        cvc_result = self.validate_cvc()
        if pan_result+expiration_result+cvc_result == 3:
            return True
        return False
    