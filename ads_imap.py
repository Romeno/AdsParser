# -*- coding: utf-8 -*-

import ads_parser
import ads_db

from itertools import chain
import imaplib
import datetime
import email
import logging


def get_ads_email(host, port, username, password, from_uid):
	criteria = {
		# 'FROM': '',
		# 'SUBJECT': '',
		# 'BODY': '',
	}
	uid_min = from_uid

	logger = logging.getLogger()

	# Produce search string in IMAP format:
	#   e.g. (FROM "me@gmail.com" SUBJECT "abcde" BODY "123456789" UID 9999:*)
	def search_string(uid_min, criteria):
		c = list(map(lambda t: (t[0], '"' + str(t[1]) + '"'), criteria.items())) + [('UID', '%d:*' % (uid_min + 1))]
		return '(%s)' % ' '.join(chain(*c))

	with imaplib.IMAP4_SSL(host, port) as server:
		server.login(username, password)
		server.select()

		result, data = server.uid('search', None, search_string(uid_min, criteria))

		uids = [int(s) for s in data[0].split()]
		for uid in uids:
			# Have to check again because Gmail sometimes does not obey UID criterion.
			if uid > uid_min:
				result, data = server.uid('fetch', str(uid), '(RFC822)')  # fetch entire message
				logger.info("Got UID {}".format(uid))
				# msg = email.message_from_bytes(data[0][1])

				# uid_min = uid
				#
				# text = get_first_text_block(msg)

				email_msg, body = ads_parser.extract_email_body(data[0][1], uid)
				if not email_msg:
					logger.info("Skipping message with UID {}".format(uid))
					continue

				ad_data = ads_parser.parse_ads_email(body)

				if ad_data.get('total'):
					ad_data['total'] = int(ad_data['total'])

				if ad_data.get('order_time'):
					ad_data['order_time'] = datetime.datetime.strptime(ad_data['order_time'], '%H:%M:%S %d.%m.%Y')

				ad_data['message_id'] = uid
				ad_data['message_udate'] = email_msg['date'].datetime
				ad_data['message_date'] = str(email_msg['date'])
				ad_data['message_from'] = email_msg['from']
				ad_data['message_subject'] = email_msg['subject']
				ad_data['message_body'] = body
				ad_data['mailbox'] = username

				ads_db.store_to_db(ad_data)
