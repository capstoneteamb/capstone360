from flask import render_template
import logging

def display_access_control_error():
    """
    Returns a rendering of an access control violation error message page. Also logs the event
    Input: self (so nothing really)
    Output: a rendering of the errorMsg.html page with an access control violation message
    """
    logging.warning("Someone, who wasn't a professor, tried to access the professor dashboard")
    return render_template('errorMsg.html', msg="You can't access this page. You aren't a professor")
