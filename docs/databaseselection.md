```bash
⚡ Why I Included ChromaDB
ChromaDB is a lightweight open-source vector store — great for:

- Storing chunks of brand strategy, prior campaign assets, etc.
- Fast similarity search for prompt history, product info, FAQs, etc.
- Runs locally, so perfect for free/open-source builds

✅ It’s good for dev-time experimentation  
❌ But may not scale well or have advanced memory tools like long-term retrieval with context compression.

🧠 Alternative Memory / Vector DB Options

| Option                               | Type                            | Good For                                 | Notes                                   |
|--------------------------------------|----------------------------------|-------------------------------------------|-----------------------------------------|
| FAISS                                | Vector DB                       | Local semantic search (LLM history, docs) | Lightweight, fast                       |
| Weaviate                             | Vector DB + APIs                | Local or cloud, integrates with LangChain | More full-featured                      |
| Qdrant                               | Vector DB                       | Local, scalable, production-ready         | Docker setup easy                       |
| Redis                                | Key-value store + vector search | Temporary short-term memory               | Great for live apps                     |
| LangChain's ConversationBufferMemory | In-memory only                  | Only good for short sessions              | No persistence                          |

✅ My Recommendation for You Right Now:

Since you're just starting out and keeping everything local + open source, you can go with:

Option 1 – ChromaDB (default):
- Easy to set up
- Works well with LangChain or LangGraph
- Good dev experience

Option 2 – FAISS:
- If you don’t need persistent disk storage yet (just embeddings + retrieval)
```