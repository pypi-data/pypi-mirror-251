import time
# < -- send file in chunks -- > 
def write_file_chunks(path,request,chunk_size=1024):
    with open(path,"rb") as file:
        try:
            while True:
                chunk = file.read(chunk_size)
                if not chunk:
                    break
                request.wfile.write(chunk)
            file.close()
        except Exception as error:
            #  print("Uer Disconnected!")
            pass
    
    return True

# < -- write video file stream -- >
def write_video_stream(VIDEO_PATH,video_type,CHUNK_IN_MB,file_size, request):
        CHUNK_SIZE = int(CHUNK_IN_MB*(1024*1024))


        try:
            # < -- getting video current range in bytes from header it not available set default 0 -- >
            range_header = request.headers.get('Range',None)
            if(not range_header): raise Exception("RangeError")

            # < -- start and end video size in bytes -- >
            start = int(range_header.replace("bytes=","").split("-")[0])
            end = min(start + CHUNK_SIZE, file_size - 1)
            
            # < -- sending user data length in bytes -- >
            content_length = end - start + 1

            # < -- set response and content header -- >
            request.send_response(206)
            request.send_header("Content-Type", video_type)
            # < -- set headers and end -- >
            request.send_header("Content-Range", f"bytes {start}-{end}/{file_size}")
            request.send_header("Accept-Ranges", "bytes")
            request.send_header("Content-Length", content_length)
            request.end_headers()

            # < -- write file in bytes -- >
            with open(VIDEO_PATH, "rb") as file:
                file.seek(start)
                while content_length > 0:
                    chunk_size = min(CHUNK_SIZE, content_length)
                    chunk = file.read(chunk_size)
                    if not chunk:
                        break
                    request.wfile.write(chunk)
                    content_length -= len(chunk)
            return
        except Exception as  error:
            pass

        # < -- if user try to downlaod or request direct file without any broswer an he don't have any range -- >
        # < -- set response and content header -- >
        request.send_response(200)
        request.send_header("Content-Type", video_type)
        request.send_header("Content-Length", file_size)
        request.end_headers()
        # < -- write full file chunks by chunks -- >
        write_file_chunks(VIDEO_PATH,request)