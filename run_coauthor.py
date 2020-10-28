from os.path import join as pjoin
from pprint import pprint

from problog.program import PrologString
from problog import get_evaluatable
from problog.learning import lfi


def get_text(dir_path, file):
	with open(pjoin(dir_path, file)) as f:
		return f.read() + "\n"


def get_model(fold_n):
	path = f"data/5folds-processed/fold{fold_n}"
	model = get_text(".", "coauthor_rules.pl") \
	    + get_text("data/5folds-processed", "facts.pl") \
	    + get_text(path, "evidence.pl")
	return model


def run_fold(fold_i):
	print(f"Running fold {fold_i}")
	fold_n = fold_i + 1

	test = get_text(f"data/5folds-processed/fold{fold_n}", "test.pl")

	model = get_model(fold_n)

	score, weights, atoms, iteration, lfi_problem = lfi.run_lfi(PrologString(model), examples=[])
	learned_model = lfi_problem.get_model()
	with open(pjoin(f"data/5folds-processed/fold{fold_n}", "model.pl"), "w") as f:
		f.write(learned_model + "\n")
	print("model learned, weights:")
	pprint(weights)

	pl_model = PrologString(learned_model + "\n" + test)

	knowledge = get_evaluatable().create_from(pl_model)

	pprint(knowledge.evaluate())
	print()


def main():
	for i in range(5):
		run_fold(i)


if __name__ == '__main__':
	main()
