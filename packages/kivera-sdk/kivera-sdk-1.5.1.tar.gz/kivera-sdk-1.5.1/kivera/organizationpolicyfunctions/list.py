from gql import gql
from typing import Sequence

class listMethods:

    _ListOrganizationPolicyFunctionsQuery = """
    query ListOrganizationPolicyFunctions {
    OrganizationPolicyFunctions {
        id
        function
        name
    }
}
    """

    def ListOrganizationPolicyFunctions(self):
        query = gql(self._ListOrganizationPolicyFunctionsQuery)
        variables = {
        }
        operation_name = "ListOrganizationPolicyFunctions"
        return self.execute(query, variable_values=variables, operation_name=operation_name)
