class course:

    def __init__(self, name, duration, link):
        self.name = name
        self.duration = duration
        self.link = link

    def __repr__(self):
        return f"[+] Course:\n\t{self.name}\n\tDuration: {self.duration} Hours\n\tLink: {self.link}\n"

courses = [
    course("Introducción a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/"),
    course("Personalización de Linux", 3, "https://hack4u.io/cursos/personalizacion-de-entorno-en-linux/"),
    course("Introducción al Hacking", 53, "https://hack4u.io/cursos/introduccion-al-hacking/")
]

def list_courses():
    for course in courses:
        print(course)

def search_course_by_name(name):
    for course in courses:
        if course.name == name:
            return course

    return None
