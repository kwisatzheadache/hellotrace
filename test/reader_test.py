import unittest
import utils


class MyTestCase(unittest.TestCase):

    def test_single_query_generation(self):
        # Test integer
        query_tuple = ("name_of_dimension", 33)
        query = utils.make_single_query_filter(query_tuple)
        self.assertEqual(query, '`name_of_dimension` == 33')
        # Test float
        query_tuple = ("name_of_dimension", 33.0)
        query = utils.make_single_query_filter(query_tuple)
        self.assertEqual(query, '`name_of_dimension` == 33.0')
        # test string
        query_tuple = ("name_of_dimension", "fish")
        query = utils.make_single_query_filter(query_tuple)
        self.assertEqual(query, '`name_of_dimension` == \'fish\'')

    def test_multiple_query_generation(self):
        query_tuples = [
            ("dim_1", 33),
            ("dim_2", "a"),
            ("dim_3", 25.0),
            ("dim_4", "b"),
        ]
        query = utils.make_many_query_filter(query_tuples)
        self.assertEqual(query, "`dim_1` == 33 & `dim_2` == \'a\' & `dim_3` == 25.0 & `dim_4` == \'b\'")

    def test_combo_generation_with_validation(self):
        a = [1, 2]
        b = [3, 4]
        c = [5, 6]
        d = [7, 8]
        input_lists = [a, b, c, d]
        combos, indices = utils.generate_combinations_and_indices(input_lists, validate_function=utils.check_valid)
        expected_combos = [(1,), (2,), (3,), (4,), (5,), (6,), (7,), (8,), (1, 4), (2, 3), (2, 4), (1, 5), (1, 6),
                           (2, 5), (2, 6), (1, 7), (1, 8), (2, 7), (2, 8), (3, 5), (3, 6), (4, 5), (4, 6), (3, 7),
                           (3, 8), (4, 7), (4, 8), (5, 7), (5, 8), (6, 7), (6, 8), (1, 4, 5), (1, 4, 6), (2, 3, 5),
                           (2, 3, 6), (2, 4, 5), (2, 4, 6), (1, 4, 7), (1, 4, 8), (2, 3, 7), (2, 3, 8), (2, 4, 7),
                           (2, 4, 8), (1, 5, 7), (1, 5, 8), (1, 6, 7), (1, 6, 8), (2, 5, 7), (2, 5, 8), (2, 6, 7),
                           (2, 6, 8), (3, 5, 7), (3, 5, 8), (3, 6, 7), (3, 6, 8), (4, 5, 7), (4, 5, 8), (4, 6, 7),
                           (4, 6, 8), (1, 4, 5, 7), (1, 4, 5, 8), (1, 4, 6, 7), (1, 4, 6, 8), (2, 3, 5, 7),
                           (2, 3, 5, 8), (2, 3, 6, 7), (2, 3, 6, 8), (2, 4, 5, 7), (2, 4, 5, 8), (2, 4, 6, 7),
                           (2, 4, 6, 8)]
        expected_indices = [(0,), (0,), (1,), (1,), (2,), (2,), (3,), (3,), (0, 1), (0, 1), (0, 1), (0, 2), (0, 2),
                            (0, 2), (0, 2), (0, 3), (0, 3), (0, 3), (0, 3), (1, 2), (1, 2), (1, 2), (1, 2), (1, 3),
                            (1, 3), (1, 3), (1, 3), (2, 3), (2, 3), (2, 3), (2, 3), (0, 1, 2), (0, 1, 2), (0, 1, 2),
                            (0, 1, 2), (0, 1, 2), (0, 1, 2), (0, 1, 3), (0, 1, 3), (0, 1, 3), (0, 1, 3), (0, 1, 3),
                            (0, 1, 3), (0, 2, 3), (0, 2, 3), (0, 2, 3), (0, 2, 3), (0, 2, 3), (0, 2, 3), (0, 2, 3),
                            (0, 2, 3), (1, 2, 3), (1, 2, 3), (1, 2, 3), (1, 2, 3), (1, 2, 3), (1, 2, 3), (1, 2, 3),
                            (1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3),
                            (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3), (0, 1, 2, 3),
                            (0, 1, 2, 3)]
        self.assertEqual(len(combos), len(indices))
        self.assertEqual(combos, expected_combos)
        self.assertEqual(indices, expected_indices)
        for i in range(len(indices)):
            self.assertEqual(len(combos[i]), len(indices[i]))

    def test_check_valid(self):
        sublist = [1, 2, 3, 4, 5]
        indices = [0, 1, 2, 3, 4]
        # This should be false because function looks for 1 and 3 in the sublist
        self.assertFalse(utils.check_valid(sublist, indices))
        sublist = [2, 3, 4, 5]
        indices = [1, 2, 3, 4]
        # This should be false because function looks for 1 and 3 in the sublist
        self.assertTrue(utils.check_valid(sublist, indices))

    def test_build_query_from_subset_list_and_indices(self):
        sublist = [1, 2, 3, 4, 5]
        indices = [0, 1, 2, 3, 4]
        index_map = {0: "a", 1: "b", 2: "c", 3: "d", 4: "e"}
        query = utils.build_query_from_subset_list_indices_and_index_map(sublist, indices, index_map)
        assert query == '`a` == 1 & `b` == 2 & `c` == 3 & `d` == 4 & `e` == 5'


if __name__ == '__main__':
    unittest.main()
