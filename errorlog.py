import re
import json
f = open("/var/log/apache2/error.log","r")
content = f.readlines()

def log_extract(string_lines):
    string_array = string_lines.split(" PHP Notice:")
    output = {}
    if string_array[0] != '\n':
        trip = string_array[0].strip()
        info = string_array[1].strip()
        cause = info.strip().split(",")
        clean_info = re.findall("\[(.*?)\]", trip) 
        output = {
            "info": {
                "time": clean_info[0],
                "client": clean_info[-1].replace("client ","").split(':')[0],
                "referrer": cause[1]
            },
            "cause": cause[0],
            "filename": cause[1]
        }
    return output

clients = {}
causes = {}
files = {}

for x in content:
    data = log_extract(x)
    if 'info' in data:
        if data['info']['client'] in clients:
       	 clients[data['info']['client']] += 1
        else:
         clients[data['info']['client']] = 1
    
        data_cause = data['cause']
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
