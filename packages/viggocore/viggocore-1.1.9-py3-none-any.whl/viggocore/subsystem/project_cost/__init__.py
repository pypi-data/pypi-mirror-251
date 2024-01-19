from viggocore.common import subsystem
from viggocore.subsystem.project_cost \
    import resource, manager

subsystem = subsystem.Subsystem(resource=resource.ProjectCost,
                                manager=manager.Manager)
