from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from unittest.mock import patch, MagicMock, ANY
import requests
from . import services
from . import scraper
from .models import Article

# --- MOCK DATA ---

def mock_news_api_success_data():
    """A sample successful response from NewsAPI."""
    return {
        "status": "ok",
        "totalResults": 1,
        "articles": [
            {
                "source": {"id": "test-source", "name": "Test Source"},
                "author": "Test Author",
                "title": "This is a test article title",
                "description": "This is a short test description.",
                "url": "http://example.com/test-article",
                "urlToImage": "http://example.com/image.jpg",
                "publishedAt": "2025-07-14T12:00:00Z",
                "content": "This is the full test content."
            }
        ]
    }

def mock_scraper_success_html():
    """A sample HTML page for the scraper to parse that is long enough to pass heuristics."""
    return """
    <html>
        <body>
            <article>
                <h1>Main Title</h1>
                <p>This is the first paragraph of the scraped content. It needs to be very long to avoid any short-content warnings. We will add a lot of repeated text here just to be absolutely sure that it exceeds any minimum length requirements, which is good practice for a unit test. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                <p>This is the second paragraph, which should also be included. By making this text sufficiently long, we ensure that our test is focused solely on the scraper's ability to correctly parse and combine the text from the HTML structure, rather than being affected by other business logic rules. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.</p>
            </article>
        </body>
    </html>
    """

# --- UNIT TESTS ---

class ServiceUnitTests(TestCase):
    """
    Unit tests for individual functions in services.py and scraper.py.
    These tests do not involve live network requests or model loading.
    """

    @patch('api.services.pipeline')
    def test_summarize_text_success(self, mock_pipeline):
        """Test that summarize_text returns a valid summary without loading the real model."""
        print("\n--- UNIT TEST: Testing summarize_text (Success) ---")
        # This mock simulates the summarizer object that the pipeline function would return
        mock_summarizer_instance = MagicMock(return_value=[{'summary_text': 'This is a mock summary.'}])
        # We configure the mock for pipeline() to return our simulated summarizer
        mock_pipeline.return_value = mock_summarizer_instance
        
        # Reset the global pipeline variable to ensure our mock is used
        services.summarizer_pipeline = None
        
        print("LOG: Calling summarize_text with mock pipeline...")
        summary = services.summarize_text("This is a long piece of text to summarize.")
        
        self.assertEqual(summary, "This is a mock summary.")
        print("LOG: Successfully received mock summary.")
        
        # Assert that the pipeline function was called to create the summarizer.
        # In a non-GPU environment, the 'device' argument is not passed.
        mock_pipeline.assert_called_once_with("summarization", model='sshleifer/distilbart-cnn-12-6')
        
        # Assert that the summarizer instance itself was called with the correct text
        mock_summarizer_instance.assert_called_once_with("This is a long piece of text to summarize.", truncation=True)

    def test_summarize_text_empty_input(self):
        """Test that summarize_text handles empty or whitespace input gracefully."""
        print("\n--- UNIT TEST: Testing summarize_text (Empty Input) ---")
        print("LOG: Testing with an empty string...")
        result = services.summarize_text("")
        self.assertEqual(result, "Content was empty or could not be scraped. No summary available.")
        print("LOG: Correctly handled empty string.")
        
        print("LOG: Testing with a whitespace string...")
        result_whitespace = services.summarize_text("   ")
        self.assertEqual(result_whitespace, "Content was empty or could not be scraped. No summary available.")
        print("LOG: Correctly handled whitespace string.")

    @patch('api.scraper.requests.get')
    def test_scrape_article_text_success(self, mock_requests_get):
        """Test successful scraping of an HTML page."""
        print("\n--- UNIT TEST: Testing scrape_article_text (Success) ---")
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = mock_scraper_success_html().encode('utf-8')
        mock_requests_get.return_value = mock_response

        print("LOG: Calling scrape_article_text with mock HTML...")
        content = scraper.scrape_article_text("http://example.com/article")
        
        self.assertIsNotNone(content)
        # This explicit check helps with type hinting for the linter
        if content:
            self.assertIn("This is the first paragraph", content)
            print("LOG: Successfully scraped and found content.")

    @patch('api.scraper.requests.get')
    def test_scrape_article_text_http_error(self, mock_requests_get):
        """Test that the scraper handles HTTP errors (like 404) correctly."""
        print("\n--- UNIT TEST: Testing scrape_article_text (HTTP Error) ---")
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
        mock_requests_get.return_value = mock_response

        print("LOG: Calling scrape_article_text expecting an error...")
        content = scraper.scrape_article_text("http://example.com/not-found")
        self.assertIsNone(content)
        print("LOG: Correctly handled HTTP error by returning None.")


# --- INTEGRATION TESTS ---

@patch('api.views.services.summarize_text', return_value="A perfect mock summary.")
@patch('api.views.scrape_article_text', return_value="Mocked scraped content.")
class APIIntegrationTests(TestCase):
    """
    Integration tests for the API endpoints.
    External services are mocked for all tests in this class.
    """

    def setUp(self):
        """Set up a test user and an authenticated client."""
        print("\n--- INTEGRATION TEST SETUP: Creating base user and client ---")
        self.client = APIClient()
        self.test_user = User.objects.create_user(
            username='testuser', 
            password='testpassword123',
            email='test@example.com'
        )
        self.client.force_authenticate(user=self.test_user)
        print(f"LOG: User 'testuser' created and client authenticated.")

    def test_user_registration_and_login(self, mock_scrape, mock_summarize):
        """Test that a new user can register and then log in."""
        print("\n--- INTEGRATION TEST: Testing User Registration and Login ---")
        unauthenticated_client = APIClient()
        
        print("LOG: Step 1 - Registering a new user 'new_user'...")
        reg_data = {'username': 'new_user', 'password': 'new_password', 'email': 'new@example.com'}
        reg_response = unauthenticated_client.post('/api/register/', reg_data, format='json')
        self.assertEqual(reg_response.status_code, 201)  # type: ignore
        self.assertEqual(User.objects.count(), 2)
        print("LOG: Registration successful. Status 201.")

        print("\nLOG: Step 2 - Logging in with the new user...")
        login_data = {'username': 'new_user', 'password': 'new_password'}
        login_response = unauthenticated_client.post('/api/token/', login_data, format='json')
        self.assertEqual(login_response.status_code, 200)  # type: ignore
        self.assertIn('access', login_response.data)  # type: ignore
        print("LOG: Login successful. Received access token.")

    def test_unauthenticated_access_is_denied(self, mock_scrape, mock_summarize):
        """Test that protected endpoints reject requests without a valid token."""
        print("\n--- INTEGRATION TEST: Testing Unauthenticated Access ---")
        unauthenticated_client = APIClient()
        print("LOG: Making request to protected endpoint /api/latest/ without a token...")
        response = unauthenticated_client.get('/api/latest/')
        self.assertEqual(response.status_code, 401)  # type: ignore
        print("LOG: Access denied with status 401 as expected.")

    @patch('api.views.services.fetch_from_news_api')
    def test_latest_news_endpoint(self, mock_fetch, mock_scrape, mock_summarize):
        """Test the /api/latest/ endpoint."""
        print("\n--- INTEGRATION TEST: Testing /api/latest/ endpoint ---")
        mock_fetch.return_value = mock_news_api_success_data()

        print("LOG: Calling /api/latest/ (external services are mocked)...")
        response = self.client.get('/api/latest/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)  # type: ignore
        print("LOG: Received successful response with 1 article.")
        self.assertEqual(response.data[0]['summary'], "A perfect mock summary.")  # type: ignore
        print("LOG: Verified that the summary is the mocked summary.")
        
        mock_fetch.assert_called_once_with()
        mock_scrape.assert_called_once_with('http://example.com/test-article')
        mock_summarize.assert_called_once_with("Mocked scraped content.")

    @patch('api.views.services.fetch_from_news_api')
    def test_search_news_endpoint(self, mock_fetch, mock_scrape, mock_summarize):
        """Test the /api/search/ endpoint."""
        print("\n--- INTEGRATION TEST: Testing /api/search/ endpoint ---")
        mock_fetch.return_value = mock_news_api_success_data()

        print("LOG: Calling /api/search/?q=testing (external services are mocked)...")
        response = self.client.get('/api/search/?q=testing')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]['summary'], "A perfect mock summary.")  # type: ignore
        print("LOG: Received successful response with correct mock data.")
        
        mock_fetch.assert_called_once_with(search_term='testing')

    def test_save_and_list_news_endpoints(self, mock_scrape, mock_summarize):
        """Test saving and listing articles, ensuring external services are not called."""
        print("\n--- INTEGRATION TEST: Testing /api/save/ and /api/saved/ endpoints ---")
        article_data = {
            "title": "An Article to Save",
            "url": "http://example.com/to-save",
            "source_name": "Save Source",
            "summary": "A summary of the article to be saved.",
            "published_at": "2025-07-14T13:00:00Z"
        }

        print("LOG: Step 1 - Saving an article via POST to /api/save/...")
        save_response = self.client.post('/api/save/', article_data, format='json')
        self.assertEqual(save_response.status_code, 201)
        print("LOG: Article saved successfully. Status 201.")
        
        self.assertTrue(Article.objects.filter(user=self.test_user, url=article_data['url']).exists())
        print("LOG: Verified article exists in the database for the correct user.")

        print("\nLOG: Step 2 - Retrieving saved articles via GET to /api/saved/...")
        list_response = self.client.get('/api/saved/')
        self.assertEqual(list_response.status_code, 200)
        self.assertEqual(len(list_response.data), 1)  # type: ignore
        self.assertEqual(list_response.data[0]['title'], "An Article to Save")  # type: ignore
        print("LOG: Successfully retrieved saved articles and verified content.")

        mock_scrape.assert_not_called()
        mock_summarize.assert_not_called()
        print("LOG: Verified that external services (scrape, summarize) were not called.")
