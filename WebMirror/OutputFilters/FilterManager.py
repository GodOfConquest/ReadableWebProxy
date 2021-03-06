

import WebMirror.LogBase as LogBase
import WebMirror.OutputFilters.AmqpInterface
import config


class FilterManager(LogBase.LoggerMixin):


	loggerPath = "Main.SiteArchiver"

	def __init__(self):
		amqp_settings = {
			"RABBIT_LOGIN" : config.C_RABBIT_LOGIN,
			"RABBIT_PASWD" : config.C_RABBIT_PASWD,
			"RABBIT_SRVER" : config.C_RABBIT_SRVER,
			"RABBIT_VHOST" : config.C_RABBIT_VHOST,
		}

		self.amqp_conn = WebMirror.OutputFilters.AmqpInterface.RabbitQueueHandler(amqp_settings)



	def processPage(self, url, title, content, mimetype):
		pass
