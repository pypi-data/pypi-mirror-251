import sys
import json
import time
import traceback
import importlib
import requests
import datetime
import subprocess
import base64
import io
import os
import os.path
from threading import Thread

from nwebclient import web
from nwebclient import base
from nwebclient import util
from nwebclient import ticker
from nwebclient import NWebClient


ERROR_SERVER = 500
ERROR_UNKNOWN_JOB_TYPE = 599

class MoreJobs(Exception):
    """ raise MoreJobs([...]) """
    def __init__(self, jobs=[]):
        self.data = {'jobs': jobs}


class JobRunner(base.Base):

    MQTT_TOPIC = 'jobs'
    MQTT_RESULT_TOPIC = 'result'
    
    counter = 0 
    
    # Start Time
    start = None
    
    jobexecutor = None
    
    web = None
    
    def __init__(self, jobexecutor):
        super().__init__()
        self.jobexecutor = jobexecutor
        self.addChild(self.jobexecutor)
    def info(self, msg):
        #out = lambda msg: "[JobRunner] "+str(msg)
        print("[JobRunner] " + msg)
    def __call__(self, job):
        return self.execute_job(job)
    def execute(self, job):
        return self.execute_job(job)
    def execute_job(self, job):
        try:
            result = self.jobexecutor(job)
        except MoreJobs as mj:
            result = self.execute_data(mj.data)
        except Exception as e:
            self.info('Error: Job faild')
            result = job
            result['success'] = False
            result['error'] = True
            result['error_code'] = ERROR_SERVER
            result['error_message'] = str(e)
            result['trace'] = str(traceback.format_exc())
        return result
    def execute_data(self, data):
        self.start = datetime.datetime.now()
        result = {'jobs': []}
        for job in data['jobs']:
            job_result = self.execute_job(job)
            result['jobs'].append(job_result)
            self.counter = self.counter + 1
        delta = (datetime.datetime.now()-self.start).total_seconds() // 60
        self.info("Duration: "+str(delta)+"min")
        return result
    def execute_file(self, infile, outfile=None):
        try:
            data = json.load(open(infile))
            result = self.execute_data(data)
            outcontent = json.dumps(result)
            print(outcontent)
            if not outfile is None:
                if outfile == '-':
                    print(outcontent)
                else:
                    with open(outfile, 'w') as f:
                        f.write(outcontent)
        except Exception as e:
            self.info("Error: " + str(e))
            self.info(traceback.format_exc());
            self.info("Faild to execute JSON-File "+str(infile))
    def execute_mqtt(self, args, forever=False):
        from paho.mqtt import client as mqtt_client
        if 'mqtt_topic' in args:
            self.MQTT_TOPIC = args['mqtt_topic']
        if 'mqtt__result_topic' in args:
            self.MQTT_RESULT_TOPIC = args['mqtt_result_topic']
        self.mqtt = mqtt_client.Client('NPyJobRunner', transport='tcp')

        # client.username_pw_set(username, password)
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                self.info("Connected to MQTT Broker. Subscribe to Topic: " + self.MQTT_TOPIC)
                client.subscribe(self.MQTT_TOPIC)
            else:
                self.info("Failed to connect, return code %d\n", rc)

        def on_message(client, userdata, msg):
            data = json.loads(msg.payload.decode())
            result = self.execute(data)
            client.publish(self.MQTT_RESULT_TOPIC, json.dumps(result))
            #print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        # def on_log(client, userdata, level, buf):
        #    print("MQTT Log")
        self.mqtt.on_connect = on_connect
        self.mqtt.on_message = on_message
        # client.on_log = on_log
        self.mqtt.connect_async(args['MQTT_HOST'], args['MQTT_PORT'], keepalive=6000)
        if forever:
            self.mqtt.loop_forever()
        else:
            self.mqtt.loop_start()
    def execute_rest(self, port=8080, run=True, route='/', app=None):
        self.info("Starting webserver")
        from flask import Flask, request
        if app is None:
            app = Flask(__name__)
        #@app.route('/')
        #def home():
        #    return json.dumps(execute_data(request.form.to_dict(), jobexecutor))
        # Add To Root
        self.info("Executor: " + str(type(self.jobexecutor).__name__))
        self.jobexecutor.setupRestApp(app)
        app.add_url_rule(route, 'job_runner', view_func=lambda: json.dumps(self.execute_job({**request.args.to_dict(), **request.form.to_dict()})), methods=['GET', 'POST'])
        app.add_url_rule('/pysys/job-counter', 'job_counter', view_func=lambda: str(self.count))
        app.add_url_rule('/pysys/runner-ui', 'r_runner_ui', view_func=lambda self.page_ui())
        app.add_url_rule('/pysys/runner', 'r_runner', view_func=lambda: self.jobexecutor.page({**request.args.to_dict(), **request.form.to_dict()}))
        self.web = web.route_root(app, self.getRoot())
        if run:
            self.info("Flask.run(...)")
            app.run(host='0.0.0.0', port=int(port))
        else:
            return app
    def page_ui(self):
        p = base.Page()
        p.h1("Runner UI")
        p.script(web.js_fn('add', [], [
            '$ctrls = document.getElementById("ctrls");',
            '$d = document.createElement("div");',
            '$d.innerHTML = "<input class=\\"name\\" /><input class=\\"value\\" />"'
            '$ctrls.appendChild($d)'
            ])+
            web.js_fn('run', [], [
                'var data = {};'
                'document.querySelectorAll("#ctrl div").forEach(function(node) {',
                '  data[node.querySelector(".name").value] = node.querySelector(".value").value;'
                '});'
                # TODO fetch
            ])
        p.div(web.button_js("+",'add()'), id='ctrls')
        p.div(web.button_js("Run", 'run()'))
        p.div(id='result')
        p.hr()
        p.a("PyModule", 'pymodule')
        return p.simple_page()

        
class BaseJobExecutor(base.Base):
    def __init__(self):
        super().__init__()
    def __call__(self, data):
        return self.execute(data)
    def js(self):
        return web.js_fn('base_url', [], [
            '  var res = location.protocol+"//"+location.host;',
            '  res += "/";'
            '  return res;'
        ])+web.js_fn('post_url_encode', ['data'], [
            'var formBody = [];',
            'for (var property in data) {',
            '  var encodedKey = encodeURIComponent(property);',
            '  var encodedValue = encodeURIComponent(data[property]);',
            '  formBody.push(encodedKey + "=" + encodedValue);}',
            'return formBody.join("&");'
        ])+web.js_fn('post', ['data'], [
            'return {method:"POST",',
            ' headers: {'
            '  "Content-Type": "application/x-www-form-urlencoded"',
            ' },',
            ' body: post_url_encode(data)'
            '};'
        ])
    def execute(self, data):
        pass
    def canExecute(self, data):
        return True
    def setupRestApp(self, app):
        pass
    @classmethod
    def pip_install(cls):
        print("PIP Install")
        try:
            m = ' '.join(cls.MODULES)
            exe = sys.executable + ' -m pip install ' + m
            print("Install: " + exe)
            subprocess.run(exe.split(' '), stdout=subprocess.PIPE)
            print("Install Done.")
        except AttributeError:
            print("No Modules to install.")



class MultiExecutor(BaseJobExecutor):
    executors = []
    def __init__(self, *executors):
        self.executors = executors
    def execute(self, data):
        for exe in self.executors:
            if exe.canExecute(data):
                exe(data)
    def canExecute(self, data):
        for exe in self.executors:
            if exe.canExecute(data):
                return True
        return False

class SaveFileExecutor(BaseJobExecutor):
    filename_key = 'filename'
    content_key = 'content'
    def execute(self, data):
        with open(data[self.filename_key], 'w') as f:
            f.write(data[self.content_key])
    def canExecute(self, data):
        return 'type' in data and data['type']=='savefile'
    @staticmethod
    def run(data):
        r = SaveFileExecutor()
        return r(data)
    
class Pipeline(BaseJobExecutor):
    executors = []
    def __init__(self, *args):
        self.executors.extend(args)
        for item in self.executors:
            self.addChild(item)
    def execute(self, data):
        for item in self.executors:
            data = item(data)
        return data
      
class Dispatcher(BaseJobExecutor):
    key = 'type'
    runners = {}
    def __init__(self, key='type',**kwargs):
        #for key, value in kwargs.items():
        self.key = key
        self.runners = kwargs
        for item in self.runners.values():
            self.addChild(item)
    def execute(self, data):
        if self.key in data:
            runner = self.runners[data[self.key]]
            return runner(data)
        else:
            return {'success': False, 'message': "Key not in Data", 'data': data}
    def canExecute(self, data):
        if self.key in data:
            return data[self.key] in self.runners
        return False
    

class LazyDispatcher(BaseJobExecutor):
    key = 'type'
    classes = {}
    instances = {}
    def __init__(self, key='type',**kwargs):
        self.key = key
        self.loadDict(kwargs)
    def loadDict(self, data):
        if data is None:
            return
        for k in data.keys():
            v = data[k]
            if isinstance(v, str):
                try:
                    self.info("type:"+k+" "+v)
                    self.classes[k] = util.load_class(v)
                except ModuleNotFoundError:
                    self.error("Error: type: " + k + "Modul " + v + " not found.")
            else:
                self.loadRunner(k, v)
    def loadRunner(self, key, spec):
        self.info(f"Load runner: " + str(spec) + " key: " + str(key))
        if isinstance(spec, dict) and 'py' in spec:
            runner = eval(spec['py'], globals())
            self.addChild(runner)
            self.instances[key] = runner
        else:
            self.addChild(spec)
            self.instances[key] = spec
        web = getattr(self.owner(), 'web', None)
        if web is not None:
            spec.setupRestApp(web)

    def execute(self, data):
        if self.key in data:
            t = data[self.key]
            if t in self.instances:
                data = self.instances[t].execute(data)
            elif t in self.classes:
                c = self.classes[t]
                self.instances[t] = c()
                self.addChild(self.instances[t])
                data = self.instances[t].execute(data)
            elif 'list_runners' == t:
                return {'names': self.classes.keys()}
            # TODO elif: loadClass directly
            else:
                data['success'] = False
                data['error_code'] = ERROR_UNKNOWN_JOB_TYPE
                data['message'] = 'Unkown Type'
        else:
            data['message'] = "LazyDispatcher, No Dispatch Key, " + self.key
            data['success'] = False
        return data
    def canExecute(self, data):
        if self.key in data:
            return data[self.key] in self.classes or data[self.key] in ['list_runners']
        return False

    def page_dispatcher(self):
        return 'Dispatcher'

    def setupRestApp(self, app):
        app.add_url_rule('/pysys/dispatcher', 'dispatcher', view_func=lambda: self.page_dispatcher())
        for runner in self.instances.values():
            runner.setupRestApp(app)


class AutoDispatcher(LazyDispatcher):
    def __init__(self, key='type', **kwargs):
        super().__init__(key, **kwargs)
        args = util.Args()
        data = args.env('runners')
        if isinstance(data, dict):
            self.loadDict(data)
            self.info("Runner-Count: " + str(len(data)))
        elif len(self.classes) == 0:
            print("===================================================================================")
            self.info("Warning: No Runners configurated.")
            self.info("")
            self.info("Edit /etc/nweb.json")
            self.info("{")
            self.info("  \"runners\": {")
            self.info("      <name>: <class>,")
            self.info("      \"print\": \"nwebclient.runner:PrintJob\"")
            self.info("   }")
            self.info("}")
            list()
            print("===================================================================================")

        
class RestRunner(BaseJobExecutor):
    ssl_verify = False
    def __init__(self, url):
        self.url = url
    def execute(self, data):
        response = requests.post(self.url, data=data, verify=self.ssl_verify)
        return json.load(response.content)
    

class PrintJob(BaseJobExecutor):
    """ nwebclient.runner.PrintJob """
    def execute(self, data):
        print(json.dumps(data, indent=2))
        return data
    
class ImageExecutor(BaseJobExecutor):
    image = None
    image_key = 'image'
    def load_image(self, filename):
        with open(filename, "rb") as f:
            return base64.b64encode(f.read()).decode('ascii')
    def image_filename(self):
        filename = 'image_executor.png'
        self.image.save(filename)
        return filename
    def execute(self, data):
        if 'image_filename' in data:
            data[self.image_key] = self.load_image(data['image_filename'])
        if 'image_url' in data:
            response = requests.get(data['image_url'])
            self.image = Image.open(BytesIO(response.content))
            data = self.executeImage(self.image, data)
        elif self.image_key in data:
            from PIL import Image
            image_data = base64.b64decode(data[self.image_key])
            self.image = Image.open(io.BytesIO(image_data))
            data = self.executeImage(self.image, data)
        if 'unset_image' in data and self.image_key in data:
            dict.pop(self.image_key)
        return data
    def executeImage(self, image, data):
        return data
    

class NWebDocMapJob(BaseJobExecutor):
    def execute(self, data):
        # python -m nwebclient.nc --map --meta_ns ml --meta_name sexy --limit 100 --meta_value_key sexy --executor nxml.nxml.analyse:NsfwDetector --base nsfw.json
        from nwebclient import nc
        n = NWebClient(None)
        exe = util.load_class(data['executor'], create=True)
        filterArgs = data['filter']
        meta_ns = data['meta_ns']
        meta_name = data['meta_name']
        meta_value_key = data['meta_value_key']
        base  = data['base']
        dict_map = data['dict_map']
        update = data['update']
        limit  = data['limit']
        fn = nc.DocMap(exe, meta_value_key, base, dict_map)
        n.mapDocMeta(meta_ns=meta_ns, meta_name=meta_name, filterArgs=filterArgs, limit=limit, update=update, mapFunction=fn)
        data['count'] = fn.count
        return data


class TickerCmd(BaseJobExecutor):
    type='ticker_cmd'
    def execute(self, data):
        args = data['args']
        if isinstance(args, str):
            args = args.split(' ')
        data['result'] = self.onParentClass(ticker.Cpu, lambda cpu: cpu.cmd(args))
        return data
        
        
class PyModule(BaseJobExecutor):
    type = 'pymodule'
    def js(self):
        return super().js() + web.js_fn('exec_job', ['data'], [
            'fetch(base_url(), post(data)).then((response) => response.json()).then( (data) => { ',
            '  document.getElementById("result").innerHTML = JSON.stringify(data); ',
            '});'])
    def page_ui(self):
        p = base.Page(owner=self)
        p.h1("PyModule Executor")
        # eval_runner
        # eval_ticker
        p.div('modul.GpioExecutor(17)')
        p.input('py', id='py', placeholder='Python')
        p.input('modul', id='modul', placeholder='Module', value='nwebclient.runner')
        p += web.button_js("Add Runner", 'exec_job({type:"pymodule",modul:document.getElementById("modul").value,eval_runner:document.getElementById("py").value});')
        p += web.button_js("Add Ticker", 'exec_job({type:"pymodule",modul:document.getElementById("modul").value,eval_ticker:document.getElementById("py").value});')
        p.div('', id='result')
        p.tag('textarea', id='code',spellcheck='false')
        p += web.button_js("Exec", 'exec_job({type:"pymodule",exec:document.getElementById("code").value});')
        return p.simple_page()

    def setupRestApp(self, app):
        super().setupRestApp(app)
        route = '/pysys/pymodule'
        self.info("Route: " + route)
        app.add_url_rule(route, 'py_module_ui', view_func=lambda: self.page_ui())
    def execute(self, data):
        if 'modul' in data:
            modul = importlib.import_module(data['modul'])
            if 'run' in data:
                exe = getattr(modul, data['run'], None)
                return exe(data)
            if 'eval_runner' in data:
                runner = eval(data['eval_runner'], globals(), {'modul': modul})
                r_type = data['new_type'] if 'new_type' in data else runner.type
                self.owner().loadRunner(r_type, runner)
                return {'success': True, 'type': r_type}
            if 'eval_ticker' in data:
                ticker = eval(data['eval_ticker'], globals(), {'modul': modul})
                self.getRoot().add(ticker)
                return {'success': True}
        elif 'exec' in data:
            code = data['exec']
            self.info("exec:" + str(code))
            result = {}
            exec(code, globals(), {
                'owner': self,
                'result': result
            })
            return result
        elif 'file' in data:
            with open(data['file'],'r') as f:
                result = {}
                exec(f.read(), globals(), {
                    'owner': self,
                    'result': result
                })
                return result
            pass
        return {'success': False, 'message': 'PyModule Unknown'}

        

class PyEval(BaseJobExecutor):
    type = 'eval'
    def execute(self, data):
        return eval(data['eval'], globals(), {'data': data, 'runner': self.owner()})
    

class MainExecutor(AutoDispatcher):
    """
      python -m nwebclient.runner --executor nwebclient.runner:MainExecutor --rest --mqtt
    """
    def __init__(self, **kwargs):
        super().__init__(key='type', pymodule='nwebclient.runner:PyModule')
        self.execute({'type': 'pymodule'})


class CmdExecutor(BaseJobExecutor):
    pids = []
    type = 'cmd'
    def execute(self, data):
        if 'async' in data:
            pid = subprocess.popen(data['cmd'], stderr=subprocess.STDOUT, shell=True)
            self.pids.append(pid)
        else:
            try:
                data['output'] = subprocess.check_output(data['cmd'])
            except Exception as e:
                data['error_source'] = "CmdExecutor"
                data['error_message'] = str(e)
                #data['output'] = str(e.output)
        return data
    
    
class WsExecutor(BaseJobExecutor):
    type = 'ws'
    def execute(self, data):
        from nwebclient import ws
        w = ws.Website(data['url'])
        if 'py' in data:
            data['result'] = eval(data['py'], globals(), {'w': w})
        return data
    
    
class ThreadedQueueExecutor(BaseJobExecutor):
    queue = []
    thread = None
    job_count = 0
    def __init__(self, start_thread=True):
        super().__init__()
        self.queue = []
        self.job_count = 0
        self.thread = Thread(target=lambda: self.thread_main())
        self.thread.setName(self.__threadName())
        if start_thread:
            self.thread.start()
    def __threadName(self):
        return 'ThreadedQueueExecutor'
    def thread_start(self):
        self.info("Thread begin")
    def thread_main(self):
        self.info("Thread started")
        self.thread_start()
        while True:
            self.thread_tick()
    def thread_tick(self):
        try:
            if not len(self.queue) == 0:
                print("In Thread Job Tick")
                first = self.queue[0]
                self.queue.remove(first)
                self.thread_execute(first)
                self.job_count += 1
        except Exception as e:
            self.error("Exception: " + str(e))
    def thread_execute(self, data):
        pass
    def is_busy(self):
        return len(self.queue)>0
    def execute(self, data):
        if 'start_thread' in data:
            self.thread.start()
            return {'success': True}
        else:
            self.queue.append(data)
        return {
          'message': "Result from ThreadedQueueExecutor",
          'request_data': data
        }

class GpioExecutor(BaseJobExecutor):
    """
       modul.GpioExecutor(22)

    """
    type = 'gpio'
    pin = None
    state = False
    def __init__(self, pin=None):
        super().__init__()
        if pin is not None:
            self.initPin(pin)
    def initPin(self, pin):
        import RPi.GPIO as GPIO
        # sudo apt-get install python-rpi.gpio
        self.pin = int(pin)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.gpio = GPIO
        self.output(False)
        return {'success': True}

    def output(self, state):
        self.state = state
        self.gpio.output(self.pin, state)
        return {'success': True}

    def page_ui(self):
        p = base.Page(owner=self)
        p.h1("GPIO BCM " + str(self.pin) + " State: " + str(self.state))
        p.style('button { padding: 10px;font-size: 150%; font-weight: bold;}')
        p.script(web.js_fn('exec_job', ['data'], [
            'fetch(base_url(), post(data)).then((response) => response.json()).then( (data) => { ',
            '  document.getElementById("result").innerHTML = JSON.stringify(data); ',
            '});'
        ]))
        p += web.button_js("Pulse", 'exec_job({type:"gpio",pulse:1000});')
        p += web.button_js("On", 'exec_job({type:"gpio",high:1});')
        p += web.button_js("Off", 'exec_job({type:"gpio",low:1});')
        p.div('', id='result')
        return p.simple_page()

    def setupRestApp(self, app):
        super().setupRestApp(app)
        app.add_url_rule('/pysys/gpio', 'gpio', view_func=lambda: self.page_ui())

    def execute(self, data):
        if 'high' in data:
            return self.output(True)
        if 'low' in data:
            return self.output(False)
        if 'pulse' in data:
            self.output(True)
            time.sleep(float(data['pulse'])/1000)
            self.output(False)
            return {'success': True}
        if 'init' in data:
            return self.initPin(data['init'])
        return super().execute(data)




class SerialExecutor(ThreadedQueueExecutor):
    """
      python -m nwebclient.runner --executor nwebclient.runner:SerialExecutor --rest --mqtt

      Connect:
        curl -X GET "http://192.168.178.79:8080/?port=/dev/ttyS0"
        curl -X GET "http://192.168.178.79:8080/?start_thread=true"
        curl -X GET "http://192.168.178.79:8080/?send=Hallo"
        curl -X GET "http://192.168.178.79:8080/?enable=rs485"
        curl -X POST https://reqbin.com/ -H "Content-Type: application/x-www-form-urlencoded"  -d "param1=value1&param2=value2"

    """
    MODULES = ['pyserial']
    type = 'serial'
    #port = '/dev/ttyUSB0'
    # S0
    port = '/dev/ttyAMA0'
    baudrate = 9600
    serial = None
    send = None
    buffer = ''
    rs485 = False
    send_pin = 17 #S3
    gpio = None

    def __init__(self, start_thread=False, port = None, baudrate = None):
        super().__init__(start_thread=start_thread)
        if port is not None:
            self.port = port
        if baudrate is not None:
            self.baudrate = baudrate

    def _sendData(self):
        if self.send is not None:
            if self.rs485:
                self.gpio.output(self.send_pin, True)
            self.serial.write((self.send + "\n").encode())
            self.send = None
            if self.rs485:
                self.gpio.output(self.send_pin, False)
    def thread_tick(self):
        self._sendData()
        line = self.serial.readline()
        if line != -1:
            self.info(line.decode('ascii'))
            self.buffer += line.decode('ascii') + "\n"
    def thread_start(self):
        import serial
        #from serial.tools import list_ports
        # https://github.com/ShyBoy233/PyGcodeSender/blob/main/pyGcodeSender.py
        self.info("Connect to " + self.port)
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=3)
            self.info("Connected.")
        except Exception as e:
            self.error("Connection failed. " + str(e))
    def enableRs485(self, data):
        import RPi.GPIO as GPIO
        # sudo apt-get install python-rpi.gpio
        if 'pin' in data:
            self.send_pin = int(data['pin'])
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.send_pin, GPIO.OUT)
        GPIO.output(self.send_pin, False)
        self.gpio = GPIO
        self.rs485 = True
        return {'success': self.rs485, 'pin': self.send_pin, 'mode': 'BCM'}

    def read_buffer(self):
        buf = self.buffer
        self.buffer = ''
        return {'buffer': buf}

    def execute(self, data):
        if 'send' in data:
            self.send = data['send']
            return {'result': 'queued'}
        elif 'port' in data:
            self.port = data['port']
            return {'success': True}
        elif 'info' in data:
            return {'baud': self.baudrate, 'port': self.port}
        elif 'getbuffer' in data:
            return {'buffer': self.buffer}
        elif 'readbuffer' in data:
            return self.read_buffer()
        elif 'enable' in data and data['enable'] == 'rs485':
            return self.enableRs485(data)
        else:
            return super().execute(data)
    def page_ctrl(self):
        p = base.Page(owner=self)
        p.h1("Serial Executor")
        p.script(web.js_fn('exec_job', ['data'], [
            'fetch(base_url(), post(data)).then((response) => response.json()).then( (data) => { ',
            '  document.getElementById("result").innerHTML = JSON.stringify(data); ',
            '});'
        ]))
        p += web.button_js("Connect", 'exec_job({type:"serial",start_thread:true});')
        p += web.button_js("ttyS0", 'exec_job({type:"serial",port:"/dev/ttyS0"});')
        p += web.button_js("ttyUSB0", 'exec_job({type:"serial",port:"/dev/ttyUSB0"});')
        p += web.button_js("Enable RS485", 'exec_job({type:"serial",enable:"rs485"});')
        p += web.button_js("Send", 'exec_job({type:"serial",send:"Hallo"});')
        p += web.button_js("Info", 'exec_job({type:"serial",info:1});')
        p += web.button_js("Get Buffer", 'exec_job({type:"serial",getbuffer:1});')
        p.div('', id='result')
        return p.simple_page()

    def setupRestApp(self, app):
        super().setupRestApp(app)
        app.add_url_rule('/pysys/serial_ctrl', 'serial_ctrl', view_func=lambda: self.page_ctrl())

    def page(self, params):
        # link to action
        return self.buffer


class GCodeExecutor(ThreadedQueueExecutor):
    """
      python -m nwebclient.runner --executor nwebclient.runner:GCodeExecutor --rest

      git -C ~/nwebclient/ pull && pip3 install ~/nwebclient/ && python3 -m nwebclient.runner --executor nwebclient.runner:GCodeExecutor --rest

      
      UI: http://127.0.0.1:8080/runner
    """
    MODULES = ['pyserial']
    type='gcode'
    port = '/dev/ttyUSB0'
    baudrate = 250000
    serial = None
    timeout_count = 0
    log = None
    mqtt_topic = 'main'
    def __init__(self, start_thread=False):
        super().__init__(start_thread=start_thread)
        self.timeout_count = 0
        self.args = util.Args()
        self.initMqtt()
    def initMqtt(self):
        mqtt_host = self.args.env('MQTT_HOST')
        if mqtt_host is not None: 
            self.log = ticker.MqttPub(host=mqtt_host)
            self.log(self.mqtt_topic,'__init__')
    def __len__(self):
        return len(self.queue)
    def prn(self, msg):
        print(msg)
        if self.log is not None:
            self.log(self.mqtt_topic, msg)
    def thread_start(self):
        import serial
        #from serial.tools import list_ports
        # https://github.com/ShyBoy233/PyGcodeSender/blob/main/pyGcodeSender.py
        self.info("Connect to " + self.port)
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=3)
            self.info("Connected.")
        except Exception as e:
            self.error("Connection faild. " + str(e))
    def thread_execute(self, data):
        if 'gcode' in data:
            self.execGCode(data['gcode'])
    def execGCode(self, gcode):
        if gcode.strip().startswith(';') or gcode.isspace() or len(gcode) <=0:
            return
        self.info(gcode)
        self.serial.write((gcode+'\n').encode())
        while(1): # Wait untile the former gcode has been completed.
            line = self.serial.readline()
            self.info(line.decode('ascii'))
            if line.startswith(b'ok'):
                break
            self.timeout_count += 1
            # print("readline timeout")
    def is_connected(self):
        return self.serial is not None
    def queueGCode(self, gcode):
        self.queue.append({'gcode': gcode})
    def moveX(self, val = 10):
        self.queueGCode('G0 X'+str(val))
    def moveY(self, val = 10):
        self.queueGCode('G0 Y'+str(val))
    def moveZ(self, val = 10):
        self.queueGCode('G0 Z'+str(val))
    def heatBed(self, temp):
        self.queueGCode('M190 S'+str(temp)); # M140 for without wait
    def heatE0(self, temp):
        self.queueGCode('M109 T0 S'+str(temp)); # M104
    # G92 X0 Y0 Z0 ; Set Home
    def __repr__(self):
        return "GCode(queue({0}),thread, port:{1} count:{2})".format(len(self), self.port, self.job_count)
    def moveControls(self):
        return """
          <table>
            <tr>
              <td></td>
              <td><a href="?gcode=G1%20Y10">Y+</a></td>
              <td></td>
              <td><a href="?gcode=G1%20Z10">Z+</a></td>
            </tr>
            <tr>
              <td><a href="?gcode=G1%20X-10">X-</a></td>
              <td></td>
              <td><a href="?gcode=G1%20X10">X+</a></td>
              <td></td>
            </tr>
            <tr>
              <td></td>
              <td><a href="?gcode=G1%20Y-10">Y-</a></td>
              <td></td>
              <td><a href="?gcode=G1%20Z-10">Z-</a></td>
            </tr>
          <table>
          <div>
            <a href="?gcode=M109%20T0%20S205">Heat E0 205</a>
            <a href="?gcode=M190%20S60">Heat Bed 60</a>
            <a href="?gcode=G1%20E5">Extrude</a>
            <a href="?gcode=G92%20X0%20Y0%20Z0">Set Home</a>
            <a href="?a=connect">Connect</a>
          </div>
          <div>
            Einstellungen:
            <a href="?gcode=M17">M17 Steppers On</a><br />
            <a href="?gcode=M18">M18 Steppers Off</a><br />
            <a href="?gcode=M82">M82 E Absolute Pos</a><br />
            <a href="?gcode=M83">M83 E Relativ Pos</a><br />
            <a href="?gcode=M92%20E10%20X10%20Y10%20Z50">M92 Steps per Unit</a><br />
            <a href="?gcode=G90">G90 Absolute Pos</a><br />
            <a href="?gcode=G91">G91 Relativ Pos</a><br />
            <a href="?gcode=G92%20X0%20Y0%20Z0">G92 Set Home here</a><br />
            <a href="?gcode=M121">M121 Disable Endstops</a><br />
            <a href="?gcode=M204%20T10">M204 Setze Beschleunigung</a><br />
            GCode: """ +str(self.args.env('GCODE_PATH'))+ """
          </div>
          <button id="btnFocus">Tastatur</button>
        """
    def gcodes(self):
        path = self.args.env('GCODE_PATH')
        if path is None:
            path = '.'
        files = [f for f in os.listdir(path) if os.path.isfile(path+'/'+f)]
        html = ''
        for f in files:
            html += '<li><a href="?file='+str(f)+'">'+str(f)+'</a></li>'
        return '<div><span title="'+path+'">GCodes:</span><br /><ul>'+html+'</ul></div>'
    def queueFile(self, file):
        path = self.args.env('GCODE_PATH')
        if path is None:
            path = '.'
        f = path + '/' + file
        with open(f, 'r') as fh:
            for line in fh.readlines():
                self.queueGCode(line)
    def handleActions(self, params):
        try:
            if 'gcode' in params:
                self.queue.append(params)
            if 'a' in params and params['a']=='connect':
                print("Start Thread")
                self.thread.start()
            if 'a' in params and 'port' in params and params['a']=='set_port':
                self.port = params['port']
            if 'a' in params and 'baudrate' in params and params['a']=='set_baudrate':
                self.port = params['baudrate']
            if 'file' in params:
                self.queueFile(params['file'])
        except Exception as e:
            return "Error: " + str(e)
        return ""
    def js(self):
        return """
         $(function() {
               function gcode(code) {
                 console.log(code);
                 $.get('?gcode='+encodeURI(code));
               };
               $('#btnFocus').click(function() {
                $(document).bind('keydown', function (evt) {
                    console.log(evt.keyCode);
                    switch (evt.keyCode) {
                        case 40: // Pfeiltaste nach unten
                        case 98: // Numpad-2
                            gcode('G0 Y-1');
                            return false; break;
                        case 38: // nach oben
                        case 104: // Numpad-8
                            gcode('G0 Y1');
                            return false; break;
                        case 37: // Pfeiltaste nach links
                        case 100: // Numpad-4
                            gcode('G0 X-1');
                            return false; break;
                        case 39: 
                        case 102: // NumPad-6
                            gcode('G0 X1');
                            return false; break;
                        // w=87
                        // S=83
                        // NumPad+ = 107
                        // NumPad- = 109
                    }		
                });
               });
               
            
            });
        """
    def page(self, params):
        p = base.Page()
        p += '<script src="https://bsnx.net/4.0/templates/sb-admin-4/vendor/jquery/jquery.min.js"></script>'
        p += '<script>'+self.js()+'</script>'
        p += self.handleActions(params) + self.__repr__() + self.moveControls() + self.gcodes()
        return p.simple_page()



restart_process = None

def restart(args):
    global restart_process
    newargs = args.argv[1:]
    newargs.remove('--install')
    newargs = [sys.executable, '-m', 'nwebclient.runner', '--sub'] + newargs
    print("Restart: " + ' '.join(newargs))
    #subprocess.run(newargs, stdout=subprocess.PIPE)
    with subprocess.Popen(newargs, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, bufsize=1, universal_newlines=True) as p:
        restart_process = p
        for line in p.stdout:
            print(line, end='') # process line here
    exit()

def list():
    import inspect
    clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
    print("Executors: ")
    for c in clsmembers:
        if issubclass(c[1], BaseJobExecutor):
            print("  " + str(c[0]))

def usage(exit_program=False):
    print("Usage: "+sys.executable+" -m nwebclient.runner --install --ticker 1 --executor module:Class --in in.json --out out.json")
    print("")
    print("Options:")
    print("  --install           Installiert die Abhaegigkeiten der Executoren")
    print("  --rest              Startet den Buildin Webserver")
    print("  --mqtt              Verbindet MQTT")
    print("  --ticker 1          Startet einen nwebclient.ticker paralell")
    print("  --executor          Klasse zum Ausführen der Jobs ( nwebclient.runner.AutoDispatcher )")
    print("                          - nwebclient.runner.AutoDispatcher")
    print("")
    list()
    if exit_program:
        exit()

def main():
    try:
        args = util.Args()
        print("nwebclient.runner Use --help for more Options")
        if args.help_requested():
            usage(exit_program=True)
        if args.hasFlag('list'):
            list()
            exit()
        executor = args.getValue('executor')
        if executor is None:
            print("No executor found. Using AutoDispatcher")
            executor = AutoDispatcher()
        print("Executor: " + str(executor))
        if args.hasFlag('install'):
            print("Install")
            util.load_class(executor, create=False).pip_install()
            if not args.hasFlag('--exit'):
                restart(args)
        else:
            jobrunner = util.load_class(executor, create=True)
            runner = JobRunner(jobrunner)
            if args.hasFlag('ticker'):
                ticker.create_cpu(args).add(ticker.JobExecutor(executor=runner)).loopAsync()
            if args.hasFlag('rest'):
                if args.hasFlag('mqtt'):
                    runner.execute_mqtt(args)
                runner.execute_rest(port=args.getValue('port', 8080), run=True)
            elif args.hasFlag('mqtt'):
                runner.execute_mqtt(args, True)
            else:
                runner.execute_file(args.getValue('in', 'input.json'), args.getValue('out', 'output.json'))
    except KeyboardInterrupt:
        print("")
        print("Exit nwebclient.runner")
        if not restart_process is None:
            print("Close Sub")
            restart_process.terminate()

        
if __name__ == '__main__':
    main()
            
#import signal
#def sigterm_handler(_signo, _stack_frame):
#    # Raises SystemExit(0):
#    sys.exit(0)
#
#    signal.signal(signal.SIGTERM, sigterm_handler)
