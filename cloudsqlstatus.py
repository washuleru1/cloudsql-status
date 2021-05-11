# This file uses the Cloud SQL API to turn on a Cloud SQL instance.
import googleapiclient.discovery
from oauth2client.client import GoogleCredentials
from google.oauth2 import service_account
import logging, os, json

logging.basicConfig(level=logging.INFO)
logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.ERROR)
logger = logging.getLogger(__name__)

class CloudSqlStatus:

    def __init__(self):
        """
        Inicializador, se inicializa la conectividad a la api de GCP, v1beta4
        project: variable que indica el project ID. Para segunda iteracion debe ser automático
                 discriminando por los labels env:dev
        """
        try:
            credentials = service_account.Credentials.from_service_account_info(json.loads(os.environ['SERVICE_ACCOUNT']))
            self.__service = googleapiclient.discovery.build('sqladmin', 'v1beta4', credentials=credentials)
        except Exception as e:
            logger.error('Error en conexion a api GCP: {} '.format(e))

    def __getProjectSqlInstances(self, projectId):
        try:
            instances = self.__service.instances().list(project=projectId).execute()
        except Exception as e:
            logger.error('Error obteniendo instancias: {}'.format(e))
            instances = {'items':{}}
        finally:
            return instances.get('items')
   
    def changeInstanceStatus(self, projectModel):
        """
        Método para cambiar el estado de la instancia cloudsql
        projectModel: Dict que representa el contenido del evento, contiene:
            project_id: id del proyecto en gcp
            cloudsql_status: nuevo estado de la instancia cloudsql (ALWAYS o NEVER)
        cuentas de servicio de las apis de gcp 
        """
        instances = self.__getProjectSqlInstances(projectModel.get('project_id'))
        if instances == None:
            msg = 'El proyecto: {} no tiene instancias de cloudsql'.format(projectModel.get('project_id'))
            logger.warning(msg)
            return {'status': False, 'msg': msg}
        try:
            response = []
            for instance in instances:
                logger.info('INSTANCE: {}'.format(instance.get('name')))
                projectModel.update(instance_name=str(instance.get('name')))
                db_body = {
                    "settings": {
                        "activationPolicy": projectModel.get('cloudsql_status')
                    }
                }
                request = self.__service.instances().patch(
                    project=projectModel.get('project_id'),
                    instance=projectModel.get('instance_name'),
                    body=db_body,
                )
                logging.info('Actualizando estado de la BD.... {}'.format(projectModel.get('instance_name')))
                res_gcp = request.execute()
                response.append(res_gcp) 
            response = {'status': True, 'msg': response}
        except Exception as e:
            logger.error("Exception: {} ".format(e))
            response = {'status': False, 'msg': e}
        finally:
            return response