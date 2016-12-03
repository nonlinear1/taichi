import taichi as tc
import taichi.util
# TODO: Remove cv2
import cv2
import time
import os
from taichi.core import tc_core
from taichi.util import *

class Renderer(object):
    def __init__(self, name, output_dir=taichi.util.get_uuid(), overwrite=False):
        self.c = tc_core.create_renderer(name)
        self.output_dir = output_dir + '/'
        try:
            os.mkdir(self.output_dir)
        except Exception as e:
            print e
            if not overwrite:
                exit(-1)

    def initialize(self, **kwargs):
        self.c.initialize(config_from_dict(kwargs))

    def render(self, stages, cache_interval=1000):
        for i in range(stages):
            print 'stage', i,
            t = time.time()
            self.render_stage()
            print 'time:', time.time() - t
            self.show()
            if i % cache_interval == 0:
                self.write('%07d.png' % i)

    def get_full_fn(self, fn):
        return self.output_dir + fn

    def write(self, fn):
        self.write_output(self.get_full_fn(fn))

    def show(self):
        self.write('tmp.png')
        cv2.imshow('Rendered', cv2.imread(self.get_full_fn('tmp.png')))
        cv2.waitKey(1)

    def __getattr__(self, key):
        return self.c.__getattribute__(key)

class Camera:
    def __init__(self, name, **kwargs):
        self.c = tc_core.create_camera(name)
        self.c.initialize(config_from_dict(kwargs))
