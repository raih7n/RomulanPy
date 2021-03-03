# Romulan Py

### Windows driver export scanner

Scans a driver for a few exports commonly assocaited with arbitrary physical memory access exposure

Check a single driver

	python3 romulan_ale.py -p [filepath]
	
Or scan a directory

	python3 romulan_ale.py -p [directory]


Example output:
~~~text
Checking ssadcmnt.sys...                                      [  OK  ]
Checking ssadmdfl.sys...                                      [  OK  ]
Checking ssadmdm.sys...                                       [  OK  ]
Checking ssadserd.sys...                                      [  OK  ]
Checking ssadwhnt.sys...                                      [  OK  ]
Checking ssadadb.sys...                                       [  OK  ]
Checking ssadbus.sys...                                       [ FAIL ]
Found MmMapIoSpace @ 0x2997c                                             
~~~
