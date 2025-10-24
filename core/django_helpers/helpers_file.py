import os
from django.core.exceptions import ValidationError
from django.http import JsonResponse

def read_file(path, mode="r"):
    """Read content from a file"""
    if not os.path.exists(path):
        return None
    with open(path, mode) as f:
        return f.read()

def write_file(path, content, mode="w"):
    """Write content to a file"""
    with open(path, mode) as f:
        f.write(content)
    return path

def delete_file(path):
    """Delete a file if it exists"""
    if os.path.exists(path):
        os.remove(path)
        return True
    return False

def file_exists(path):
    """Check if a file exists"""
    return os.path.exists(path)

def file_size(path):
    """Return file size in bytes"""
    return os.path.getsize(path) if os.path.exists(path) else None

"""
Example usage

from django_helpers import helpers_file

# Write file
helpers_file.write_file("test.txt", "Hello World")

# Read file
print(helpers_file.read_file("test.txt"))

# Check file
print(helpers_file.file_exists("test.txt"))

# Get size
print(helpers_file.file_size("test.txt"))

# Delete file
helpers_file.delete_file("test.txt")
"""
#============================================================================================
# FILE VALIDATION
#============================================================================================
# WORKING VALIDATORS
#==============================================================================================
def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.doc', '.docx', '.pdf', '.jpg', '.jpeg', '.png']
    if not ext.lower() in valid_extensions:
        return {'success': False, 'Notflix':'Failure', 'response_advise': 'Unsupported file extension. Allowed: DOC, DOCX, PDF, JPG, PNG.'}
        #raise ValidationError('Unsupported file extension. Allowed: DOC, DOCX, PDF, JPG, PNG.')
    return {'success': True, 'Notflix':'Success', 'response_advise': 'File Uploaded accepted!'}
#==============================================================================================
# UNDER TESTING
#==============================================================================================
def validate_file_and_image_type(uploaded_file):
    import magic
    """
    Validates the MIME type of an uploaded file.
    """
    if not uploaded_file:
        raise ValidationError("No file was uploaded.")

    # Define the expanded list of allowed MIME types for documents and images
    allowed_mimes = [
        'application/msword',  # .doc
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',  # .docx
        'application/pdf',
        'image/jpeg',
        'image/png',
        'image/gif'
    ]

    # Use python-magic to get the true MIME type
    try:
        mime_type = magic.from_buffer(uploaded_file.read(1024), mime=True)
        if mime_type not in allowed_mimes:
            raise ValidationError(f"File type '{mime_type}' is not supported.")
    except Exception:
        raise ValidationError("Could not determine file type.")

    # Reset the file pointer after reading it for validation
    uploaded_file.seek(0)
    return uploaded_file
#==============================================================================================
# TEST FILE VALID
#============================================================================================
# NOT YET WORKING    
def is_valid_mime(file):
    import magic
    mime = magic.from_buffer(file.read(1024), mime=True)  # read first 1KB 
    file.seek(0)  # reset pointer so Django can save it later
    allowed_mime_types = [
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/pdf",
        "image/jpeg",
        "image/png"
    ]
    print("Validator called for:",mime,' : ',allowed_mime_types)  # debug
    return mime in allowed_mime_types

#
"""
def upload_file(request):
    if request.method == "POST" and request.FILES.get("file"):
        file = request.FILES["file"]

        # 1. Extension check
        import os
        ext = os.path.splitext(file.name)[1].lower()
        if ext not in [".doc", ".docx", ".pdf", ".jpg", ".jpeg", ".png"]:
            return JsonResponse({"error": f"Invalid extension: {ext}"}, status=400)

        # 2. MIME type check
        if not is_valid_mime(file):   # ✅ pass request.FILES object here
            return JsonResponse({"error": "Invalid MIME type"}, status=400)

        # 3. Save if valid
        doc = Document.objects.create(file=file)
        return JsonResponse({"success": True, "id": doc.id})

    return JsonResponse({"error": "No file uploaded"}, status=400)
"""
#============================================================================================
# TEST FILE VALID
#============================================================================================


