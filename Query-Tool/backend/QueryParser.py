from backend.Boolean import Boolean
from backend.CaptureGroups import CaptureGroups
from backend.Sequential import Sequential
import json
from backend.Field import Field
from backend.QueryProcessor import QueryProcessor



class QueryParser:
	def __init__(self,query,ip_filename,section,):
		self.query=query
		self.ip_filename=ip_filename
		self.section=section
		self.db=QueryProcessor.get_db(ip_filename,self.section)

	def ParseQuery(self):
		
		if '{' in self.query:
			obj=WildCard(self.query,self.db)
			return(obj.CheckQuery())
		elif ',' in self.query:
			obj=Sequential(self.query,self.db)
			return(obj.CheckQuery())
		elif '?' in self.query:
			obj=CaptureGroups(self.query,self.db)
			return(obj.CheckQuery())
		elif 'word' in self.query or 'lemma' in self.query or 'tag' in self.query or 'entity' in self.query:
				if ':' not in self.query:
					obj=Field(self.query,self.db)
					return(obj.CheckQuery())
				else:
					obj=CaptureGroups(self.query,self.db)
					return(obj.CheckQuery())
		else:
			if ':' not in self.query:
				obj=Boolean(self.query,self.db)
				return(obj.CheckQuery())
			else:
				obj=CaptureGroups(self.query,self.db)
				return(obj.CheckQuery())


