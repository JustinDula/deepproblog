import re
import os
from os.path import join as pjoin
from shutil import rmtree

NUM_FOLDS = 5
INPUT_DIR = "data/5folds/"
OUTPUT_DIR = "data/5folds-processed/"
FOLDS = ["data/5folds/fold" + str(i + 1) for i in range(NUM_FOLDS)]
OUTPUT_FOLDS = ["data/5folds-processed/fold" + str(i + 1) for i in range(NUM_FOLDS)]
COAUTHOR_TUPLES = []
AUTHORS = set()
AUTH_DICT = dict()

# RANDOM_SEED = 214812934
# random.seed(RANDOM_SEED)


def pl_bool(b):
	return str(bool(b)).lower()


def to_evidences(l, truth_val):
	evidences = [f"""evidence(coauthor({a},{b}), {pl_bool(truth_val)}).""" for a, b in l]
	return "\n".join(evidences)


def to_queries(l, label):
	queries = [f"""query(coauthor({a},{b})). % {label}""" for a, b in l]
	return "\n".join(queries)


def make_test_train_files():
	try:
		rmtree(OUTPUT_DIR)
	except OSError:
		pass

	for i in range(NUM_FOLDS):
		path = OUTPUT_FOLDS[i]
		os.makedirs(path)
		test_p, test_n = COAUTHOR_TUPLES[i]
		train_p, train_n = [], []

		for pos, neg in COAUTHOR_TUPLES[:i] + COAUTHOR_TUPLES[i+1:]:
			train_p += pos
			train_n += neg

		with open(pjoin(path, "evidence.pl"), "w") as f:
			f.write(f"""{to_evidences(train_p, True)}\n""")
			f.write(f"""{to_evidences(train_n, False)}\n""")

		with open(pjoin(path, "test_pos.pl"), "w") as f:
			f.write(f"""{to_queries(test_p, 1)}\n""")

		with open(pjoin(path, "test_neg.pl"), "w") as f:
			f.write(f"""{to_queries(test_n, 0)}\n""")

		with open(pjoin(path, "tr_labels.txt"), "w") as f:
			f.writelines(["1\n" for _ in train_p] + ["0\n" for _ in train_n])

		with open(pjoin(path, "te_labels.txt"), "w") as f:
			f.writelines(["1\n" for _ in test_p] + ["0\n" for _ in test_n])



def process_folds():
	global FOLDS, OUTPUT_FOLDS, COAUTHOR_TUPLES, AUTHORS, AUTH_DICT

	try:
		rmtree("data/5folds-processed")
	except OSError:
		pass

	raw_pattern = r"""([\w]+)\("([\w_]+)","([\w_]+)"\)\."""
	re_pattern = re.compile(raw_pattern)

	for in_path in FOLDS:
		neg = []
		with open(pjoin(in_path, "neg.txt"), "r") as f:
			for line in f.readlines():
				line = line.lower()
				if match := re_pattern.match(line):
					rel, a, b = match.groups()
					neg.append((a,b))
					AUTHORS.update((a, b))
		pos = []
		with open(pjoin(in_path, "pos.txt"), "r") as f:
			for line in f.readlines():
				line = line.lower()
				if match := re_pattern.match(line):
					rel, a, b = match.groups()
					pos.append((a, b))
					AUTHORS.update((a, b))

		COAUTHOR_TUPLES.append((pos, neg))


	AUTHORS = list(AUTHORS)

	make_test_train_files()

	with open(pjoin(INPUT_DIR, "train_facts.txt"), "r") as f_in:
		with open(pjoin(OUTPUT_DIR, "facts.pl"), "w") as f_out:
			for line in f_in.readlines():
				line = line.strip().lower().replace('"', "").replace("-", "_")
				line = "".join(x for x in line if ord(x) < 128)
				f_out.write(line + "\n")


def main():
	process_folds()


if __name__ == "__main__":
	main()
