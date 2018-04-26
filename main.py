

def get_ads_email():
	import time
	from itertools import chain
	import imaplib

	imap_ssl_host = 'imap.gmail.com'  # imap.mail.yahoo.com
	imap_ssl_port = 993
	username = 'RomenoEx@gmail.com'
	password = 'Cidikk#3Pljhjdmt'

	# Restrict mail search. Be very specific.
	# Machine should be very selective to receive messages.
	criteria = {
		'FROM': 'PRIVILEGED EMAIL ADDRESS',
		'SUBJECT': 'SPECIAL SUBJECT LINE',
		'BODY': 'SECRET SIGNATURE',
	}
	uid_max = 0

	def search_string(uid_max, criteria):
		c = list(map(lambda t: (t[0], '"' + str(t[1]) + '"'), criteria.items())) + [('UID', '%d:*' % (uid_max + 1))]
		return '(%s)' % ' '.join(chain(*c))

	# Produce search string in IMAP format:
	#   e.g. (FROM "me@gmail.com" SUBJECT "abcde" BODY "123456789" UID 9999:*)


	def get_first_text_block(msg):
		type = msg.get_content_maintype()

		if type == 'multipart':
			for part in msg.get_payload():
				if part.get_content_maintype() == 'text':
					return part.get_payload()
		elif type == 'text':
			return msg.get_payload()

	server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
	server.login(username, password)
	server.select('INBOX')

	result, data = server.uid('search', None, search_string(uid_max, criteria))

	uids = [int(s) for s in data[0].split()]
	if uids:
		uid_max = max(uids)
	# Initialize `uid_max`. Any UID less than or equal to `uid_max` will be ignored subsequently.

	server.logout()

	# Keep checking messages ...
	# I don't like using IDLE because Yahoo does not support it.
	while 1:
		# Have to login/logout each time because that's the only way to get fresh results.

		server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
		server.login(username, password)
		server.select('INBOX')

		result, data = server.uid('search', None, search_string(uid_max, criteria))

		uids = [int(s) for s in data[0].split()]
		for uid in uids:
			# Have to check again because Gmail sometimes does not obey UID criterion.
			if uid > uid_max:
				result, data = server.uid('fetch', uid, '(RFC822)')  # fetch entire message
				msg = email.message_from_string(data[0][1])

				uid_max = uid

				text = get_first_text_block(msg)
				print('New message :::::::::::::::::::::')
				print(text)

		server.logout()
	time.sleep(1)


def parse_ads_email(body):
	import re

	rules = [
		# regex, field name
		(re.compile(r'^\s*время заказа:(.*)$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'order_time'),
		(re.compile(r'^\s*имя:(.*)$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'client_name'),
		(re.compile(r'^\s*телефон:(.*)$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'phone_number'),
		(re.compile(r'^\s*e-mail:(.*)$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'email'),
		(re.compile(r'^\s*адрес:(.*)$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'address'),
		(re.compile(r'^\s*комментарии:(.*)$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'comments'),
		(re.compile(r'^\s*заказ:(.*?)\n\n', re.UNICODE | re.IGNORECASE | re.DOTALL | re.MULTILINE), 'order'),
		(re.compile(r'^\s*итого:(.*)$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'order_cost'),
		(re.compile(r'^\s*ip:(.*)$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'ip'),
		(re.compile(r'^\s*\[roistat\](.*)\[/roistat\]\s*?$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'roistat'),
		(re.compile(r'^\s*\[utm\](.*)\[/utm\]\s*?$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'utm'),
	]

	results = {}

	lines = body.split('\n')
	it_lines = iter(lines)

	line = next(it_lines)
	while not line or line.isspace():
		line = next(it_lines)

	results['wesbite'] = line.strip()

	for rule in rules:
		m = rule[0].search(body)
		if m:
			results[rule[1]] = m.group(1).strip()

	return results


def store_to_db(data):
	import sqlalchemy




def extract_email_body():
	from email.parser import Parser
	from email.policy import default

	with open('i:\\message.txt', encoding='utf-8') as f:
		# data = f.read()
		p = Parser(policy=default)
		msg = p.parse(f)

		body = msg.get_body(['plain']).get_payload()

		print('To: {}'.format(msg['to']))
		print('From: {}'.format(msg['from']))
		print('Subject: {}'.format(msg['subject']))

		# You can also access the parts of the addresses:
		print('Recipient username: {}'.format(msg['to'].addresses[0].username))
		print('Sender name: {}'.format(msg['from'].addresses[0].display_name))

		return body


def test():
	import time
	from itertools import chain
	import imaplib

	imap_ssl_host = 'imap.gmail.com'  # imap.mail.yahoo.com
	imap_ssl_port = 993
	username = 'RomenoEx@gmail.com'
	password = 'Cidikk#3Pljhjdmt!'

	# Restrict mail search. Be very specific.
	# Machine should be very selective to receive messages.
	criteria = {
		'FROM': 'no-reply@twitch.tv',
		# 'SUBJECT': 'SPECIAL SUBJECT LINE',
		# 'BODY': 'SECRET SIGNATURE',
	}
	uid_max = 0

	def search_string(uid_max, criteria):
		c = list(map(lambda t: (t[0], '"' + str(t[1]) + '"'), criteria.items())) + [('UID', '%d:*' % (uid_max + 1))]
		return '(%s)' % ' '.join(chain(*c))

	# Produce search string in IMAP format:
	#   e.g. (FROM "me@gmail.com" SUBJECT "abcde" BODY "123456789" UID 9999:*)


	def get_first_text_block(msg):
		type = msg.get_content_maintype()

		if type == 'multipart':
			for part in msg.get_payload():
				if part.get_content_maintype() == 'text':
					return part.get_payload()
		elif type == 'text':
			return msg.get_payload()

	server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
	server.login(username, password)
	server.select('INBOX')

	result, data = server.uid('search', None, search_string(uid_max, criteria))

	uids = [int(s) for s in data[0].split()]
	if uids:
		uid_max = max(uids)
	# Initialize `uid_max`. Any UID less than or equal to `uid_max` will be ignored subsequently.

	server.logout()

	# Keep checking messages ...
	# I don't like using IDLE because Yahoo does not support it.
	while 1:
		# Have to login/logout each time because that's the only way to get fresh results.

		server = imaplib.IMAP4_SSL(imap_ssl_host, imap_ssl_port)
		server.login(username, password)
		server.select('INBOX')

		result, data = server.uid('search', None, search_string(uid_max, criteria))

		uids = [int(s) for s in data[0].split()]
		for uid in uids:
			# Have to check again because Gmail sometimes does not obey UID criterion.
			if uid > uid_max:
				result, data = server.uid('fetch', uid, '(RFC822)')  # fetch entire message
				msg = email.message_from_string(data[0][1])

				uid_max = uid

				text = get_first_text_block(msg)
				print('New message :::::::::::::::::::::')
				print(text)

		server.logout()
	time.sleep(1)


def main():
	get_ads_email()
	body = extract_email_body()
	ad_data = parse_ads_email(body)
	store_to_db(ad_data)


if __name__ == "__main__":
	body = extract_email_body()
	print(parse_ads_email(body))
