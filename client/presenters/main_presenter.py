# client/presenters/main_presenter.py

"""
    מחלקה שמגדירה את ה־
    Presenter  
    עבור המסך הראשי – 
    MainView.
    התפקיד של ה־
    Presenter  
    הוא לתווך בין הממשק הגרפי  
    (View)  
    לבין הלוגיקה של הניווט וההתנהגות.
    """
class MainPresenter:
  
    def __init__(self, view, session_manager, go_to_auth):
        self.view = view
        self.session = session_manager

        # פונקציית מעבר למסך התחברות/הרשמה –
        # go_to_auth  
        # נשמרת לשימוש כאשר לוחצים על הכפתור
        self._go_to_auth = go_to_auth

        # חיבור הכפתור 
        # Login
        # מה־
        # View  
        # לפונקציה החיצונית –
        # go_to_auth
        self.view.auth_button.clicked.connect(self._go_to_auth)

