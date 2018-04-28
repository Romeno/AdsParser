# -*- coding: utf-8 -*-

import ads_db
import ads_imap
import ads_parser

from sqlalchemy import desc
import logging


def init_logger():
	from logging.config import dictConfig

	logging_config = {
		'version': 1,
		'disable_existing_loggers': False,
		'formatters': {
			'f': {
				'format':
					'%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
			}
		},
		'handlers': {
			'h': {
				'class': 'logging.handlers.RotatingFileHandler',
				'formatter': 'f',
				'level': 'DEBUG',
				'filename': 'errors.log',
				'maxBytes': 10485760,
				'backupCount': 20,
				'encoding': 'utf8'
			}
		},
		'root': {
			'handlers': ['h'],
			'level': logging.DEBUG,
		},
	}

	dictConfig(logging_config)


def main():
	init_logger()

	db_username = "postgres"
	db_password = ""
	db_host = "localhost"
	db_name = "AdsTest"

	logger = logging.getLogger()

	try:
		ads_db.connect(db_username, db_password, db_host, db_name)
		for mailbox in ads_db.get_servers():
			logger.info("Getting mail for mailbox {}".format(mailbox.mail_name))

			q = ads_db.session.query(ads_db.MailboxStore)
			last_message = q.filter(ads_db.MailboxStore.mailbox == mailbox.mail_name).order_by(desc(ads_db.MailboxStore.message_id)).first()
			last_uid = 0
			if last_message:
				last_uid = last_message.message_id

			logger.info("Last time stopped on UID {}".format(last_uid))

			server, port = ads_parser.parse_server_(mailbox)
			if server:
				ads_imap.get_ads_email(server, port, mailbox.mail_name, mailbox.password, last_uid)
	except Exception as e:
		logger.exception("Exception during parser run")
		raise


if __name__ == "__main__":
	main()

