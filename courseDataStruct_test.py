""" Unit tests for courseDataStruct.py """

import unittest
from courseDataStruct import Course, UntakeableError, PrerequisiteError


class TestCourseInit(unittest.TestCase):
    def test_init_with_prereq(self):
        prereq1 = Course('CSC101')
        prereq2 = Course('CSC102')
        course = Course('CSC151', [prereq1, prereq2])
        self.assertEqual('CSC151', course.name)
        self.assertFalse(course.taken)
        self.assertEqual(course.prereqs, [prereq1, prereq2])

    def test_init_with_no_prereq(self):
        course = Course('CSC101')
        self.assertEqual('CSC101', course.name)
        self.assertFalse(course.taken)
        self.assertEqual(course.prereqs, [])


class TestCourseIsTakeable(unittest.TestCase):
    def setUp(self):
        self.c1 = Course('CSC101')
        self.c2 = Course('CSC151', [self.c1])
        self.c3 = Course('CSC102')
        self.c7 = Course('CSC180')
        self.c4 = Course('CSC201', [self.c1, self.c2, self.c7])
        self.c5 = Course('CSC202', [self.c2, self.c3])
        self.c6 = Course('CSC251', [self.c4])

    def test_takeable_one_prereq_satisfied(self):
        self.c1.taken = True
        self.assertTrue(self.c2.is_takeable())

    def test_takeable_more_than_one_prereq_satisfied(self):
        self.c1.taken = True
        self.c7.taken = True
        # self.c2 not taken
        self.assertFalse(self.c4.is_takeable())

    def test_takeable_all_prereq_satisfied(self):
        self.c1.taken = True
        self.c2.taken = True
        self.c7.taken = True
        self.assertTrue(self.c4.is_takeable())

    def test_takeable_one_prereq_not_satisfied(self):
        self.c2.taken = True
        # self.c3 not taken
        self.assertFalse(self.c5.is_takeable())

    def test_takeable_more_than_one_prereq_not_satisfied(self):
        self.c7.taken = True
        # self.c1 and self.c2 not taken
        self.assertFalse(self.c4.is_takeable())

    def test_takeable_none_prereq_satisfied(self):
        self.assertFalse(self.c5.is_takeable())

    def test_taken_courses_are_takeable(self):
        self.c3.taken = True
        self.assertTrue(self.c3.is_takeable())


class TestCourseTake(unittest.TestCase):

    def setUp(self):
        self.c1 = Course('CSC101')
        self.c2 = Course('CSC151', [self.c1])
        self.c3 = Course('CSC102')
        self.c7 = Course('CSC180')
        self.c4 = Course('CSC201', [self.c1, self.c2, self.c7])
        self.c5 = Course('CSC202', [self.c2, self.c3])
        self.c6 = Course('CSC251', [self.c4])

    def test_take_one_prereq_satisfied(self):
        self.c1.taken = True
        self.assertFalse(self.c2.taken)
        self.c2.take()
        self.assertTrue(self.c2.taken)

    def test_take_all_prereq_satisfied(self):
        self.c1.taken = True
        self.c2.taken = True
        self.c7.taken = True
        self.c4.taken = True
        self.c6.take()
        self.assertTrue(self.c6.taken)

    def test_take_one_prereq_not_satisfied(self):
        self.c1.taken = True
        self.c2.taken = True
        self.c7.taken = True
        self.assertFalse(self.c3.taken)
        self.c4.take()
        self.assertTrue(self.c4.taken)
        # self.c3 is not taken in this case
        self.assertRaises(UntakeableError, self.c5.take)

    def test_take_more_than_one_prereq_not_satisfied(self):
        self.c1.taken = True
        # self.c2 and self.c7 are not taken in this case
        self.assertRaises(UntakeableError, self.c4.take)

    def test_take_all_prereq_not_satisfied(self):
        self.assertRaises(UntakeableError, self.c4.take)

    def test_taken_courses_can_be_retake(self):
        self.c3.taken = True
        self.c3.take()
        self.assertTrue(self.c3.taken)


class TestCourseAddPrereq(unittest.TestCase):

    def setUp(self):
        self.c1 = Course('PSY101')
        self.c2 = Course('PSY201')
        self.c3 = Course('BCH101')
        self.c4 = Course('PSY201', [self.c1])
        self.c5 = Course('PSY251', [self.c4])
        self.c6 = Course('PSY202', [self.c5, self.c4])

    def test_add_one_prereq_to_no_prereqs(self):
        prereq = Course('MAT223')
        self.c3.add_prereq(prereq)
        self.assertEqual([prereq], self.c3.prereqs)

    def test_add_more_than_one_prereq_to_no_prereqs(self):
        prereq1 = Course('Calc')
        prereq2 = Course('Trig')
        prereq3 = Course('Alg')
        prereq4 = Course('Matrices')
        self.c3.add_prereq(prereq1)
        self.c3.add_prereq(prereq2)
        self.c3.add_prereq(prereq3)
        self.c3.add_prereq(prereq4)
        self.assertEqual([prereq1, prereq2, prereq3, prereq4],
                         self.c3.prereqs)

    def test_add_one_prereq_to_prereqs(self):
        self.c4.add_prereq(self.c2)
        self.assertEqual([self.c1, self.c2], self.c4.prereqs)

    def test_add_more_than_one_prereq_to_prereqs(self):
        prereq1 = Course('STA101')
        prereq2 = Course('STA201')
        prereq3 = Course('SOC101')
        self.c6.add_prereq(prereq1)
        self.c6.add_prereq(prereq2)
        self.c6.add_prereq(prereq3)
        self.assertEqual([self.c5, self.c4, prereq1, prereq2, prereq3],
                         self.c6.prereqs)

    def test_add_existing_prereq_to_prereqs(self):
        # self.c4 is already an existing prereq for self.c6
        with self.assertRaises(PrerequisiteError):
            self.c6.add_prereq(self.c4)


class TestCourseMissingPrereqs(unittest.TestCase):

    def setUp(self):
        self.c1 = Course('CSC101')
        self.c2 = Course('CSC151', [self.c1])
        self.c3 = Course('BIO101')
        self.c4 = Course('CHM101')
        self.c5 = Course('CHM201', [self.c4])
        self.c6 = Course('CHM301', [self.c3, self.c5])

    def test_missing_prereqs_one_missing(self):
        self.assertEqual(['CSC101'], self.c2.missing_prereqs())

    def test_missing_prereqs_more_than_one_missing(self):
        self.c3.take()
        # self.c4 and self.c5 are not taken
        self.assertEqual(['CHM101', 'CHM201'], self.c6.missing_prereqs())

    def test_missing_prereqs_all_missing(self):
        self.assertEqual(['BIO101', 'CHM101', 'CHM201'],
                         self.c6.missing_prereqs())

    def test_missing_prereqs_none_missing(self):
        self.c4.take()
        self.assertEqual([], self.c5.missing_prereqs())

    def test_missing_prereqs_without_existing_prereq(self):
        # self.c1 has no prereq
        self.assertEqual([], self.c1.missing_prereqs())


if __name__ == '__main__':
    unittest.main(exit=False)
