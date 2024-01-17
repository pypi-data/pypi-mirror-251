def write_file(path,chunk_size,request):
    with open(path,"rb") as file:
        while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                request.wfile.write(chunk)
        file.close()
    
    return True