from __future__ import print_function
import urllib
import eventlet
import os
import random

from grab.spider import Spider, Task
from model import RequestItem, Image, db
from app import app, socketio

eventlet.monkey_patch()

class Spider(Spider):
    def prepare(self):
        self.base_url = self.initial_urls[0]
        self.downloader = urllib.URLopener()
        self.request_item = RequestItem(
            self.initial_urls[0],
            self.total,
            '',
            self.result_status
        )
        db.session.add(self.request_item)
        self.result_counter = 0
        self.urls = [];

    def task_initial(self, grab, task):
        self.request_item.title = grab.doc.select('//title').text()
        for elem in grab.xpath_list('//a[not(contains(@href, "http"))]'):
            if (self.result_counter >= self.total):
                self.result_status = 'success'
                self.info = 'All images grabbed'
                self.request_item.status = self.result_status
                self.request_item.info = self.info
                db.session.commit()
                with app.test_request_context('/'):
                    socketio.emit('finish', 'finish', namespace='/main')
                eventlet.sleep(0)
                self.stop()
                return
            else:
                if elem.get('href') not in self.urls:
                    self.urls.append(elem.get('href'))
                    yield Task('link', url=elem.get('href'))
        if (self.result_counter != self.total):
            self.result_status = 'error'
            self.info = 'Not of all images grabbed'
        else:
            self.request_item.status = self.result_status
            self.request_item.info = self.info
            db.session.commit()
            with app.test_request_context('/'):
                socketio.emit('finish', 'finish', namespace='/main')
            eventlet.sleep(0)
            self.stop()

    def task_link(self, grab, task):
        for image in grab.doc.select('//img'):
            try:
                if (self.result_counter >= self.total):
                    self.result_status = 'success'
                    self.info = 'All images grabbed'
                    self.request_item.status = self.result_status
                    self.request_item.info = self.info
                    db.session.commit()
                    with app.test_request_context('/'):
                        socketio.emit('finish', 'finish', namespace='/main')
                    eventlet.sleep(0)
                    self.stop()
                    return
                src = image.attr('src')
                hash = os.urandom(16).encode('hex')
                filename = hash + src.split('/')[-1]
                self.downloader.retrieve(src, 'app/static/images/' + filename)
                self.result_counter += 1
                image_item = Image(
                    self.request_item,
                    src,
                    filename)
                db.session.add(image_item)
                with app.test_request_context('/'):
                    socketio.emit('grabed_count', self.result_counter, namespace='/main')
                eventlet.sleep(0)
            except Exception as e:
                continue