#region Import Packages

from flask import Flask

#endregion

#region FlaskStart Class

class FlaskStart():

    # region Global Variables

    app = None

    __name__ = None

    # endregion

    # region Init
    
    def __init__(self,app,__name__): 
        self.app = app
        self.__name__ = __name__
    
    # endregion
        
    # region Start

    def start(self):
        if self.__name__ == "__main__":
            self.app.run(host='0.0.0.0', port=6001, use_reloader=True)
        
    # endregion
        
#endregion