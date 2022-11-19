import json


def txtToJson(inputfile,outfile):
    dependencies = []
    with open(inputfile,"r") as packages:#"requirements.txt"
        for pkg in packages:
            pkg = pkg.rstrip().split("==")
            dependencies.append(dict(name= pkg[0],version= pkg[1]))
        dependencies = json.dumps(dependencies,indent=4)
    with open(outfile,"w") as outfile:#"PR_Packages.json"
        outfile.write(dependencies)
