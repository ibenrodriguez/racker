# python code to iterate through lists and build trees
import json

var lists = {
	"cloudlist": ["gcp", "aws", "az", "oci"],
	"bizunit": ["crp", "eng", "spt", "mkt", "sls", "int"],
	"tier": ["brz", "slv", "gld", "plt"],
}
json_array = json.load(lists)

for item in lists:
print(item)
