import os
def path_normalizer(filepath):
     if (not os.path.splitdrive(filepath)[0]):
            base_path = os.getcwd()
            return os.path.normpath(os.path.join(base_path,filepath))