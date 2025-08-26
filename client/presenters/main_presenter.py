# #client/presenters/main_presenter.py
# class MainPresenter:
#     """
#     מחלקת  
#     Presenter  
#     שמטפלת במסך הראשי (Main View).  

#     במסך הזה יש כפתור יחיד –  
#     auth_button  

#     כאשר לוחצים עליו, ה־
#     Presenter  
#     מפעיל פונקציה שמועברת מבחוץ,  
#     והתפקיד שלה הוא לנווט אל מסך ההתחברות / הרשמה.
#     """

#     def __init__(self, view, session_manager, go_to_auth):
#         # שמירה של ה־View (כדי לשלוט בכפתורים ולהגיב ללחיצות)
#         self.view = view

#         # שמירה של מנהל הסשן (Session Manager) – כרגע לא בשימוש כאן
#         self.session = session_manager

#         # פונקציה שמוחזרת מבחוץ – 
#         # מחליפה את התצוגה למסך ההתחברות / הרשמה
#         self._go_to_auth = go_to_auth  

#         # חיבור של הכפתור במסך הראשי 
#         # כך שבלחיצה עליו נקפוץ למסך ההתחברות / הרשמה
#         self.view.auth_button.clicked.connect(self._go_to_auth)



# client/presenters/main_presenter.py
class MainPresenter:
    """
    Presenter עבור MainView עם וידאו רקע.
    """
    def __init__(self, view, session_manager, go_to_auth):
        self.view = view
        self.session = session_manager
        self._go_to_auth = go_to_auth

        # חיבור הכפתור LOGIN לפונקציה חיצונית
        self.view.auth_button.clicked.connect(self._go_to_auth)

