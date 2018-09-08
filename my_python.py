import sys

for arg in sys.argv:
    if (arg) in ['All', 'Dvr', 'cGuide', 'Vod', 'Search']:
        print(arg)
        print("Module is : ", arg)

