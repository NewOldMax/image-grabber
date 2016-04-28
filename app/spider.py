import urllib
import eventlet
import os
import random

from grab.spider import Spider, Task
from model import RequestItem, Image, db
from app import app, socketio

class Spider(Spider):
    def prepare(self):
        self.base_url = self.initial_urls[0]
        self.downloader = urllib.URLopener()
        self.request_item = RequestItem(
            self.initial_urls[0],
            self.total,
            '',
            self.status
        )
        db.session.add(self.request_item)
        self.index = 0

    def task_initial(self, grab, task):
        self.request_item.title = grab.doc.select('//title').text()
        for elem in grab.xpath_list('//a[not(contains(@href, "http"))]'):
            if (self.index == self.total):
                self.status = 'success'
                self.info = 'All images grabbed'
                break
            else:
                yield Task('link', url=elem.get('href'))
        if (self.index != self.total):
            self.status = 'error'
            self.info = 'Not of all images grabbed'
        self.request_item.status = self.status
        self.request_item.info = self.info
        db.session.commit()
        with app.test_request_context('/'):
            socketio.emit('finish', 'finish')

    def task_link(self, grab, task):
        for image in grab.doc.select('//img'):
            try:
                if (self.index >= self.total):
                    self.status = 'success'
                    break
                src = image.attr('src')
                hash = os.urandom(16).encode('hex')
                filename = hash + src.split('/')[-1]
                self.downloader.retrieve(src, 'app/static/images/' + filename)
                image_item = Image(
                    self.request_item,
                    src,
                    filename)
                db.session.add(image_item)
                self.index += 1
                with app.test_request_context('/'):
                    socketio.emit('grabed_count')
                eventlet.greenthread.sleep(0)
            except Exception as e:
                continue