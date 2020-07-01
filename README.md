# Romulan Py

### Python version of Romulan Ale

Scans a driver for exports typically used for exploiting

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
Found MmMapLockedPages @ 0x2997c                                             
~~~