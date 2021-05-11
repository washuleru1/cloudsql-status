from cloudsqlstatus import CloudSqlStatus
import base64, json, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def pubsub_subscriber(event, context):
     """Triggered from a message on a Cloud Pub/Sub topic.
     Args:
          event (dict): Event payload.
          context (google.cloud.functions.Context): Metadata for the event.
     """
     data = (base64.b64decode(event['data']).decode('utf-8'))
     data = json.loads(data.replace("'", "\""))
     for key in data:
          data[key] = str(data[key])
     sql_status = CloudSqlStatus()
     response = sql_status.changeInstanceStatus(data)
     if response.get('status') == True:
          logger.info('Exitoso cambio de estado a: {}'.format(data.get('project_id')))
     else:
          logger.warning('Falla cambio de estado de cloudsql a: {} por motivo: {}'.format(data.get('project_id'), response.get('msg')))