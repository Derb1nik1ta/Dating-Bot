import logging 


# admins logger
admins_logger = logging.getLogger('AdminsLogger')
admins_handler = logging.FileHandler('database\\logging_files\\01_admins.log', 'a', encoding='utf-8')
admins_logger.setLevel(logging.INFO)
admins_logger.addHandler(admins_handler)

# owner logger
owner_logger = logging.getLogger('OwnerLogger')
owner_handler = logging.FileHandler('database\\logging_files\\01_owner.log', 'a', encoding='utf-8')
owner_logger.setLevel(logging.INFO)
owner_logger.addHandler(owner_handler)

# error logger
error_logger = logging.getLogger('ErorrLogger')
error_handler = logging.FileHandler('database\\logging_files\\01_error_db.log', 'a', encoding='utf-8')
error_logger.setLevel(logging.ERROR)
error_logger.addHandler(error_handler)
