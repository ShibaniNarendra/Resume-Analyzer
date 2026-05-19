import unittest
from unittest.mock import MagicMock, patch
from utils.parser import preprocess_text
from utils.analyzer import extract_keywords, match_keywords, get_semantic_similarity
from utils.scorer import calculate_ats_score

class TestResumeAnalyzerRobust(unittest.TestCase):

    # --- Parser Tests ---
    def test_preprocess_text_empty(self):
        self.assertEqual(preprocess_text(""), "")
        self.assertEqual(preprocess_text(None), "")

    def test_preprocess_text_whitespace(self):
        text = "  Hello   \n  World  "
        self.assertEqual(preprocess_text(text), "Hello World")

    # --- Analyzer Tests ---
    def test_extract_keywords_empty(self):
        self.assertEqual(extract_keywords(""), [])

    def test_match_keywords_full(self):
        res = ["python", "sql", "aws"]
        jd = ["python", "sql", "aws"]
        matched, missing = match_keywords(res, jd)
        self.assertEqual(set(matched), set(jd))
        self.assertEqual(missing, [])

    def test_match_keywords_none(self):
        res = ["java", "c++"]
        jd = ["python", "sql"]
        matched, missing = match_keywords(res, jd)
        self.assertEqual(matched, [])
        self.assertEqual(set(missing), set(jd))

    def test_match_keywords_partial(self):
        res = ["python", "docker"]
        jd = ["python", "sql"]
        matched, missing = match_keywords(res, jd)
        self.assertEqual(matched, ["python"])
        self.assertEqual(missing, ["sql"])

    def test_semantic_similarity_identical(self):
        text = "Senior Python Developer with 5 years of experience in AI and Machine Learning."
        score = get_semantic_similarity(text, text)
        self.assertAlmostEqual(score, 1.0, places=2)

    def test_semantic_similarity_different(self):
        text1 = "Cooking recipes for pasta and pizza."
        text2 = "Software engineering principles and data structures."
        score = get_semantic_similarity(text1, text2)
        self.assertLess(score, 0.5)

    def test_semantic_similarity_empty(self):
        self.assertEqual(get_semantic_similarity("", "text"), 0.0)

    # --- Scorer Tests ---
    def test_calculate_ats_score_max(self):
        # 100% keyword match (1.0) and 100% similarity (1.0)
        score = calculate_ats_score(1.0, 1.0)
        self.assertEqual(score, 100.0)

    def test_calculate_ats_score_min(self):
        score = calculate_ats_score(0.0, 0.0)
        self.assertEqual(score, 0.0)

    def test_calculate_ats_score_mixed(self):
        # 0.5 keyword match, 0.8 similarity
        # (0.4 * 0.5 + 0.6 * 0.8) * 100 = (0.2 + 0.48) * 100 = 68
        score = calculate_ats_score(0.5, 0.8)
        self.assertEqual(score, 68.0)

    # --- Mocked API Tests ---
    @patch('utils.scorer.get_gemini_model')
    def test_generate_recommendations_mock(self, mock_get_model):
        from utils.scorer import generate_recommendations
        
        # Mocking the Gemini model and its response
        mock_model = MagicMock()
        mock_response = MagicMock()
        mock_response.text = "Mocked Recommendation"
        mock_model.generate_content.return_value = mock_response
        mock_get_model.return_value = mock_model
        
        rec = generate_recommendations("resume", "jd", ["missing"])
        self.assertEqual(rec, "Mocked Recommendation")

if __name__ == "__main__":
    unittest.main()
