import requests, sys
import json 
server = "https://rest.ensembl.org"
ext = "/vep/human/hgvs/9:g.22125504G>CATC?"
r = requests.get(server+ext, headers={ "Content-Type" : "application/json"})
if not r.ok:
  r.raise_for_status()
  sys.exit()
decoded = r.json()
print(type(decoded))
for i in decoded[0]['transcript_consequences']:
    print("*",i)
