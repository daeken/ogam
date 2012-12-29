from kivy.app import App
from kivy.logger import Logger
import screens

class Ogam1(App):
	pass

if __name__=='__main__':
	App.instance = Ogam1()
	App.instance.run()
