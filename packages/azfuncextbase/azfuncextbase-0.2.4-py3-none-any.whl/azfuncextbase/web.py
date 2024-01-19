from abc import abstractmethod
from typing import Callable

base_extension_module = __name__

# #  Base extension pkg
class PackageTrackerMeta(type):
    _class_package = None

    def __new__(cls, name, bases, dct, **kwargs):
        new_class = super().__new__(cls, name, bases, dct)
        new_module_to_track = dct.get('__module__')
        if new_module_to_track != base_extension_module:
            if cls._class_package is None:
                cls._class_package = new_module_to_track
            elif cls._class_package != new_module_to_track:
                raise Exception('Only one web extension package shall be imported')
        
        return new_class

    @classmethod
    def get_class_package(cls):
        return cls._class_package

    @classmethod
    def package_imported(cls):
        return cls._class_package is not None
    

class RequestTrackerMeta(type):
    _request_type = None

    def __new__(cls, name, bases, dct, **kwargs):
        new_class = super().__new__(cls, name, bases, dct)

        request_type = dct.get('request_type')
        if request_type:
            if cls._request_type is None:
                cls._request_type = request_type
            elif cls._request_type != request_type:
                raise Exception('Only one request type shall be recorded')

        return new_class

    @classmethod
    def get_request_type(cls):
        return cls._request_type
    
    @classmethod
    def check_type(cls, pytype: type) -> bool:
        return cls._request_type != None and issubclass(pytype, cls._request_type)

class ResponseTrackerMeta(type):
    _response_type = None

    def __new__(cls, name, bases, dct, **kwargs):
        new_class = super().__new__(cls, name, bases, dct)

        response_type = dct.get('response_type')
        if response_type:
            if cls._response_type is None:
                cls._response_type = response_type
            elif cls._response_type != response_type:
                raise Exception('Only one response type shall be recorded')

        return new_class

    @classmethod
    def get_response_type(cls):
        return cls._response_type
    
    @classmethod
    def check_type(cls, pytype: type) -> bool:
        return cls._response_type != None and issubclass(pytype, cls._response_type)
    
class WebApp(metaclass=PackageTrackerMeta):
    @abstractmethod
    def route(self, func: Callable):
        pass
    
    @abstractmethod
    def get_app(self):
        pass

class WebServer(metaclass=PackageTrackerMeta):
    def __init__(self, hostname, port, web_app: WebApp):
        self.hostname = hostname
        self.port = port
        self.web_app = web_app.get_app()

    @abstractmethod
    async def serve(self):
        pass



class InConverter(_BaseConverter, binding=None):

    @classmethod
    @abc.abstractmethod
    def check_input_type_annotation(cls, pytype: type) -> bool:
        pass

    @classmethod
    @abc.abstractmethod
    def decode(cls, data: Datum, *, trigger_metadata) -> Any:
        raise NotImplementedError

    @classmethod
    @abc.abstractmethod
    def has_implicit_output(cls) -> bool:
        return False


class OutConverter(_BaseConverter, binding=None):

    @classmethod
    @abc.abstractmethod
    def check_output_type_annotation(cls, pytype: type) -> bool:
        pass

    @classmethod
    @abc.abstractmethod
    def encode(cls, obj: Any, *,
               expected_type: Optional[type]) -> Optional[Datum]:
        raise NotImplementedError
