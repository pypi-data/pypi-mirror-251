import threading
import time
import logging
import json
import queue
import paho.mqtt.client as mqtt

from abc import abstractmethod, ABC
from pydantic import BaseModel
from typing import Any, Callable

logger = logging.getLogger(__name__)

class Message(BaseModel):
    payload:Any = None
    message_id:int
    transmitter_id:str

class AbstractMessager(ABC):
    @abstractmethod
    def start():
        raise NotImplementedError()
    
    @abstractmethod
    def stop():
        raise NotImplementedError()
    
    @abstractmethod
    def publish_message(self, topic: str, payload: Any, timeout:int=5, on_publish:Callable|None=None, wait_for_response:bool=True):
        raise NotImplementedError()
    
    @abstractmethod
    def reply_to_message(self, payload:Any, original_message:Message)->None:
        raise NotImplementedError()

    @abstractmethod
    def subscribe(self, topic: str, callback: Callable|None = None):
        raise NotImplementedError()
    


MESSAGERS:dict[str, AbstractMessager] = {}

class MQTTMessager(AbstractMessager):    
    def __init__(
        self,
        name:str, 
        mqtt_host:str,
        mqtt_port:int,
        transmitter_id:str, 
        enable_tls:bool=False, 
        username:str='username', 
        password:str='password', 
        ca_cert_location:str='./certs/ca-root-cert.crt'
    ):
        self.name = name
        self.mqtt_host = mqtt_host
        self.mqtt_port = mqtt_port
        self.transmitter_id = transmitter_id
        self.username = username
        self.password = password

        self.message_id = 0
        self.mqtt_client = mqtt.Client()
        self.stopflag = threading.Event()
        self.main_thread = None

        if enable_tls:
            logger.info('TLS is enabled on the mqqt client')
            self.mqtt_client.tls_set(ca_certs=ca_cert_location)
            self.mqtt_client.tls_insecure_set(False)
        else:
            logger.warning('TLS is disabled on the mqqt client')
        self.mqtt_client.on_connect = self.on_connect
        self.mqtt_client.on_disconnect = self.on_disconnect
        self.mqtt_client.on_publish = self.on_publish
        self.mqtt_client.on_message = self.on_message

        self.response_queue:dict[int, queue.Queue[Message]] = {}
        self.messages_info:dict[int, mqtt.MQTTMessageInfo] = {}
        self.topic_to_callback:dict[str, Callable] = {}


        self.connected = False       
        self.lock = threading.Lock()

    def start(self):
        def _start():
            while not self.stopflag.set():
                try:
                    self.mqtt_client.username_pw_set(
                        self.username, 
                        self.password
                    )
                    self.mqtt_client.connect(
                        self.mqtt_host,
                        self.mqtt_port
                    )
                    self.subscribe(f'msgbox/{self.transmitter_id}', self.on_receive_message)
                    break
                except Exception as e:
                    logger.exception(f'{self.name}: Failure to connect to opra2opra mqtt broker on first try')
                time.sleep(1)
            self.mqtt_client.loop_forever()
        self.main_thread = threading.Thread(target=_start, daemon=True)
        self.main_thread.start() 

    def stop(self):
        self.stopflag.set()
        self.mqtt_client.disconnect()

    def publish(self, topic: str, payload: Any, on_publish:Callable|None=None):
        with self.lock:
            message_info = self.mqtt_client.publish(topic, payload)
        if on_publish is not None:
            self.messages_info[message_info.mid] = on_publish

    def publish_message(self, topic: str, payload: Any, timeout:int=5, on_publish:Callable|None=None, wait_for_response=True)->Message:
        with self.lock:
            self.message_id += 1
            message_id = self.message_id
        payload = Message(
            payload=payload, 
            message_id=message_id, 
            transmitter_id=self.transmitter_id
        )
        self.response_queue[message_id] = queue.Queue(maxsize=1) #prepare blocking queue to wait for response
        with self.lock:
            message_info = self.mqtt_client.publish(topic, payload=payload.model_dump_json(), qos=2)
        if on_publish is not None:
            self.messages_info[message_info.mid] = on_publish
        if not wait_for_response:
            return None
        try:
            response = self.response_queue[message_id].get(timeout=timeout)
        except queue.Empty:
            raise TimeoutError('No response was received within timeout')
        finally:
            del self.response_queue[message_id]
        return response

    def reply_to_message(self, payload:Any, original_message:Message)->None:
        message = Message(
            payload=payload, 
            message_id=original_message.message_id, 
            transmitter_id=self.transmitter_id
        )
        receiver = original_message.transmitter_id
        self.publish(f'msgbox/{receiver}', message.model_dump_json())

    def on_receive_message(self, message:Message):
        rq = self.response_queue.get(message.message_id, None)
        if rq is None:
            logger.error(f'Received a reply to message with id {message.message_id} but no response queue has been registrated')
            return 
        rq.put(message)

    def subscribe(self, topic: str, callback: Callable, qos=2):
        logger.info(f"Subscribing to topic {topic}")
        self.mqtt_client.subscribe(topic, qos)
        self.topic_to_callback[topic] = callback
        
    def on_connect(self, client, userdata, flags, rc):
        self.connected = True
        logger.info(f'Successfully connected to opra2opra mqtt broker ({self.mqtt_host}:{self.mqtt_port})')

    def on_disconnect(self, client, userdata, rc):
        self.connected = False
        logger.error('Connection to opra2opra mqtt broker lost')

    def on_publish(self, mqttc, userdata, mid):
        logger.info(f"Successfully published message with 'mid' id {mid} to mqtt broker")
        try:
            f = self.messages_info.pop(mid)
        except KeyError:
            logger.info(f'No on_publish callback registered for the message with id {mid}')
            return
        f()

    def on_message(self, client, userdata, message: mqtt.MQTTMessage):
        logger.info(f'Message received on topic {message.topic}')
        try:
            callback = self.topic_to_callback[message.topic]
        except KeyError:
            logger.error(f'Received a message on topic {message.topic} but no callback was registered.')
            return
        def target():
            try:
                m = Message(**json.loads(message.payload))
            except:
                logger.error('Failed to deserialize message')
                return 
            callback(m)
        t = threading.Thread(target=target)
        t.start()
            
def get_messager(name:str)->AbstractMessager:
    return MESSAGERS[name]