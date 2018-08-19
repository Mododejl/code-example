# -*- coding: utf-8 -*-
from gui.SystemMessages import SM_TYPE
from gui.SystemMessages import pushMessage
from gui.Scaleform.daapi.view.lobby.LobbyView import LobbyView

class EventHook(object):

    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        if handler in self.__handlers:
            self.__handlers.remove(handler)
        return self

    def fire(self, *args, **keywargs):
        for handler in self.__handlers:
            handler(*args, **keywargs)

    def clearObjectHandlers(self, inObject):
        for theHandler in self.__handlers:
            if theHandler.im_self == inObject:
                self -= theHandler

           
class HookMethod(object):
    
    def __init__(self):
        self.log = self.log_exception
        self.registerEvent = self.hook_decorator(self.register_event) 
        self.overrideMethod = self.hook_decorator(self.override_method)
        self.overrideClassMethod = self.hook_decorator(self.override_classmethod)
        self.overrideStaticMethod = self.hook_decorator(self.override_staticmethod)
    
    def logtrace(self, func=None):
        import traceback, sys
        print '=' * 20 + ' [ekspointCore] - detected error start '.upper() + '=' * 20
        if func:  
            logging = []
            etype, value, tb = sys.exc_info()
            co_filename = func.func_code.co_filename.replace('\\', '/')
            filename = co_filename.split('/')[co_filename.count('/')].replace('.pyc', '').replace('.py', '') if co_filename.count('/') else co_filename
            for scriptName in sys.modules.keys():
                if filename in scriptName:
                    scriptDir = str(sys.modules[scriptName]).split('from')[1].replace(' ', '').replace('>', '').replace("'", '')           
                    for values in traceback.format_exception(etype, value, tb): 
                        if func.func_code.co_filename in values:
                            values = '  File "%s", line %d, in %s\n' % (scriptDir, tb.tb_lineno, func.func_code.co_name)
                        logging.append(values)   
                    count = len(logging) - 1
                    logging[count] = logging[count].replace('\n', '')
                    print ''.join(logging)
        else:
            traceback.print_stack()
        print '=' * 20 + ' [ekspointCore] - detected error stop '.upper() + '=' * 21
    
    def event_handler(self, func, prepend, e, m, *a, **k):
        try:
            if prepend:
                e.fire(*a, **k)
                r = m(*a, **k)
            else:
                r = m(*a, **k)
                e.fire(*a, **k)
            return r
        except:
            self.logtrace(func)
            
    def override_handler(self, func, orig, *a, **k):
        try: 
            return func(orig, *a, **k)
        except:
            self.logtrace(func)
  
    def log_exception(self, func):
        
        def exception(*a, **k):
            try: 
               return func(*a, **k)
            except: 
               self.logtrace(func)
               
        return exception
         
    def hook_decorator(self, func):
        
        def decorator1(*a, **k):
             
            def decorator2(handler):
                func(handler, *a, **k)

            return decorator2

        return decorator1
        
    def override(self, cls, method, newm):
        orig = getattr(cls, method)
        if type(orig) is not property:
            setattr(cls, method, newm)
        else:
            setattr(cls, method, property(newm)) 
               
    def register_event(self, handler, cls, method, prepend = False):
        evt = '__event_%i_%s' % (1 if prepend else 0, method)
        if hasattr(cls, evt):
            e = getattr(cls, evt)
        else:
            newm = '__orig_%i_%s' % (1 if prepend else 0, method)
            setattr(cls, evt, EventHook())
            setattr(cls, newm, getattr(cls, method))
            e = getattr(cls, evt)
            m = getattr(cls, newm)
            l = lambda *a, **k: self.event_handler(handler, prepend, e, m, *a, **k)
            l.__name__ = method
            setattr(cls, method, l)
        e += handler
            
    def override_method(self, handler, cls, method):
        orig = getattr(cls, method)
        newm = lambda *a, **k: self.override_handler(handler, orig, *a, **k)
        newm.__name__ = method
        self.override(cls, method, newm)

    def override_staticmethod(self, handler, cls, method):
        orig = getattr(cls, method)
        newm = staticmethod(lambda *a, **k: self.override_handler(handler, orig, *a, **k))
        self.override(cls, method, newm)
        
    def override_classmethod(self, handler, cls, method):
        orig = getattr(cls, method)
        newm = classmethod(lambda *a, **k: self.override_handler(handler, orig, *a, **k))
        self.override(cls, method, newm)
        
            
hookMethod = HookMethod()   

show = True

@hookMethod.registerEvent(LobbyView, '_populate')
@hookMethod.log
def populate(self):
    global show
    if show:
        show = False
        pushMessage(u'<font color="#D042F3">Hello world</font>', SM_TYPE.GameGreeting)



# если в классе то так

class Hello(object):
    
    def __init__(self):
        self.show = True
        hookMethod.registerEvent(LobbyView, '_populate')(hookMethod.log(self.populate))
        
    def populate(self, base_self):
        if self.show:
            self.show = False
            pushMessage(u'<font color="#D042F3">Hello world</font>', SM_TYPE.GameGreeting)
            

Hello()
