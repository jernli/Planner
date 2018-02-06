"""Program for helping users plan schedules.

This module contains the main class that is used to interact with users
who are trying to plan their schedules. It requires the course module
to store prerequisite information.
"""

from courseDataStruct import Course


class NoCourseFound(Exception):
    pass


def parse_course_data(filename):
    """ (str) -> Course

    Read in prerequisite data from the file called filename,
    create the Course data structures for the data,
    and then return the root (top-most) course.
    """
    all_courses = []
    top_course = None

    with open(filename, 'r') as my_file:
        for line in my_file:
            one_line = line.split()
            add_courses(one_line[0], one_line[1], all_courses)

            course_1 = parse_get_course(one_line[0], all_courses)
            course_2 = parse_get_course(one_line[1], all_courses)

            course_2.add_prereq(course_1)

            if top_course is None:
                top_course = course_2
            # If the top course becomes a prerequisite, the course on the
            # top will become the new top
            elif course_1 == top_course:
                top_course = course_2

    return top_course

def add_courses(course_1_name, course_2_name, all_courses):
    """ (str, str, list of Course) -> Nonetype

    Add course_1_name and course_2_name to all_courses if they do not
    exist in all_courses.
    """
    course_1 = None
    course_2 = None

    # Check if the courses has been created before
    for course in all_courses:
        if course.name == course_1_name:
            course_1 = course
    for course in all_courses:
        if course.name == course_2_name:
            course_2 = course

    # If any course was not created, then create and add to the list
    if course_1 is None:
        course_1 = Course(course_1_name)
        all_courses.append(course_1)
    if course_2 is None:
        course_2 = Course(course_2_name)
        all_courses.append(course_2)


def parse_get_course(course_name, all_courses):
    """ (str, list) -> Course

    Return an object Course that has the same name as course_name
    from all_courses.
    """
    for each_course in all_courses:
        if course_name == each_course.name:
            return each_course

""" TermPlanner: answers queries about schedules based on prerequisite tree."""
class TermPlanner:
    """Tool for planning course enrolment over multiple terms.

    Attributes:
    - course (Course): tree containing all available courses
    """

    def __init__(self, filename):
        """ (TermPlanner, str) -> NoneType

        Create a new term planning tool based on the data in the file
        named filename.
        """
        self.course = parse_course_data(filename)

    def is_valid(self, schedule):
        """ (TermPlanner, list of (list of str)) -> bool

        Return True if schedule is a valid schedule.
        """
        for term in schedule:
            for each_course in term:
                # a string is given => find the course itself
                one_course = self.get_course(each_course)

                if one_course.is_takeable() and one_course.taken is False:
                    one_course.take()
                else:
                    # if any course at a specific term is not takeable,
                    # then the schedule is not valid
                    return False

        return True

    def generate_schedule(self, selected_courses):
        """ (TermPlanner, list of str) -> list of (list of str)

        Return a schedule containing the courses in selected_courses.
        """
        schedule = []
        must_courses = self.direct_prerequisites(selected_courses)

        while self.is_schedule_done(selected_courses, schedule) is False:
            # All takeable courses at the tree
            takeable = self.all_takeable(self.course)
            # All courses that must be taken to reach the selected courses
            # among all courses that are available to be taken
            must_list = self.must_takeable(takeable, must_courses)
            # Fill term deals with the number by term
            final_term = self.fill_term(must_list)
            # Take all the courses at this generated term
            self.take_term(final_term)
            # Add the term with all courses already taken at schedule
            schedule.append(final_term)

        for terms in schedule:
            for course in terms:
                resetcourse = self.get_course(course)
                resetcourse.taken = False
        return schedule

    def all_takeable(self, course):
        """ (TermPlanner, Course) -> list of str

        Return a list containing all Course course that are actually
        takeable and has not been taken.
        """
        takeable_list = []

        if course.is_takeable() and course.taken is False:
            takeable_list.append(course.name)
        else:
            for each_prereq in course.prereqs:
                takeable_list += self.all_takeable(each_prereq)

        return takeable_list

    def must_takeable(self, takeable_courses, must_courses):
        """ (TermPlanner, list of str, list of str) -> list of str

        Return a list containing all courses that must be taken
        in must_courses and are takeable in takeable_courses.
        """
        must_list = []

        for each_must in must_courses:
            for each_takeable in takeable_courses:
                if each_must is each_takeable:
                    must_list.append(each_must)

        # Filter duplicates
        filtered = []
        for each in must_list:
            if each not in filtered:
                filtered.append(each)

        return filtered

    def direct_prerequisites(self, selected_courses):
        """ (TermPlanner, list of str) -> list of str

        Return a list of courses that are directly prerequisites from the
        selected_courses, plus the course itself, given by the user.
        """
        all_must_prereqs = []
        for each_course in selected_courses:
            course = self.get_course(each_course)
            all_must_prereqs += course.name
            all_must_prereqs += course.missing_prereqs()

        return all_must_prereqs

    def fill_term(self, must_term_courses):
        """ (TermPlanner, list of str) -> list of str

        Check the greedy behaviour of term must_term_courses received,
        if the list has less than five courses, add more available
        courses and return a list of courses, if the list has
        more than 5 courses, select 5.
        """
        # If more than five elements, send just five
        if len(must_term_courses) > 5:
            term_list = must_term_courses[:5]
        # If less than five elements, fill up with more
        elif len(must_term_courses) < 5:
            term_list = must_term_courses[:]
            takeable_courses = self.all_takeable(self.course)
            # Add courses from the takeable pool of courses to satisfy
            # the greed behaviour.
            while len(term_list) < 5 and len(takeable_courses) is not 0:
                add_course = takeable_courses.pop()
                if add_course not in term_list:
                    term_list.append(add_course)
        # The term has 5 elements
        else:
            term_list = must_term_courses[:]

        return term_list

    def take_term(self, term_list):
        """ (TermPlanner, list of str) -> NoneType

        Take all courses at term_list.
        """
        for each_course in term_list:
            course = self.get_course(each_course)
            course.take()

    def is_schedule_done(self, selected_courses, schedule):
        """ (TermPlanner, list of str, list of str) -> bool

        Return True if all selected_courses given by the user is already
        in the schedule provided.
        """
        # Check if each course given by the user is inside the schedule
        for each_selected in selected_courses:
            not_found = True
            for term in schedule:
                for each_course in term:
                    if each_selected == each_course:
                        not_found = False
            # if any course given is not in schedule, return false.
            if not_found is True:
                return False
        # After all given courses checked, return true.
        return True

    def get_course(self, course_name):
        """ (TermPlanner, str) -> Course

        Return an object Course that has the same name as course_name.
        """
        return self.get_course_helper(course_name, self.course)[0]

    def get_course_helper(self, course_name, course):
        """ (TermPlanner, str, Course) -> list of Course

        Return Course course with course_name.
        """
        one_course = []
        if course.name == course_name:
            one_course.append(course)
            return one_course
        else:
            for each_prereq in course.prereqs:
                one_course += self.get_course_helper(course_name, each_prereq)
        return one_course
