#!/usr/bin/env python
'''
Ported from the original ClueNet fishbot written by many people.
'''
from twisted.words.protocols import irc
from twisted.internet import reactor, protocol
from twisted.python import log
import time
import random
import re

channel_responses = {
	'hampster': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': '%n: There is no \'p\' in hamster you retard.',
	},

	'vinegar.*aftershock': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Ah, a true connoisseur!',
	},

	'aftershock.*vinegar': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Ah, a true connoisseur!',
	},

	'^some people are being fangoriously devoured by a gelatinous monster$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Hillary\'s legs are being digested.',
	},

	'^ag$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Ag, ag ag ag ag ag AG AG AG!',
	},

	'^fishbot owns$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Aye, I do.',
	},

	'vinegar': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Nope, too sober for vinegar. Try later.',
	},

	'^just then, he fell into the sea$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Ooops!',
	},

	'aftershock': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'mmmm, Aftershock.',
	},

	'^why are you here\?$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Same reason.  I love candy.',
	},

	'^spoon$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'There is no spoon.',
	},

	'^(bounce|wertle)$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'moo',
	},

	'^crack$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Doh, there goes another bench!',
	},

	'^you can\'t just pick people at random!$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'I can do anything I like, %n, I\'m eccentric!  Rrarrrrrgh!  Go!',
	},

	'^flibble$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'plob',
	},

	'(the fishbot has created splidge|fishbot created splidge)': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'omg no! Think I could show my face around here if I was responsible for THAT?',
	},

	'^now there\'s more than one of them\?$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'A lot more.',
	},

	'^i want everything$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Would that include a bullet from this gun?',
	},

	'we are getting aggravated': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Yes, we are.',
	},

	'^how old are you, fishbot\?$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'action',
		'message': 'is older than time itself!',
	},

	'^atlantis$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Beware the underwater headquarters of the trout and their bass henchmen. From there they plan their attacks on other continents.',
	},

	'^oh god$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'fishbot will suffice.',
	},

	'^fishbot$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Yes?',
	},

	'^what is the matrix\?$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'No-one can be told what the matrix is.  You have to see it for yourself.',
	},

	'^what do you need\?$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Guns. Lots of guns.',
	},

	'^i know kungfu$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Show me.',
	},

	'^cake$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'fish',
	},

	'^trout go m[o0][o0]$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Aye, that\'s cos they\'re fish.',
	},

	'^kangaroo$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'The kangaroo is a four winged stinging insect.',
	},

	'^sea bass$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Beware of the mutant sea bass and their laser cannons!',
	},

	'^trout$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Trout are freshwater fish and have underwater weapons.',
	},

	'^where are we\?$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Last time I looked, we were in %c.',
	},

	'^fish go m[o0][o0]$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'action',
		'message': 'notes that %n is truly enlightened.',
	},

	'^(.*) go m[o0][o0]$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': '%n: only when they are impersonating fish.',
	},

	'^fish go ([a-z0-9 _]+)$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': '%n LIES! Fish don\'t go %1! fish go m00!',
	},

	'^you know who else (.*)$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': '%n: YA MUM!',
	},

	'^if there\'s one thing i know for sure, it\'s that fish don\'t m00\.$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': '%n: HERETIC! UNBELIEVER!',
	},

	'^ammuu\?$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': '%n: fish go m00 oh yes they do!',
	},

	'^fish$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': '%n: fish go m00!',
	},

	'^snake$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Ah snake a snake! Snake, a snake! Ooooh, it\'s a snake!',
	},

	'sledgehammer': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'sledgehammers go quack!',
	},

	'^badger badger badger badger badger badger badger badger badger badger badger badger$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'mushroom mushroom!',
	},

	'^moo\?$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'To moo, or not to moo, that is the question. Whether \'tis nobler in the mind to suffer the slings and arrows of outrageous fish...',
	},

	'^herring$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'herring(n): Useful device for chopping down tall trees. Also moos (see fish).',
	}
}

action_responses = {
	'hampster': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': '%n: There is no \'p\' in hamster you retard.',
	},

	'^feeds fishbot hundreds and thousands$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'MEDI.. er.. FISHBOT',
	},

	'(vinegar.*aftershock|aftershock.*vinegar)': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Ah, a true connoisseur!',
	},

	'vinegar': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Nope, too sober for vinegar.  Try later.',
	},

	'aftershock': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'mmmm, Aftershock.',
	},

	'(the fishbot has created splidge|fishbot created splidge)': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'omg no! Think I could show my face around here if I was responsible for THAT?',
	},

	'we are getting aggravated': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'Yes, we are.',
	},

	'^strokes fishbot$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'action',
		'message': 'm00s loudly at %n.',
	},

	'^slaps (.*) around a bit with a large trout$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': 'trouted!',
	},

	'^fish go m[o0][o0]$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'action',
		'message': 'notes that %n is truly enlightened.',
	},

	'^(.*) go m[o0][o0]$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': '%n: only when they are impersonating fish.',
	},

	'^fish go ([a-z0-9 _]+)$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': '%n LIES! Fish don\'t go %1! fish go m00!',
	},

	'^you know who else (.*)$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': '%n: YA MUM!',
	},

	'^thinks happy thoughts about pretty (.*)$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'action',
		'message': 'has plenty of pretty %1. Would you like one %n?',
	},

	'^snaffles a (.*) off fishbot.$': {
		'regex_flags': re.IGNORECASE,
		'response_type': 'msg',
		'message': ':(',
	}
}

class fishbotProtocol(irc.IRCClient):
	nickname = "fishbot"

	def __init__(self, channels):
		self.channels = channels

	def connectionMade(self):
		irc.IRCClient.connectionMade(self)

	def connectionLost(self, reason):
		irc.IRCClient.connectionLost(self, reason)

	def signedOn(self):
		for chan, passw in self.channels:
			self.join(chan, passw)

		self.mode(self.nickname, True, '+B', limit=None, user=self.nickname)
		print "Signed on as %s." % (self.nickname)

	def joined(self, channel):
		print "Joined %s" % (channel)
	
	def kickedFrom(self, channel, kicker, message):
		print "Kicked from %s" % (channel)
	
	def nickChanged(self, nick):
		print "Nick changed to %s" % (nick)

	def privmsg(self, user, channel, msg):
		user = user.split('!', 1)[0]
		if channel[0] == "#":
			for regex in channel_responses:
					try:
						ret = re.match(regex, msg, flags=channel_responses[regex]['regex_flags'])
						if ret:
							groups = ret.groups()
							message = channel_responses[regex]['message']
							message = message.replace("%n", user)
							message = message.replace("%c", channel)
							if len(groups) > 0:
								message = message.replace("%1", groups[0])

							if channel_responses[regex]['response_type'] == "action":
								self.me(channel, message)
							elif channel_responses[regex]['response_type'] == "msg":
								self.msg(channel, message)

							break;
					except:
						print "Bad stuff happended when checking '%s' against '%s':" % (msg, regex)
						print e
						pass

		else:
			self.msg(user, "Talking to bots is a bad idea")

	def action(self, user, channel, msg):
		user = user.split('!', 1)[0]

		for regex in action_responses:
				try:
					ret = re.match(regex, msg, flags=action_responses[regex]['regex_flags'])
					if ret:
						groups = ret.groups()
						message = action_responses[regex]['message']
						message = message.replace("%n", user)
						message = message.replace("%c", channel)
						if len(groups) > 0:
							message = message.replace("%1", groups[0])

						if action_responses[regex]['response_type'] == "action":
							self.me(channel, message)
						elif action_responses[regex]['response_type'] == "msg":
							self.msg(channel, message)

						break;
				except Exception, e:
					print "Bad stuff happended when checking '%s' against '%s':" % (msg, regex)
					print e
					pass

	def alterCollidedNick(self, nickname):
		nickname = "%s-%d" (nickname, random.rand(0, 5))
		return nickname

class fishBot(protocol.ClientFactory):
	protocol = fishbotProtocol

	def __init__(self, channels):
		self.channels = channels
		protocol.channels = channels

	def buildProtocol(self, addr):
		p = self.protocol(self.channels)
		p.factory = self
		return p

	def clientConnectionLost(self, connector, reason):
		print "Lost connection (%s), reconnecting." % (reason)
		connector.connect()

	def clientConnectionFailed(self, connector, reason):
		print "Could not connect: %s" % (reason)
		time.sleep(2)
		connector.connect()

if __name__ == '__main__':
	channels = [
		('#vancraft', ''),
		('#chat', ''),
		('#allgamer', ''),
		('#support', ''),
	]

	reactor.connectTCP("irc.rawrirc.net", 6667, fishBot(channels))
	reactor.run()
