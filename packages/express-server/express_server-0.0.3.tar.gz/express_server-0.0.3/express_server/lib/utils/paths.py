import os
from ..constants import file_types

# < -- make path simple example: 1: c://programming 2: ./index.php output:-c://programming/index.php -- >
def path_normalizer(filepath):
     if (not os.path.splitdrive(filepath)[0]):
            base_path = os.getcwd()
            return os.path.normpath(os.path.join(base_path,filepath))


# < -- it's reutrn content type of paths that available in file types -- >
def get_content_info_by_extension(extension):
    for FileCategory in file_types:
        for ext in file_types[FileCategory]:
                if ext == extension:
                    return ((file_types[FileCategory][ext],FileCategory))
    return (None,None)

# < -- Find Content Type From File Path -- >
def find_content_type(path,path_info):
    extension = path
    if path_info == "filename":
            extension = os.path.splitext(path)[1]
      
    elif path_info == "extention":
         if not str(extension).startswith("."): extension = "."+extension
    try:
        return get_content_info_by_extension(extension)
    except:
        return (None,None)