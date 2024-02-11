class DBRouter(object):
    def __init__(self):
        self.database_by_app_dict = {
            'wubuApp': 'default',
            'mongoDBApp': 'mongodb'
        }

    def db_for_read(self, model, **hints):
        return self.database_by_app_dict.get(model._meta.app_label)

    def db_for_write(self, model, **hints):
        return self.database_by_app_dict.get(model._meta.app_label)

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        return None
