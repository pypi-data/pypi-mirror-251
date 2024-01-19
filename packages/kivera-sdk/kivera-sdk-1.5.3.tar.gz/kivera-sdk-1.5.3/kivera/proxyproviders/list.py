from gql import gql
from typing import Sequence

class listMethods:

    _ListProxyProvidersQuery = """
    query ListProxyProviders {
    ProxyProviders(where: {enabled: {_eq: true}}) {
        provider_autoupdate
        Provider {
            name
        }
        ProviderVersion {
            version_name
            url
            created
            hash
        }
    }
}
    """

    def ListProxyProviders(self):
        query = gql(self._ListProxyProvidersQuery)
        variables = {
        }
        operation_name = "ListProxyProviders"
        return self.execute(query, variable_values=variables, operation_name=operation_name)
