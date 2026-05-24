from dataclasses import dataclass, field
from functools import total_ordering

@total_ordering
@dataclass
class Book:
	recorder_id: int = 0
	title: str = ""
	author: str = ""
	favourite: bool = False
	year: int = 2000
	url: str = ""
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
	
	def __contains__(self, keyword):
		return keyword.lower() in self.title.lower() or keyword.lower() in self.author.lower()
	
	def __eq__(self, book: 'Book'):
		return self.title == book.title and self.author == book.author and self.year == book.year
	
	def __lt__(self, book: 'Book'):
		return (self.year, self.title, self.author) < (book.year, book.title, book.author)
