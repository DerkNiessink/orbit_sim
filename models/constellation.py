from typing import Sequence

from models.physicalobject_model import PhysicalObjectModel

from pygame.math import Vector3


class CenterOfMass(PhysicalObjectModel):
    def update_position(self, bodies: Sequence[PhysicalObjectModel], time_step: float) -> None:
        """Update the position of the center of mass."""
        total_mass = sum(body.mass for body in bodies)
        center_of_mass = sum(
            ((body.position * (body.mass / total_mass)) for body in bodies),
            start=self.null_vector,
        )
        self.position = center_of_mass


class Constellation:
    def __init__(self, body_models: Sequence[PhysicalObjectModel]) -> None:
        self.body_models = body_models
        self.center_of_mass = CenterOfMass(Vector3(0, 0, 0), Vector3(0, 0, 0), 100, 0)

    def update_positions(self, time_step: float) -> None:
        for body_model in self.body_models:
            body_model.update_position(self.body_models, time_step)
        self.center_of_mass.update_position(self.body_models, time_step)
