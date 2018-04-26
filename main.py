

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
		# regex, field name, is multiline?
		(re.compile(r'\s*(.*)\s*', re.UNICODE | re.IGNORECASE), 'website', False),
		(re.compile(r'время заказа:\s*(.*)', re.UNICODE | re.IGNORECASE), 'order_time', False),
		(re.compile(r'имя:\s*(.*)', re.UNICODE | re.IGNORECASE), 'client_name', False),
		(re.compile(r'телефон:\s*(.*)', re.UNICODE | re.IGNORECASE), 'phone_number', False),
		(re.compile(r'e-mail:\s*(.*)', re.UNICODE | re.IGNORECASE), 'email', False),
		(re.compile(r'адрес:\s*(.*)', re.UNICODE | re.IGNORECASE), 'address', False),
		(re.compile(r'комментарии:\s*(.*)', re.UNICODE | re.IGNORECASE), 'comments', False),
		(re.compile(r'order:\s*(.*)', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'order', True),
		(re.compile(r'итого:\s*(.*)', re.UNICODE | re.IGNORECASE), 'order_cost', False),
		(re.compile(r'ip:\s*(.*)', re.UNICODE | re.IGNORECASE), 'order_cost', False),
		(re.compile(r'[roistat](.*)[/roistat]', re.UNICODE | re.IGNORECASE), 'roistat', False),
		(re.compile(r'\s*[utm](.*)[/utm]\s*', re.UNICODE | re.IGNORECASE), 'utm', False),
	]

	results = {}

	lines = body.split('\n')
	it_lines = iter(lines)

	skip_till_empty_line = False
	for l in it_lines:
		if l.isspace() or skip_till_empty_line:
			skip_till_empty_line = False
			continue

		for rule in rules:
			m = rule[0].search(l)
			if m:
				results[rule[1]] = m.group(0)
			skip_till_empty_line = rule[2]


def store_to_db():
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
	parse_ads_email(body)
	store_to_db()


if __name__ == "__main__":
	body = extract_email_body()
	parse_ads_email(body)
