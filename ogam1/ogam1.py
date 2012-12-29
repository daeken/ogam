from kivy.app import App
from kivy.logger import Logger
from screenstackmanager import NamedScreen

class Ogam1(App):
	pass

class MainScreen(NamedScreen):
	default = True

class FooScreen(NamedScreen):
	pass

if __name__=='__main__':
	App.instance = Ogam1()
	App.instance.run()
