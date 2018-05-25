from synch.models import YSUMainModel

class DatabaseRouter(object):
    def db_for_read(self, model, **hints):
        if issubclass(model, YSUMainModel):
            return 'jesus'
        return 'default'

    def db_for_write(self, model, **hints):
        if issubclass(model, YSUMainModel):
            return None
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        return (isinstance(obj1, YSUMainModel) == isinstance(obj2, YSUMainModel))

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == 'jesus':
            return False
        return (db == 'default')