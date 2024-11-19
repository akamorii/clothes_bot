from yookassa import Configuration, Payment
from vars import ACCOUNT_ID, PAYMENT_TOKEN
import uuid

import asyncio

Configuration.account_id = ACCOUNT_ID
Configuration.secret_key = PAYMENT_TOKEN

async def make_payment (amount:float, desctiption = 'test'):
    payment = Payment.create({
    "amount": {
        "value": amount,
        "currency": "RUB"
    },
    "confirmation": {
        "type": "redirect",
        "return_url": "https://www.example.com/return_url"
    },
    "capture": True,
    "description": desctiption
}, uuid.uuid4())
    return dict(payment)


async def get_payment_status(pay_id):
    return dict(Payment.find_one(pay_id))  
    
    
async def main():
   await make_payment()

if __name__ == "__main__":
    asyncio.run(main())