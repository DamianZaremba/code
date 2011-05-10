#!/usr/bin/python
import random, sys
"""
Silly little guess the number game
"""
number = random.randrange(10, 100)
i = 0
goes = 10

try:
	while i <= goes:
		guess = raw_input('Your Guess? ')
		try:
			guess = int(guess.strip())
		except ValueError:
			print "You must enter a number!\n"
		else:
			if guess == number:
				print "You got it right :)\n"
				break
			else:
				i += 1
				gl = goes-i

				if gl == 0:
					print "You failed, The answer was %d\n" % (number)
					break
				else:
					print "Wrong Try Again. Goes left: %d\n" % (gl)
except KeyboardInterrupt:
	print "\nThe answer was %d. ByeBye!\n" % (number)
	sys.exit(1)
