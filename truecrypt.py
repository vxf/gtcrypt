# truecrypt.py
# python access to truecrypt command line utilities

import pexpect, re

askpass = re.compile('Enter password for (\S+):')
errpass = re.compile('Incorrect password or not a TrueCrypt volume.\r\nEnter password for (\S+):')
errvolume = 'Cannot open volume: No such file or directory'
errmntfail = 'Mount failed'
errvolumemapped = 'Volume already mapped'
errnotmapped = re.compile('(\S+) not mounted')

class WrongPassword(Exception):
   def __init__(self):
      Exception.__init__(self, None)

class UnexistentVolume(Exception):
   def __init__(self):
      Exception.__init__(self, None)

class MountFailed(Exception):
   def __init__(self):
      Exception.__init__(self, None)

class VolumeMapped(Exception):
   def __init__(self):
      Exception.__init__(self, None)

class VolumeNotMapped(Exception):
   def __init__(self):
      Exception.__init__(self, None)

def mountVolume(volume, mntpnt, askPassword, mntopts = ''):
	child = pexpect.spawn(' '.join(('truecrypt', volume, mntpnt, mntopts)))

	i = child.expect([pexpect.EOF, askpass, errvolume, errvolumemapped])
	if i == 0 :
		return
	if i == 1 :
		child.sendline(askPassword(volume, mntpnt))
	elif i == 2 :
		child.terminate()
		raise UnexistentVolume()
	elif i == 3 :
		child.terminate()
		raise VolumeMapped()


	i = child.expect([pexpect.EOF, errpass, errmntfail])
	if i == 0 :
		return
	elif i == 1 :
		child.terminate()
		raise WrongPassword()
	elif i == 2 :
		child.terminate()
		raise MountFailed()

def unmountVolume(volume):
	child = pexpect.spawn(' '.join(('truecrypt -d', volume)))

	i = child.expect([pexpect.EOF, errnotmapped])
	if i == 0 :
		return
	elif i == 1 :
		child.terminate()
		raise VolumeNotMapped()

if __name__ == "__main__":
	import getpass, sys

	def askPassword(volume, mntpnt):
		return getpass.getpass()
	try:
		if len(sys.argv) != 3 :
			print 'Usage: python command.py VOLUME_PATH MOUNT_DIRECTORY'
		else:
			mountVolume(sys.argv[1], sys.argv[2], askPassword)
			print 'Volume sucessfuly mounted'
	except WrongPassword:
		print 'Wrong password'
	except UnexistentVolume:
		print 'Volume does not exist'
	except MountFailed:
		print 'Mount failure'
	except VolumeMapped:
		print 'Volume already mapped'

	try:
		if len(sys.argv) == 3 :
			unmountVolume(sys.argv[1])
			print 'Volume sucessfuly unmounted'
	except VolumeNotMapped:
		print 'Volume not mapped'

