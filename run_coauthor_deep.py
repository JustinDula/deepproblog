from train import train_model
from data_loader import load
from model import Model
from optimizer import Optimizer
from network import Network
import torch
import torchvision
import torchvision.transforms as transforms
import torch.nn as nn
from torch.autograd import Variable
import numpy as np
import os


class coauthor_net(nn.Module):
	def __init__(self, N=10):
		super(coauthor_net, self).__init__()
		self.encoder = nn.Sequential(
			nn.Conv2d(1, 6, 5),
			nn.MaxPool2d(2, 2),  # 6 24 24 -> 6 12 12
			nn.ReLU(True),
			nn.Conv2d(6, 16, 5),  # 6 12 12 -> 16 8 8
			nn.MaxPool2d(2, 2),  # 16 8 8 -> 16 4 4
			nn.ReLU(True)
		)
		self.classifier = nn.Sequential(
			nn.Linear(16 * 4 * 4, 120),
			nn.ReLU(),
			nn.Linear(120, 84),
			nn.ReLU(),
			nn.Linear(84, N),
			nn.Softmax(1)
		)

	def forward(self, x):
		x = self.encoder(x)
		x = x.view(-1, 16 * 4 * 4)
		x = self.classifier(x)
		return x


def test_coauthor(model, max_digit=10, name='mnist_net'):
	confusion = np.zeros((max_digit, max_digit), dtype=np.uint32)  # First index actual, second index predicted
	N = 0
	for d, l in mnist_test_data:
		if l < max_digit:
			N += 1
			d = Variable(d.unsqueeze(0))
			outputs = model.networks[name].net.forward(d)
			_, out = torch.max(outputs.data, 1)
			c = int(out.squeeze())
			confusion[l, c] += 1
	print(confusion)
	F1 = 0
	for nr in range(max_digit):
		TP = confusion[nr, nr]
		FP = sum(confusion[:, nr]) - TP
		FN = sum(confusion[nr, :]) - TP
		F1 += 2 * TP / (2 * TP + FP + FN) * (FN + TP) / N
	print('F1: ', F1)
	return [('F1', F1)]


def run_coauthor(fold_i):


	def neural_predicate(network, i, dataset='train'):
		i = int(i)
		dataset = str(dataset)
		if dataset == 'train':
			d, l = mnist_train_data[i]
		elif dataset == 'test':
			d, l = mnist_test_data[i]
		d = Variable(d.unsqueeze(0))
		output = network.net(d)
		return output.squeeze(0)

	queries = load('train_data.txt')

	with open('coauthor_rules.pl') as f:
		problog_string = f.read()

	network = coauthor_net()
	net = Network(network, f'coauthor {i+1}', neural_predicate)
	net.optimizer = torch.optim.Adam(network.parameters(), lr=0.001)
	model = Model(problog_string, [net], caching=False)
	optimizer = Optimizer(model, 2)

	train_model(model, queries, 1, optimizer, test_iter=1000, test=test_coauthor, snapshot_iter=10000)


def main():
	for i in range(5):
		run_coauthor(i)


if __name__ == '__main__':
	main()