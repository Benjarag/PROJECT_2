class PaymentValidator:
    def validator(self, creditCard: dict):
        valid = self.validate_credit_card(creditCard)
        if valid == True:
            return 1
        return 0

    def validate_credit_card(self, creditCard_info):
        valid = True
        if not self._luhn_check(creditCard_info["cardNumber"]):
            valid = False
        if not self._expiry_and_cvc_validation(creditCard_info["expirationMonth"], creditCard_info["expirationYear"], creditCard_info["cvc"]):
            valid = False
        return valid

    def _luhn_check(self, cardNo):
        digits = len(cardNo)
        sum = 0
        isSecond = False
        for i in range(digits - 1, -1, -1):
            d = ord(cardNo[i]) - ord('0')
            if (isSecond == True):
                d = d * 2
            sum += d // 10
            sum += d % 10
            isSecond = not isSecond
        if (sum % 10 == 0):
            return True
        else:
            return False

    def _expiry_and_cvc_validation(self, month, year, cvc):
        if not (1 <= month <= 12):
            return False
        if not (year >= 2023) and len(str(year)) == 4:
            return False
        if not (cvc <= 999) and len(str(cvc)) == 3:
            return False
        return True
