from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
#================================================================================================================
def insert_item(model_class, data, db='default'):
    try:
        #item = model_class.objects.create(**data)
        item = model_class.objects.using(db).create(**data)
        return {'success': True, 'Notflix':'Success', 'response_advise': 'Insert successful!', 'item_id': item.id}
    except Exception as e:
        return {'success': False, 'Notflix':'Failure', 'response_advise': f'Insert failed: {str(e)}'}
#================================================================================================================
def check_insert(model_class, data, db='default'):
    try:
        # Define the lookup criteria (what makes an item unique)
        lookup_criteria = {'StringID': data.get('StringID')}
        # Use get_or_create() to find or create the item
        #item, created = model_class.objects.get_or_create(**lookup_criteria,defaults=data)
        item, created = model_class.objects.using(db).get_or_create(**lookup_criteria, defaults=data)
        if created:
            return {'success': True, 'Notflix':'Success', 'response_advise': 'Insert successful!', 'item_id': item.id}
        else:
            return {'success': False, 'Notflix':'Failure', 'response_advise': 'Item already exists.', 'item_id': item.id}
    except Exception as e:
        return {'success': False, 'Notflix':'Failure', 'response_advise': f'Insert failed: {str(e)}'}
#================================================================================================================
def insert_update_where(model_class, data, where_data, db='default'):
    """
    Updates an existing record based on `where_data` or creates a new one.

    Args:
        model_class: The Django model class (e.g., SummaryReport).
        data (dict): A dictionary of data for the record. This will be used
                     for updating existing records and creating new ones.
        where_data (dict): A dictionary of lookup criteria to find the record.
                           The keys should be model field names.
        db (str): The name of the database to use.

    Returns:
        A dictionary with the result of the operation.
    """
    try:
        # Separate the fields used for matching from the rest of the data.
        # where_data forms the lookup criteria.
        # data (minus any overlapping keys in where_data) forms the defaults.
        defaults = {k: v for k, v in data.items() if k not in where_data}
        
        # Use update_or_create for atomic upsert functionality.
        instance, created = model_class.objects.using(db).update_or_create(
            defaults=defaults,
            **where_data
        )
        
        if created:
            return {'success': True, 'Notflix': 'Success', 'response_advise': 'Insert successful!', 'item_id': instance.id}
        else:
            return {'success': True, 'Notflix': 'Success', 'response_advise': 'Update successful!', 'item_id': instance.id}

    except IntegrityError as e:
        return {
            'success': False,'Notflix': 'Failure','response_advise': f'Database integrity error: {str(e)}','item_id': None }
    except Exception as e:
        return {'success': False,'Notflix': 'Failure','response_advise': f'Operation failed: {str(e)}','item_id': None }
#================================================================================================================
def check_and_update(model_class, data, db='default'):
    """
    Creates a new record if no 'id' is provided, otherwise updates the existing one.
    
    Args:
        model_class: The Django model class (e.g., SummaryReport).
        data (dict): A dictionary of data for the record.
        db (str): The name of the database to use.
    
    Returns:
        A dictionary with the result of the operation.
    """
    item_id = data.get('id')
    
    try:
        if item_id:
            # Cast the item_id to int to ensure it's a valid primary key.
            # This will raise a ValueError if item_id is not a valid integer.
            item_id = int(item_id)
            
            # Retrieve the existing object, or raise 404 if not found.
            # Using get_object_or_404 is a clean way to handle missing objects.
            instance = get_object_or_404(model_class.objects.using(db), pk=item_id)
            
            # Remove the 'id' from data so it doesn't try to change the primary key.
            data.pop('id', None)
            
            # Update the instance with the new data.
            for key, value in data.items():
                setattr(instance, key, value)
            
            instance.save(using=db)
            
            return {'success': True,'Notflix': 'Success','response_advise': 'Update successful!','item_id': instance.id}
        else:
            # Create a new record as no ID was provided.
            # Remove the 'id' key to avoid issues when creating.
            data.pop('id', None)
            
            instance = model_class.objects.using(db).create(**data)
            
            return {'success': True,'Notflix': 'Success','response_advise': 'Insert successful!','item_id': instance.id}
            
    except ValueError:
        return {'success': False,'Notflix': 'Failure','response_advise': 'Invalid ID format. Must be an integer.','item_id': None
        }
    except IntegrityError as e:
        return {'success': False,'Notflix': 'Failure','response_advise': f'Database integrity error: {str(e)}','item_id': None
        }
    except Exception as e:
        return {'success': False,'Notflix': 'Failure','response_advise': f'Operation failed: {str(e)}','item_id': None}
#================================================================================================================
def update_item_where(model_class, data, where_data, db='default'):
    """
    Updates records matching the `where_data` criteria with the `data` provided.

    Args:
        model_class: The Django model class.
        data (dict): The dictionary of data to be updated.
        where_data (dict): The lookup criteria to find the record(s) to update.
        db (str): The name of the database to use.

    Returns:
        A dictionary with the result of the operation.
    """
    if not where_data:
        return {'success': False, 'response_advise': 'Missing lookup criteria.'}

    try:
        updated_count = model_class.objects.using(db).filter(**where_data).update(**data)

        if updated_count > 0:
            return {'success': True, 'response_advise': f'Successfully updated {updated_count} item(s).'}
        else:
            return {'success': False, 'response_advise': 'No matching item found to update.'}

    except Exception as e:
        return {'success': False, 'response_advise': f'Update failed: {str(e)}'}
#================================================================================================================
def update_item(model_class, item_id, data, db='default'):
    try:
        item = model_class.objects.using(db).get(id=item_id)
        for key, value in data.items():
            setattr(item, key, value)
        item.save()
        return {'success': True, 'response_advise': 'Update successful!'}
    except ObjectDoesNotExist:
        return {'success': False, 'response_advise': 'Item not found.'}
    except Exception as e:
        return {'success': False, 'response_advise': f'Update failed: {str(e)}'}
#================================================================================================================    
def delete_item(model_class, item_id, db='default'):
    try:
        item = model_class.objects.using(db).get(id=item_id)
        item.delete()
        return {'success': True, 'response_advise': 'Delete successful!'}
    except ObjectDoesNotExist:
        return {'success': False, 'response_advise': 'Item not found.'}
    except Exception as e:
        return {'success': False, 'response_advise': f'Delete failed: {str(e)}'}
#================================================================================================================
def delete_where(model_class, where_data, db='default'):
    
    if not where_data:
        return {'success': False, 'response_advise': 'Missing lookup criteria.'}
    try:
        # Filter the queryset based on `where_data` and perform the deletion.
        # This will return a tuple: (number_of_deletions, {model_name: number_of_deletions})
        deleted_count, _ = model_class.objects.using(db).filter(**where_data).delete()

        if deleted_count > 0:
            return {'success': True, 'response_advise': f'Successfully deleted {deleted_count} item(s).'}
        else:
            return {'success': False, 'response_advise': 'No matching item found to delete.'}
        
    except Exception as e:
        return {'success': False, 'response_advise': f'Delete failed: {str(e)}'}
#================================================================================================================

