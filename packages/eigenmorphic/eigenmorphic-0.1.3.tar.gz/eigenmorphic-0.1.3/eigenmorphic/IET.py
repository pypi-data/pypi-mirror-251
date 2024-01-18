# Compute a substitution 

def induce(e, i, flipped):
	"""
	Compute one step of induction on place, and return the associated substitution.
	e : couple of lists, before and after exchange
	i : top or bottom induction (i=0: bottom losing letter, i=1: top losing letter)
	"""
	from sage.combinat.words.morphism import WordMorphism
	if i == 0:
		i0 = 0
		i1 = 1 # losing letter
	else:
		i0 = 1
		i1 = 0 # losing letter
	d = dict()
	for i in e[0]:
		d[i] = [i]
	d[e[i1][-1]] = [e[i0][-1], e[i1][-1]]
	if flipped[e[i0][-1]]:
		from operator import xor
		e[i1].insert(e[i1].index(e[i0][-1]), e[i1][-1])
		flipped[e[i1][-1]] = not flipped[e[i1][-1]]
	else:
		e[i1].insert(e[i1].index(e[i0][-1])+1, e[i1][-1])
	e[i1].pop()
	return WordMorphism(d)

def rauzy_loop_substitution(per, loop, flips=None, verb=False):
	"""
	Compute the susbtitution of a loop in the Rauzy graph from a given permutation per.

	INPUT:

		- ``per`` - list -- a permutation
			The i-th element of the list is the image of (i+1) by the permutation.

		- ``loop`` - list or string or vector -- list with values in {0,1} indicating which rauzy induction
			where 0 indicate that the losing letter is at bottom and
				  1 indicate that the losing letter is at top
			or vector of lengths with same length as per

		- ``flips`` - dict (default: ``None``) -- dictionnary indicating for each letter whether it is flipped (value True) or not (value False).

		- ``verb`` - int (default: ``False``) - if >0, print informations.

	OUTPUT:
		A WordMorphism

	EXAMPLES:

		sage: from eigenmorphic import *
		sage: per = [9, 8, 7, 6, 5, 4, 3, 2, 1] # permutation
		sage: loop = "11010101101100011110000011111010000000110"
		sage: rauzy_loop_substitution(per, loop)
		WordMorphism: 1->19276271, 2->192762712762, 3->197127623653, 4->1971276236534454, 5->197127623653445, 6->1971276236, 7->197127, 8->18181918, 9->181819

		sage: a = AA(2*cos(pi/7))
		sage: l = [1, 2*a-3, 2-a, a^2-a, 2*a^2-3*a-1, -3*a^2+5*a+1]
		sage: rauzy_loop_substitution([4,3,2,6,5,1], l)
		WordMorphism: 1->41641, 2->412432, 3->4124323, 4->4124, 5->415416415, 6->415416

	"""
	from copy import copy
	from sage.combinat.words.morphism import WordMorphism
	e = [list(range(1,len(per)+1)), per]
	if flips is None:
		f = {i:False for i in range(1,len(per)+1)}
	else:
		f = copy(flips)
	f0 = copy(f)
	if verb > 0:
		print("flips = %s" % f)
	d = dict()
	for i in e[0]:
		d[i] = [i]
	s = WordMorphism(d)
	if isinstance(loop, str):
		loop = [int(c) for c in loop] # convert it to numbers
	if len(loop) == len(per) and len([i for i in loop if i not in [0,1]]) != 0:
		from sage.modules.free_module_element import vector
		if verb > 0:
			print("loop is a vector")
		v = vector(loop)
		v /= sum(v)
		v0 = vector(v)
		while True:
			cmp = int(v[e[0][-1]-1] < v[e[1][-1]-1])
			if verb > 1:
				print(cmp)
			s0 = induce(e, cmp, flipped=f)
			s *= s0
			m = s0.incidence_matrix()
			v = m.inverse()*v
			v /= sum(v)
			if v == v0:
				break
			if verb > 1:
				print([t.n() for t in v])
	else:
		if verb > 0:
			print("loop is a list of inductions")
		for i in loop:
			if verb > 0:
				print(e)
				print(f)
				print(s)
			s *= induce(e, i, f)
		# check if it is indeed a loop
		for i in range(len(e[0])):
			if e[0][i] != i+1 or e[1][i] != per[i]:
				raise ValueError("This is not a loop in the Rauzy graph !\n%s != %s" % (e,[list(range(1,len(per)+1)), per]))
		if f != f0:
			raise ValueError("This is not a loop in the Rauzy graph (flips are different) !\n%s != %s" % (f,f0))
	return s

