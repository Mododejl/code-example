# -*- coding: utf-8 -*-
import re, os, BigWorld
from json import dumps
from json import loads
from os.path import isdir
from os.path import exists
from os.path import isfile
from datetime import datetime
from helpers import getClientVersion
from helpers import getShortClientVersion

class ConfigClass(object):

    def __init__(self):
        self.data = {}
        self.version = '0.1.0'
        self.author = 'Ekspoint'
        self.appName = 'loads_json'
        self.path = self.json_section()[3]
        self.appFile = 'mod_' + self.appName + '.json'
        self.default()
        self.load_info()
        self.load_json(self.appFile, self.path)
    
    def default(self):
        self.data = {'default': 'default'}
    
    def load_info(self): 
        self.configs = ['/'.join([self.path, self.appFile])]
        print '[NOTE] Loading mod: %s, [v.%s WOT: %s] by %s' % (self.appName,
        self.version, getClientVersion(), self.author)
        print '-------------------------------------------------------------------------'
        
    def comments(self, string): 
        if string:
            comment = []
            comments = False
            for line in string.split('\n'):
                if '/*' in line:
                    comments = True
                    continue
                if '*/' in line:
                    comments = False
                    continue
                if comments:
                    continue
                line = line.split('// ')[0]
                line = line.split('# ')[0]
                line = line.strip()
                if line: comment.append(line)
            string = '\n'.join(comment)
            for response in re.compile('\${"\w*/?\w*\.json"\}').findall(string):
                self.configs.append('/'.join(['%s', '%s']) % (self.path, response.replace('${"', '').replace('"}', '')))
                string = string.replace(response, '"ekspoint":""')
        return string

    def json_section(self):                
        clientVersion = getShortClientVersion().replace('v.', '').strip()
        gui_mods = '/'.join(['.', 'res_mods', clientVersion, 'scripts', 'client', 'gui', 'mods'])                
        configs = '/'.join(['.', 'res_mods', 'configs', 'ekspoint'])         
        mods = '/'.join(['.', 'mods', 'configs', 'ekspoint']) 
        return [gui_mods, configs, mods]
    
    def json_dumps(self, data):
        return dumps(data, sort_keys=True, indent=4, ensure_ascii=False, separators=(',', ': '))
                
    def byteify(self, input):
        if input:
            if isinstance(input, dict): return {self.byteify(key): self.byteify(value) for key, value in input.iteritems()}
            elif isinstance(input, list): return [self.byteify(element) for element in input]
            elif isinstance(input, unicode): return input.encode('utf-8')
            else: return input
        return input
        
    def association(self, data):
        for i in data:
            if type(data[i]) is dict and self.data.get(i): self.data[i].update(data[i])
            else: self.data[i] = data[i]   
                                  
    def load(self, new_path, mode = 'load'):
        if mode == 'load':
            for config in self.configs:
                with open(config, 'r') as json_file:
                    file_data = json_file.read().decode('utf-8-sig')
                    data = self.byteify(loads(self.comments(file_data)))
                    self.association(data)
                    json_file.close()
            return self.data
        if mode == 'read':
            with open(new_path, 'w+') as json_file:
                data = self.json_dumps(self.data)
                json_file.write('%s' % data)
                json_file.close()
            return self.data

    def file_time(self):
        return datetime.fromtimestamp(os.stat('/'.join([self.path, self.appFile]))[8]).strftime("%H:%M:%S")
    
    def autoReloadConfig(self):
        if self.data.get('autoReloadConfig', False):
            if self.file_time() > self.fileTime:
                self.update_configs()
                self.fileTime = self.file_time()
            BigWorld.callback(2, self.autoReloadConfig)
                                 
    def load_json(self, name, path, mode = 'load'):
        new_path = '/'.join(['%s', '%s']) % (path, name)
        if not exists(path):
            os.makedirs(path)
        if isdir(path):                   
            if mode == 'load':
                if isfile(new_path):
                    try:
                        self.load(new_path)
                        print '[%s]: Config file [%s] successfully loaded' % (self.appName, name)
                        print '-------------------------------------------------------------------------'
                    except Exception as error:
                        print '[%s]: Error: %s' % (self.appName, error)
                        print '[%s]: Config file [%s] is not configured correctly' % (self.appName, name)
                        print '[%s]: Loading of mod default config [%s]' % (self.appName, name.split('.')[0])
                        print '-------------------------------------------------------------------------'
                        return self.data
                else:
                    print '[%s]: Config file [%s] not found, create a new' % (self.appName, name)
                    self.load(new_path, 'read')
                    print '[%s]: Config file [%s] successfully created and loaded' % (self.appName, name)
                    print '-------------------------------------------------------------------------'
                self.fileTime = self.file_time()
                self.autoReloadConfig()
            elif mode == 'update':
                if isfile(new_path):
                    try:
                        self.load(new_path)
                        print '[%s]: Config file [%s] successfully updated and loaded' % (self.appName, name)
                        print '-------------------------------------------------------------------------'
                    except Exception as error:
                        print '[%s]: Error: %s' % (self.appName, error)
                        print '[%s]: Update failed, Config file [%s] is not configured correctly' % (self.appName, name)
                        print '[%s]: Loading of mod default config [%s]' % (self.appName, name.split('.')[0])
                        print '-------------------------------------------------------------------------'
                        return self.data   
                else:
                    print '[%s]: Update failed, Config file [%s] not found, create a new' % (self.appName, name)
                    self.load(new_path, 'read')
                    print '[%s]: Config file [%s] successfully created and loaded' % (self.appName, name)
                    print '-------------------------------------------------------------------------'
            elif mode == 'read':
                try:
                    self.load(new_path, 'read')
                except Exception as error:
                    print '[%s]: Error: %s' % (self.appName, error)
                    print '[%s]: Rewriting failed, Config file [%s] is not configured correctly' % (self.appName, name)
                    print '[%s]: Loading of mod default config [%s]' % (self.appName, name.split('.')[0])
                    print '-------------------------------------------------------------------------'
                    return self.data
        
    def read_configs(self): # внесение изменений в конфиг
        self.load_json(self.appFile, self.path, 'read')

    def update_configs(self): # обновление конфига
        self.load_json(self.appFile, self.path, 'update')
        
    
class Config(ConfigClass):

    def __init__(self):
        self.data = {}
        self.version = '0.1.0'
        self.author = 'Ekspoint'
        self.appName = 'test'
        self.path = self.json_section()[3]
        self.appFile = 'mod_' + self.appName + '.json'
        self.default()
        self.load_info()
        self.load_json(self.appFile, self.path)
    
    def default(self):
        self.data = {'test': 'good'}
        
        
configs = Config()

print configs.data['test']
