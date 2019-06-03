import os
import datetime
import logging
import logging.handlers
import traceback

## Class to handle all loggers
##
class MyLoggers(object):

	def __init__(self, Name = None, LogDirectory = None):
	
		if Name is None:
			raise Exception("Please give a name to the MyLoggers instance.")	
	
		# check log directory
		if LogDirectory is None:
			ThisDirectory = os.path.dirname(os.path.realpath(__file__))
			LogDirectory = os.path.join(ThisDirectory, 'logs')
			if not os.path.exists(LogDirectory):
				os.makedirs(LogDirectory)
				
		# create file handler
		AtkLogFileName = os.path.join(LogDirectory, '{}_{}.log'.format(datetime.datetime.now().strftime("%y%m%d_%H%M%S"), Name))
		fh = logging.handlers.RotatingFileHandler(
			filename = AtkLogFileName,
			maxBytes = 10*1024*1024,
			backupCount = 1000,
		)
		fh.setLevel(logging.DEBUG)
		
		# create console handler
		ch = logging.StreamHandler()
		ch.setLevel(logging.DEBUG)
		
		# create formatter and add it to the handlers
		formatter = logging.Formatter('%(asctime)s | %(name)20s | %(threadName)20s | %(levelname)10s | %(message)s')
		fh.setFormatter(formatter)
		ch.setFormatter(formatter)
		
		self.Name = Name
		self.fh   = fh
		self.ch   = ch
		
	def Create(self, LoggerName = None):
	
		if LoggerName is None:
			raise Exception("Please give a name to the logger.")
		
		# create new logger
		NewLogger = logging.getLogger(self.Name+"."+LoggerName)
		NewLogger.setLevel(logging.DEBUG)

		# add the handlers to the logger
		NewLogger.addHandler(self.fh)
		NewLogger.addHandler(self.ch)

		NewLogger.debug("Created logger")
		
		return NewLogger

## fcr loggers
##		
MyLoggersObj = MyLoggers(Name = "fcr")

## Function to create new logger
##
def CreateLogger(LoggerName = None):
	
	# get new logger
	LOG = MyLoggersObj.Create(LoggerName = LoggerName)
	
	# create associated logging decorator
	def handle_retval_and_log(func):
		
		def wrapper(*args, **kwargs):
			# get function call info
			func_call_info = traceback.extract_stack()[-2]
			
			# log function info
			LOG.debug("I    = {}:{}".format(func_call_info[0], func_call_info[1]))
			LOG.debug(" F   = {}".format(func))
			LOG.debug("  P  = {} {}".format(args, kwargs))
			
			# actual function call
			RetVal_ = func(*args, **kwargs)
			
			# log function results
			RetVal = None
			ResultBaseMessage = "   R ="
			if type(RetVal_) == list and len(RetVal_) == 2:
				if RetVal_[0] != 1:
					LOG.error("{} *** {}".format(ResultBaseMessage, RetVal_[1]))
					sys.exit(RetVal_[1])
				else:
					LOG.debug("{} {}".format(ResultBaseMessage, RetVal_[1]))
					RetVal = RetVal_[1]
			else:
				LOG.debug("{} {}".format(ResultBaseMessage, RetVal_))
				RetVal = RetVal_

			# settling delay (fixed)
			# time.sleep(0.1)

			# return
			return RetVal
		
		return wrapper
	
	return LOG, handle_retval_and_log
LOG, handle_retval_and_log = CreateLogger(__name__)
