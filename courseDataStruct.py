"""Course prerequisite data structure.

This module contains the class that should store all of the
data about course prerequisites and track taken courses. Restricting the use
of this class to be one instance per student (otherwise, "taken" doesn't make
sense).

Course: a course and its prerequisites.
"""

class UntakeableError(Exception):
    pass


class PrerequisiteError(Exception):
    pass


class Course:
    """A tree representing a course and its prerequisites.

    This class not only tracks the underlying prerequisite relationships,
    but also can change over time by allowing courses to be "taken".

    Attributes:
    - name (str): the name of the course
    - prereqs (list of Course): a list of the course's prerequisites
    - taken (bool): represents whether the course has been taken or not
    """

    def __init__(self, name, prereqs=None):
        """ (Course, str, list of Courses) -> NoneType

        Create a new course with given name and prerequisites.
        By default, the course has no prerequisites.
        The newly created course is not taken.
        """

        self.name = name
        if prereqs is None:
            self.prereqs = []
        else:
            self.prereqs = prereqs
        self.taken = False

    def is_takeable(self):
        """ (Course) -> bool

        Return True if the user can take this course.
        A course is takeable if and only if all of its prerequisites are taken.
        """
        if self.missing_prereqs() == []:
            return True
        else:
            return False

    def take(self):
        """ (Course) -> NoneType

        If this course is takeable, change self.taken to True.
        Do nothing if self.taken is already True.
        Raise UntakeableError if this course is not takeable.
        """
        if self.is_takeable():
            self.taken = True
        else:
            raise UntakeableError

    def add_prereq(self, prereq):
        """ (Course, Course) -> NoneType

        Add a prereq as a new prerequisite for this course.

        Raise PrerequisiteError if either:
        - prereq has this course in its prerequisite tree, or
        - this course already has prereq in its prerequisite tree
        """
        if prereq.prereqs_in_tree(self):
            raise PrerequisiteError
        if self.prereqs_in_tree(prereq):
            raise PrerequisiteError

        self.prereqs.append(prereq)

    def prereqs_in_tree(self, course):
        """(Course, Course) -> bool
        Helper method. Check if course is present in pre requesites.
        """
        if self.prereqs == []:
            return False
        else:
            if self == course:
                return True
            else:
                # First search course in prereqs, then recurse on them
                for pre_course in self.prereqs:
                    if pre_course == course:
                        return True
                    else:
                        if pre_course.prereqs_in_tree(course):
                            return True
                return False

    def missing_prereqs(self):
        """ (Course) -> list of str

        Return a list of all of the names of the prerequisites of this course
        that are not taken.
        """
        result = []

        # Case where has no prereq
        if self.prereqs == []:
            return result
        else:
            for pre_course in self.prereqs:
                #If a prerequisite is not taken, add to the list
                # and go recursively
                if pre_course.taken is False:
                    result.append(pre_course.name)
                    result += pre_course.missing_prereqs()
            
            # alphabetical order
            result.sort()
            return result
