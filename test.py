import platform
a = [getattr(platform, method)for method in dir(platform) if not method.startswith('_')]
for x in a:
    if callable(x):
        try:
            print(x())
        except Exception as ex:
            print(ex)
    else:
        print(x)



