readme.txt

WESmith 01/11/22

The code in this area was copied from an excellent article by Alan Davies
demonstrating the use of ajax to communicate data to/from the server
without a page reload:

https://towardsdatascience.com/using-python-flask-and-ajax-to-pass-information-between-the-client-and-server-90670c64d688

I need ajax to communicate user-defined inputs (via buttons, dialog boxes)
to the opencv camera object without having to refresh the streaming-video page.


01/14/22 update
- successful implementation of flask-ajax in implementing buttons and
  a form field
- button then implemented in main app.py to control camera options:
  invert, blur, flip, grayscale
