class PaymentMail:
    def __init__(self, orderId, buyerMail, merchantMail, state) -> None:
        self.orderId = orderId
        self.buyerMail = buyerMail
        self.merchantMail = merchantMail
        self.state = state