# Contributing

## Implementing more Kivy widgets
Creating new widgets (implementing more of Kivy+KV) is possible simply
by adding the py file equivalent to the kivy py file (same directory
structure as Kivy) and then importing the class from
`kivy-tkinter/kivy/app.py`. The app.py in kivy-tkinter uses eval to
create the widgets from the KV language, so probably no other steps are
required.
