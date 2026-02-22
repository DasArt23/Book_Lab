from dataclasses import dataclass, field

@dataclass
class Book:
	recorder_id: int
	title: str
	author: str
	metadata: dict = field(default_factory=lambda: {
		"source": "Test",
		"category": "Audio",	
		"tags": [],
	})

	def __str__(self):
		meta_inf = ", ".join(f"{key}={val}" for key, val in self.metadata.items())
		return f"Title: {self.title} | "\
			   f"Author: {self.author}\n"\
			   f"ID: {self.recorder_id}\n"\
			   f"Meta: {meta_inf}"
	
	def get_title(self) -> str:
		return self.title
		
	def get_author(self) -> str:
		return self.author
	
	def get_rec_id(self) -> int:
		return self.recorder_id
	
	def get_metadata(self) -> dict:
		return self.metadata