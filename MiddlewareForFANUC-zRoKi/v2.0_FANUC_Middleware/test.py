import json
import base64 

# with open("fromFANUC.json") as jsonFile:
#     jsonObject = json.load(jsonFile)
#     print(len(jsonObject))
#     c=1
#     for i in jsonObject:
#         img=i.get("ImageData").get("Picture")
#         with open(f'IMG{10+c}.png', 'wb') as local_file:
#             local_file.write(base64.decodebytes(img.encode('utf-8')))
#             c=c+1
#             print('[X-FTP] Image downloaded successfully....',i.get("timeStamp"))
file_name="IMG1.png"
#image to base64 string
def cvt_2_base64(file_name):
    with open(file_name , "rb") as image_file :
        data = base64.b64encode(image_file.read())
        print(f"data_type: {type(data)}")
    return data.decode('utf-8')
decode = cvt_2_base64(file_name)

print(f"decode_type: {type(decode)}")

jsonSTR= json.dumps({"dd":decode})
print(f"jsonSTR_type: {type(jsonSTR)}")

with open(f'IMG1_ENCODEbase64.txt', 'w') as local_file:
    local_file.write(decode)


with open(f'IMG1_ENCODEbase64.png', 'wb') as local_file:
    print(f"decode.encode_type: {type(decode.encode('utf-8'))}")
    local_file.write(base64.decodebytes(decode.encode('utf-8')))