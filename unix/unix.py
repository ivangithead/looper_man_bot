from datetime import datetime

def unix_to_date(unix: int) -> str:
	return datetime.fromtimestamp(unix).strftime("%d/%m/%Y %H:%M")