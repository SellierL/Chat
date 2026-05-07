class DatabaseRouter:
    shelter_app_labels = {"shelter"}

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.shelter_app_labels:
            return "shelter"
        return "default"

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.shelter_app_labels:
            return "shelter"
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        obj1_is_shelter = obj1._meta.app_label in self.shelter_app_labels
        obj2_is_shelter = obj2._meta.app_label in self.shelter_app_labels

        if obj1_is_shelter or obj2_is_shelter:
            return obj1_is_shelter and obj2_is_shelter

        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.shelter_app_labels:
            return db == "shelter"

        if db == "shelter":
            return False

        return db == "default"