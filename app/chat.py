# from langchain_community.vectorstores import Chroma
# from langchain_community.chat_models import ChatOllama
# from langchain_community.document_loaders import JSONLoader
# from langchain_text_splitters import RecursiveJsonSplitter
# from langchain_huggingface.embeddings import HuggingFaceEmbeddings
# from langchain_core.runnables import RunnablePassthrough
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
# from langchain_community.retrievers import BM25Retriever, EnsembleRetriever

# import os
# import json
# from pathlib import Path


# vectorstore_path = '../vectorstore2'
# os.makedirs(vectorstore_path, exist_ok=True)

# directory_path = Path('../files')

# # 모든 JSON 파일 경로 가져오기
# json_files = directory_path.glob('*.json')

# splitter = RecursiveJsonSplitter(max_chunk_size=2000)

# embedding_function = HuggingFaceEmbeddings(
#     model_name="peoplecombine-schoolai/9-chemistry-atoms_and_molecules-finetuned_sentence_embedding",
#     model_kwargs = {'device': 'cpu'},
#     encode_kwargs = {'normalize_embeddings': True})

# data = []
# for json_file in json_files:
#     with json_file.open('r', encoding='utf-8') as f:
#         data.append(json.load(f))

# flattened_data = [str(item) for sublist in data for item in sublist]

# bm25_retriever = BM25Retriever.from_texts(
#     # doc_list_1의 텍스트와 메타데이터를 사용하여 BM25Retriever를 초기화합니다.
#     flattened_data,
#     metadatas=[{"source": 1}] * len(flattened_data),
# )
# bm25_retriever.k = 1 

# # for i in range(len(data)):
# #     docs = splitter.create_documents(texts=[data[i]], convert_lists=True)
    
# #     # 벡터스토어 생성 및 저장
# #     vectorstore = Chroma.from_documents(docs, embedding_function, persist_directory=vectorstore_path)
    
# vectorstore = Chroma(persist_directory=vectorstore_path, embedding_function=embedding_function)

# retriever = vectorstore.as_retriever()

# ensemble_retriever = EnsembleRetriever(
#     retrievers=[bm25_retriever, retriever],
#     weights=[0.5, 0.5],
#     search_type="mmr",
# )

# model = ChatOllama(model="chemllm-7b-chat.Q4_K_M.gguf:latest")

# # Prompt 설정
# prompt = ChatPromptTemplate.from_messages(
#     [
#         (
#             "system",
#             "A chat between a curious user and an artificial intelligence assistant. The assistant gives helpful, detailed, and polite answers to the user's questions.",
#         ),
#         MessagesPlaceholder(variable_name="messages"),
#     ]
# )

# # RAG Chain 연결
# chain = (
#     {'context': ensemble_retriever}
#     | prompt
#     | model
#     | StrOutputParser()
# )