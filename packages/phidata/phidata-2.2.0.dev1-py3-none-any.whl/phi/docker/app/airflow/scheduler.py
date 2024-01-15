from typing import Optional, Union, List

from phi.docker.app.airflow.base import AirflowBase


class AirflowScheduler(AirflowBase):
    # -*- App Name
    name: str = "airflow-scheduler"

    # Command for the container
    command: Optional[Union[str, List[str]]] = "scheduler"
