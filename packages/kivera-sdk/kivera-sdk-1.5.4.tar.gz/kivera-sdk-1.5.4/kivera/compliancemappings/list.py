from gql import gql
from typing import Sequence

class listMethods:

    _ListAllComplianceMappingsQuery = """
    query ListAllComplianceMappings {
    ComplianceMappings{
        framework
        control
        organization_id
    }
}
    """

    def ListAllComplianceMappings(self):
        query = gql(self._ListAllComplianceMappingsQuery)
        variables = {
        }
        operation_name = "ListAllComplianceMappings"
        return self.execute(query, variable_values=variables, operation_name=operation_name)

    _ListComplianceMappingsForCurrentOrgQuery = """
    query ListComplianceMappingsForCurrentOrg {
    ComplianceMappings(where: {organization_id: {_neq: 0}}) {
        framework
        control
    }
}
    """

    def ListComplianceMappingsForCurrentOrg(self):
        query = gql(self._ListComplianceMappingsForCurrentOrgQuery)
        variables = {
        }
        operation_name = "ListComplianceMappingsForCurrentOrg"
        return self.execute(query, variable_values=variables, operation_name=operation_name)

    _ListComplianceMappingsForManagedRulesQuery = """
    query ListComplianceMappingsForManagedRules {
    ComplianceMappings(where: {organization_id: {_eq: 0}}) {
        framework
        control
    }
}
    """

    def ListComplianceMappingsForManagedRules(self):
        query = gql(self._ListComplianceMappingsForManagedRulesQuery)
        variables = {
        }
        operation_name = "ListComplianceMappingsForManagedRules"
        return self.execute(query, variable_values=variables, operation_name=operation_name)
