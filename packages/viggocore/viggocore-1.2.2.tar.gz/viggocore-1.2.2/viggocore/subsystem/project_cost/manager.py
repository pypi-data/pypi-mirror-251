from viggocore.common.subsystem import operation, manager


class GetCostByNameMostRecent(operation.List):

    def do(self, session, **kwargs):
        kwargs['order_by'] = 'created_at desc'
        costs = super().do(session, **kwargs)
        if len(costs) > 0:
            return costs[0].cost
        return None


class Manager(manager.Manager):

    def __init__(self, driver):
        super(Manager, self).__init__(driver)
        self.get_cost_by_name_most_recent = GetCostByNameMostRecent(self)
