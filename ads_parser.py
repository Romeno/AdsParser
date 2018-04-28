# -*- coding: utf-8 -*-

import re
from email.parser import BytesParser
from email.policy import default
import logging

rules = [
	# regex, column name
	(re.compile(r'^\s*время заказа:(.*)$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'order_time'),
	(re.compile(r'^\s*имя:(.*)$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'name'),
	(re.compile(r'^\s*телефон:(.*)$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'phone'),
	(re.compile(r'^\s*e-mail:(.*)$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'email'),
	(re.compile(r'^\s*адрес:(.*)$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'adress'),

	(re.compile(r'^\s*комментарии:(.*?)\r?\n\r?\n', re.UNICODE | re.IGNORECASE | re.DOTALL | re.MULTILINE), 'comment'),
	(re.compile(r'^\s*заказ:(.*?)\r?\n\r?\n', re.UNICODE | re.IGNORECASE | re.DOTALL | re.MULTILINE), 'order'),

	(re.compile(r'^\s*итого:\s*(\d*).*?$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'total'),
	(re.compile(r'^\s*ip:(.*)$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'ip'),
	(re.compile(r'^\s*\[roistat\](.*)\[/roistat\].*?\s*?$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'roistat'),
	(re.compile(r'^\s*\[utm\](.*)\[/utm\].*?\s*?$', re.UNICODE | re.IGNORECASE | re.MULTILINE), 'utm'),
]


def parse_server_(mailbox):
	regex = re.compile("\{(.*?):(\d+).*\}")
	m = regex.match(mailbox.server_)
	if not m:
		logger = logging.getLogger()
		logger.error('Failed to get server and port from string {} of Mailbox item with id {}'.format(mailbox.server_, mailbox.id))
		return None, None
	else:
		return m.group(1), m.group(2)


def extract_email_body(rfc2822, uid):
	# with open('i:\\message.txt', encoding='utf-8') as f:
	# 	# data = f.read()
	p = BytesParser(policy=default)
	msg = p.parsebytes(rfc2822)

	plain_body = msg.get_body(['plain'])
	if plain_body:
		body = plain_body.get_content()
	else:
		logger = logging.getLogger()
		logger.warning('No plain body for message with UID {}'.format(uid))
		html_body = msg.get_body(['html'])
		if html_body:
			logger.warning('But HMTL body exist and contains: {}'.format(html_body.get_content()))

		return None, None

	return msg, body


def parse_ads_email(body):
	results = {
		'order_time': None,
		'name': '',
		'phone': '',
		'email': '',
		'adress': '',
		'comment': '',
		'order': '',
		'total': 0,
		'ip': '',
		'roistat': '',
		'utm': '',
	}

	lines = body.split('\n')
	it_lines = iter(lines)

	line = next(it_lines)
	while not line or line.isspace():
		line = next(it_lines)

	results['site'] = line.strip()
	results['path'] = ''

	for rule in rules:
		m = rule[0].search(body)
		if m:
			results[rule[1]] = m.group(1).strip()

	return results
