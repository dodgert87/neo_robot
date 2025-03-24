from app.services.query_generators.base_query import BaseQueryGenerator
from app.services.news_service import NewsService
import json

class NewsQueryGenerator(BaseQueryGenerator):
    """
    Generates AI query for news-related requests.
    """

    def generate_query(self, parsed_json: dict) -> dict:
        """
        Converts structured JSON into a formatted AI query.
        Handles news retrieval before formatting.
        """
        # Extract parameters
        delivery_method = parsed_json["parameters"].get("delivery_method", "default")

        # Fetch news articles
        news_articles = NewsService.fetch_news_from_json(parsed_json)

        # Handle errors or empty results
        if "error" in news_articles:
            return {"error": news_articles["error"]}
        if not news_articles:
            return {"error": "No relevant news found."}

        # Copy the first article
        first_article = news_articles[0]

        # Generate AI query based on delivery method
        if delivery_method == "default":
            return self._generate_ai_default(first_article)

        elif delivery_method == "summary":
            return self._generate_ai_summary(first_article)

        elif delivery_method == "bullet_points":
            return self._generate_ai_bullet_points(first_article)

        elif delivery_method == "one_sentence":
            return self._generate_ai_one_sentence(first_article)

        else:
            return self._generate_ai_default(first_article)  # Fallback to default

    def _generate_ai_default(self, article):
        """
        Generates an AI query for a natural response based on the first article.
        """
        ai_query = (
            f"You are a newscaster and you are going to do a readout to this text to one person only,"
            f"make it conversational, not formal and\n"
            f"Generate a natural, engaging response based on the following news article:\n"
            f"Title: {article['title']}\n"
            f"Description: {article['description']}\n"
            f"Published: {article['pubDate']} | Country: {article['country'][0]}\n"
            f"And always mention the publication source {article['source']}\n"
            f"\n"
            f"Make it conversational, informative, and human-like. Avoid listing all details—just focus on the key takeaways.\n"
        )

        return ai_query

    def _generate_ai_summary(self, article):
        """
        Generates an AI query to summarize the first news article.
        """
        ai_query = (
            f"You are a newscaster and you are going to do a readout to this text to one person only,"
            f"Summarize the following news article:\n"
            f"make it conversational, not formal and\n"
            f"Title: {article['title']}\n"
            f"Description: {article['description']}\n"
            f"And always mention the publication source {article['source']}\n"
            f"Provide a concise summary in 2-3 sentences."
        )

        return ai_query

    def _generate_ai_bullet_points(self, article):
        """
        Generates an AI query to extract key takeaways as bullet points.
        """
        ai_query = (
            f"You are a newscaster and you are going to do a readout to this text to one person only,"
            f"Extract the most important takeaways from this news article:\n"
            f"Summarize the following news article:\n"
            f"Title: {article['title']}\n"
            f"Description: {article['description']}\n"
            f"And always mention the publication source {article['source']}\n"
            f"Format the response as a bullet-point list."
        )

        return ai_query

    def _generate_ai_one_sentence(self, article):
        """
        Generates an AI query to return a single-sentence summary.
        """
        ai_query = (
            f"You are a newscaster and you are going to do a readout to this text to one person only,"
            f"Extract the most important takeaways from this news article:\n"
            f"Condense the following news article into a single, informative sentence:\n"
            f"Title: {article['title']}\n"
            f"Description: {article['description']}\n"
            f"And always mention the publication source {article['source']}\n"
            f"Return only one sentence."
        )

        return ai_query

