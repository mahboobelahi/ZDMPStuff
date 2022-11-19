import json


def txtToJson(inputfile,outfile):
    dependencies = []
    with open(inputfile,"r") as packages:#"requirements.txt"
        for pkg in packages:
            pkg = pkg.rstrip().split("==")
            dependencies.extend((dict(name= pkg[0]),
                                dict(version= pkg[1]))
                                )
        dependencies = json.dumps(dependencies,indent=4)
    with open(outfile,"w") as outfile:#"PR_Packages.json"
        outfile.write(dependencies)
