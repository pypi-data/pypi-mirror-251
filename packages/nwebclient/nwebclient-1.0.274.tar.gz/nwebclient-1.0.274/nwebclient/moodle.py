
import tarfile
import xml.etree.ElementTree as ET
from nwebclient import base as b

class SkipElement(Exception):
    pass

class MoodleUser:
    id =''
    username =''
    firstname =''
    lastname =''
    def __init__(self, xml):
        # username firstname lastname
        self.id = xml.attrib['id']
        self.username = xml.find('./username').text
        self.firstname = xml.find('./firstname').text
        self.lastname = xml.find('./lastname').text
    def __str__(self):
        return "{0} {1}".format(self.firstname, self.lastname)


class QuestionAttempt:
    def __init__(self, xml, owner, userid = None):
        self.owner = owner
        self.question = None
        # question_attept
        # Actung kann auch part 1: sein
        #  <rightanswer>Teil 1: nicht kohäsiv; Teil 2: kohäsiv; Teil 3: kohäsiv; Teil 4: gering gekoppelt; Teil 5: gering gekoppelt; Teil 6: stark gekoppelt; Teil 7: kohäsiv</rightanswer>
        #   <responsesummary>Teil 1: nicht kohäsiv; Teil 2: kohäsiv;
        self.rightanswer = xml.find('./rightanswer').text
        self.responsesummary = xml.find('./responsesummary').text
        self.questionid = xml.find('./questionid').text
        self.question = self.owner.questionById(self.questionid)
        self.userid = userid
        # nur steps haben userid
        i = 0
        for step in xml.findall('./steps/step'):
            if i == 0:
                self.userid = step.find('./userid').text
            i += 1
            if step.find('./state').text == 'complete':
                pass
                #<response >
                #< variable >
                #< name > answer < / name >
                #< value > 0 < / value >
                #< / variable >
                #< / response >

    def __str__(self):
        return "QuestionId: {0} ResSummary: {1} Right: {2}  UserId: {3}".format(self.questionid, self.responsesummary, self.rightanswer, self.userid)


class MoodleQuiz:
    attempts = []
    questions = []

    def __init__(self, xml, owner):
        self.owner = owner
        self.attempts = []
        # attempts/attempt/question_usage/question_attempts/question_attempt/steps/step
        for x_attempt in xml.findall('.//attempt'):
            userid = x_attempt.find('./userid').text
            for attempt in x_attempt.findall('.//question_attempt'):
                self.attempts.append(QuestionAttempt(attempt, self.owner, userid))
        # question_instances/question_instance/questionid
        for qi in xml.findall('./question_instances/question_instance'):
            self.questions.append(self.owner.questionById(qi.find('./questionid').text))




class MoodleQuestion:
    name: str = ''
    text: str = ''
    id = None

    def __init__(self, xml, owner):
        self.owner = owner
        try:
            self.name = getattr(xml.find('./name'), 'text', None)
            if 'type' in xml.attrib:
                self.type = xml.attrib['type']
            self.text = xml.find('./questiontext').text
            if 'id' in xml.attrib:
                self.id = xml.attrib['id']
            else:
                self.id = None
        # <answers>
        #   <answer id="11785">
        #       <answertext>&lt;p&gt;Antwort 1&lt;/p&gt;</answertext>\n
        #       <answerformat>1</answerformat>
        #       <fraction>1.0000000</fraction>
        except:
            print("Fehler beim Verarbeiten einer Frage.")
            print(ET.tostring(xml))
            raise SkipElement

    def __str__(self):
        return "ID:" + str(self.id) + " " + self.text

    def attempts(self):
        res = []
        for quiz in self.owner.quizes.values():
            if isinstance(quiz, MoodleQuiz):
                for a in quiz.attempts:
                    if a.questionid == self.id:
                        res.append(a)
        return res


class CorectionFreeText:
    def __init__(self, points=1, full=[], point_for=[]):
        self.points = points
        self.full = points
        self.point_for = point_for

    def is_correct(self, answer):
        return answer.lower() in self.full

    def part_points(self, answer):
        res = 0
        a = answer.lower()
        for part in self.points_for.lower():
            if part in a:
                res += 1
        return res

    def check(self, answer):
        if self.is_correct(answer):
            return self.points
        else:
            return self.part_points()


class MoodleCourse(b.WebPage):
    items = []
    users = []
    quizes = {}
    questions = []

    def __init__(self, filename):
        tar = tarfile.open(filename, "r:gz")
        self.items = []
        self.users = []
        self.quizes = {}
        self.questions = []
        for member in tar.getmembers():
            self.items.append(member)
            print(member.name)
            if member.name == 'users.xml':
                self._set_users(tar, member)
            if member.name == 'questions.xml':
                self._set_questions(tar, member)
        for member in tar.getmembers():
            if member.name.startswith('activities/quiz_'):
                self._add_activiy_quiz(tar, member)

    def _add_activiy_quiz(self, tar, member):
        n = member.name.replace('activities/quiz_', '')
        if not '/' in n:
            #self.quizes[n] = {}
            return
        # inforef.xml grade_history.xml module.xml filters.xml calendar.xml comments.xml quiz.xml grades.xml completion.xml roles.xml
        if n.endswith('quiz.xml'):
            f = tar.extractfile(member)
            if f is not None:
                content = f.read()
                root = ET.fromstring(content)
                self.quizes[n] = MoodleQuiz(root, self)
                # print(content)
                # <question_instances>

    #      <question_instance id="57445">\n
    #	  <slot>1</slot>\n
    #	  <page>1</page>\n
    #      <requireprevious>0</requireprevious>\n
    #	  <questionid>5013</questionid>\n
    #	  <questioncategoryid>$@NULL@$</questioncategoryid>\n
    #      <includingsubcategories>$@NULL@$</includingsubcategories>\n
    #      <maxmark>1.0000000</maxmark>\n
    #	  <tags>\n        </tags>\n
    #  </question_instance>\n
    #  </question_instances>
    def _set_questions(self, tar, member):
        f = tar.extractfile(member)
        if f is not None:
            content = f.read()
            # print(content)
            root = ET.fromstring(content)
            for q in root.findall('.//question'):
                try:
                    self.questions.append(MoodleQuestion(q, self))
                except SkipElement:
                    pass
        # TODO map with id

    def _set_users(self, tar, member):
        f = tar.extractfile(member)
        if f is not None:
            content = f.read()
            # print(content)
            # https://towardsdatascience.com/processing-xml-in-python-elementtree-c8992941efd2
            root = ET.fromstring(content)
            for child in root:
                self.users.append(MoodleUser(child))

    def questionById(self, id):
        for q in self.questions:
            if q.id == id:
                return q
        raise Exception("Question not found.")

    def printQuestions(self):
        for q in self.questions:
            print(q)
            print(q.attempts())
            print("###########################")

    def printAttempts(self):
        for q in self.quizes.values():
            for a in q.attempts:
                print(a)

    def page(self, params={}):
        return "Moodle Course"

filename = '/mnt/c/Users/root/Downloads/moodle_quiz-activity-194093-quiz194093-20230809-1410.mbz.tar.gz'
m = MoodleCourse(filename)
m.printQuestions()
m.printAttempts()

# TODO als Webseite ausliefern
