#encoding: utf-8
import Allhandlers
handlers = [
            (r'/', Allhandlers.IndexHandler),
            (r'/cart', Allhandlers.CartHandler),
            (r'/cart/status', Allhandlers.StatusHandler),
            (r'/push',Allhandlers.PushHandler)
        ]