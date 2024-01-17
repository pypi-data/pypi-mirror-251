from agora_redis_client import redis
from agora_logging import logger
from agora_config import config
from enum import Enum

class RedisPattern(Enum):
    DESIRED = "desired"
    REPORTED = "reported"    

class TwinPropertySingleton(): 
    _instance = None

    def __init__(self) -> None:
        self.__sub_devices = dict()
        self.__sleep_time = 0.01

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    class __Device:
        def __init__(self, device_id,  pattern, callback_method): 
            self.device_id = device_id
            self.pattern = pattern
            self.callback_method = callback_method

    class CallbackResponse(__Device):
        def __init__(self, device_id, key, value):
            self.device_id = device_id
            self.key = key
            self.value = value

    def set_property_change_callback(self, method_to_callback:any, device_ids:list=None):
        try:
            self.__clear_all_device()
            if not callable(method_to_callback):
                raise TypeError("Required Call-back method")
                    
            if device_ids is None:
                device_id = get_device_id()
                device_ids = [device_id]
            
            for device_id in device_ids:
                pattern = f"twin_properties/{device_id}/{RedisPattern.DESIRED.value}/"
                obj_device = self.__Device(device_id = int(device_id), pattern = pattern, callback_method = method_to_callback)
                self.__sub_devices[int(device_id)] = obj_device
                self.__subscribe_patterns(obj_device)
                
        except Exception as error:
            logger.exception(error, "Error while set property change callback ")

        return self.__sub_devices    

    def __clear_all_device(self):
        self.__sub_devices.clear()

    def __subscribe_patterns(self, device:__Device):
        try:
            if not redis.is_connected():
                redis.connect()

            pubsub = redis.pubsub()
            redis.config_set('notify-keyspace-events', 'KEA')
            pubsub.psubscribe(**{"__key*__:"+ device.pattern +"*": self.__subscription_callback})
            pubsub.run_in_thread(sleep_time=float(self.__sleep_time))

            logger.info("Running : {0} redis event subscriber ...".format(device.pattern))


        except Exception as error:
            logger.exception(error, "Error while suscribing to pattern {0} ".format(device.pattern))

    def __subscription_callback(self, msg):
        try:
            channel = msg["channel"]
            keys = channel.split(":")
            prop_value = redis.get(keys[1])
            logger.debug(f"Desired Key : {keys[1]}, value : {prop_value}")
            prop = str(keys[1]).split(sep="/")
            prop_name_value = str(keys[1]).split(sep=f"/{RedisPattern.DESIRED.value}/")
            device_id= prop[1]
            prop_name =  prop_name_value[1].rstrip("/") if len(prop_name_value) > 0 else ''
            is_valid, error = is_valid_prop_name(prop_name)
            if (is_valid == False): raise error

            is_valid, error = is_valid_prop_value(prop_value)
            if (is_valid == False): raise error


            robj =  self.CallbackResponse(
                device_id= device_id,
                key= prop_name,
                value= prop_value
            )

            obj_device = self.__sub_devices.get(int(device_id))
            obj_device.callback_method(robj)

        except Exception as error:
            logger.exception(error, "Error while executing callback method")
        return None
    
    @staticmethod
    def set_reported_property( prop_name:str, prop_value:any, device_id =None):
        try:
            if device_id is None : device_id = get_device_id()
            
            is_valid, error = is_valid_prop_name(prop_name)
            if (is_valid == False): raise error

            if prop_value is None:
                raise ValueError("Property Value is not set")

            key = f'twin_properties/{device_id}/{RedisPattern.REPORTED.value}/{prop_name}'
            appname = f"twin_properties/{device_id}/reported/__appname"
            if not redis.is_connected():
               redis.connect()            
            if type(prop_value) ==bool:
                if prop_value:
                     prop_value = "1"
                else:
                    prop_value = "0"
            
            redis.set(appname, config["Name"])
            redis.set(key, prop_value)
            

        except Exception as error:
            logger.exception(error, 'Exception occurred while setting the set reported property')
            
    @staticmethod        
    def get_desired_property(prop_name:str, device_id = None):
        try:
            if device_id is None : device_id = get_device_id()
            
            is_valid, error = is_valid_prop_name(prop_name)
            if (is_valid == False): raise error            

            key = f'twin_properties/{device_id}/{RedisPattern.DESIRED.value}/{prop_name}'

            if not redis.is_connected():
               redis.connect()            

            if redis.exists(key) <= 0:
                logger.info("Property Name - {} does not exists".format(key))

            return redis.get(key)

        except Exception as error:
            logger.exception(error, 'Exception occurred while setting the get desired property')

    @staticmethod        
    def get_reported_property(prop_name:str, device_id = None):
        try:
            if device_id is None : device_id = get_device_id()

            is_valid, error = is_valid_prop_name(prop_name)
            if (is_valid == False): raise error

            key = f'twin_properties/{device_id}/{RedisPattern.REPORTED.value}/{prop_name}'

            if not redis.is_connected():
               redis.connect()  

            if redis.exists(key) <= 0:
                logger.info("Property Name - {} does not exists".format(key))

            return redis.get(key)

        except Exception as error:
            logger.exception(error, 'Exception occurred while setting the get reported property')


@staticmethod
def get_device_id():
    device_id=config.get("AEA2:BusClient:DeviceId", "999")
    return device_id

@staticmethod
def is_valid_prop_name(prop_name:str):
    if prop_name is None:
        return (False, ValueError("Property Name is not set"))
    return (True, None)       

@staticmethod
def is_valid_prop_value(prop_value:str):
    if prop_value is None:
        return (False, ValueError("Property value is not set"))
    return (True, None)       


TwinProperty = TwinPropertySingleton()