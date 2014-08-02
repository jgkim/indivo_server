"""
Vocabularies Database Router

"""

class VocabularyRouter(object):
	"""
	A router to control all database operations on models in the
	vocabulary application.
	"""
	def db_for_read(self, model, **hints):
		"""
		Attempts to read vocabularies models go to vocabularies.
		"""
		if model._meta.app_label == 'vocabularies':
			return 'vocabularies'
		return None

	def db_for_write(self, model, **hints):
		"""
		Attempts to write vocabularies models go to vocabularies.
		"""
		if model._meta.app_label == 'vocabularies':
			return 'vocabularies'
		return None

	def allow_relation(self, obj1, obj2, **hints):
		"""
		Allow relations if two models in the vocabularies application are involved.
		"""
		if (obj1._meta.app_label == 'vocabularies') and (obj2._meta.app_label == 'vocabularies'):
			return True
		elif (obj1._meta.app_label == 'vocabularies') != (obj2._meta.app_label == 'vocabularies'):
		   return False
		return None

	def allow_syncdb(self, db, model):
		"""
		Make sure the vocabularies application only appears in the 'vocabularies' database.
		"""
		if db == 'vocabularies':
			return model._meta.app_label == 'vocabularies'
		elif model._meta.app_label == 'vocabularies':
			return False
		return None