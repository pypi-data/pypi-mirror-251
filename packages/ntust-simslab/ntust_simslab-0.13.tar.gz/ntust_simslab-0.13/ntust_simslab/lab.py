class Lab:
    def __init__(self, professor: str) -> None:
        """_summary_
        
        Parameters
        ----------
        professor : str
            教授姓名
        
        Attributes
        ----------
        lab_students : list
            實驗室學生名單
        """
        self.professor = professor
        self.lab_students = []
    
    def add_student(self, student: str) -> None:
        """_summary_
        
        Parameters
        ----------
        student : str
            學生姓名

        Example
        -------
        >>> from demo import Lab
        >>> lab = Lab("楊龍龍")
        >>> lab.add_student("石剪剪")

        >>> Add 石剪剪 to 楊龍龍's lab.
        """
        self.lab_students.append(student)
        
        print(f"Add {student} to {self.professor}'s lab.")