class Course:

    def __init__(self, name, duration, link):

        self.name = name
        self.duration = duration
        self.link = link

    def __repr__(self): # Esto es para que puedas hacer un print(courses) en vez de tener que hacer un bucle for.
        
        return f"{self.name} [{self.duration}] ({self.link})"


courses = [
    Course("Introducción a Linux", 15, "https://hack4u.io/cursos/introduccion-a-linux/"),
    Course("Personalización de Linux", 3, "https://hack4u.io/cursos/personalizacion-de-linux/"),
    Course("Introducción al Hacking", 53, "https://hack4u.io/cursos/introduccion-al-hacking/")
]

def list_courses():

    [print(course) for course in courses]

def search_course_by_name(name):

    course = [course for course in courses if course.name == name]
    
    if course:
        return course[0]
    else:
        return None
