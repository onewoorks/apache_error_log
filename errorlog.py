import re
import json
f = open("error.log","r")
content = f.readlines()

def log_extract(string_lines):
    string_array = string_lines.split(" PHP Notice:")
    output = {}
    if string_array[0] != '\n':
        trip = string_array[0].strip()
        info = string_array[1].strip().split(' in ')
        cause = info[0].strip()
        file_refer = info[1].split(',')
        filename = file_refer[0]
        referrer = file_refer[1]
        clean_info = re.findall("\[(.*?)\]", trip) 
        output = {
            "info": {
                "time": clean_info[0],
                "client": clean_info[-1].replace("client ","").split(':')[0],
                "referrer": referrer
            },
            "cause": cause,
            "filename": filename
        }
    return output

clients = {}
causes = {}
files = {}

for x in content:
    data = log_extract(x)
    if data['info']['client'] in clients:
        clients[data['info']['client']] += 1
    else:
        clients[data['info']['client']] = 1
    
    data_cause = data['cause'] + ' @ ' + data['filename']
    if data_cause in clients:
        causes[data_cause] += 1
    else:
        causes[data_cause] = 1

    if data['filename'] in clients:
        files[data['filename']] += 1
    else:
        files[data['filename']] = 1

reports = {
    "client": clients,
    "causes": causes
}
print(json.dumps(reports))

f.close()