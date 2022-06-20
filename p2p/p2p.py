from pyqiwip2p import QiwiP2P
from data import QIWITOKEN

statuses = ["PAID", "WAITING", "REJECTED", "EXPIRED"]

def create_bill(amount: int, lifetime: int=60) -> tuple:
	"""amount - рубли, lifetime - минуты"""
	try:
		p2p = QiwiP2P(auth_key=QIWITOKEN)
		bill = p2p.bill(amount=amount, lifetime=lifetime)

		return (bill.bill_id, bill.pay_url)
	except Exception as ex:
		pass
		### LOG

def check_bill_state(bill_id: str) -> str:
	try:
		p2p = QiwiP2P(auth_key=QIWITOKEN)

		return p2p.check(bill_id=bill_id).status
	except Exception as ex:
		pass
		### LOG