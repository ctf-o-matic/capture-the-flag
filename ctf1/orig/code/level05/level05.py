#!/usr/bin/env python
import logging
import json
import optparse
import os
import pickle
import random
import re
import string
import sys
import time
import traceback
import urllib

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

LOGGER_NAME = 'queue'
logger = logging.getLogger(LOGGER_NAME)
logger.addHandler(logging.StreamHandler(sys.stderr))

TMPDIR = '/tmp/level05'


class Job(object):
    QUEUE_JOBS = os.path.join(TMPDIR, 'jobs')
    QUEUE_RESULTS = os.path.join(TMPDIR, 'results')

    def __init__(self):
        self.id = self.generate_id()
        self.created = time.time()
        self.started = None
        self.completed = None

    def generate_id(self):
        return ''.join([random.choice(string.ascii_letters) for i in range(20)])

    def job_file(self):
        return os.path.join(self.QUEUE_JOBS, self.id)

    def result_file(self):
        return os.path.join(self.QUEUE_RESULTS, self.id)

    def start(self):
        self.started = time.time()

    def complete(self):
        self.completed = time.time()


class QueueUtils(object):
    @staticmethod
    def deserialize(serialized):
        logger.debug('Deserializing: %r' % serialized)
        parser = re.compile('^type: (.*?); data: (.*?); job: (.*?)$', re.DOTALL)
        match = parser.match(serialized)
        direction = match.group(1)
        data = match.group(2)
        job = pickle.loads(match.group(3))
        return direction, data, job

    @staticmethod
    def serialize(direction, data, job):
        serialized = """type: %s; data: %s; job: %s""" % (direction, data, pickle.dumps(job))
        logger.debug('Serialized to: %r' % serialized)
        return serialized

    @staticmethod
    def enqueue(type, data, job):
        logger.info('Writing out %s data for job id %s' % (type, job.id))
        if type == 'JOB':
            file = job.job_file()
        elif type == 'RESULT':
            file = job.result_file()
        else:
            raise ValueError('Invalid type %s' % type)

        serialized = QueueUtils.serialize(type, data, job)
        with open(file, 'w') as f:
            f.write(serialized)
            f.close()


class QueueServer(object):
    # Called in server
    def run_job(self, data, job):
        QueueUtils.enqueue('JOB', data, job)
        result = self.wait(job)
        if not result:
            result = (None, 'Job timed out', None)
        return result

    def wait(self, job):
        job_complete = False
        for i in range(10):
            if os.path.exists(job.result_file()):
                logger.debug('Results file %s found' % job.result_file())
                job_complete = True
                break
            else:
                logger.debug('Results file %s does not exist; sleeping' % job.result_file())
                time.sleep(0.2)

        if job_complete:
            f = open(job.result_file())
            result = f.read()
            os.unlink(job.result_file())
            return QueueUtils.deserialize(result)
        else:
            return None


class QueueWorker(object):
    def __init__(self):
        # ensure tmp directories exist
        if not os.path.exists(Job.QUEUE_JOBS):
            os.mkdir(Job.QUEUE_JOBS)
        if not os.path.exists(Job.QUEUE_RESULTS):
            os.mkdir(Job.QUEUE_RESULTS)

    def poll(self):
        while True:
            available_jobs = [os.path.join(Job.QUEUE_JOBS, job) for job in os.listdir(Job.QUEUE_JOBS)]
            for job_file in available_jobs:
                try:
                    self.process(job_file)
                except Exception, e:
                    logger.error('Error processing %s' % job_file)
                    traceback.print_exc()
                else:
                    logger.debug('Successfully processed %s' % job_file)
                finally:
                    os.unlink(job_file)
            if available_jobs:
                logger.info('Processed %d available jobs' % len(available_jobs))
            else:
                time.sleep(1)

    def process(self, job_file):
        serialized = open(job_file).read()
        type, data, job = QueueUtils.deserialize(serialized)

        job.start()
        result_data = self.perform(data)
        job.complete()

        QueueUtils.enqueue('RESULT', result_data, job)

    def perform(self, data):
        return data.upper()


class QueueHttpServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(404)
        self.send_header('Content-type','text/plain')
        self.end_headers()

        output = { 'result' : "Hello there! Try POSTing your payload. I'll be happy to capitalize it for you." }
        self.wfile.write(json.dumps(output))
        self.wfile.close()

    def do_POST(self):
        length = int(self.headers.getheader('content-length'))
        post_data = self.rfile.read(length)
        raw_data = urllib.unquote(post_data)

        queue = QueueServer()
        job = Job()
        type, data, job = queue.run_job(data=raw_data, job=job)
        if job:
            status = 200
            output = { 'result' : data, 'processing_time' : job.completed - job.started, 'queue_time' : time.time() - job.created }
        else:
            status = 504
            output = { 'result' : data }

        self.send_response(status)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write(json.dumps(output, sort_keys=True, indent=4))
        self.wfile.write('\n')
        self.wfile.close()

def run_server():
    try:
        server = HTTPServer(('127.0.0.1', 9020), QueueHttpServer)
        logger.info('Starting QueueServer')
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info('^C received, shutting down server')
        server.socket.close()

def run_worker():
    worker = QueueWorker()
    worker.poll()

def main():
    parser = optparse.OptionParser("""%prog [options] type""")
    parser.add_option('-v', '--verbosity', help='Verbosity of debugging output.',
                      dest='verbosity', action='count', default=0)
    opts, args = parser.parse_args()
    if opts.verbosity == 1:
        logger.setLevel(logging.INFO)
    elif opts.verbosity >= 2:
        logger.setLevel(logging.DEBUG)

    if len(args) != 1:
        parser.print_help()
        return 1

    if args[0] == 'worker':
        run_worker()
    elif args[0] == 'server':
        run_server()
    else:
        raise ValueError('Invalid type %s' % args[0])

    return 0

if __name__ == '__main__':
    sys.exit(main())
