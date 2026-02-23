from dataclasses import dataclass, field

@dataclass
class Book:
	recorder_id: int = 0
	title: str = ""
	author: str = ""
	favourite: bool = False
	metadata: dict = field(default_factory=lambda: {
		"source": "test",
		"category": "Text",
		"tags": [],
	})

	def toggle_favourite(self):
		self.favourite = not self.favourite

	def set_source(self, source: str) -> 'Book':
		if source:
			self.metadata['source'] = source
		return self