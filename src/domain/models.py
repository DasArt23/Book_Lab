from dataclasses import dataclass, field

@dataclass
class Book:
	_recorder_id: int = 0
	_title: str = ""
	_author: str = ""
	_metadata: dict = field(default_factory=lambda: {
		"source": "test",
		"category": "Text",	
		"tags": [],
	})
	_favourite: bool = False

	def __str__(self):
		meta_inf = ", ".join(f"{key}={val}" for key, val in self.metadata.items())
		return f"Title: {self.title} | "\
			   f"Author: {self.author}\n"\
			   f"ID: {self.recorder_id}\n"\
			   f"Meta: {meta_inf}"
	
	@property
	def title(self) -> str:
		return self._title
		
	@property
	def author(self) -> str:
		return self._author
	
	@property
	def recorder_id(self) -> int:
		return self._recorder_id
	
	@property
	def metadata(self) -> dict:
		return self._metadata
	
	def is_favourite(self) -> bool:
		return self._favourite
	
	def change_favourite(self) -> None:
		self._favourite = not self._favourite
	
	def set_source(self, source: str) -> None:
		if source:
			self._metadata['source'] = source
	
	@property
	def source(self) -> str:
		return self._metadata['source']