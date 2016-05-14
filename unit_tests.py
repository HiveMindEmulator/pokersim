import unittest
import deal
import hand_eval
from deck_constants import suits, values, hands

class Tests(unittest.TestCase):
    def test_generate_deck(self):
        d = deal.generate_deck()
        self.assertEqual(len(d), 52)
        for s in suits:
            for v in values:
                self.assertIn(v+s, d)

    def test_deal(self):
        for num_players in range(2,10):
            d = deal.generate_deck()
            h = deal.deal_preflop(d, num_players)
            self.assertEqual(len(d), 52-2*num_players)
            self.assertEqual(len(h), num_players)
            for hand in h:
                self.assertEqual(len(hand), 2)
            b = deal.deal_flop(d)
            self.assertEqual(len(d), 49-2*num_players)
            self.assertEqual(len(b), 3)
            b = deal.deal_turn(d, b)
            self.assertEqual(len(d), 48-2*num_players)
            self.assertEqual(len(b), 4)
            b = deal.deal_river(d, b)
            self.assertEqual(len(d), 47-2*num_players)
            self.assertEqual(len(b), 5)
            full_list = d + b + [c[0] for c in h] + [c[1] for c in h]
            for s in suits:
                for v in values:
                    self.assertIn(v+s, full_list)

    def test_five_card_value(self):
        tests = [[['AS','KS','QS','JS','TS'],hands.index('STRAIGHT_FLUSH'),['A']],
                 [['9S','KS','QS','JS','TS'],hands.index('STRAIGHT_FLUSH'),['K']],
                 [['AS','2S','3S','4S','5S'],hands.index('STRAIGHT_FLUSH'),['5']],
                 [['5S','Th','Tc','Td','TS'],hands.index('QUADS'),['T','5']],
                 [['8S','Th','Tc','Td','TS'],hands.index('QUADS'),['T','8']],
                 [['8S','8h','8c','8d','TS'],hands.index('QUADS'),['8','T']],
                 [['5S','5h','5c','5d','TS'],hands.index('QUADS'),['5','T']],
                 [['5S','Th','Tc','Td','TS'],hands.index('QUADS'),['T','5']],
                 [['5S','5h','Tc','Td','TS'],hands.index('FULL'),['T','5']],
                 [['5S','5h','5c','Td','TS'],hands.index('FULL'),['5','T']],
                 [['As','6s','3S','JS','5S'],hands.index('FLUSH'),['A','J','6','5','3']],
                 [['AS','6S','3S','4S','5S'],hands.index('FLUSH'),['A','6','5','4','3']],
                 [['3h','6H','8h','4h','5h'],hands.index('FLUSH'),['8','6','5','4','3']],
                 [['AS','Kh','QS','JS','TS'],hands.index('STRAIGHT'),['A']],
                 [['9S','Kh','QS','JS','TS'],hands.index('STRAIGHT'),['K']],
                 [['AS','2h','3S','4S','5S'],hands.index('STRAIGHT'),['5']],
                 [['5S','5h','5c','Ad','TS'],hands.index('TRIPS'),['5','A','T']],
                 [['5S','5h','5c','4d','TS'],hands.index('TRIPS'),['5','T','4']],
                 [['5S','6h','5c','6d','3S'],hands.index('TWO_PAIR'),['6','5','3']],
                 [['2S','6h','2c','6d','3S'],hands.index('TWO_PAIR'),['6','2','3']],
                 [['5S','4h','5c','4d','QS'],hands.index('TWO_PAIR'),['5','4','Q']],
                 [['5S','4h','5c','4d','TS'],hands.index('TWO_PAIR'),['5','4','T']],
                 [['5S','4h','5c','4d','3S'],hands.index('TWO_PAIR'),['5','4','3']],
                 [['2S','6h','Kc','6d','3S'],hands.index('PAIR'),['6','K','3','2']],
                 [['2S','6h','Ac','3d','3S'],hands.index('PAIR'),['3','A','6','2']],
                 [['2S','6h','Kc','3d','3S'],hands.index('PAIR'),['3','K','6','2']],
                 [['2S','6h','4c','3d','3S'],hands.index('PAIR'),['3','6','4','2']],
                 [['8S','Kh','QS','JS','TS'],hands.index('HIGH_CARD'),['K','Q','J','T','8']],
                 [['8S','4h','QS','JS','TS'],hands.index('HIGH_CARD'),['Q','J','T','8','4']]]
        for test in tests:
            res, hc_list = hand_eval.five_card_value(test[0])
            self.assertEqual(res, test[1])
            self.assertEqual(hc_list, test[2])

    def test_is_staight_flush(self):
        trues = [['AS','KS','QS','JS','TS'],
                 ['As','KS','Qs','JS','TS'],
                 ['As','2S','3s','4S','5S'],
                 ['Ts','8S','9s','JS','QS'],
                 ['Ts','KS','9s','JS','QS'],
                 ['Th','8h','9h','Jh','7h'],
                 ['Tc','8c','9c','6C','7C'],
                 ['2d','3d','4D','5d','6D']]
        falses = [['AS','Kh','QS','JS','TS'],
                  ['As','KS','Qs','JS','9S'],
                  ['As','2d','3s','4S','5S'],
                  ['Ts','8S','9s','7S','QS'],
                  ['Ts','KS','8s','JS','QS'],
                  ['Th','6h','9d','Jh','7h'],
                  ['Tc','6c','9h','6C','7C'],
                  ['2d','3d','7D','5d','6D']]
        for hand in trues:
            self.assertTrue(hand_eval.is_straight_flush(hand))
        for hand in falses:
            self.assertFalse(hand_eval.is_straight_flush(hand))

    def test_hand_cmp(self):
        tests = [[['AS','KS','QS','JS','TS'],['AS','KS','QS','JS','TH'],1],
                 [['AS','KS','QS','JS','TC'],['AS','KS','QS','JS','9S'],-1]]
        for test in tests:
            self.assertEqual(hand_eval.hand_cmp(test[0],test[1]),test[2])
            self.assertEqual(hand_eval.hand_cmp(test[1],test[0]),-test[2])

    def test_best_five_holdem(self):
        tests = [[['AS','KS','TS','8S','JS','QH','QS'],['AS','KS','QS','JS','TS']],
                 [['AS','KS','TS','8S','JS','QH','QD'],['AS','KS','8S','JS','TS']],
                 [['as','ks','td','8s','js','qh','qd'],['as','ks','qd','js','td']],
                 [['AS','KS','TD','8S','JS','QH','QD'],['AS','KS','QH','JS','TD']],
                 [['as','ks','kd','kh','4s','3d','th'],['as','ks','kd','kh','th']],
                 [['ah','ad','kd','kh','4s','3d','th'],['ah','ad','kd','kh','th']],
                 [['as','ks','kd','qh','4s','3d','th'],['as','ks','kd','qh','th']],
                 [['ah','ad','kd','qh','4s','3d','th'],['ah','ad','kd','qh','th']]]
        for test in tests:
            self.assertEqual(hand_eval.hand_cmp(hand_eval.best_five_holdem(test[0]), test[1]), 0)

    def test_showdown(self):
        tests = [[['as','ks'],['ah','ad'],['kd','kh','4s','3d','th'],1],
                 [['as','ks'],['ah','ad'],['kd','qh','4s','3d','th'],-1]]
        for test in tests:
            self.assertEqual(hand_eval.showdown(test[0], test[1], test[2]), test[3])
            

if __name__ == '__main__':
    unittest.main()

