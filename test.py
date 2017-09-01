from hardest.python_searcher import PythonSearcher

x = PythonSearcher()
data = x.search()
for key, value in data.items():
    print("-> ", key)
    for vl in value:
        if len(vl.binaries) > 0:
            print("   --:", str(vl.binaries[0]))
    print('')
