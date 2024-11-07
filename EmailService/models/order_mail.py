class OrderMail:
    def __init__(self, orderId, buyerMail, merchantMail, productName, totalPrice) -> None:
        self.orderId = orderId
        self.buyerMail = buyerMail
        self.merchantMail = merchantMail
        self.productName = productName
        self.totalPrice = totalPrice