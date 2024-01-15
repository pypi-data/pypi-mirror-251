"""
Upload quizes to GradeScope.
"""

import json
import os
import re
import time

import bs4
import requests

import quizgen.converter.gstemplate
import quizgen.latex
import quizgen.variant
import quizgen.util.file

URL_HOMEPAGE = 'https://www.gradescope.com'
URL_LOGIN = 'https://www.gradescope.com/login'
URL_ASSIGNMENTS = 'https://www.gradescope.com/courses/%s/assignments'
URL_ASSIGNMENT = 'https://www.gradescope.com/courses/%s/assignments/%s'
URL_ASSIGNMENT_GROUP = 'https://www.gradescope.com/courses/%s/assignment_containers'
URL_ASSIGNMENT_EDIT = 'https://www.gradescope.com/courses/%s/assignments/%s/edit'
URL_NEW_ASSIGNMENT_FORM = 'https://www.gradescope.com/courses/%s/assignments/new'
URL_EDIT_OUTLINE = 'https://www.gradescope.com/courses/%s/assignments/%s/outline/edit'
URL_PATCH_OUTLINE = 'https://www.gradescope.com/courses/%s/assignments/%s/outline'

NAME_BOX_ID = 'name'
ID_BOX_ID = 'id'
SIGNATURE_BOX_ID = 'signature'
MANUAL_GRADING_BOX_ID = 'manual_grading'

EXTEND_BOX_QUESTION_TYPES = [
    'ma',
    'mcq',
    'mdd',
    'tf',
]

STANDARD_BOX_QUESTION_TYPES = [
    'essay',
    'fimb',
    'matching',
    'numerical',
    'sa',
]

SPECIAL_QUESTION_TYPES = [
    NAME_BOX_ID,
    ID_BOX_ID,
    SIGNATURE_BOX_ID,
    MANUAL_GRADING_BOX_ID,
]

BOX_TYPES = EXTEND_BOX_QUESTION_TYPES + STANDARD_BOX_QUESTION_TYPES + SPECIAL_QUESTION_TYPES

SP_PER_PT = 65536
GRADESCOPE_SLEEP_TIME_SEC = 0.75

class GradeScopeUploader(object):
    def __init__(self, course_id, user, password, force = False, **kwargs):
        super().__init__(**kwargs)

        self.course_id = course_id
        self.user = user
        self.password = password
        self.force = force

    def convert_quiz(self, variant, base_dir = None, **kwargs):
        """
        Compile a quiz and upload it to GradeScope.

        If base_dir is left None, then a temp dir will be created which will be destroyed on exit.
        If supplied, the base_dir will be left alone when finished.
        """

        if (not isinstance(variant, quizgen.variant.Variant)):
            raise ValueError("GradeScope quiz uploader requires a quizgen.variant.Variant type, found %s." % (type(variant)))

        if (base_dir is None):
            base_dir = quizgen.util.file.get_temp_path(prefix = 'quizgen-gradescope-')

        self.write_quiz(variant, base_dir)
        self.compile_tex(variant, base_dir)

        boxes, special_boxes = self.get_bounding_boxes(variant, base_dir)
        return self.upload(variant, base_dir, boxes, special_boxes)

    def write_quiz(self, variant, base_dir):
        converter = quizgen.converter.gstemplate.GradeScopeTemplateConverter()
        tex = converter.convert_quiz(variant)

        path = os.path.join(base_dir, "%s.tex" % (variant.title))
        quizgen.util.file.write(path, tex)

    def create_assignment_group(self, title, gradescope_ids):
        session = requests.Session()

        self.login(session)

        assignments_url = URL_ASSIGNMENTS % (self.course_id)
        csrf_token = self.get_csrf_token(session, assignments_url)

        headers = {
            'x-csrf-token': csrf_token,
        }

        post_url = URL_ASSIGNMENT_GROUP % (self. course_id)
        data = {
            'title': title,
            'assignment_ids[]': gradescope_ids,
        }

        response = session.post(post_url, params = data, headers = headers)
        response.raise_for_status()
        time.sleep(GRADESCOPE_SLEEP_TIME_SEC)

    def compile_tex(self, variant, base_dir):
        path = os.path.join(base_dir, "%s.tex" % (variant.title))

        quizgen.latex.compile(path)

        # Need to compile twice to get positioning.
        quizgen.latex.compile(path)

    def get_bounding_boxes(self, variant, base_dir):
        # {<quetion id>: {<part id>: box, ...}, ...}
        boxes = {}
        # {NAME_BOX_ID: box, ID_BOX_ID: box, SIGNATURE_BOX_ID: box}
        special_boxes = {}

        path = os.path.join(base_dir, "%s.pos" % (variant.title))
        with open(path, 'r') as file:
            for line in file:
                line = line.strip()
                if (line == ""):
                    continue

                parts = [part.strip() for part in line.split(',')]
                if (len(parts) != 12):
                    raise ValueError("Position file has row with bad number of parts. Expecting 11, found %d." % (len(parts)))

                # "ll" == "lower-left"
                # "ur" == "upper-right"
                (question_id, part_id, answer_id, question_type, page_number, ll_x, ll_y, ur_x, ur_y, page_width, page_height, origin) = parts

                if (origin != 'bottom-left'):
                    raise ValueError("Unknown bounding box origin: '%s'." % (origin))

                # Note that the position file and GradeScope use 1-indexed pages.
                page_number = int(page_number)

                if (question_type not in BOX_TYPES):
                    raise ValueError("Unknown content type: '%s'." % (question_type))

                extend_box_right = False
                if (question_type in EXTEND_BOX_QUESTION_TYPES):
                    extend_box_right = True

                (x1, y1), (x2, y2) = self._compute_box(ll_x, ll_y, ur_x, ur_y, page_width, page_height, extend_box_right = extend_box_right)

                if (question_type in SPECIAL_QUESTION_TYPES):
                    # These boxes are special.
                    if (question_type in special_boxes):
                        raise ValueError("Multiple %s bounding boxes found." % (question_type))

                    special_boxes[question_type] = {
                        'page_number': page_number,
                        'x1': x1,
                        'y1': y1,
                        'x2': x2,
                        'y2': y2,
                    }

                    continue

                if (question_id not in boxes):
                    boxes[question_id] = {}

                # If there is an existing box, extend it.
                if (part_id in boxes[question_id]):
                    old_box = boxes[question_id][part_id]

                    old_x1 = old_box['x1']
                    old_y1 = old_box['y1']
                    old_x2 = old_box['x2']
                    old_y2 = old_box['y2']

                    old_page = old_box['page_number']
                    if (old_page != page_number):
                        raise ValueError("Question %s has bounding boxes that span pages." % (question_id))

                    x1 = min(x1, old_x1)
                    y1 = min(y1, old_y1)
                    x2 = max(x2, old_x2)
                    y2 = max(y2, old_y2)

                boxes[question_id][part_id] = {
                    'page_number': page_number,
                    'x1': x1,
                    'y1': y1,
                    'x2': x2,
                    'y2': y2,
                }

        return boxes, special_boxes

    def _compute_box(self, ll_x, ll_y, ur_x, ur_y, page_width, page_height, extend_box_right = False):
        ll_x = float(ll_x.removesuffix('sp'))
        ll_y = float(ll_y.removesuffix('sp'))
        ur_x = float(ur_x.removesuffix('sp'))
        ur_y = float(ur_y.removesuffix('sp'))

        page_width = float(page_width.removesuffix('pt')) * SP_PER_PT
        page_height = float(page_height.removesuffix('pt')) * SP_PER_PT

        # Origin is upper-left, point 1 is upper-left, point 2 is lower-right.
        x1 = round(100.0 * (ll_x / page_width), 1)
        y1 = round(100.0 * (1.0 - (ur_y / page_height)), 1)
        # The lower right x should always extend (at least) to the end of the page (to capture the answers).
        x2 = round(100.0 * (ur_x / page_width), 1)
        y2 = round(100.0 * (1.0 - (ll_y / page_height)), 1)

        if (extend_box_right):
            # In some question types, we want to extend (at least) to the end of the page (to capture the answers).
            x2 = max(95.0, x2)

        return (x1, y1), (x2, y2)

    def create_outline(self, variant, bounding_boxes, special_boxes):
        question_data = []
        for (question_id, parts) in bounding_boxes.items():
            question_index = int(question_id) - 1

            if (len(parts) == 1):
                # Single-part question.
                question_data.append({
                    'title': variant.questions[question_index].base_name,
                    'weight': variant.questions[question_index].points,
                    'crop_rect_list': list(parts.values()),
                })
            else:
                # Multi-part question.
                children = []
                for (part_id, box) in parts.items():
                    children.append({
                        'title': "%s - %s" % (variant.questions[question_index].base_name, part_id),
                        'weight': round(variant.questions[question_index].points / len(parts), 2),
                        'crop_rect_list': [box],
                    })

                question_data.append({
                    'title': variant.questions[question_index].base_name,
                    'weight': variant.questions[question_index].points,
                    # The top-level question just needs one of the bounding boxes.
                    'crop_rect_list': [list(parts.values())[0]],
                    'children': children,
                })

        name_box = None
        id_box = None

        for (question_type, box) in special_boxes.items():
            if (question_type == NAME_BOX_ID):
                name_box = special_boxes[NAME_BOX_ID]
            elif (question_type == ID_BOX_ID):
                id_box = special_boxes[ID_BOX_ID]
            else:
                question_data.append({
                    'title': question_type,
                    'weight': 0,
                    'crop_rect_list': [box],
                })

        outline = {
            'assignment': {
                'identification_regions': {
                    'name': name_box,
                    'sid': id_box
                }
            },
            'question_data': question_data,
        }

        return outline

    def upload(self, variant, base_dir,  bounding_boxes, special_boxes):
        outline = self.create_outline(variant, bounding_boxes, special_boxes)

        session = requests.Session()

        self.login(session)
        print('Logged in.')

        assignment_id = self.get_assignment_id(session, variant)
        if (assignment_id is not None):
            if (not self.force):
                print("Assignment '%s' (%s) already exists. Skipping upload." % (variant.title, assignment_id))
                return

            self.delete_assignment(session, assignment_id)
            print('Deleted assignment: ', assignment_id)

        assignment_id = self.create_assignment(session, variant, base_dir)
        print('Created assignment: ', assignment_id)

        self.submit_outline(session, assignment_id, outline)
        print('Submitted outline.')

        return assignment_id

    def login(self, session):
        token = self.get_authenticity_token(session, URL_HOMEPAGE, action = '/login')

        data = {
            'utf8': '✓',
            'session[email]': self.user,
            'session[password]': self.password,
            'session[remember_me]': 0,
            'commit': 'Log+In',
            'session[remember_me_sso]': 0,
            'authenticity_token': token,
        }

        # Login.
        response = session.post(URL_LOGIN, params = data)
        response.raise_for_status()
        time.sleep(GRADESCOPE_SLEEP_TIME_SEC)

    def get_authenticity_token(self, session, url, action = None):
        response = session.get(url)
        response.raise_for_status()
        time.sleep(GRADESCOPE_SLEEP_TIME_SEC)

        document = bs4.BeautifulSoup(response.text, 'html.parser')

        form_selector = 'form'
        if (action is not None):
            form_selector = 'form[action="%s"]' % (action)

        auth_input = document.select('%s input[name="authenticity_token"]' % (form_selector))
        if (len(auth_input) != 1):
            raise ValueError("Did not find exactly one authentication token input, found %d." % (len(auth_input)))
        auth_input = auth_input[0]

        return auth_input.get('value')

    def get_csrf_token(self, session, url):
        # Get outline submission csrf token.
        response = session.get(url)
        response.raise_for_status()
        time.sleep(GRADESCOPE_SLEEP_TIME_SEC)

        document = bs4.BeautifulSoup(response.text, 'html.parser')

        meta_tag = document.select('meta[name="csrf-token"]')
        if (len(meta_tag) != 1):
            raise ValueError("Did not find exactly one CSRF meta tag, found %d." % (len(meta_tag)))
        meta_tag = meta_tag[0]

        return meta_tag.get('content')

    def get_assignment_id(self, session, variant):
        url = URL_ASSIGNMENTS % (self.course_id)

        response = session.get(url)
        response.raise_for_status()
        time.sleep(GRADESCOPE_SLEEP_TIME_SEC)

        document = bs4.BeautifulSoup(response.text, 'html.parser')

        nodes = document.select('div[data-react-class="AssignmentsTable"]')
        if (len(nodes) != 1):
            raise ValueError("Did not find exactly one assignments table, found %d." % (len(nodes)))

        assignment_data = json.loads(nodes[0].get('data-react-props'))

        for row in assignment_data['table_data']:
            if (row['type'] != 'assignment'):
                continue

            id = row['id'].strip().removeprefix('assignment_')
            name = row['title'].strip()

            if (name == variant.title):
                return id

        return None

    def delete_assignment(self, session, assignment_id):
        form_url = URL_ASSIGNMENT_EDIT % (self.course_id, assignment_id)
        delete_url = URL_ASSIGNMENT % (self.course_id, assignment_id)

        token = self.get_csrf_token(session, form_url)

        data = {
            '_method': 'delete',
            'authenticity_token': token,
        }

        response = session.post(delete_url, data = data)
        response.raise_for_status()
        time.sleep(GRADESCOPE_SLEEP_TIME_SEC)

    def create_assignment(self, session, variant, base_dir):
        form_url = URL_NEW_ASSIGNMENT_FORM % (self.course_id)
        create_url = URL_ASSIGNMENTS % (self.course_id)

        token = self.get_csrf_token(session, form_url)

        data = {
            'authenticity_token': token,
            'assignment[title]': variant.title,
            'assignment[submissions_anonymized]': 0,
            'assignment[student_submission]': "false",
            'assignment[when_to_create_rubric]': 'while_grading',
        }

        path = os.path.join(base_dir, "%s.pdf" % (variant.title))
        files = {
            'template_pdf': (
                os.path.basename(path),
                open(path, 'rb')
            ),
        }

        response = session.post(create_url, data = data, files = files)
        response.raise_for_status()
        time.sleep(GRADESCOPE_SLEEP_TIME_SEC)

        if (len(response.history) == 0):
            raise ValueError("Failed to create assignment. Is the name ('%s') unique?" % (variant.title))

        match = re.search(r'/assignments/(\d+)/outline/edit', response.history[0].text)
        if (match is None):
            print("--- Create Body ---\n%s\n------" % response.history[0].text)
            raise ValueError("Could not parse assignment ID from response body.")

        return match.group(1)

    def submit_outline(self, session, assignment_id, outline):
        edit_url = URL_EDIT_OUTLINE % (self.course_id, assignment_id)
        patch_outline_url = URL_PATCH_OUTLINE % (self.course_id, assignment_id)

        csrf_token = self.get_csrf_token(session, edit_url)

        headers = {
            'Content-Type': 'application/json',
            'x-csrf-token': csrf_token,
        }

        response = session.patch(patch_outline_url,
            data = json.dumps(outline, separators = (',', ':')),
            headers = headers,
        )
        response.raise_for_status()
