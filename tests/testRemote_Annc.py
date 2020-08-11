#
#	tesRemote_Annc.py
#
#	(c) 2020 by Andreas Kraft
#	License: BSD 3-Clause License. See the LICENSE file for further details.
#
#	Unit tests for Announcementfunctionality to a remote CSE. Tests are
#	skipped if there is no remote CSE.
#

import unittest, sys
sys.path.append('../acme')
from Constants import Constants as C
from Types import ResourceTypes as T
from init import *


# The following code must be executed before anything else because it influences
# the collection of skipped tests.
# It checks whether there actually is a remote CSE.
noRemote = not connectionPossible(REMOTEcseURL)
# _, rsc = RETRIEVE(REMOTEcseURL, REMOTEORIGINATOR)
# noRemote = rsc != C.rcOK

class TestRemote_Annc(unittest.TestCase):

	@classmethod
	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def setUpClass(cls):
		# check connection to CSE's
		cls.cse, rsc = RETRIEVE(cseURL, ORIGINATOR)
		assert rsc == C.rcOK, 'Cannot retrieve CSEBase: %s' % cseURL
		cls.remoteCse, rsc = RETRIEVE(REMOTEcseURL, REMOTEORIGINATOR)
		assert rsc == C.rcOK, 'Cannot retrieve CSEBase: %s' % REMOTEcseURL


	@classmethod
	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def tearDownClass(cls):
		DELETE(aeURL, ORIGINATOR)	# Just delete the AE and everything below it. Ignore whether it exists or not
		DELETE(nodURL, ORIGINATOR)	# Just delete the Node and everything below it. Ignore whether it exists or not


	# Create an AE with AT, but no AA
	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_createAnnounceAEwithATwithoutAA(self):
		jsn = 	{ 'm2m:ae' : {
					'rn': 	aeRN, 
					'api': 	'NMyApp1Id',
				 	'rr': 	False,
				 	'srv': 	[ '3' ],
				 	'at': 	[ REMOTECSEID ]
				}}
		r, rsc = CREATE(cseURL, 'C', T.AE, jsn)
		self.assertEqual(rsc, C.rcCreated)
		self.assertIsNotNone(findXPath(r, 'm2m:ae/at'))
		self.assertIsInstance(findXPath(r, 'm2m:ae/at'), list)
		self.assertEqual(len(findXPath(r, 'm2m:ae/at')), 2)
		self.assertIn(REMOTECSEID, findXPath(r, 'm2m:ae/at'))

		TestRemote_Annc.remoteAeRI = None
		for x in findXPath(r, 'm2m:ae/at'):
			if x == REMOTECSEID:
				continue
			if x.startswith('%s/' % REMOTECSEID):
				TestRemote_Annc.remoteAeRI = x
		self.assertIsNotNone(self.remoteAeRI)
		self.assertIsNone(findXPath(r, 'm2m:ae/aa'))
		TestRemote_Annc.ae = r


	# Retrieve the announced AE with AT, but no AA
	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_retrieveAnnouncedAEwithATwithoutAA(self):
		if TestRemote_Annc.remoteAeRI is None:
			self.skipTest('remote AE.ri not found')
		r, rsc = RETRIEVE('%s/~%s' %(REMOTEURL, TestRemote_Annc.remoteAeRI), CSEID)
		self.assertEqual(rsc, C.rcOK)
		self.assertIsNotNone(findXPath(r, 'm2m:aeA'))
		self.assertIsNotNone(findXPath(r, 'm2m:aeA/ty'))
		self.assertEqual(findXPath(r, 'm2m:aeA/ty'), T.AEAnnc)
		self.assertIsNotNone(findXPath(r, 'm2m:aeA/ct'))
		self.assertIsNotNone(findXPath(r, 'm2m:aeA/lt'))
		self.assertIsNotNone(findXPath(r, 'm2m:aeA/et'))
		self.assertIsNotNone(findXPath(r, 'm2m:aeA/pi'))
		self.assertTrue(CSEID.endswith(findXPath(r, 'm2m:aeA/pi')))
		self.assertIsNotNone(findXPath(r, 'm2m:aeA/lnk'))
		self.assertTrue(findXPath(r, 'm2m:aeA/lnk').endswith( findXPath(TestRemote_Annc.ae, 'm2m:ae/ri') ))


	# Delete the AE with AT, but no AA
	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_deleteAnnounceAE(self):
		if TestRemote_Annc.remoteAeRI is None:
			self.skipTest('remote AE.ri not found')
		_, rsc = DELETE(aeURL, ORIGINATOR)
		self.assertEqual(rsc, C.rcDeleted)
		# try to retrieve the announced AE. Should not be found
		r, rsc = RETRIEVE('%s/~%s' %(REMOTEURL, TestRemote_Annc.remoteAeRI), CSEID)
		self.assertEqual(rsc, C.rcNotFound)
		TestRemote_Annc.ae = None
		TestRemote_Annc.aremoteAeRIe = None


	# Create an AE with AT and AA
	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_createAnnounceAEwithATwithAA(self):
		jsn = 	{ 'm2m:ae' : {
					'rn': 	aeRN, 
					'api': 	'NMyApp1Id',
				 	'rr': 	False,
				 	'srv': 	[ '3' ],
				 	'lbl':	[ 'aLabel'],
				 	'at': 	[ REMOTECSEID ],
				 	'aa': 	[ 'lbl' ]
				}}
		r, rsc = CREATE(cseURL, 'C', T.AE, jsn)
		self.assertEqual(rsc, C.rcCreated)
		self.assertIsNotNone(findXPath(r, 'm2m:ae/lbl'))
		self.assertIsInstance(findXPath(r, 'm2m:ae/lbl'), list)
		self.assertEqual(len(findXPath(r, 'm2m:ae/lbl')), 1)
		self.assertIsNotNone(findXPath(r, 'm2m:ae/at'))
		self.assertIsInstance(findXPath(r, 'm2m:ae/at'), list)
		self.assertEqual(len(findXPath(r, 'm2m:ae/at')), 2)
		self.assertIn(REMOTECSEID, findXPath(r, 'm2m:ae/at'))
		self.assertIsInstance(findXPath(r, 'm2m:ae/aa'), list)
		self.assertEqual(len(findXPath(r, 'm2m:ae/aa')), 1)
		self.assertIn('lbl', findXPath(r, 'm2m:ae/aa'))

		TestRemote_Annc.remoteAeRI = None
		for x in findXPath(r, 'm2m:ae/at'):
			if x == REMOTECSEID:
				continue
			if x.startswith('%s/' % REMOTECSEID):
				TestRemote_Annc.remoteAeRI = x
		self.assertIsNotNone(self.remoteAeRI)
		TestRemote_Annc.ae = r


	# Retrieve the announced AE with AT and AA
	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_retrieveAnnouncedAEwithATwithAA(self):
		if TestRemote_Annc.remoteAeRI is None:
			self.skipTest('remote AE.ri not found')
		r, rsc = RETRIEVE('%s/~%s' %(REMOTEURL, TestRemote_Annc.remoteAeRI), CSEID)
		self.assertEqual(rsc, C.rcOK)
		self.assertIsNotNone(findXPath(r, 'm2m:aeA'))
		self.assertIsNotNone(findXPath(r, 'm2m:aeA/ty'))
		self.assertEqual(findXPath(r, 'm2m:aeA/ty'), T.AEAnnc)
		self.assertIsNotNone(findXPath(r, 'm2m:aeA/ct'))
		self.assertIsNotNone(findXPath(r, 'm2m:aeA/lt'))
		self.assertIsNotNone(findXPath(r, 'm2m:aeA/et'))
		self.assertIsNotNone(findXPath(r, 'm2m:aeA/pi'))
		self.assertTrue(CSEID.endswith(findXPath(r, 'm2m:aeA/pi')))
		self.assertIsNotNone(findXPath(r, 'm2m:aeA/lnk'))
		self.assertTrue(findXPath(r, 'm2m:aeA/lnk').endswith( findXPath(TestRemote_Annc.ae, 'm2m:ae/ri') ))
		self.assertIsNotNone(findXPath(r, 'm2m:aeA/lbl'))
		self.assertEqual(len(findXPath(r, 'm2m:aeA/lbl')), 1)
		self.assertIn('aLabel', findXPath(r, 'm2m:aeA/lbl'))


	# Update an non-AA AE with AA
	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_addAAtoAnnounceAEwithoutAA(self):
		jsn = 	{ 'm2m:ae' : {
				 	'lbl':	[ 'aLabel'],
				 	'aa': 	[ 'lbl' ]
				}}
		r, rsc = UPDATE(aeURL, ORIGINATOR, jsn)
		self.assertEqual(rsc, C.rcUpdated)
		self.assertIsNotNone(findXPath(r, 'm2m:ae/lbl'))


	# Create a Node with AT
	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_createAnnounceNode(self):
		jsn = 	{ 'm2m:nod' : {
					'rn': 	nodRN, 
					'ni': 	'aNI', 
				 	'at': 	[ REMOTECSEID ]
				}}
		r, rsc = CREATE(cseURL, ORIGINATOR, T.NOD, jsn)
		self.assertEqual(rsc, C.rcCreated)
		self.assertIsNotNone(findXPath(r, 'm2m:nod/at'))
		self.assertIsInstance(findXPath(r, 'm2m:nod/at'), list)
		self.assertEqual(len(findXPath(r, 'm2m:nod/at')), 2)
		self.assertIn(REMOTECSEID, findXPath(r, 'm2m:nod/at'))

		TestRemote_Annc.remoteNodRI = None
		for x in findXPath(r, 'm2m:nod/at'):
			if x == REMOTECSEID:
				continue
			if x.startswith('%s/' % REMOTECSEID):
				TestRemote_Annc.remoteNodRI = x
		self.assertIsNotNone(self.remoteNodRI)
		self.assertIsNone(findXPath(r, 'm2m:nod/aa'))
		TestRemote_Annc.node = r


	# Retrieve the announced Node with AT
	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_retrieveAnnouncedNode(self):
		if TestRemote_Annc.remoteNodRI is None:
			self.skipTest('remote Node.ri not found')
		r, rsc = RETRIEVE('%s/~%s' %(REMOTEURL, TestRemote_Annc.remoteNodRI), CSEID)
		self.assertEqual(rsc, C.rcOK)
		self.assertIsNotNone(findXPath(r, 'm2m:nodA'))
		self.assertIsNotNone(findXPath(r, 'm2m:nodA/ty'))
		self.assertEqual(findXPath(r, 'm2m:nodA/ty'), T.NODAnnc)
		self.assertIsNotNone(findXPath(r, 'm2m:nodA/ct'))
		self.assertIsNotNone(findXPath(r, 'm2m:nodA/lt'))
		self.assertIsNotNone(findXPath(r, 'm2m:nodA/et'))
		self.assertIsNotNone(findXPath(r, 'm2m:nodA/pi'))
		self.assertTrue(CSEID.endswith(findXPath(r, 'm2m:nodA/pi')))
		self.assertIsNotNone(findXPath(r, 'm2m:nodA/lnk'))
		self.assertTrue(findXPath(r, 'm2m:nodA/lnk').endswith( findXPath(TestRemote_Annc.node, 'm2m:nod/ri') ))


	# Create a mgmtObj under the node
	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_announceMgmtobj(self):
		jsn = 	{ 'm2m:bat' : {
					'mgd' : T.BAT,
					'dc'  : 'battery',
					'rn'  : batRN,
					'btl' : 23,
					'bts' : 1,
				 	'at'  : [ REMOTECSEID ],
				 	'aa'  : [ 'btl']
				}}
		r, rsc = CREATE(nodURL, ORIGINATOR, T.MGMTOBJ, jsn)
		self.assertEqual(rsc, C.rcCreated)
		self.assertIsNotNone(findXPath(r, 'm2m:bat/at'))
		self.assertIsInstance(findXPath(r, 'm2m:bat/at'), list)
		self.assertEqual(len(findXPath(r, 'm2m:bat/at')), 2)
		self.assertIn(REMOTECSEID, findXPath(r, 'm2m:bat/at'))
		self.assertEqual(findXPath(r, 'm2m:bat/btl'), 23)
		self.assertEqual(findXPath(r, 'm2m:bat/bts'), 1)

		TestRemote_Annc.remoteBatRI = None
		for x in findXPath(r, 'm2m:bat/at'):
			if x == REMOTECSEID:
				continue
			if x.startswith('%s/' % REMOTECSEID):
				TestRemote_Annc.remoteBatRI = x
		self.assertIsNotNone(self.remoteBatRI)
		self.assertIsNotNone(findXPath(r, 'm2m:bat/aa'))
		self.assertEqual(len(findXPath(r, 'm2m:bat/aa')), 1)
		self.assertIn('btl', findXPath(r, 'm2m:bat/aa'))
		TestRemote_Annc.bat = r


	# Retrieve the announced mgmtobj 
	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_retrieveAnnouncedMgmtobj(self):
		if TestRemote_Annc.remoteBatRI is None:
			self.skipTest('remote bat.ri not found')
		r, rsc = RETRIEVE('%s/~%s' %(REMOTEURL, TestRemote_Annc.remoteBatRI), ORIGINATOR)
		self.assertEqual(rsc, C.rcOK)
		self.assertIsNotNone(findXPath(r, 'm2m:batA'))
		self.assertIsNotNone(findXPath(r, 'm2m:batA/ty'))
		self.assertEqual(findXPath(r, 'm2m:batA/ty'), T.MGMTOBJAnnc)
		self.assertIsNotNone(findXPath(r, 'm2m:batA/mgd'))
		self.assertEqual(findXPath(r, 'm2m:batA/mgd'), T.BAT)
		self.assertIsNotNone(findXPath(r, 'm2m:batA/ct'))
		self.assertIsNotNone(findXPath(r, 'm2m:batA/lt'))
		self.assertIsNotNone(findXPath(r, 'm2m:batA/et'))
		self.assertIsNotNone(findXPath(r, 'm2m:batA/pi'))
		self.assertTrue(CSEID.endswith(findXPath(r, 'm2m:batA/pi')))
		self.assertIsNotNone(findXPath(r, 'm2m:batA/lnk'))
		self.assertTrue(findXPath(r, 'm2m:batA/lnk').endswith( findXPath(TestRemote_Annc.bat, 'm2m:bat/ri') ))
		self.assertIsNotNone(findXPath(r, 'm2m:batA/btl'))
		self.assertEqual(findXPath(r, 'm2m:batA/btl'), 23)
		self.assertIsNone(findXPath(r, 'm2m:batA/bts'))


	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_updateMgmtObjAttribute(self):
		jsn = 	{ 'm2m:bat' : {
					'btl' : 42,
					'bts' : 2
				}}
		r, rsc = UPDATE(batURL, ORIGINATOR, jsn)
		self.assertEqual(rsc, C.rcUpdated)
		self.assertEqual(findXPath(r, 'm2m:bat/btl'), 42)
		self.assertEqual(findXPath(r, 'm2m:bat/bts'), 2)

		r, rsc = RETRIEVE('%s/~%s' %(REMOTEURL, TestRemote_Annc.remoteBatRI), ORIGINATOR)
		self.assertEqual(rsc, C.rcOK)
		self.assertIsNotNone(findXPath(r, 'm2m:batA/btl'))
		self.assertEqual(findXPath(r, 'm2m:batA/btl'), 42)
		self.assertIsNone(findXPath(r, 'm2m:batA/bts'))


	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_addMgmtObjAttribute(self):
		jsn = 	{ 'm2m:bat' : {
					'aa' : [ 'btl', 'bts']
				}}
		r, rsc = UPDATE(batURL, ORIGINATOR, jsn)
		self.assertEqual(rsc, C.rcUpdated)
		self.assertEqual(findXPath(r, 'm2m:bat/btl'), 42)
		self.assertEqual(findXPath(r, 'm2m:bat/bts'), 2)
		self.assertIsNotNone(findXPath(r, 'm2m:bat/aa'))
		self.assertEqual(len(findXPath(r, 'm2m:bat/aa')), 2)
		self.assertIn('btl', findXPath(r, 'm2m:bat/aa'))
		self.assertIn('bts', findXPath(r, 'm2m:bat/aa'))

		r, rsc = RETRIEVE('%s/~%s' %(REMOTEURL, TestRemote_Annc.remoteBatRI), ORIGINATOR)
		self.assertEqual(rsc, C.rcOK)
		self.assertIsNotNone(findXPath(r, 'm2m:batA/btl'))
		self.assertEqual(findXPath(r, 'm2m:batA/btl'), 42)
		self.assertIsNotNone(findXPath(r, 'm2m:batA/bts'))
		self.assertEqual(findXPath(r, 'm2m:batA/bts'), 2)


	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_removeMgmtObjAttribute(self):
		jsn = 	{ 'm2m:bat' : {
					'aa' : [ 'bts']
				}}
		r, rsc = UPDATE(batURL, ORIGINATOR, jsn)
		self.assertEqual(rsc, C.rcUpdated)
		self.assertEqual(findXPath(r, 'm2m:bat/btl'), 42)
		self.assertEqual(findXPath(r, 'm2m:bat/bts'), 2)
		self.assertIsNotNone(findXPath(r, 'm2m:bat/aa'))
		self.assertEqual(len(findXPath(r, 'm2m:bat/aa')), 1)
		self.assertNotIn('btl', findXPath(r, 'm2m:bat/aa'))
		self.assertIn('bts', findXPath(r, 'm2m:bat/aa'))

		r, rsc = RETRIEVE('%s/~%s' %(REMOTEURL, TestRemote_Annc.remoteBatRI), ORIGINATOR)
		self.assertEqual(rsc, C.rcOK)
		self.assertIsNone(findXPath(r, 'm2m:batA/btl'))
		self.assertIsNotNone(findXPath(r, 'm2m:batA/bts'))
		self.assertEqual(findXPath(r, 'm2m:batA/bts'), 2)


	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_removeMgmtObjAA(self):
		jsn = 	{ 'm2m:bat' : {
					'aa' : None
				}}
		r, rsc = UPDATE(batURL, ORIGINATOR, jsn)
		self.assertEqual(rsc, C.rcUpdated)
		self.assertEqual(findXPath(r, 'm2m:bat/btl'), 42)
		self.assertEqual(findXPath(r, 'm2m:bat/bts'), 2)
		self.assertIsNone(findXPath(r, 'm2m:bat/aa'))

		r, rsc = RETRIEVE('%s/~%s' %(REMOTEURL, TestRemote_Annc.remoteBatRI), ORIGINATOR)
		self.assertEqual(rsc, C.rcOK)
		self.assertIsNone(findXPath(r, 'm2m:batA/btl'))
		self.assertIsNone(findXPath(r, 'm2m:batA/bts'))


	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_removeMgmtObjCSIfromAT(self):
		at = findXPath(TestRemote_Annc.bat, 'm2m:bat/at').copy()
		at.remove(REMOTECSEID)
		jsn = 	{ 'm2m:bat' : {
					'at' : at 			# with REMOTECSEID removed
				}}
		r, rsc = UPDATE(batURL, ORIGINATOR, jsn)
		self.assertEqual(rsc, C.rcUpdated)
		self.assertEqual(len(findXPath(r, 'm2m:bat/at')), 0)

		r, rsc = RETRIEVE('%s/~%s' %(REMOTEURL, TestRemote_Annc.remoteBatRI), ORIGINATOR)
		self.assertEqual(rsc, C.rcNotFound)


	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_addMgmtObjCSItoAT(self):
		jsn = 	{ 'm2m:bat' : {
					'at' : [ REMOTECSEID ] 			# with REMOTECSEID added
				}}
		r, rsc = UPDATE(batURL, ORIGINATOR, jsn)
		self.assertEqual(rsc, C.rcUpdated)
		self.assertEqual(len(findXPath(r, 'm2m:bat/at')), 2)

		TestRemote_Annc.remoteBatRI = None
		for x in findXPath(r, 'm2m:bat/at'):
			if x == REMOTECSEID:
				continue
			if x.startswith('%s/' % REMOTECSEID):
				TestRemote_Annc.remoteBatRI = x
		self.assertIsNotNone(self.remoteBatRI)
		TestRemote_Annc.bat = r

		r, rsc = RETRIEVE('%s/~%s' %(REMOTEURL, TestRemote_Annc.remoteBatRI), ORIGINATOR)
		self.assertEqual(rsc, C.rcOK)


	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_removeMgmtObjAT(self):
		jsn = 	{ 'm2m:bat' : {
					'at' : None 			# with at removed
				}}
		r, rsc = UPDATE(batURL, ORIGINATOR, jsn)
		self.assertEqual(rsc, C.rcUpdated)
		self.assertIsNone(findXPath(r, 'm2m:bat/at'))

		r, rsc = RETRIEVE('%s/~%s' %(REMOTEURL, TestRemote_Annc.remoteBatRI), ORIGINATOR)
		self.assertEqual(rsc, C.rcNotFound)
		TestRemote_Annc.bat = None
		TestRemote_Annc.remoteBatRI = None


	@unittest.skipIf(noRemote, 'No remote CSEBase')
	def test_deleteAnnounceNode(self):
		if TestRemote_Annc.node is None:
			self.skipTest('node not found')
		_, rsc = DELETE(nodURL, ORIGINATOR)
		self.assertEqual(rsc, C.rcDeleted)
		# try to retrieve the announced Node. Should not be found
		r, rsc = RETRIEVE('%s/~%s' %(REMOTEURL, TestRemote_Annc.remoteNodRI), CSEID)
		self.assertEqual(rsc, C.rcNotFound)
		TestRemote_Annc.node = None
		TestRemote_Annc.remoteNodRI = None
		# Actually, the mgmtobj should been deleted by now in another test case
		r, rsc = RETRIEVE('%s/~%s' %(REMOTEURL, TestRemote_Annc.remoteBatRI), ORIGINATOR)
		self.assertEqual(rsc, C.rcNotFound)
		TestRemote_Annc.bat = None
		TestRemote_Annc.remoteBatRI = None



# rcn=7 (original resource)



def run():
	suite = unittest.TestSuite()

	# create an announced AE, but no extra attributes
	suite.addTest(TestRemote_Annc('test_createAnnounceAEwithATwithoutAA'))
	suite.addTest(TestRemote_Annc('test_retrieveAnnouncedAEwithATwithoutAA'))
	suite.addTest(TestRemote_Annc('test_deleteAnnounceAE'))

	# create an announced AE, including announced attribute
	suite.addTest(TestRemote_Annc('test_createAnnounceAEwithATwithAA'))
	suite.addTest(TestRemote_Annc('test_retrieveAnnouncedAEwithATwithAA'))
	suite.addTest(TestRemote_Annc('test_deleteAnnounceAE'))

	# create an announced Node & MgmtObj [bat]
	suite.addTest(TestRemote_Annc('test_createAnnounceNode'))
	suite.addTest(TestRemote_Annc('test_retrieveAnnouncedNode'))
	suite.addTest(TestRemote_Annc('test_announceMgmtobj'))
	suite.addTest(TestRemote_Annc('test_retrieveAnnouncedMgmtobj'))
	suite.addTest(TestRemote_Annc('test_updateMgmtObjAttribute'))
	suite.addTest(TestRemote_Annc('test_addMgmtObjAttribute'))
	suite.addTest(TestRemote_Annc('test_removeMgmtObjAttribute'))
	suite.addTest(TestRemote_Annc('test_removeMgmtObjAA'))
	suite.addTest(TestRemote_Annc('test_removeMgmtObjCSIfromAT'))
	suite.addTest(TestRemote_Annc('test_addMgmtObjCSItoAT'))
	suite.addTest(TestRemote_Annc('test_removeMgmtObjAT'))
	suite.addTest(TestRemote_Annc('test_deleteAnnounceNode'))

	result = unittest.TextTestRunner(verbosity=testVerbosity, failfast=True).run(suite)
	return result.testsRun, len(result.errors + result.failures), len(result.skipped)


if __name__ == '__main__':
	_, errors, _ = run()
	sys.exit(errors)
