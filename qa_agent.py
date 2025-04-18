# qa_agent.py

import argparse
from crawler import crawl_website
from processor import process_documents
from vector_store import VectorStore
from answer_engine import AnswerEngine

def main():
    parser = argparse.ArgumentParser(description="AI Help Doc Q&A Agent")
    parser.add_argument('--url', required=True, help="Base help site URL to crawl")
    args = parser.parse_args()

    # Step 1: Crawl
    print("🌐 Crawling website...")
    raw_docs = crawl_website(args.url)
    if not raw_docs:
        print("[!] No data was crawled. Please check the URL and try again.")
        exit()

    # Step 2: Clean/process
    print("🧹 Processing documents...")
    cleaned_docs = process_documents(raw_docs)
    if not cleaned_docs:
        print("[!] No documents to index. Exiting.")
        exit()


    # Step 3: Embed + Index
    print("📦 Building vector store...")
    vs = VectorStore()
    vs.add_documents(cleaned_docs)

    # Step 4: Answer loop
    engine = AnswerEngine(vs)
    print("\n🤖 Ask me anything about the site! (type 'exit' to quit)")
    while True:
        query = input("\nYou: ")
        if query.lower() in ("exit", "quit"):
            print("👋 Bye!")
            break
        response = engine.answer(query)
        print("\nAI:", response)

if __name__ == "__main__":
    main()
