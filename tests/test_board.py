"""
Test the Board class.
"""
#!/usr/bin/python
import unittest
from app.Board import Board

class TestBoard(unittest.TestCase):
    """
    Parent class to run unittests.
    """

    def test_init_sizing(self):
        """
        Tests the Board init function sizing.
        """
        width = 45
        height = 45
        bd = Board(width, height)

        self.assertEquals(bd.getSize(), [width, height])

    def test_init_width_too_small(self):
        """
        Tests initilising board that has a width too small.
        """
        width = 1
        height = 20
        with self.assertRaises(ValueError):
            Board(width, height)

    def test_init_height_too_small(self):
        """
        Tests initilising board that has a height too small.
        """
        width = 20
        height = 1
        with self.assertRaises(ValueError):
            Board(width, height)

    def test_init_weighting(self):
        """
        Tests the Board init function initial weighting.
        """
        width = 40
        height = 40
        bd = Board(width, height)
        for y in range(height):
            for x in range(width):
                self.assertEquals(50.0, bd.dictionary[str(y) + ',' + str(x)])

    def test_check_number_int(self):
        """
        Tests checkNumber using an int.
        """
        try:
            Board.checkNumber(5)
        except ValueError:
            self.fail(msg="checkNumber failed to identify an int")

    def test_check_number_float(self):
        """
        Tests checkNumber using an float.
        """
        try:
            Board.checkNumber(5.04)
        except ValueError:
            self.fail(msg="checkNumber failed to identify a float")

    def test_check_number_string(self):
        """
        Tests checkNumber using a string, which should raise an error.
        """
        self.assertRaises(ValueError, Board.checkNumber, "Hello world!")

    def test_check_int_positive(self):
        """
        Tests checkInt using an int.
        """
        try:
            Board.checkInt(5)
        except ValueError:
            self.fail(msg="checkInt failed to identify an int")

    def test_check_int_negative(self):
        """
        Tests checkInt using a float, which should raise an error.
        """
        self.assertRaises(ValueError, Board.checkInt, 5.05)

    def test_check_node_getting_setting(self):
        """
        Tests checkNode for valid nodes.
        """
        height = 30
        width = 30
        bd = Board(width, height)
        for x in range(width):
            for y in range(height):
                try:
                    bd.checkNode([x, y])
                except ValueError:
                    self.fail(msg="Valid node raised ValueError")

    def test_check_node_invalid_bound(self):
        """
        Tests checkNode for out-of-bound nodes.
        """
        height = 30
        width = 30
        bd = Board(width, height)
        self.assertRaises(ValueError, bd.checkNode, [-1, -1])                   # above, left corner
        self.assertRaises(ValueError, bd.checkNode, [-1, width / 2])            # left of
        self.assertRaises(ValueError, bd.checkNode, [height + 1, width / 2])    # directly above
        self.assertRaises(ValueError, bd.checkNode, [height / 2, width + 1])    # right of
        self.assertRaises(ValueError, bd.checkNode, [height + 1, width + 1])    # below
        self.assertRaises(ValueError, bd.checkNode, [height / 2, -1])

    def test_check_node_invalid_format(self):
        """
        Tests checkNode for invalid formats.
        """
        bd = Board(30, 30)
        self.assertRaises(ValueError, bd.checkNode, [1])
        self.assertRaises(ValueError, bd.checkNode, {0:1, 1:2})
        self.assertRaises(ValueError, bd.checkNode, (5, 15))

    def test_set_and_get_node_weight(self):
        """
        Tests setting and getting node weight.
        """
        bd = Board(30, 30)
        coords = [[12, 4], [0, 27], [8, 12], [4, 16], [1, 0], [8, 26], [3, 10], [22, 5], [24, 14], [4, 17], [1, 7], [27, 2], [21, 25], [10, 22], [25, 12]]
        weights = [54, 82, 42, 12, 32, 95, 87, 0, 53, 89, 10, 34, 15, 46, 72]
        for coord, weight in zip(coords, weights):
            bd.setWeight(coord, weight)
            self.assertEquals(bd.getWeight(coord), weight)

    def test_set_weight_too_large(self):
        """
        Tests setting a node's weight to a value over the maximum (100).
        """
        bd = Board(30, 30)
        coord = [0, 5]
        bd.setWeight(coord, 105)
        self.assertEquals(bd.getWeight(coord), 100)

    def test_set_weight_too_small(self):
        """
        Tests setting a node's weight to a value under the minimum (0).
        """
        bd = Board(30, 30)
        coord = [0, 5]
        bd.setWeight(coord, -55)
        self.assertEquals(bd.getWeight(coord), 0)

    def test_set_many_weights(self):
        """
        Tests setting many nodes' weight all at once.
        """
        bd = Board(30, 30)
        coords = [[26, 24], [5, 1], [19, 13]]
        weight = 75
        bd.setWeights(coords, weight)
        for coord in coords:
            if bd.getWeight(coord) != weight:
                self.fail(msg="Weight %2.1f != %2.1f for node [%i, %i]" % \
                (bd.getWeight(coord), weight, coord[0], coord[1]))

    def test_reset_node_weights(self):
        """
        Tests resetting node weights to default value (50.0).
        """
        bd = Board(30, 30)
        weights = [60, 39, 67, 46, 61, 77, 61, 47, 13, 79, 66, 4, 58, 86, 49]
        coords = [[11, 21], [10, 22], [20, 26], [17, 3], [12, 13], [16, 13], [16, 3], [19, 29], [27, 21], [13, 11], [18, 14], [2, 6], [26, 27], [12, 23], [28, 29]]
        for coord, weight in zip(coords, weights):
            bd.setWeight(coord, weight)
        bd.resetWeights()
        for coord in coords:
            failMsg = "%2.1F != %2.1f at %s" % (bd.getWeight(coord), 50.0, coord)
            self.assertEquals(bd.getWeight(coord), 50.0, msg=failMsg)

    def test_multiply_weight(self):
        """
        Tests multiplying node weight.
        """
        fraction = 0.5
        bd = Board(30, 30)
        coords = [[15, 15], [2, 7], [9, 25]]
        for coord in coords:
            bd.multiplyWeight(coord, fraction)
        for coord in coords:
            self.assertEquals(bd.getWeight(coord), 50.0 * fraction)

    def test_divide_weight(self):
        """
        Tests dividing node weight using an even divisor.
        """
        divisor = 4
        bd = Board(30, 30)
        coords = [[29, 3], [16, 22], [6, 2]]
        for coord in coords:
            bd.divideWeight(coord, divisor)
        for coord in coords:
            self.assertAlmostEquals(bd.getWeight(coord), 50.0 / divisor, places=4)

    def test_add_weight(self):
        """
        Tests adding to node weight.
        """
        addend = 35
        bd = Board(30, 30)
        coords = [[23, 9], [15, 15], [6, 19]]
        for coord in coords:
            bd.addWeight(coord, addend)
        for coord in coords:
            self.assertEquals(bd.getWeight(coord), 50.0 + addend)

    def test_subtract_weight(self):
        """
        Tests subtracting from node weight.
        """
        subtrahend = 23
        bd = Board(30, 30)
        coords = [[26, 24], [5, 1], [19, 13]]
        for coord in coords:
            bd.subtractWeight(coord, subtrahend)
        for coord in coords:
            self.assertEquals(bd.getWeight(coord), 50.0 - subtrahend)

    def test_multiply_many_nodes(self):
        """
        Tests multiplying many nodes weights.
        """
        fraction = 0.5
        bd = Board(30, 30)
        coords = [[15, 15], [2, 7], [9, 25]]
        bd.modifyWeights('*', coords, fraction)
        for coord in coords:
            self.assertEquals(bd.getWeight(coord), 50.0 * fraction)

    def test_divide_many_weights(self):
        """
        Tests dividing many nodes weights using an odd divisor.
        """
        divisor = 3
        bd = Board(30, 30)
        coords = [[29, 3], [16, 22], [6, 2]]
        bd.modifyWeights('/', coords, divisor)
        for coord in coords:
            self.assertAlmostEquals(bd.getWeight(coord), 50.0 / divisor, places=4)

    def test_divide_many_weights_cleanly(self):
        """
        Tests dividing many nodes weights using a divisor that cleanly divides the weight.
        i.e. weight % divisor = 0
        """
        divisor = 5
        bd = Board(30, 30)
        coords = [[29, 3], [16, 22], [6, 2]]
        bd.modifyWeights('/', coords, divisor)
        for coord in coords:
            self.assertAlmostEquals(bd.getWeight(coord), 50.0 / divisor, places=4)

    def test_add_many_nodes(self):
        """
        Tests adding to many nodes weights.
        """
        addend = 35
        bd = Board(30, 30)
        coords = [[23, 9], [15, 15], [6, 19]]
        bd.modifyWeights('+', coords, addend)
        for coord in coords:
            self.assertEquals(bd.getWeight(coord), 50.0 + addend)

    def test_subtract_many_nodes(self):
        """
        Tests subtracting from many nodes weights.
        """
        subtrahend = 23
        bd = Board(30, 30)
        coords = [[26, 24], [5, 1], [19, 13]]
        bd.modifyWeights('-', coords, subtrahend)
        for coord in coords:
            self.assertEquals(bd.getWeight(coord), 50.0 - subtrahend)

    def test_modify_weights_invalid_operator(self):
        """
        Tests modifyWeightsErorrCheck with an invalid operator.
        """
        bd = Board(30, 30)
        with self.assertRaises(ValueError):
            bd.modifyWeightsErrorCheck('^')

    def test_get_priority_node(self):
        """
        Tests getting node of highest priority.
        """
        bd = Board(30, 30)
        coords = [[5, 5], [17, 7], [19, 9], [29, 16], [5, 14]]
        weights = [96, 43, 31, 75, 4]
        for coord, weight in zip(coords, weights):
            bd.setWeight(coord, weight)
        priority = coords[weights.index(max(weights))]
        self.assertEquals(bd.getNodeWithPriority(0), priority)

    def test_get_priority_nodes(self):
        """
        Tests getting 5 nodes of highest priority.
        """
        bd = Board(30, 30)
        coords = [[5, 5], [17, 7], [19, 9], [29, 16], [5, 14]]
        weights = [51, 55, 60, 65, 70]
        for coord, weight in zip(coords, weights):
            bd.setWeight(coord, weight)
        # Returns lowest priority first
        self.assertEquals(bd.getNodesWithPriority(0, 4), coords)

    def test_unique_weights_negative(self):
        """
        Tests to confirm negative result with more than 1 of the same weight across all nodes.
        """
        bd = Board(30, 30)
        coords = [[5, 15], [25, 3]]
        weight = 85
        for coord in coords:
            bd.setWeight(coord, weight)
        self.assertEquals(bd.isNodeWeightUnique(coords[0]), False)

    def test_unique_weights_positive(self):
        """
        Tests to confirm positive result when node weight is unique.
        """
        bd = Board(30, 30)
        coord = [5, 15]
        weight = 85
        bd.setWeight(coord, weight)
        self.assertEquals(bd.isNodeWeightUnique(coord), True)

    def test_count_nodes_with_weight(self):
        """
        Tests counting of nodes that have given weight.
        """
        bd = Board(30, 30)
        weight = 65
        coords = [[5, 5], [17, 7], [19, 9], [29, 16], [5, 14]]
        for coord in coords:
            bd.setWeight(coord, weight)
        self.assertEquals(bd.countNodeWeightCopies(coords[0]), len(coords))

    def test_optimum_path_error_check_same_node(self):
        """
        Tests that optimumPathErrorCheck raises an error if `u` and `v` are the same.
        """
        coord = [0, 1]
        bd = Board(30, 30)
        with self.assertRaises(ValueError):
            bd.optimumPathErrorCheck(coord, coord)

    def test_optimum_path_regular(self):
        """
        Tests a board which has no optimal path by length, but does by weight.
        Path is expected to be `coords`.
        """
        bd = Board(5, 5)
        coords = [[0, 1], [0, 0], [1, 0], [2, 0], [3, 0]]
        start = [0, 2]
        end = [4, 0]
        ideal_path = [start] + coords + [end]
        weight = 60
        for coord in coords:
            bd.setWeight(coord, weight)
        bd.setEdges()
        path = bd.optimumPath(start, end)

        # Confirm returned path is same as ideal path from start to end (inclusive)
        self.assertEquals(ideal_path, path)

    def test_optimum_path_long(self):
        """
        Tests a board which has a shortest path that is shorter than the path by optimal weight.
        Path is expected to be `ideal_path`.
        """
        bd = Board(5, 5)
        coords = [[1, 2], [1, 3], [2, 3], [3, 3], [3, 2]]
        start = [0, 2]
        end = [4, 2]
        ideal_path = [start, [1, 2], [2, 2], [3, 2], end]
        weight = 60
        for coord in coords:
            bd.setWeight(coord, weight)
        bd.setEdges()
        path = bd.optimumPath(start, end)

        # Confirm returned path is same as ideal path from start to end (inclusive)
        self.assertEquals(ideal_path, path)

    def test_optimum_path_very_long(self):
        """
        Tests a board which has a path obviously much shorter by length, but not as highly weighted.
        Path is expected to be `ideal_path`.
        """
        bd = Board(5, 5)
        coords = [[0, 1], [0, 2], [0, 3], [0, 4], [1, 4], [2, 4], [2, 3], [2, 2], [2, 1]]
        start = [0, 0]
        end = [2, 0]
        ideal_path = [start, [1, 0], end]
        weight = 60
        for coord in coords:
            bd.setWeight(coord, weight)
        bd.setEdges()
        path = bd.optimumPath(start, end)

        # Confirm returned path is same as ideal path from start to end (inclusive)
        self.assertEquals(ideal_path, path)

    def test_optimum_path_length(self):
        """
        Tests for total weight of optimum path.
        Path is expected to be `ideal_path`.
        """
        bd = Board(5, 5)
        coords = [[1, 2], [1, 3], [2, 3], [3, 3], [3, 2]]
        start = [0, 2]
        end = [4, 2]
        ideal_path = [start, end, [1, 2], [2, 2], [3, 2]]
        weight = 60
        for coord in coords:
            bd.setWeight(coord, weight)
        bd.setEdges()
        path_length = bd.optimumPathLength(start, end)
        # Include only interior points along path - not start or end.
        self.assertEquals(path_length, (len(ideal_path) - 2) * weight)

if __name__ == "__main__":
    unittest.main()
