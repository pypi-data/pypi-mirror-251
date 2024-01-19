from gql import gql
from typing import Sequence

class listMethods:

    _ListProvidersQuery = """
    query ListProviders {
    Providers(order_by: {id: asc}) {
        name
        id
    }
}
    """

    def ListProviders(self):
        query = gql(self._ListProvidersQuery)
        variables = {
        }
        operation_name = "ListProviders"
        return self.execute(query, variable_values=variables, operation_name=operation_name)
