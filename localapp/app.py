import logging 
from logging.handlers import RotatingFileHandler  
logging.basicConfig(format='%(asctime)s %(levelname)s :: %(message)s', level = logging.INFO) 
logger = logging.getLogger('pythonapp') 
handler = RotatingFileHandler("/home/ansible/app/app.log", mode='a', maxBytes=1000000, backupCount=100, encoding='utf-8', delay=0) 
handler.setLevel(logging.INFO) 
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')) 
logger.addHandler(handler)  
logger.info("This is an info level") 
logger.warning("THis is a warning log") 
logger.critical("This is critical!')

