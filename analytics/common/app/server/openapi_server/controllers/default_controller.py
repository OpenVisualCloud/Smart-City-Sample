import connexion
import six

from modules.PipelineManager import PipelineManager
from http import HTTPStatus
from common.utils import logging

logger = logging.get_logger('Default Controller', is_static=True)

from modules.ModelManager import ModelManager

bad_request_response = 'Invalid pipeline, version or instance'


def models_get():  # noqa: E501
    """models_get

    Return supported models # noqa: E501


    :rtype: List[ModelVersion]
    """
    try:
        logger.debug("GET on /models")
        return ModelManager.get_loaded_models()
    except Exception as e:
        logger.error('pipelines_name_version_get '+e)
        return ('Unexpected error', HTTPStatus.INTERNAL_SERVER_ERROR)

def pipelines_get():  # noqa: E501
    """pipelines_get

    Return supported pipelines # noqa: E501


    :rtype: List[Pipeline]
    """
    try:
        logger.debug("GET on /pipelines")
        return PipelineManager.get_loaded_pipelines()
    except Exception as e:
        logger.error('pipelines_name_version_get '+e)
        return ('Unexpected error', HTTPStatus.INTERNAL_SERVER_ERROR)


def pipelines_name_version_get(name, version):  # noqa: E501
    """pipelines_name_version_get

    Return pipeline description and parameters # noqa: E501

    :param name: 
    :type name: str
    :param version: 
    :type version: str

    :rtype: None
    """
    try:
        logger.debug("GET on /pipelines/{name}/{version}".format(name=name, version=version))
        result = PipelineManager.get_pipeline_parameters(name, version)
        if result:
            return result
        return ('Invalid Pipeline or Version', HTTPStatus.BAD_REQUEST)
    except Exception as e:
        logger.error('pipelines_name_version_get '+e)
        return ('Unexpected error', HTTPStatus.INTERNAL_SERVER_ERROR)


def pipelines_name_version_instance_id_delete(name, version, instance_id):  # noqa: E501
    """pipelines_name_version_instance_id_delete

    Stop and remove an instance of the customized pipeline # noqa: E501

    :param name: 
    :type name: str
    :param version: 
    :type version: int
    :param instance_id: 
    :type instance_id: int

    :rtype: None
    """
    try:
        logger.debug("DELETE on /pipelines/{name}/{version}/{id}".format(name=name, version=version, id=instance_id))
        result = PipelineManager.stop_instance(name, version, instance_id)
        if result:
            return result
        return (bad_request_response, HTTPStatus.BAD_REQUEST)
    except Exception as e:
        logger.error('pipelines_name_version_instance_id_delete '+e)
        return ('Unexpected error', HTTPStatus.INTERNAL_SERVER_ERROR)

def pipelines_name_version_instance_id_get(name, version, instance_id):  # noqa: E501
    """pipelines_name_version_instance_id_get

    Return instance summary # noqa: E501

    :param name: 
    :type name: str
    :param version: 
    :type version: int
    :param instance_id: 
    :type instance_id: int

    :rtype: object
    """
    try:
        logger.debug("GET on /pipelines/{name}/{version}/{id}".format(name=name, version=version, id=instance_id))
        result = PipelineManager.get_instance_parameters(name, version, instance_id)
        if result:
            return result
        return (bad_request_response, HTTPStatus.BAD_REQUEST)
    except Exception as e:
        logger.error('pipelines_name_version_instance_id_get '+e)
        return ('Unexpected error', HTTPStatus.INTERNAL_SERVER_ERROR)

def pipelines_name_version_instance_id_status_get(name, version, instance_id):  # noqa: E501
    """pipelines_name_version_instance_id_status_get

    Return instance status summary # noqa: E501

    :param name: 
    :type name: str
    :param version: 
    :type version: int
    :param instance_id: 
    :type instance_id: int

    :rtype: object
    """
    try:
        logger.debug(
            "GET on /pipelines/{name}/{version}/{id}/status".format(name=name, version=version, id=instance_id))
        result = PipelineManager.get_instance_status(name, version, instance_id)
        if result:
            return result
        return ('Invalid pipeline, version or instance', HTTPStatus.BAD_REQUEST)
    except Exception as e:
        logger.error('pipelines_name_version_instance_id_status_get '+e)
        return ('Unexpected error', HTTPStatus.INTERNAL_SERVER_ERROR)


def pipelines_name_version_post(name, version):  # noqa: E501
    """pipelines_name_version_post

    Start new instance of pipeline. Specify the source and destination parameters as URIs # noqa: E501

    :param name: 
    :type name: str
    :param version: 
    :type version: int
    :param pipeline_request: 
    :type pipeline_request: dict | bytes

    :rtype: None
    """

    logger.debug("POST on /pipelines/{name}/{version}".format(name=name, version=version))
    if connexion.request.is_json:
        try:
            pipeline_id, err = PipelineManager.create_instance(name, version, connexion.request.get_json())
            if pipeline_id is not None:
                return pipeline_id
            return (err, HTTPStatus.BAD_REQUEST)
        except Exception as e:
            logger.error('pipelines_name_version_post ' +e)
            return ('Unexpected error', HTTPStatus.INTERNAL_SERVER_ERROR)
