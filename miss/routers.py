class AppRouter:
    """
    A router to control all database operations on models in
    the pnpki and spms apps.
    """

    route_app_labels = {
        'pnpki': 'dopnpki',
        'spms': 'dospms',
    }

    def db_for_read(self, model, **hints):
        """Point all read operations to the appropriate database."""
        return self.route_app_labels.get(model._meta.app_label, 'default')

    def db_for_write(self, model, **hints):
        """Point all write operations to the appropriate database."""
        return self.route_app_labels.get(model._meta.app_label, 'default')

    def allow_relation(self, obj1, obj2, **hints):
        """Allow any relation if both models are in the same database."""
        db_obj1 = self.route_app_labels.get(obj1._meta.app_label, 'default')
        db_obj2 = self.route_app_labels.get(obj2._meta.app_label, 'default')
        if db_obj1 and db_obj2:
            return db_obj1 == db_obj2
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Ensure that apps only appear in the correct database."""
        target_db = self.route_app_labels.get(app_label, 'default')
        return db == target_db
