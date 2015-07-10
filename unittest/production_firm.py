from __future__ import division
import abce
from abce.tools import *
from collections import defaultdict


class ProductionFirm(abce.Agent, abce.Firm):
    def init(self, simulation_parameters, agent_parameters):
        self.last_round = simulation_parameters['num_rounds'] - 1

        if self.idn == 0:
            def mes(goods):
                return max(goods['a'] ** 2, goods['a'] ** 0.5 * goods['b'])
            use = {'a': 1, 'b': 0.1}

            self.set_production_function(mes, 'consumption_good', use)

        elif self.idn == 1:
            self.set_cobb_douglas('consumption_good', 5, {'a': 2, 'b': 1})

        elif self.idn == 2:
            self.leontief = self.set_leontief('consumption_good', {'a': 3, 'b': 1})

        elif self.idn == 3:

            def many_goods_pf(goods):
                output = {'soft_rubber': goods['a'] ** 0.25 * goods['b'] ** 0.5 * goods['c'] ** 0.25,
                                  'hard_rubber': goods['a'] ** 0.1 * goods['b'] ** 0.2 * goods['c'] ** 0.01,
                                  'waste': goods['b'] / 2}
                return output

            use = {'a': 1, 'b': 0.1, 'c': 0}

            self.set_production_function_many_goods(many_goods_pf, use)

        elif self.idn == 4:
            self.set_leontief('car', {'wheels': 4, 'chassi': 1})



    def one(self):
        pass

    def two(self):
        pass

    def three(self):
        pass

    def clean_up(self):
        pass

    def production(self):
        if self.idn == 0:
            self.create('a', 2)
            self.create('b', 2)
            self.produce({'a': 1, 'b': 2})

            assert self.possession('a') == 1, self.possession('a')
            assert self.possession('b') == 1.8, self.possession('b')
            assert self.possession('consumption_good') == 1 ** 0.5 * 2, self.possession('consumption_good')
            self._haves = defaultdict(float)  # resets all possessions to zero

            output = self.predict_produce_output({'a': 10, 'b': 10})
            assert output['consumption_good'] == max(10 ** 2, 10 ** 0.5 * 10)

            input = self.predict_produce_input({'a': 10, 'b': 10})
            assert input['a'] == 10, input['a']
            assert input['b'] == 1, input['b']

            nv = self.net_value(output, input, {'consumption_good': 10, 'a': 1, 'b': 2})
            assert nv == 100 * 10 - (10 * 1 + 1 * 2), nv

        elif self.idn == 1:
            self.create('a', 2)
            self.create('b', 2)
            self.produce({'a': 1, 'b': 2})

            assert self.possession('a') == 1, self.possession('a')
            assert self.possession('b') == 0, self.possession('b')
            assert self.possession('consumption_good') == 5 * 1 ** 2 * 2 ** 1, self.possession('consumption_good')
            self._haves = defaultdict(float)

        elif self.idn == 2:
            self.create('a', 2)
            self.create('b', 2)
            self.produce({'a': 1, 'b': 2})

            assert self.possession('a') == 1, self.possession('a')
            assert self.possession('b') == 0, self.possession('b')
            assert self.possession('consumption_good') == min(1 * 3, 2 * 1), self.possession('consumption_good')
            self._haves = defaultdict(float)

        elif self.idn == 3:
            self.create('a', 10)
            self.create('b', 10)
            self.create('c',10)
            self.produce({'a' : 1, 'b' : 2, 'c': 5})

            assert self.possession('a') == 9, self.possession('a')
            assert self.possession('b') == 9.8, self.possession('b')
            assert self.possession('c') == 10, self.possession('c')
            assert self.possession('soft_rubber') == 1 ** 0.25 * 2 ** 0.5 * 5 **0.25
            assert self.possession('hard_rubber') == 1 ** 0.1 * 2 ** 0.2 * 5 ** 0.01
            assert self.possession('waste') == 2 / 2, self.possession('waste')
            self._haves = defaultdict(float)


        elif self.idn == 4:
            input_goods = {'wheels': 4, 'chassi': 1}
            price_vector = {'wheels': 10, 'chassi': 100, 'car':1000}
            nv = self.predict_net_value(input_goods, price_vector)
            assert  nv == 860

    def all_tests_completed(self):
        if self.round == self.last_round and self.idn == 0:
            print('Test produce:                             \tOK')
            print('Test set_production_function              \tOK')
            print('Test set_production_function_many_goods:  \tOK')
            print('Test leontief:                            \tOK')
            print('Test create_production_function_many_goods\tOK')
            print('Test predict_produce_output               \tOK')
            print('Test predict_produce_input                \tOK')
            print('Test net_value                            \tOK')
            print('Test predict_net_value                    \tOK')



