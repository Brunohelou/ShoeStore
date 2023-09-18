'''
This script reads the database of information from local text files
and uses a large language model to answer questions about their content.
'''
# define n_ctx manually to permit larger contexts
n_gpu_layers = 40  # Metal set to 1 is enough.
n_batch = 516  # Should be between 1 and n_ctx, consider the amount of RAM of your chip

from langchain.llms import LlamaCpp
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory



callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

# prepare the template we will use when prompting the AI

# load the language model

#llm = CTransformers(model='./pytorch_model-00001-of-00002.bin',
#                    model_type='llama',
#                    batch_size = n_batch,
#                    config={'max_new_tokens': 2000, 'temperature': 0.01, "context_length": 5000, "gpu_layers": n_gpu_layers, "batch_size": n_batch})

llm = LlamaCpp(
    model_path='./remm-v2.1-l2-13b.Q4_K_M.gguf',
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    n_ctx=3000,
    max_tokens=1000,
    temperature=0,
    f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
    callback_manager=callback_manager,
    verbose=False,
   repeat_penalty=1.1,
)


# load the interpreted information from the local database
embeddings = HuggingFaceEmbeddings(
    model_name='sentence-transformers/all-MiniLM-L6-v2',
    model_kwargs={'device': 'cpu'})



new_db = FAISS.load_local('faiss', embeddings)


# prepare a version of the llm pre-loaded with the local content
retriever = new_db.as_retriever(search_kwargs={'k': 3})

template = '''
You are an sales assistant of a shoes store called "The Shoes".
Your introduction is: "Hello! Welcome to The Shoes Store! How can I assist you today?". You are allowed to make variations.
Only talk about shoes and the store.


History of you conversation with customer: {history}
Use the history of you conversation with customer as part of the context.

shoe models catalog: {context}
Only use shoe models data from the catalog. When it is not on the catalog, say you dont have that information.

When shoe age_range value is "KIDS", dont suggest for adults (older than 15).
When a shoe age_range value is "ADULT", dont suggest for kids (younger than 15).

When the question asks you for agregated information, say that your agregation is limited but you will do your best, and state that the best way for you to help is by providing information about the store or specific brands, shoes, or categories.
Dont provide counts of the catalog. Insted, ask for the customer to consult you about a model or to suggest some models based on a description.

Only provide the information of the shoes in the following format:  
< Name, Brand, age_range, cateogory, price, Availability, Image. >
 for example:< Superstar, Adidas, ADULT, CASUAL, $90, Available, https://assets.adidas.com/images/h_320,f_auto,q_auto:sensitive,fl_lossy/12365dbc7c424288b7cdab4900dc7099_9366/Superstar_Shoes_White_FW3553_FW3553_01_standard.jpg >
In the example, there is the name, brand, age_range, category, price, availability and the image.

Jump one line between one shoes model and the other.

Dont chage any information from the catalog.
Suggestions must match the requirements for age_range, brand, price and category.

Below is an instruction that describes a task. Write a response that appropriately completes the request.
### Instruction:
{question}
### Response:
'''
prompt = PromptTemplate(
    input_variables=['history', 'context', 'question'],
    template=template,
)


memory=ConversationBufferMemory(
            memory_key='history',
            input_key='question')

qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type='stuff',
    retriever=retriever,
    chain_type_kwargs={
        'prompt': prompt,
        'memory': memory,
    }
)


while 1==1:
    print('\n Send your message \n')
    question = input("Your message: ")
    print("AI answer:")
    qa.run({'query': question})






