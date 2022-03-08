class Constellation:
    def __init__(self, body_models):
        self.body_models = body_models

    def update_positions(self):
        for body_model in self.body_models:
            body_model.update_position(self.body_models)

    # def calc_center_of_mass(self):

    # def collision(self):
