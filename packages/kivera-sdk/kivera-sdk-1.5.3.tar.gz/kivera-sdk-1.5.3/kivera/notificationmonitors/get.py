from gql import gql
from typing import Sequence

class getMethods:

    _GetNotificationMonitorQuery = """
    query GetNotificationMonitor ($id: String!) {
  NotificationMonitors(where: {id: {_eq: $id}}) {
    id
    name
    description
    org_id
    enabled
    query_parameters
    interval
    severity
    NotificationMonitorDestinations {
      destination_id
    }
  }
}
    """

    def GetNotificationMonitor(self, id: str):
        query = gql(self._GetNotificationMonitorQuery)
        variables = {
            "id": id,
        }
        operation_name = "GetNotificationMonitor"
        return self.execute(query, variable_values=variables, operation_name=operation_name)

    _GetNotificationMonitorV2Query = """
    query GetNotificationMonitorV2($id: String!) {
  NotificationMonitors_by_pk(id: $id) {
    id
    name
    description
    org_id
    enabled
    query_parameters
    interval
    severity
    NotificationMonitorDestinations {
      destination_id
    }
  }
}
    """

    def GetNotificationMonitorV2(self, id: str):
        query = gql(self._GetNotificationMonitorV2Query)
        variables = {
            "id": id,
        }
        operation_name = "GetNotificationMonitorV2"
        return self.execute(query, variable_values=variables, operation_name=operation_name)
