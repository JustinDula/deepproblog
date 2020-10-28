from os.path import join as pjoin
from pprint import pprint
from datetime import datetime
from os import makedirs

from problog.program import PrologString
from problog import get_evaluatable
from problog.learning import lfi


def get_text(dir_path, file):
	with open(pjoin(dir_path, file)) as f:
		return f.read() + "\n"


def get_untrained_model(fold_n):
	path = f"data/5folds-processed/fold{fold_n}"
	model = get_text(".", "coauthor_rules.pl") \
	    + get_text("data/5folds-processed", "facts.pl") \
	    + get_text(path, "evidence.pl")
	return model


def learn_model(fold_i):
	fold_n = fold_i + 1
	print(f"Learning fold {fold_n} @ {datetime.now()}")

	model = get_untrained_model(fold_n)

	score, weights, atoms, iteration, lfi_problem = lfi.run_lfi(PrologString(model), examples=[])
	learned_model = lfi_problem.get_model()
	with open(pjoin("models", f"model{fold_n}.pl"), "w") as f:
		f.write(learned_model + "\n")


def evaluate_model(fold_i):
	print(f"Testing fold {fold_i} @ {datetime.now()}")
	fold_n = fold_i + 1

	test = get_text(f"data/5folds-processed/fold{fold_n}", "test_neg.pl")
	learned_model = get_text("models", f"model{fold_n}.pl")

	pl_model = PrologString(learned_model + "\n" + test)

	knowledge = get_evaluatable().create_from(pl_model)

	pprint(knowledge.evaluate())


def main():
	try:
		makedirs("models/")
	except OSError:
		pass

	for i in range(5):
		learn_model(i)

	for i in range(5):
		evaluate_model(i)


if __name__ == '__main__':
	main()
