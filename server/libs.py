from bson import ObjectId
from server import db


class Puhjiii:
	"""
	This is the base class for all savable objects.
	"""
	
	filters = {}
	
	def __init__(self, **kwargs):
		"""
		Automatically loads all kwargs as filters
		:param kwargs: kwargs
		:return: self
		"""
		self.filter(**kwargs)
		self.result = None  # for query results
	
	def get(self):
		"""
		Query the database with this object's data
		:return: object loaded with data
		"""
		self.result = self.__class__._get(**self.data())
		data = Puhjiii._data(self, self.result)
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
		    **{'set__%s' % k: v for k, v in self.data(defaults=True).items()}
		)
		data = Puhjiii._data(self, self.result)
		return self.load(**data)
		
	def load(self, **kwargs):
		"""
		Save all passed-in data to object
		- convert all ID objects and strings into ObjectIds
		:param kwargs: data
		:return: self
		"""
		for k, v in kwargs.items():
			if k == 'id' or (k in self.model._fields.keys() \
                 and isinstance(self.model._fields[k], db.ReferenceField)):
				if idify or k == 'id':
					if not isinstance(v, ObjectId):
						if isinstance(v, str):
							v = ObjectId(v)
						else:
							v = getattr(v, 'id')
				elif issubclass(v.__class__, db.Document):
					v = v.to_dbref()
				elif isinstance(v, str):
					v = DBRef(k, ObjectId(v))
				elif hasattr(v, 'model'):
					v = v.model(**v.data()).to_dbref()
				else:
					v = None
			setattr(self, k, v)
		return self	
		
	def data(self, defaults=False):
		"""
		Returns all data associated with object
		:return: data for specified fields, or all data
		"""
		return Puhjiii._data(self, self, defaults)
	
	@staticmethod
	def _data(self, obj, defaults=False):
		data = {}
		for f, v in self.fields().items():
			if f.startswith('updated_'):
				setattr(obj, f, None)
			if getattr(obj, f, None):
				data[f] = getattr(obj, f)
			elif getattr(v, 'default') and defaults:
				data[f] = v.default()
		return data

	def fields(self):
		"""
		Fetches all fields based on this object's model
		:return: list of fields
		"""
		return Puhjiii._fields(getattr(self, 'model'))
	
	@staticmethod
	def _fields(model):
		"""
		Fetches all fields for a model
		:param model: model
		:return: dictionary of fields
		"""
		return {k: v for k, v in model._fields.items() if not isinstance(k, int)}
		
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
		self.load(**kwargs)
		self.filters = dict(self.data())
		return self
	
	def delete(self):
		"""
		Delete the object
		:return: None
		"""
		self.get().model(**self.data()).delete()

	def assemble(self, form):
		"""
		Assemble all data from form and package into info.
		:return: self
		"""
		self.info = {k: v.data for k, v in form._fields.items()}
		return self
	
	def exists(self):
		"""
		Test if the current object exists.
		:return:
		"""
		if not self.result:
			self.get()
		return hasattr(self, 'id')