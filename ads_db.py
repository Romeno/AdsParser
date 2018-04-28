# -*- coding: utf-8 -*-

from sqlalchemy import Column, ForeignKey, Integer, String, Text, TIMESTAMP,text, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class Mailbox(Base):
	__tablename__ = 'mailbox'

	id = Column(Integer, primary_key=True)
	server_ = Column(Text)			# сервер
	mail_name = Column(Text) 		# адрес электронной почты
	password = Column(Text) 		# пароль
	comment = Column(Text)			# комментарий
	last_update_time = Column(Integer)
	update_interval = Column(Integer)
	last_imap_time = Column(Integer)
	b_time = Column(Integer)
	time_load = Column(TIMESTAMP, server_default=text('NOW()'))
	user_load = Column(Text, server_default=text('"current_user"()'))


class MailboxStore(Base):
	__tablename__ = 'mailbox_store'

	message_id = Column(Integer, nullable=False, primary_key=True)	# ID сообщения
	message_udate = Column(TIMESTAMP) 				# Дата сообщения(число)
	message_date = Column(Text)						# Дата сообщения(текст)
	message_from = Column(Text)						# Отправитель
	message_subject = Column(Text)					# Тема сообщения
	message_body = Column(Text)						# Текст сообщения
	order_time = Column(TIMESTAMP)					# ИЗТелаСообщения\время
	name = Column(Text)								# ИЗТелаСообщения\Имя
	phone = Column(Text)							# ИЗТелаСообщения\Телефон
	email = Column(Text)							# ИЗТелаСообщения\E - mail
	adress = Column(Text)							# ИЗТелаСообщения\Адрес
	comment = Column(Text)							# ИЗТелаСообщения\Комментарий
	order = Column(Text)							# ИЗТелаСообщения\Заказ
	total = Column(Numeric)
	ip = Column(Text)								# ИЗТелаСообщения\IP
	riostat = Column(Text)							# ИЗТелаСообщения\riostat
	utm = Column(Text)								# ИЗТелаСообщения\utm
	path = Column(Text)								# Путь к файлу
	site = Column(Text)								# сайт
	mailbox = Column(Text, primary_key=True)		# ПочтаСайта


engine = None
DBSession = None
session = None


def connect(db_username, db_password, db_host, db_name):
	global engine
	global DBSession
	global session

	engine = create_engine('postgresql://{}:{}@{}/{}'.format(db_username, db_password, db_host, db_name))

	Base.metadata.bind = engine

	DBSession = sessionmaker(bind=engine)

	session = DBSession()


def create_db():
	Base.metadata.create_all(engine)


def get_servers():
	return session.query(Mailbox).all()


def store_to_db(parsed_message):
	new_msg = MailboxStore(message_id=parsed_message['message_id'],
						   message_udate=parsed_message['message_udate'],
						   message_date=parsed_message['message_date'],
						   message_from=parsed_message['message_from'],
						   message_subject=parsed_message['message_subject'],
						   message_body=parsed_message['message_body'],
						   order_time=parsed_message['order_time'],
						   name=parsed_message['name'],
						   phone=parsed_message['phone'],
						   email=parsed_message['email'],
						   adress=parsed_message['adress'],
						   comment=parsed_message['comment'],
						   order=parsed_message['order'],
						   total=parsed_message['total'],
						   ip=parsed_message['ip'],
						   riostat=parsed_message['roistat'],
						   utm=parsed_message['utm'],
						   path=parsed_message['path'],
						   site=parsed_message['site'],
						   mailbox=parsed_message['mailbox'])
	session.add(new_msg)
	session.commit()
