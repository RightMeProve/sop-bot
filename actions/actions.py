import logging
from typing import Any, Dict, List, Text
import spacy
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from chroma_client import get_sop_collection

FILE_SERVER_URL = "http://localhost:8000"   # Adjust if serving elsewhere

logger = logging.getLogger(__name__)

try:
    nlp = spacy.load("en_core_web_md")
except OSError:
    from spacy.cli import download
    download("en_core_web_md")
    nlp = spacy.load("en_core_web_md")

def extract_keywords(text: str) -> str:
    doc = nlp(text)
    keywords = [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop and not token.is_punct and token.pos_ in {"NOUN", "VERB", "ADJ"}
    ]
    unique_keywords = list(dict.fromkeys(keywords))
    return " ".join(unique_keywords) if unique_keywords else text[:50]

class ActionSearchSOP(Action):
    MAX_SNIPPET_LENGTH = 250

    def name(self) -> Text:
        return "action_search_sop"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_query = tracker.latest_message.get("text", "")
        if not user_query.strip():
            dispatcher.utter_message(text="Could you please repeat your question?")
            return []

        keywords = extract_keywords(user_query)
        try:
            collection = get_sop_collection()
            results = collection.query(
                query_texts=[keywords],
                n_results=10,   # Fetch more chunks to improve chance of 3 uniques
                include=["documents", "metadatas"],
            )
            documents = results.get("documents", [[]])[0]
            metadatas = results.get("metadatas", [[]])[0]
            if not documents:
                dispatcher.utter_message(
                    text="I couldn't find a relevant SOP. Please try rephrasing your question."
                )
                return []

            responses = []
            used_filenames = set()
            for doc, meta in zip(documents, metadatas):
                filename = meta.get("filename", "Document")
                if filename in used_filenames:
                    continue  # Skip duplicate documents!
                used_filenames.add(filename)

                snippet = doc[:self.MAX_SNIPPET_LENGTH]
                if len(doc) > self.MAX_SNIPPET_LENGTH:
                    snippet += "..."
                file_url = f"{FILE_SERVER_URL}/{filename}"
                responses.append(
                    f"📄 **{filename}**\n"
                    f"{snippet}\n"
                    f"[⤵️ View full document]({file_url})\n"
                )
                if len(responses) == 3:
                    break  # Only want top 3 unique documents

            if responses:
                full_response = "Here are the top 3 relevant SOPs I found:\n\n" + "\n".join(responses)
            else:
                full_response = "I couldn't find relevant unique SOPs. Please try rephrasing your question."

            dispatcher.utter_message(text=full_response)
        except Exception as e:
            logger.error(f"Error querying ChromaDB: {e}", exc_info=True)
            dispatcher.utter_message(
                text="Our sop database is temporarily unavailable. Please try again later."
            )
        return []