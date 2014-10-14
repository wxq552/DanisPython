#encoding: utf-8
import tornado.web
import handlers
"""路径配置文件，配置各种url的匹配与对应RequestHandler的映射关系"""
handlers = [
            (r"/",handlers.IndexHandler),
            (r"/article_page/(\d+)/",handlers.IndexHandler),
        ]

