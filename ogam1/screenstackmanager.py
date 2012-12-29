from kivy.app import App
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.properties import BooleanProperty, ListProperty
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.widget import WidgetMetaclass

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
		App.instance.pushScreen = self.push
		App.instance.popScreen = self.pop

		self.transition = SlideTransition()

		for screen in self.all_screens:
			screen = screen()
			self.add_widget(screen)
			if screen.default:
				self.current = screen.name
				screen.active = True
				screen.visible = True

	def push(self, new):
		cur = self.get_screen(self.current)
		cur.visible = False
		self.stack.append(self.current)
		self.transition.direction = 'left'
		self.current = new
		new = self.get_screen(self.current)
		new.active = True
		new.visible = True

	def pop(self):
		if not len(self.stack):
			return

		cur = self.get_screen(self.current)
		cur.visible = False
		cur.active = False
		self.transition.direction = 'right'
		self.current = self.stack.pop()
		new = self.get_screen(self.current)
		new.visible = True

class NamedScreen(Screen):
	default = False
	active = BooleanProperty()
	visible = BooleanProperty()

	class __metaclass__(WidgetMetaclass):
		def __init__(cls, name, bases, dict):
			WidgetMetaclass.__init__(cls, name, bases, dict)
			if name != 'NamedScreen':
				ScreenStackManager.add_screen(cls)

	def __init__(self, **kwargs):
		name = self.__class__.__name__
		self.name = name[:-6] if name.endswith('Screen') else name
		setattr(App.instance, name, lambda: App.instance.pushScreen(self.name))
		try:
			Logger.debug('NamedScreen: Loading %s.kv' % name)
			Builder.load_file(name + '.kv', rulesonly=True)
		except IOError:
			Logger.debug('NamedScreen: File %s.kv not found' % name)

		Screen.__init__(self, **kwargs)
