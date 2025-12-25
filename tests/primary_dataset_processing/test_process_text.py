import unittest
from src.primary_dataset_processing import TextProcessor


class TestTextProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = TextProcessor()

    def test_process_text_example(self):
        text = "Это пример текста с числами 123 и знаками препинания: !, ?."
        # The expected result may vary depending on the lemmatization
        expected_result = "это пример текст число знак препинание"
        processed_text = self.processor.process_text(text)
        self.assertEqual(expected_result, processed_text)

    def test_process_text_with_link(self):
        text = "Здравствуйте, зайдите по ссылке и получите подарок: https://my.itmo.ru/login"
        # The expected result may vary depending on the lemmatization
        expected_result = "здравствуйте зайти ссылка получить подарок"
        processed_text = self.processor.process_text(text)
        self.assertEqual(expected_result, processed_text)

    def test_process_text_with_difficult_words(self):
        text = "Меня зовут Бакаре Тунде, я брат первого нигерийского космонавта, майора ВВС Нигерии Абака Тунде. Мой брат стал первым африканским космонавтом, который отправился с секретной миссией на советскую станцию «Салют-6» в далеком 1979 году."
        # The expected result may vary depending on the lemmatization
        expected_result = "звать бакаре тунд брат первый нигерийский космонавт майор ввс нигерия абака тунд брат стать первый африканский космонавт который отправиться секретный миссия советский станция салют далёкий год"
        processed_text = self.processor.process_text(text)
        self.assertEqual(expected_result, processed_text)

if __name__ == '__main__':
    unittest.main()
