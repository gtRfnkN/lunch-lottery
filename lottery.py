#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random, json, os, sys
from itertools import combinations

def get_file_in_current_folder(filename):
	return os.path.dirname(os.path.abspath(__file__)) + '/' + filename

def write_dict(dict, filename = 'data.json'):
	filename = get_file_in_current_folder(filename)
	with open(filename, 'w') as f:
		list = [[t[0], t[1]] for t in dict]
		json.dump(list, f)

def read_dict(filename = 'data.json'):
	filename = get_file_in_current_folder(filename)
	with open(filename) as f:
		list = json.load(f)
		return {tuple(sorted(i)) for i in list}

def is_old_combination(old_pairs, combination):
	# was this combination used before in any way?
	return combination in old_pairs or combination[::-1] in old_pairs

def find_new_combination(old_pairs, person, persons):
	# find the first unpaired person that wasn't yet paired with this person
	for p in persons:
		if not is_old_combination(old_pairs, (person, p)):
			return (0, (person, p))

	# if no one is left, pick the first unpaired person
	return (1, (person, persons[0]))

def get_combinations(old_pairs, persons):
	combinations = []
	cost = 0

	# loop through persons & match always 2 removing them from the list
	while len(persons) > 1:

		new_combo = find_new_combination(old_pairs, persons[0], persons[1:])
		cost += new_combo[0]

		# add unique combination to pair list and remove from unpaired list
		combination = new_combo[1]
		combinations.append(combination)
		persons.remove(combination[0])
		persons.remove(combination[1])

	# if persons was an odd amount, add the last one to the first pair
	if len(persons) == 1:
		combinations[0] = combinations[0] + (persons[0],)

	return (cost, combinations)

def get_best_new_combination(old_pairs, persons, n = 10):
	combinations = []

	# try to find a few new combinations to select the best from
	for i in range(n):
		random.shuffle(persons)
		combinations.append(get_combinations(old_pairs, persons[:]))

	# find the one with the minimum cost
	minimum_count = combinations[0][0]
	combination = combinations[0]
	for c in combinations[1:]:
		if c[0] < minimum_count:
			combination = c

	# set all of the pairs from this combination to the done list
	for c in combination[1]:
		if len(c) == 2:
			old_pairs.add(c)

	return combination

def print_result(combination):
	print('This week:')
	for c in combination[1]:
		print(' & '.join(c))
	print('Total of %d combinations with a duplicate score of %d' %(len(combination[1]), combination[0]))

if __name__ == "__main__":

	# print error if wrong params
	if len(sys.argv) < 2 or len(sys.argv) > 3:
		exit('wrong parameters: call with `python lottery.py \'name1 name2 name3 ...\' [-r]`')

	# read persons, split them up into a list and randomize it
	persons = sys.argv[1].split()
	random.shuffle(persons)

	# get all old pairs
	old_pairs = read_dict()

	# check if the reset flag is set
	if len(sys.argv) > 2 and sys.argv[2] == '-r':
		# reset the pairs
		old_pairs = {tuple(sorted(i)) for i in []}


	# get best new combination and print it
	print_result(get_best_new_combination(old_pairs, persons[:]))

	# store the updated old pairs
	write_dict(old_pairs)
