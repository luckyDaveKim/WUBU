#-*- coding: utf-8 -*-
import os
import inspect
import sys
sys.path.append('./module')

class autoTestHandler():
    def __init__(self):
        self.register_module_list = []
        self.enable_module_list = []
        self.info="" #TODO info 설정 필요한 내용들 로드하여 각 모듈에 전달

    def proving (self, path):
        """ Dynamically Modules Proving """
        module_list = []
        for module_file_name in os.listdir(path):
            module_name, ext = os.path.splitext(module_file_name)
            if ext == '.py':
                module_list.append(module_name)
       
        for module_name in module_list:
            module = __import__(module_name)
            for obj_type in dir(module):
                cls_type = getattr(module, obj_type)
                if inspect.isclass(cls_type) is True and 'register' in dir(cls_type):
                    if cls_type not in self.register_module_list:
                        self.register_module_list.append(cls_type)

    def activation(self):
        for module in self.register_module_list:
            self.enable_module_list.append(module(self.info))

    def process(self):
        self.proving("./module")
        self.activation()
        for module in self.enable_module_list:
            if module.checkUse() == 1:
                print("=====================")
                module.printComment()
                module.process()
        
if __name__ == "__main__":
    at = autoTestHandler()
    at.process()

