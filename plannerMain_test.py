""" Unit tests for plannerMain.py """

import unittest
from plannerMain import TermPlanner, parse_course_data
from courseDataStruct import Course


class TestParser(unittest.TestCase):

    def test_binary_simple(self):
        filename = 'test2.txt'

        actual = parse_course_data(filename)
        self.assertEqual('CSC201', actual.name)

        prereqs = actual.prereqs
        prereq_names = [p.name for p in prereqs]
        # User assertCountEqual when order doesn't matter
        self.assertCountEqual(['CSC102', 'CSC151'], prereq_names)

        for p in prereqs:
            self.assertEqual([], p.prereqs)


    def test_mytest(self):
        filename = 'test4.txt'

        top = parse_course_data(filename)
        self.assertEqual('CSC201', top.name)

        self.planner = TermPlanner(filename)

        self.assertTrue(self.planner.is_valid([['CSC101', 'MAT101', 'SOC101',
                                               'CHM101', 'CSC102'],
                                              ['CSC151', 'MAT151'],
                                              ['CSC201']]))


class TestIsValid(unittest.TestCase):
    def setUp(self):

        # Single prereq
        self.single = TermPlanner('test1.txt')
        
        # multiple prereq
        self.multi = TermPlanner('test5.txt')

    def test_single_two(self):
        self.assertTrue(self.single.is_valid([['CSC101'], ['CSC151']]))

    def test_single_two_wrong(self):
        self.assertFalse(self.single.is_valid([['CSC151'], ['CSC101']]))
        
    def test_multi_correct(self):
        self.assertTrue(self.multi.is_valid([['UT100'], ['UT101'],
                                             ['UT199'], ['UT200'],
                                             ['UT250'], ['UT300'],
                                             ['UT400']]))
        
    def test_multi_one_incorrect(self):
        # Note UT199 is switched with UT200, 199 is prereq of 200
        self.assertFalse(self.multi.is_valid([['UT100'], ['UT101'],
                                              ['UT200'], ['UT199'],
                                              ['UT250'], ['UT300'],
                                              ['UT400']]))


class TestPlanner(unittest.TestCase):
    def setUp(self):
        # Single prereq
        self.single = TermPlanner('test1.txt')

    def gen_test(self, tp, courses):
        s = tp.generate_schedule(courses)

    def test_one_prereq(self):
        self.gen_test(self.single, ['CSC101', 'CSC151'])


class TestTermPlanner(unittest.TestCase):
    # This is basically the combination of is_valid test and
    #     generate_schedule test
    # The order of prerequisites/courses does not matter, but prerequisites
    #     must be taken before the course wanted
    
    def setUp(self):
        self.first = TermPlanner('test2.txt')
        self.second = TermPlanner('test5.txt')
        self.third = TermPlanner('test4.txt')
        # forth has 6 first-level courses, test to make sure each term can
        # only have 5 courses, the sixth course will be move to next term
        self.forth = TermPlanner('test3.txt')        
        
    def test_first_empty(self):
        self.assertEqual([], self.first.generate_schedule([]))
        self.assertTrue(self.first.is_valid(self.first.generate_schedule([])))
        
    def test_first_of_one_term(self):
        # CSC201 is not generated because it's a next level course
        self.assertEqual([['CSC102', 'CSC151']],
                         self.first.generate_schedule(['CSC151']))
        self.assertTrue(self.first.is_valid(
            self.first.generate_schedule(['CSC151'])))
    
    def test_first_of_all_courses_in_first(self):
        self.assertEqual([['CSC102', 'CSC151'], ['CSC201']],
                         self.first.generate_schedule(['CSC201']))
        self.assertTrue(self.first.is_valid(
            self.first.generate_schedule(['CSC201'])))
        
    def test_second_empty(self):
        self.assertEqual([], self.second.generate_schedule([]))
        self.assertTrue(self.second.is_valid(self.second.generate_schedule([])))
        
    def test_second_of_one_term(self):
        self.assertEqual([['UT250', 'UT199', 'UT101', 'UT100']],
                         self.second.generate_schedule(['UT199']))
        self.assertTrue(self.second.is_valid(
            self.second.generate_schedule(['UT199'])))
        
        
    def test_second_of_two_term(self):
        self.assertEqual([['UT100', 'UT101', 'UT199', 'UT250'], ['UT200']],
                         self.second.generate_schedule(['UT200']))
        self.assertTrue(self.second.is_valid(
            self.second.generate_schedule(['UT200'])))
        
    def test_second_of_all_courses_in_second(self):
        self.assertEqual([['UT100', 'UT101', 'UT199', 'UT250'],
                                             ['UT200'], ['UT300'],
                                             ['UT400']],
                                             self.second.generate_schedule(['UT400']))
        
    def test_third_of_two_term(self):
        # Try generate_schedule with len(selected_courses > 1)
        self.assertEqual([['CHM101', 'MAT101', 'SOC101', 'CSC102', 'CSC101'],
                          ['MAT151', 'CSC151']],
                         self.third.generate_schedule(['CSC101','MAT151']))
        self.assertTrue(self.third.is_valid(
            self.third.generate_schedule(['CSC101', 'MAT151'])))
    
    def test_forth(self):
        self.assertEqual([['BIO101', 'CHM101', 'MAT101','SOC101', 'CSC102'],
                          ['MAT151', 'CSC101']],
                         self.forth.generate_schedule(['MAT151']))
        self.assertTrue(self.third.is_valid(
                    self.third.generate_schedule(['MAT151'])))        
        


if __name__ == '__main__':
    unittest.main(exit=False)
