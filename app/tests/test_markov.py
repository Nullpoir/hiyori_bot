from django.test import TestCase
from app.shared.markov import markov
import os
# Create your tests here.

class test_markov(TestCase):
    def test_markov_generate(self):
        test_markov = markov.Markov()
        print(test_markov.make_sentence())
