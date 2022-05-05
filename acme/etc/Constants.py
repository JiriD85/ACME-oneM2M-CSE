#
#	Constants.py
#
#	(c) 2020 by Andreas Kraft
#	License: BSD 3-Clause License. See the LICENSE file for further details.
#
""" Various CSE and oneM2M constants """


class Constants(object):
	""" Various CSE and oneM2M constants """

	version							= '0.10.0'
	"""	ACME's release version """

	textLogo						= '[dim][[/dim][red][i]ACME[/i][/red][dim]][/dim]'
	"""	ACME's colorful console logo """

	#
	#	Configuration files
	#

	defaultConfigFile			= 'acme.ini.default'
	"""	The name of the INI file that contains the default configuration settings """

	defaultUserConfigFile		= 'acme.ini'
	""" The name of the INI file that contains the user-defined configuration settings """


	#
	#	HTTP Header Fields
	#	These fields are here instead of the httpServer bc they are also used by the test cases.
	#

	hfOrigin						= 'X-M2M-Origin'
	"""	HTTP header field: originator """

	hfRI 							= 'X-M2M-RI'
	"""	HTTP header field: request identifier """
	
	hfRVI							= 'X-M2M-RVI'
	"""	HTTP header field: release version indicator """
	
	hfEC 							= 'X-M2M-EC'
	"""	HTTP header field: event category """
	
	hfRET 							= 'X-M2M-RET'
	"""	HTTP header field: request expiration timestamp """

	hfRST 							= 'X-M2M-RST'
	"""	HTTP header field: result expiration timestamp """
	
	hfOET 							= 'X-M2M-OET'
	"""	HTTP header field: operation execution time """

	hfOT 							= 'X-M2M-OT'
	"""	HTTP header field: originating timestamp """

	hfRTU 							= 'X-M2M-RTU'
	"""	HTTP header field: notificationURI element of the response type """
	
	hfRSC 							= 'X-M2M-RSC'
	"""	HTTP header field: response status code """

	hfVSI 							= 'X-M2M-VSI'
	"""	HTTP header field: vendor information """
			

	#
	#	Supported URL schemes
	#
	supportedSchemes = ['http', 'https', 'mqtt', 'mqtts', 'acme']
	""" The URL schemes supported by the CSE """


	#
	#	Magic strings and numbers
	#

	maxIDLength	= 10
	"""	Maximum length of identifiers generated by the CSE """


	
