import os
import sys
import json
import fnmatch
import string
import common.settings  # pylint: disable=import-error
from common.utils import logging  # pylint: disable=import-error

logger = logging.get_logger('ModelManager', is_static=True)

from collections.abc import MutableMapping
class ModelsDict(MutableMapping):
    def __init__(self, model_name,model_version,*args, **kw):
        self._model_name = model_name
        self._model_version = model_version
        self._dict = dict(*args, **kw)
    def __setitem__(self, key, value):
        self._dict[key] = value
    def __delitem__(self, key):
        del self._dict[key]    
    def __getitem__(self, key):
        if (key=="network"):
            if ('default' in self._dict["networks"]):
                return self._dict["networks"]["default"]
            else:
                return "{{models[{}][{}][VA_DEVICE_DEFAULT][network]}}".format(self._model_name,self._model_version)
        if (key in self._dict["networks"]):
            return self._dict["networks"][key]
        return self._dict.get(key, None)
    def __iter__(self):
        return iter(self._dict)    
    def __len__(self):
        return len(self._dict)

class ModelManager:
    models = None
    network_preference = {'CPU':"FP32",
                          'HDDL':"FP16",
                          'GPU':"FP16",
                          'VPU':"FP16"}
    
    @staticmethod
    def _get_model_proc(path):
        candidates=fnmatch.filter(os.listdir(path), "*.json")
        if (len(candidates)>1):
            raise Exception("Multiple model proc files found in %s" %(path,))
        elif(len(candidates)==1):
            return os.path.abspath(os.path.join(path,candidates[0]))
        return None
    
    @staticmethod
    def _get_model_network(path):
        candidates=fnmatch.filter(os.listdir(path), "*.xml")
        if (len(candidates)>1):
            raise Exception("Multiple networks found in %s" %(path,))
        elif(len(candidates)==1):
            return os.path.abspath(os.path.join(path,candidates[0]))
        return None

    @staticmethod
    def _get_model_networks(path):
        networks = {}
        default = ModelManager._get_model_network(path)
        if (default):
            networks["default"] = default
        for network_type in os.listdir(path):
            network_type_path = os.path.join(path,network_type)
            if (os.path.isdir(network_type_path)):
                network = ModelManager._get_model_network(network_type_path)
                if (network):
                    networks[network_type] = {'network':network}
        return networks

    @staticmethod
    def get_network(model, network):
        preferred_model=model.replace("VA_DEVICE_DEFAULT",network)
        try:
            preferred_model=string.Formatter().vformat(preferred_model, [], {'models':ModelManager.models})
            return preferred_model
        except Exception:
            pass
        return None
        
    @staticmethod
    def get_default_network_for_device(device,model):
        if "VA_DEVICE_DEFAULT" in model:
            for preference in ModelManager.network_preference[device]:
                ret = ModelManager.get_network(model,preference)
                if ret:
                    return ret
                logger.info("Device preferred network {net} not found".format(net=preference))
            model=model.replace("[VA_DEVICE_DEFAULT]","")
            logger.error("Could not resolve any preferred network {net} for model {model}".format(net=ModelManager.network_preference[device],model=model))
        return model
    
    @staticmethod
    def load_config(model_dir,network_preference):
        logger.info("Loading Models from Path {path}".format(path=os.path.abspath(model_dir)))
        if os.path.islink(model_dir):
            logger.warning("Models directory is symbolic link")
        if os.path.ismount(model_dir):
            logger.warning("Models directory is mount point")
        models = {}
        ModelManager.network_preference.update(network_preference)
        for key in ModelManager.network_preference:
            ModelManager.network_preference[key] = ModelManager.network_preference[key].split(',')
        for model_name in os.listdir(model_dir):
            try:
                model_path = os.path.join(model_dir,model_name)
                for version in os.listdir(model_path):
                    version_path = os.path.join(model_path,version)
                    if (os.path.isdir(version_path)):
                        version = int(version)
                        proc = ModelManager._get_model_proc(version_path)
                        networks = ModelManager._get_model_networks(version_path)
                        if (proc) and (networks):
                            for key in networks:
                                networks[key].update({"proc":proc,
                                                      "version":version,
                                                      "type":"IntelDLDT",
                                                      "description":model_name})
                                
                            models[model_name] = {version:ModelsDict(model_name,
                                                                     version,
                                {"networks":networks,
                                 "proc":proc,
                                 "version":version,
                                 "type":"IntelDLDT",
                                 "description":model_name
                                })
                            }
                            
            except Exception as error:
                logger.error("Error Loading Model {model_name} from: {model_dir}: {err}".format(err=error,model_name=model_name,model_dir=model_dir))

        ModelManager.models = models
        logger.info("Completed Loading Models")

    @staticmethod
    def get_model_parameters(name, version):
        if name not in ModelManager.models or version not in ModelManager.models[name] :
            return None
        params_obj = {
            "name": name,
            "version": version
        }
        if "type" in ModelManager.models[name][version]:
            params_obj["type"] = ModelManager.models[name][version]["type"]

        if "description" in ModelManager.models[name][version]:
            params_obj["description"] = ModelManager.models[name][version]["description"]
        return params_obj

    @staticmethod
    def get_loaded_models():
        results = []
        if ModelManager.models is not None:
            for model in ModelManager.models:
                for version in ModelManager.models[model].keys():
                    result = ModelManager.get_model_parameters(model, version)
                    if result :
                        results.append(result)
        return results
