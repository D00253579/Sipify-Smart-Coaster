The 2 tests releated to cup detection were made with the intention of being ran in isolation

How to run these tests:

test_no_cup_detected()
	Preperation: 
		Ensure the LDR is in a space with natural light sources. There should be no 
		object(s) blocking the LDR.
	Running:
		run 'pytest test_no_cup_detected.py'

test_cup_detected()
	Preperation: 
		Ensure the LDR is in a space with natural light sources. There should be 
		object(s) blocking the LDR.
	Running:
		run 'pytest test_no_cup_detected.py'