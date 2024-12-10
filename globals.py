import os


class Globals:
    db_folder = "/Users/yuda/PycharmProjects/Luminary/db/db_data"

    def __init__(self):
        print(Globals.db_folder)
        self.analized_proj_folder = os.path.join(Globals.db_folder, "analyzed_proj")
        print(self.analized_proj_folder)


GLOBALS = Globals()
