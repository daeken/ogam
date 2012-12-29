from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import ListProperty, StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.widget import WidgetMetaclass

class Ogam1(App):
	pass

class ScreenStackManager(ScreenManager):
	stack = ListProperty()
	all_screens = []
	default_screen = None

	@classmethod
	def add_screen(cls, screen):
		cls.all_screens.append(screen)
		if screen.default:
			default_screen = screen

	def __init__(self, **kwargs):
		ScreenManager.__init__(self, **kwargs)
		instance.push = self.push
		instance.pop = self.pop

		for screen in self.all_screens:
			screen = screen()
			self.add_widget(screen)
			if screen.default:
				self.current = screen.name

	def push(self, new):
		self.stack.append(self.current)
		self.transition = SlideTransition(direction='left')
		self.current = new

	def pop(self):
		if not len(self.stack):
			return

		self.transition = SlideTransition(direction='right')
		self.current = self.stack.pop()

class NamedScreen(Screen):
	default = False

	class __metaclass__(WidgetMetaclass):
		def __init__(cls, name, bases, dict):
			WidgetMetaclass.__init__(cls, name, bases, dict)
			if name != 'NamedScreen':
				ScreenStackManager.add_screen(cls)

	def __init__(self, **kwargs):
		name = self.__class__.__name__
		self.name = name[:-6] if name.endswith('Screen') else name
		setattr(instance, name, lambda: instance.push(self.name))
		try:
			Logger.debug('NamedScreen: Loading %s.kv' % name)
			Builder.load_file(name + '.kv', rulesonly=True)
		except IOError:
			Logger.debug('NamedScreen: File %s.kv not found' % name)

		Screen.__init__(self, **kwargs)

class MainScreen(NamedScreen):
	default = True

class FooScreen(NamedScreen):
	pass

if __name__=='__main__':
	instance = Ogam1()
	instance.run()
