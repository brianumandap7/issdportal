import random, string, hashlib
#==================================================================================================================
def GenerateCode(length=8):
    """Generate a random alphanumeric code."""
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
#==================================================================================================================
def GetInitialsUpper(full_name):
    if not full_name or not isinstance(full_name, str):
        return ""

    words = full_name.split()
    initials = [word[0].upper() for word in words if word]
    return "".join(initials)
#==================================================================================================================
def GetInitialsLower(full_name):
    if not full_name or not isinstance(full_name, str):
        return ""

    words = full_name.split()
    initials = [word[0].lower() for word in words if word]
    return "".join(initials)
#==================================================================================================================
def GetAlphaName(fname, mname, lname, exname):
    
    # Use .strip() and default to empty string to handle None or whitespace
    fname = (fname or "").strip()
    mname = (mname or "").strip()
    lname = (lname or "").strip()
    exname = (exname or "").strip()

    # Build the list of name parts
    full_name_parts = []

    # Add the last name first
    if lname:
        full_name_parts.append(lname)

    # Combine first and middle names, if they exist
    first_and_exname = []
    if fname:
        first_and_exname.append(fname)
    if exname:
        first_and_exname.append(exname)

    if first_and_exname:
        full_name_parts.append(" ".join(first_and_exname))
    
    initials = ""
    if mname:
        words = mname.split()
        initials_list = [word[0].upper() for word in words if word]
        if initials_list:
            initials = "".join(initials_list) + ""

    # Join the main name parts
    alpha_name = ", ".join(full_name_parts)

    # Append the extension, if it exists
    if initials:
        alpha_name += f" ({initials})"

    return alpha_name.upper()
#==================================================================================================================
def GetAlphaNameX(fname, mname, lname, exname):
    """
    Formats a person's name into a standard format: "LAST, FIRST E-NAME (M.I.)".
    Includes optional middle name initials and name extension.
    """
    # 1. Handle missing or non-string values gracefully
    fname = str(fname).strip() if fname else ""
    mname = str(mname).strip() if mname else ""
    lname = str(lname).strip() if lname else ""
    exname = str(exname).strip() if exname else ""

    # 2. Extract initials for the middle name if it exists
    initials = ""
    if mname:
        words = mname.split()
        initials_list = [word[0].upper() for word in words if word]
        if initials_list:
            initials = "".join(initials_list) + ""

    # 3. Build the formatted name parts, including optional middle and extension
    name_parts = [
        lname,
        fname,
        exname,
        f"({initials})" if initials else ""
    ]

    # 4. Join the parts and return in uppercase
    return " ".join(filter(None, name_parts)).upper()
#==================================================================================================================
def GetUsernameLower(fname, mname, lname, exname):
    """
    Generates a lowercase username from first name, middle name, last name, and extension.
    Example: ('JOSE ANGELO', 'SANOY', 'BARRANDA', 'SR') -> jasbarrandasr
    """
    
    # Initialize username parts with first initial of fname and mname
    username_parts = []

    # Get the first letter of the first name
    if fname and fname.strip():
    #    username_parts.append(fname.strip()[0])
        words = fname.split()
        initials = [word[0].lower() for word in words if word]
        username_parts.append("".join(initials))
    
    # Get the first letter of the middle name
    if mname and mname.strip():
    #    username_parts.append(mname.strip()[0])
        words = mname.split()
        initials = [word[0].lower() for word in words if word]
        username_parts.append("".join(initials))
    
    # Append the last name
    if lname and lname.strip():
        username_parts.append(lname.strip())
        
    # Append the extension name
    if exname and exname.strip():
        username_parts.append(exname.strip())

    # Join the parts into a single string and convert to lowercase
    return "".join(username_parts).lower()
#==================================================================================================================
def GetHash(hash_source):
    unique_hash = hashlib.sha256(hash_source.encode('utf-8')).hexdigest()
    return unique_hash
#==================================================================================================================
"""
    

	if fname_mname:
        words = fname_mname.split()
        initials_list = [word[0].upper() for word in words if word]
        if initials_list:
            initials = "".join(fname_mname) + ""
	    username_parts.append(initials)
            
	if lname:
        username_parts.append(lname)

	if exname:
        username_parts.append(exname)
"""	
	
#==================================================================================================================
"""
#==================================================================================================================
import secrets
import string
#==================================================================================================================
def generate_secure_code(length=8):
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(length))
#==================================================================================================================
#==================================================================================================================
from django.db import models
import secrets
import string
#==================================================================================================================
def generate_unique_code():
    characters = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(characters) for _ in range(10))
#==================================================================================================================
class Ticket(models.Model):
    code = models.CharField(max_length=10, unique=True, default=generate_unique_code)
    user = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)    
#==================================================================================================================

"""

def slugify(text):
    return text.lower().replace(" ", "-")

def truncate(text, length=50):
    return text if len(text) <= length else text[:length] + "..."
