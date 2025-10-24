def user_info(request):
    """
    Returns a dictionary of common user-related data for templates.
    """
    if request.user.is_authenticated:
        return {
            'UserID': request.user.id,
            'UserName': request.user.username,
            'FirstName': request.user.first_name,
            'LastName': request.user.last_name,
            'FullName': request.user.get_full_name(),
            'FullNameBlock': request.user.get_full_name().upper(),
            'ProjectName':'DOTR-MIS',
        }
    return {}