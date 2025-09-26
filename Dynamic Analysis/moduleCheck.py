import modulefinder

finder = modulefinder.ModuleFinder()
finder.run_script('C:\\Users\\Paul Collins\\Dynamic Analysis\\modules\\slot_master\\root.py')

print('Loaded modules:')
for name, mod in finder.modules.items():
    print('%s: ' % name, end='')
    print(','.join(list(mod.globalnames.keys())), end='\n\n')