import pandas as pd
#import json
import os
from dotenv import dotenv_values
#import pymongo

from vertexai.language_models import TextGenerationModel, TextEmbeddingModel
import vertexai
import tiktoken
#from sklearn.metrics.pairwise import cosine_similarity

class palm2Llm:

    def __init__(self, env_name) -> None:
        self.env_name=env_name
        self.config = dotenv_values(self.env_name)

        ## set GCP environment
        self.google_auth = self.config['google_auth_json']

        os.environ['GOOGLE_APPLICATION_CREDENTIALS']= self.google_auth
        _project_id = self.config['vertexai_project_id']
        _location = self.config['vertexai_location']
        vertexai.init(project=_project_id, location=_location)

        ## set Palm2 model
        vertex_key = self.config['vertexai_palm2_api_key']
        self.embedding_model = TextEmbeddingModel.from_pretrained('textembedding-gecko-multilingual@001')
        self.llm_palm = TextGenerationModel.from_pretrained('text-bison@001')

    
    def get_vector_embedding(self, texts):
        '''
        각 페이지 번호의 텍스트를 벡터화
        args
        - text: 임베딩할 텍스트 데이터
        return
        - df_texts: 임베딩 된 'ada_v2'와 임베딩 길이 'n_tokens'가 추가 된 데이터프레임
        sequence
        1. 문서에서 읽어온 텍스트 데이터를 pandas 데이터프레임으로 변환
        2. 컬럼 명을 'page_no','text'로 변경
        3. 'ada_v2' 컬럼에 데이터프레임 'text' 컬럼 데이터를 활용해 임베딩 진행
        4. tiktoken의 get_encoding 개체를 활용해 토크나이저 객체 생성
        5. 'n_tokens' 컬럼에 데이터프레임 'text' 컬럼 데이터를 활용해 텍스트를 인코딩하고 인코딩한 텍스트의 길이를 저장
        '''
        import traceback

        df_texts = pd.DataFrame(texts)
        # embedding vector 생성
        df_texts.columns = ['page_no', 'text']
        df_texts['embedding'] = ''

        for i in range(len(df_texts)):
            try:

                df_texts['embedding'][i] = self.embedding_model.get_embeddings([df_texts['text'][i]])[0].values            
                
            except:
                _traceback = traceback.format_exc()
                print(f'value error {i} and error message {_traceback}')
                pass

        # token 추가
        tokenizer = tiktoken.get_encoding("cl100k_base")
        df_texts['n_tokens'] = df_texts["text"].apply(lambda x: len(tokenizer.encode(x)))
        return df_texts       
    
    def vector_search(self, query,collection, num_results=3):
        query_embedding =self.embedding_model.get_embeddings([query])
        embeddings_list = []
        pipeline = [
        {
            '$search': {
                "cosmosSearch": {
                    "vector": query_embedding[0].values,
                    "path": "embedding",
                    "k": num_results
                },
                "returnStoredSource": True }},
        {'$project': { 'similarityScore': { '$meta': 'searchScore' }, 'document' : '$$ROOT' } }
        ]
        results = collection.aggregate(pipeline)
        results_list = list(results)
        
        #response preprocessing
        res_data = []
        for i in range(num_results):
            res_text = results_list[i]['document']['text']
            res_data.append(res_text)
            
        return res_data
    
    def llm_response(self, context_data, user_query, temp=0.6):
        prompt= f'''
        Assistant is an intelligent chatbot designed to answer 'Delegation Approval Criteria' questions for employees of The DL-Chemical.
        Instructions :
        - Please only include the information from the Delegation Approval Criteria context below, and do not include any additional information.
        - If there is no information about the question in the Delegation Approval Criteria context below, please answer \"죄송합니다. 답변을 찾지 못했습니다.
        - Ignore outlier context that is not related to the question. Answer only the question that is asked.
        - Please clearly distinguish the words \"reflect(반영)\" and \"not reflect(미반영)\".
        - Please mark the next line when the sentence is over
        context:{context_data}
        role: user
        question: {user_query}
        '''
        print(prompt)
        response = self.llm_palm.predict(prompt, temperature=temp)
        return response



        






                

