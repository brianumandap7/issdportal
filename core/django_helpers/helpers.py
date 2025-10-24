from django.db import models
from django.db import connection

def insert(model, **kwargs):
    return model.objects.create(**kwargs)

def update(model, filters, **kwargs):
    return model.objects.filter(**filters).update(**kwargs)

def delete(model, filters):
    return model.objects.filter(**filters).delete()

def check(model, **filters):
    return model.objects.filter(**filters).exists()

def insert_batch(model, objs):
    return model.objects.bulk_create([model(**o) for o in objs])

def update_batch(model, objs, fields):
    return model.objects.bulk_update(objs, fields)

def select(model, **filters):
    return model.objects.filter(**filters)

def select_all(model, filters=None):
    return model.objects.filter(**(filters or {}))

def count(model, **filters):
    return model.objects.filter(**filters).count()

def sum(model, field, **filters):
    return model.objects.filter(**filters).aggregate(total=models.Sum(field))["total"]

def distinct(model, field, **filters):
    return model.objects.filter(**filters).values_list(field, flat=True).distinct()
#================================================================================================================
def select_row(model,db='default',**filters):
    return model.objects.using(db).filter(**filters).first()
#================================================================================================================
def GetValue(table_name, lookup_column, lookup_id, return_column):
    """
    Universally retrieves a single column value from any table based on an ID.

    Args:
        table_name (str): The name of the database table (e.g., 'my_app_citymun').
        lookup_column (str): The name of the column to match the ID against.
        lookup_id (str): The ID value to look up.
        return_column (str): The name of the column whose value should be returned.

    Returns:
        str or None: The value of the return_column, or None if not found.
    """
    with connection.cursor() as cursor:
        query = f"SELECT {return_column} FROM {table_name} WHERE {lookup_column} = %s"
        cursor.execute(query, [lookup_id])
        result = cursor.fetchone()
        
    if result:
        return result[0]
    return None
#================================================================================================================
def GetValueDB(table_name, lookup_column, lookup_id, return_column,db='default'):
    """
    Universally retrieves a single column value from any table based on an ID.

    Args:
        table_name (str): The name of the database table (e.g., 'my_app_citymun').
        lookup_column (str): The name of the column to match the ID against.
        lookup_id (str): The ID value to look up.
        return_column (str): The name of the column whose value should be returned.

    Returns:
        str or None: The value of the return_column, or None if not found.
    """
    with connection.cursor() as cursor:
        query = f"SELECT {return_column} FROM {db}.{table_name} WHERE {lookup_column} = %s"
        cursor.execute(query, [lookup_id])
        result = cursor.fetchone()
        
    if result:
        return result[0]
    return None
#================================================================================================================
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

def GetValue_ORM(model_class, lookup_where, return_column, db='default'):
    """
    Retrieves a single value from the database using the Django ORM.

    Args:
        model_class: The Django model class (e.g., Application).
        lookup_where (dict): A dictionary of lookup criteria (e.g., {'pk': 1}).
        return_column (str): The name of the column to return.
        db (str): The database alias to use.

    Returns:
        The value of the specified column, or None if not found.
        
    Raises:
        ObjectDoesNotExist: If no object matches the lookup criteria.
        MultipleObjectsReturned: If more than one object matches.
    """
    try:
        # Use a database-specific queryset.
        queryset = model_class.objects.using(db)
        
        # Retrieve a single value using filter(), values_list(), and flat=True.
        # This is the ORM equivalent of a SELECT ... WHERE ...
        value = queryset.filter(**lookup_where).values_list(return_column, flat=True).get()

        return value
        
    except ObjectDoesNotExist:
        return None
    except MultipleObjectsReturned as e:
        # It's good practice to handle this explicitly for safety.
        print(f"Error: Multiple objects matched the criteria for {model_class.__name__}: {e}")
        raise
#================================================================================================================