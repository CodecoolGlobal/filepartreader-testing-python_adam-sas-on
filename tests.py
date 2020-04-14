import unittest
from reader import FilePartReader
from analyzer import FileAnalyzer


class ReaderTest(unittest.TestCase):
	def setUp(self):
		self.reader = FilePartReader()

	def test_read_lines(self):
		self.reader.setup("resources/lorem_ipsum.txt", 3, 6)
		rows = []
		text = ("Nam porta condimentum lorem ac egestas. Sed lectus erat, maximus vitae ex in, "
				"scelerisque convallis tortor. Ut sit amet magna ipsum. Etiam ut eleifend eros. "
				"Pellentesque bibendum at magna id iaculis. Ut et pretium risus. Curabitur aliquet, "
				"neque pharetra tristique tempus, erat justo pellentesque diam, nec rhoncus tellus massa ut nisl. "
				"Duis libero odio, ultrices non enim id, porttitor volutpat leo. Maecenas eget aliquam diam. "
				"Donec metus nibh, gravida ac euismod id, mattis vitae risus. Vivamus porta in lectus ac vehicula. "
				"Proin laoreet egestas neque sagittis finibus. In dignissim nisl in justo porta, "
				"nec maximus ex vulputate. Donec ornare, neque id pellentesque consectetur, "
				"purus ante ultrices arcu, ut vehicula neque massa a justo. Nam at sagittis metus. "
				"Ut semper, purus vel viverra vestibulum, ligula nibh maximus odio, quis gravida erat massa non magna.")
		rows.append(text)
		rows.append("")

		text = ("Fusce molestie orci magna, ac commodo massa egestas id. Proin venenatis ante eu justo "
				"molestie bibendum. In posuere augue cursus mi varius, ac vehicula orci facilisis. "
				"Donec euismod eleifend ex, sit amet sodales diam lacinia vehicula. Donec vel urna elementum, "
				"commodo orci ac, convallis velit. Donec orci massa, tempor non pulvinar in, "
				"pretium nec lectus. Duis odio libero, ultricies et aliquet quis, sollicitudin ullamcorper odio. "
				"Morbi tristique vehicula quam, ac pharetra mauris vulputate non. Quisque convallis "
				"posuere cursus. Sed metus nunc, ornare eget augue cursus, dictum venenatis risus. "
				"Nullam egestas nibh vitae lectus porttitor, eu cursus dui varius. "
				"Ut sit amet tincidunt nisl, vel pretium erat.")
		rows.append(text)
		rows.append("")
		text = "\n".join(rows)

		str_from_file = self.reader.read_lines()
		with self.subTest("Lorem ipsum reader-test, range [3, 6]"):
			self.assertEqual(text, str_from_file)


		self.reader.set_read_range(1, 1)
		text = ("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Curabitur mauris nisl, "
				"mollis vitae neque vitae, congue eleifend ligula. Nam ultrices mauris nisl, "
				"et malesuada nibh porttitor sit amet. Ut nec libero bibendum ligula lobortis rutrum. "
				"Suspendisse ut est in ante aliquam aliquet. Integer aliquet magna in urna placerat, "
				"id aliquet neque rhoncus. Pellentesque habitant morbi tristique senectus et netus "
				"et malesuada fames ac turpis egestas. Curabitur ex libero, fringilla et rhoncus sed, "
				"dapibus eget justo. Orci varius natoque penatibus et magnis dis parturient montes, "
				"nascetur ridiculus mus. Maecenas et maximus arcu. Maecenas porta, nisl maximus gravida "
				"placerat, sem ipsum interdum metus, nec imperdiet lorem ligula et erat. "
				"In hac habitasse platea dictumst.")
		str_from_file = self.reader.read_lines()
		with self.subTest("Lorem ipsum test, range [1, 1]"):
			self.assertEqual(text, str_from_file)
	#

	def test_read_lines_test_by_StarWars(self):
		self.reader.setup("resources/Star_Wars_-_Attack_of_the_Clones.txt", 313, 321)
		rows = ["ELAN SLEAZEBAGGANO: You wanna buy some death-sticks?", "",
				"OBI-WAN: You don't want to sell me death-sticks.", "",
				"ELAN: I don't want to sell you death-sticks.", "",
				"OBI-WAN: You want to go home and rethink your life.", "",
				"ELAN: I want to go home and rethink my life."]
		text = "\n".join(rows)

		str_from_file = self.reader.read_lines()
		with self.subTest("StarWars reader-test, range [313, 321]"):
			self.assertEqual(text, str_from_file)


		self.reader.set_read_range(752, 775)
		rows = ["OBI-WAN: Ever make your way as far into the interior as Coruscant?", "",
				"JANGO FETT: Once or twice.", "",
				"OBI-WAN: Recently?", "",
				"JANGO FETT: Possibly...", "",
				"OBI-WAN: Then you must know Master Sifo-Dyas?", "",
				"JANGO FETT: Boba, rood eht so-heeck.", "",
				"JANGO FETT: Master who?", "",
				"OBI-WAN: Sifo-Dyas. Is he not the Jedi who hired you for this job?", "",
				"JANGO FETT: Never heard of him.", "",
				"OBI-WAN: Really?", "",
				"JANGO FETT: I was recruited by a man called Tyranus on one of the moons of Bogden.", "",
				"OBI-WAN: Curious.", ""]
		text = "\n".join(rows)
		
		str_from_file = self.reader.read_lines()
		with self.subTest("StarWars reader-test, range [752, 775]"):
			self.assertEqual(text, str_from_file)


		self.reader.set_read_range(452, 452)
		text = "ANAKIN: May the Force be with you, Master."
		str_from_file = self.reader.read_lines()
		with self.subTest("StarWars reader-test, range [452, 452]"):
			self.assertEqual(text, str_from_file)
	#

class AnalyzerTest(unittest.TestCase):
	def setUp(self):
		reader = FilePartReader()
		self.analyzer = FileAnalyzer(reader)

	def diff_for_symmetric_thousandth_numbers(self, number):
		mod = number//1000
		mod = number - 1000*mod
		return 11 if mod > 990 else 110
	#

	def test_get_words_ordered_alphabetically_by_StarWars(self):
		self.analyzer.set_file_path("resources/Star_Wars_-_Attack_of_the_Clones.txt")
		self.analyzer.set_read_range(892, 898)

		expected = ["ANAKIN", "baan", "bata", "Booda", "boska", "chasa", "Chut", "di", "Ding", "Du", "hopa", "hota", "Jedi", "Ke", "mi", "No", "pee", "Shmi", "Skywalker", "tu", "wanga", "WATTO", "Yo"]

		self.analyzer.case_sensitive_set(False) # case-insensitive;
		self.analyzer.set_words_uniqueness(True)

		result = self.analyzer.get_words_ordered_alphabetically()
		self.assertEqual(expected, result) # assertEquals(expected, result);
	#

	def test_words_containing_substring_by_StarWars(self):
		self.analyzer.set_file_path("resources/Star_Wars_-_Attack_of_the_Clones.txt")
		self.analyzer.set_read_range(1)

		self.analyzer.case_sensitive_set(False) # case-insensitive;
		self.analyzer.set_words_uniqueness(True)

		substring = "Ani"
		expected = ["Ani", "canisters", "animals", "mechanic", "DANIELS", "DANIEL", "HASSANI"]

		result = self.analyzer.get_words_containing_substring(substring)
		with self.subTest("StarWars analyzer-test, whole file, substring \"Ani\", case-insensitive, uniqueness = True"):
			self.assertEqual(expected, result)


		self.analyzer.set_words_uniqueness(False)
		expected = ["Ani", "Ani", "Ani", "Ani", "Ani", "Ani", "Ani", "Ani", "canisters", "Ani", "Ani", "Ani", "Ani", "Ani", "Ani", "Ani", "Ani",
				"animals", "animals", "Ani", "Ani", "mechanic", "DANIELS", "DANIELS", "DANIEL", "HASSANI"]

		result = self.analyzer.get_words_containing_substring(substring)
		with self.subTest("StarWars analyzer-test, whole file, substring \"Ani\", case-insensitive, uniqueness = False"):
			self.assertEqual(expected, result)


		self.analyzer.set_words_uniqueness(True)
		substring = "Ken"
		expected = ["Kenobi", "broken", "Tusken", "Tuskens", "KENNY"]
		result = self.analyzer.get_words_containing_substring(substring)
		with self.subTest("StarWars analyzer-test, whole file, substring \"Ken\", case-insensitive, uniqueness = True"):
			self.assertEqual(expected, result)
	#

	def test_get_strings_which_palindromes_by_numbers(self):
		self.analyzer.set_file_path("resources/numbers_test.txt")
		self.analyzer.set_read_range(1)

		expected = []
		n = 1001
		diff = 110
		repeated_number = 1551
		while n <= repeated_number:
			expected.append(str(n) )
			n += diff
		expected.append(str(repeated_number) )

		repeated_number = 7007
		while n <= repeated_number:
			expected.append(str(n) )
			diff = self.diff_for_symmetric_thousandth_numbers(n)
			n += diff
		expected.append(str(repeated_number) )

		while n < 10000:
			expected.append(str(n) )
			diff = self.diff_for_symmetric_thousandth_numbers(n)
			n+= diff

		result = self.analyzer.get_strings_which_palindromes()
		self.assertEqual(expected, result)
	#


if __name__ == '__main__':
	unittest.main()

