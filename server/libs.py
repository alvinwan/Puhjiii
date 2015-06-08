from bson import ObjectId


class Puhjee:
	"""
	This is the base class for all savable objects.
	"""
	
	filters = {}
	
	def __init__(self, **kwargs):
		self.filter(**kwargs)
		self.result = None  # for query results
	
	def get(self):
		"""
		Query the database with this object's data
		:return: object loaded with data
		"""
		self.result = self.__class__._get(**self.data())
		data = Puhjee._data(self, self.result)
		return self.load(**data)

	@classmethod
	def _get(cls, **kwargs):
		"""
		Query database with passed-in data
		:param kwargs: filter
		:return: query results or None
		"""
		return cls.model.objects(**kwargs).get()
	
	def save(self):
		"""
		Save object with it's data to database
		:return: self
		"""
		if len(list(self.filters.keys())) == 0:
			self.filters = self.data()
		self.result = self.model.objects(**self.filters).modify(
			upsert=True,
			new=True,
		    **{'set__%s' % k: v for k, v in self.data().items()}
		)
		data = Puhjee._data(self, self.result)
		return self.load(**data)
		
	def load(self, **kwargs):
		"""
		Save all passed-in data to object
		- convert all ID objects and strings into ObjectIds
		:param kwargs: data
		:return: self
		"""
		for k, v in kwargs.items():
			if k == 'id' and not isinstance(v, (bytes, str, ObjectId)):
				v = getattr(v, 'id', None)
			if isinstance(v, Puhjee):
				v = v.model(**v.data()).to_dbref()
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
		return Puhjee._fields(getattr(self, 'model'))
	
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
	
	def filter(self, **kwargs):
		"""
		Set filters for next save or search.
		:param kwargs: filters as kwargs
		:return: self
		"""
		self.filters = kwargs
		self.load(**kwargs)
		return self
	
	def delete(self):
		"""
		Delete the object
		:return: None
		"""
		self.get().model(**self.data()).delete()
	
	def exists(self):
		return hasattr(self, 'id')