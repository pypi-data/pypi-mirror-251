class NTUST:
    def __init__(self, department: str, professor: str, lab: str) -> None:
        """_summary_
        
        Parameters
        ----------
        department : str
            系所名稱
        professor : str
            教授姓名
        lab : str
            實驗室名稱

        Example
        -------
        >>> from demo import NTUST
        >>> ntust = NTUST("工業管理系", "楊龍龍", "SiMS Lab")
        """
        self.department = department
        self.professor = professor
        self.lab = lab
    
    def return_info(self) -> str:
        """_summary_    
        Returns
        -------
        str
            回傳系所資訊

        Example
        -------
        >>> from demo import NTUST
        >>> ntust = NTUST("工業管理系", "楊龍龍", "SiMS Lab")
        >>> ntust.return_info()

        >>> Department: 工業管理系
        >>> Professor: 楊龍龍
        >>> Lab: SiMS Lab
        """
        return f"Department: {self.department}\nProfessor: {self.professor}\nLab: {self.lab}"