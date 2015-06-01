import server.mod_auth.models as models

class Puhjee:
	"""
	base class for all savable objects
	"""
	
	def __init__(self, **kwargs):
		self.load(**kwargs)
		self.result = None # for query results
	
	def model(self):
		"""
		Fetch this object's corresponding model
		:return: model.class
		"""
		return Puhjee._model(self.__class__)
	
	@staticmethod
	def _model(cls):
		"""
		Fetch this class's corresponding model
		* raises an error if the model is not found
		:param cls: classname
		:return: model.class
		"""
		return getattr(models, cls.__name__)
	
	def get(self):
		"""
		Query the database with this object's data
		:return: object loaded with data
		"""
		self.result = self.__class__._get(**self.data())
		data = Puhjee._data(self, self.result)
		return self.__class__(**data)
	
	@classmethod
	def _get(cls, **kwargs):
		"""
		Query database with passed-in data
		:param kwargs: filter
		:return: query results or None
		"""
		try:
			return Puhjee._model(cls).objects(**kwargs).get()
		except:
			return None
	
	def save(self):
		"""
		Save object with it's data to database
		:return: self
		"""
		mod = self.model()
		self.result = mod(**self.data()).save()
		data = Puhjee._data(self, self.result)
		return self.load(**data)
		
	def load(self, **kwargs):
		"""
		Save all passed-in data to object
		:param kwargs: data
		:return: self
		"""
		for k, v in kwargs.items():
			setattr(self, k, v)
		return self	
		
	def data(self):
		"""
		Returns all data associated with object
		:return: data for specified fields, or all data
		"""
		return Puhjee._data(self, self)
	
	@staticmethod
	def _data(self, obj):
		return {f: getattr(obj, f) for f in self.fields() if hasattr(obj, f)}
		
	def fields(self):
		"""
		Fetches all fields based on this object's model
		:return: list of fields
		"""
		return Puhjee._fields(self.model())
	
	@staticmethod
	def _fields(model):
		"""
		Fetches all fields for a model
		:param model: model
		:return: list of fields
		"""
		return [k for k, v in model._fields.items() if not isinstance(k, int)]
		
	def __str__(self):
		"""
		Pretty string representation
		:return: string
		"""
		return '{class_}({data})'.format(
			class_=self.__class__.__name__,
			data=','.join([k+'='+str(v) for k, v in self.data().items()])
		)
	
	def exists(self):
		return hasattr(self, 'id')