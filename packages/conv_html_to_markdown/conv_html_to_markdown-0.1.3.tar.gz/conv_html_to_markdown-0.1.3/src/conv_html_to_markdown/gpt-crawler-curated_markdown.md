## Get started | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/expression_language/get_started)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Get started
Introduction
Installation
Quickstart
Security
LangChain Expression Language
Get started
Why use LCEL
Interface
How to
Cookbook
Modules
Model I/O
Retrieval
Agents
Chains
More
LangServe
LangSmith
LangGraph
LangChain Expression LanguageGet started
Get started

LCEL makes it easy to build complex chains from basic components, and supports out of the box functionality such as streaming, parallelism, and logging.

Basic example: prompt + model + output parser​

The most basic and common use case is chaining a prompt template and a model together. To see how this works, let’s create a chain that takes a topic and generates a joke:

%pip install –upgrade –quiet langchain-core langchain-community langchain-openai

from langchain\_core.output\_parsers import StrOutputParser
from langchain\_core.prompts import ChatPromptTemplate
from langchain\_openai import ChatOpenAI

prompt = ChatPromptTemplate.from\_template("tell me a short joke about {topic}")
model = ChatOpenAI(model="gpt-4")
output\_parser = StrOutputParser()

chain = prompt | model | output\_parser

chain.invoke({"topic": "ice cream"})

"Why don't ice creams ever get invited to parties?\n\nBecause they always drip when things heat up!"

Notice this line of this code, where we piece together then different components into a single chain using LCEL:

chain = prompt | model | output\_parser

The | symbol is similar to a unix pipe operator, which chains together the different components feeds the output from one component as input into the next component.

In this chain the user input is passed to the prompt template, then the prompt template output is passed to the model, then the model output is passed to the output parser. Let’s take a look at each component individually to really understand what’s going on.

1. Prompt​

prompt is a BasePromptTemplate, which means it takes in a dictionary of template variables and produces a PromptValue. A PromptValue is a wrapper around a completed prompt that can be passed to either an LLM (which takes a string as input) or ChatModel (which takes a sequence of messages as input). It can work with either language model type because it defines logic both for producing BaseMessages and for producing a string.

prompt\_value = prompt.invoke({"topic": "ice cream"})
prompt\_value

ChatPromptValue(messages=[HumanMessage(content='tell me a short joke about ice cream')])

prompt\_value.to\_messages()

[HumanMessage(content='tell me a short joke about ice cream')]

prompt\_value.to\_string()

'Human: tell me a short joke about ice cream'

2. Model​

The PromptValue is then passed to model. In this case our model is a ChatModel, meaning it will output a BaseMessage.

message = model.invoke(prompt\_value)
message
AIMessage(content="Why don't ice creams ever get invited to parties?\n\nBecause they always bring a melt down!")

If our model was an LLM, it would output a string.

from langchain\_openai.llms import OpenAI

llm = OpenAI(model="gpt-3.5-turbo-instruct")
llm.invoke(prompt\_value)

'\n\nRobot: Why did the ice cream truck break down? Because it had a meltdown!'

3. Output parser​

And lastly we pass our model output to the output\_parser, which is a BaseOutputParser meaning it takes either a string or a BaseMessage as input. The StrOutputParser specifically simple converts any input into a string.

output\_parser.invoke(message)

"Why did the ice cream go to therapy? \n\nBecause it had too many toppings and couldn't find its cone-fidence!"

4. Entire Pipeline​

To follow the steps along:

We pass in user input on the desired topic as {"topic": "ice cream"}
The prompt component takes the user input, which is then used to construct a PromptValue after using the topic to construct the prompt.
The model component takes the generated prompt, and passes into the OpenAI LLM model for evaluation. The generated output from the model is a ChatMessage object.
Dict
PromptValue
ChatMessage
String
Input: topic=ice cream
PromptTemplate
ChatModel
StrOutputParser
Result

Note that if you’re curious about the output of any components, you can always test out a smaller version of the chain such as prompt or prompt | model to see the intermediate results:

input = {"topic": "ice cream"}

prompt.invoke(input)
# > ChatPromptValue(messages=[HumanMessage(content='tell me a short joke about ice cream')])

(prompt | model).invoke(input)
# > AIMessage(content="Why did the ice cream go to therapy?\nBecause it had too many toppings and couldn't cone-trol itself!")

RAG Search Example​

For our next example, we want to run a retrieval-augmented generation chain to add some context when responding to questions.

# Requires:
# pip install langchain docarray tiktoken

from langchain\_community.vectorstores import DocArrayInMemorySearch
from langchain\_core.output\_parsers import StrOutputParser
from langchain\_core.prompts import ChatPromptTemplate
from langchain\_core.runnables import RunnableParallel, RunnablePassthrough
from langchain\_openai.chat\_models import ChatOpenAI
from langchain\_openai.embeddings import OpenAIEmbeddings

vectorstore = DocArrayInMemorySearch.from\_texts(
 ["harrison worked at kensho", "bears like to eat honey"],
 embedding=OpenAIEmbeddings(),
)
retriever = vectorstore.as\_retriever()

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from\_template(template)
model = ChatOpenAI()
output\_parser = StrOutputParser()

setup\_and\_retrieval = RunnableParallel(
 {"context": retriever, "question": RunnablePassthrough()}
)
chain = setup\_and\_retrieval | prompt | model | output\_parser

chain.invoke("where did harrison work?")

In this case, the composed chain is:

chain = setup\_and\_retrieval | prompt | model | output\_parser

To explain this, we first can see that the prompt template above takes in context and question as values to be substituted in the prompt. Before building the prompt template, we want to retrieve relevant documents to the search and include them as part of the context.

As a preliminary step, we’ve setup the retriever using an in memory store, which can retrieve documents based on a query. This is a runnable component as well that can be chained together with other components, but you can also try to run it separately:

retriever.invoke("where did harrison work?")

We then use the RunnableParallel to prepare the expected inputs into the prompt by using the entries for the retrieved documents as well as the original user question, using the retriever for document search, and RunnablePassthrough to pass the user’s question:

setup\_and\_retrieval = RunnableParallel(
 {"context": retriever, "question": RunnablePassthrough()}
)

To review, the complete chain is:

setup\_and\_retrieval = RunnableParallel(
 {"context": retriever, "question": RunnablePassthrough()}
)
chain = setup\_and\_retrieval | prompt | model | output\_parser

With the flow being:

The first steps create a RunnableParallel object with two entries. The first entry, context will include the document results fetched by the retriever. The second entry, question will contain the user’s original question. To pass on the question, we use RunnablePassthrough to copy this entry.
Feed the dictionary from the step above to the prompt component. It then takes the user input which is question as well as the retrieved document which is context to construct a prompt and output a PromptValue.
The model component takes the generated prompt, and passes into the OpenAI LLM model for evaluation. The generated output from the model is a ChatMessage object.
Question
context=retrieved docs
question=Question
PromptValue
ChatMessage
String
Question
RunnableParallel
Retriever
RunnablePassThrough
PromptTemplate
ChatModel
StrOutputParser
Result
Next steps​

We recommend reading our Why use LCEL section next to see a side-by-side comparison of the code needed to produce common functionality with and without LCEL.

LangChain Expression Language (LCEL)
Next
Why use LCEL
Basic example: prompt + model + output parser
1. Prompt
3. Output parser
4. Entire Pipeline
RAG Search Example
Next steps
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## LangChain Expression Language (LCEL) | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/expression_language/)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Get started
Introduction
Installation
Quickstart
Security
LangChain Expression Language
Get started
Why use LCEL
Interface
How to
Cookbook
Modules
Model I/O
Retrieval
Agents
Chains
More
LangServe
LangSmith
LangGraph
LangChain Expression Language

LangChain Expression Language, or LCEL, is a declarative way to easily compose chains together. LCEL was designed from day 1 to support putting prototypes in production, with no code changes, from the simplest “prompt + LLM” chain to the most complex chains (we’ve seen folks successfully run LCEL chains with 100s of steps in production). To highlight a few of the reasons you might want to use LCEL:

Streaming support When you build your chains with LCEL you get the best possible time-to-first-token (time elapsed until the first chunk of output comes out). For some chains this means eg. we stream tokens straight from an LLM to a streaming output parser, and you get back parsed, incremental chunks of output at the same rate as the LLM provider outputs the raw tokens.

Async support Any chain built with LCEL can be called both with the synchronous API (eg. in your Jupyter notebook while prototyping) as well as with the asynchronous API (eg. in a LangServe server). This enables using the same code for prototypes and in production, with great performance, and the ability to handle many concurrent requests in the same server.

Optimized parallel execution Whenever your LCEL chains have steps that can be executed in parallel (eg if you fetch documents from multiple retrievers) we automatically do it, both in the sync and the async interfaces, for the smallest possible latency.

Retries and fallbacks Configure retries and fallbacks for any part of your LCEL chain. This is a great way to make your chains more reliable at scale. We’re currently working on adding streaming support for retries/fallbacks, so you can get the added reliability without any latency cost.

Access intermediate results For more complex chains it’s often very useful to access the results of intermediate steps even before the final output is produced. This can be used to let end-users know something is happening, or even just to debug your chain. You can stream intermediate results, and it’s available on every LangServe server.

Input and output schemas Input and output schemas give every LCEL chain Pydantic and JSONSchema schemas inferred from the structure of your chain. This can be used for validation of inputs and outputs, and is an integral part of LangServe.

Seamless LangSmith tracing integration As your chains get more and more complex, it becomes increasingly important to understand what exactly is happening at every step. With LCEL, all steps are automatically logged to LangSmith for maximum observability and debuggability.

Seamless LangServe deployment integration Any chain created with LCEL can be easily deployed using LangServe.

Security
Next
Get started
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Security | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/security)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Get started
Introduction
Installation
Quickstart
Security
LangChain Expression Language
Get started
Why use LCEL
Interface
How to
Cookbook
Modules
Model I/O
Retrieval
Agents
Chains
More
LangServe
LangSmith
LangGraph
Get startedSecurity
Security

LangChain has a large ecosystem of integrations with various external resources like local and remote file systems, APIs and databases. These integrations allow developers to create versatile applications that combine the power of LLMs with the ability to access, interact with and manipulate external resources.

Best Practices​

When building such applications developers should remember to follow good security practices:

Limit Permissions: Scope permissions specifically to the application's need. Granting broad or excessive permissions can introduce significant security vulnerabilities. To avoid such vulnerabilities, consider using read-only credentials, disallowing access to sensitive resources, using sandboxing techniques (such as running inside a container), etc. as appropriate for your application.

Risks of not doing so include, but are not limited to:

Data corruption or loss.
Unauthorized access to confidential information.
Compromised performance or availability of critical resources.

Example scenarios with mitigation strategies:

A user may ask an agent with access to the file system to delete files that should not be deleted or read the content of files that contain sensitive information. To mitigate, limit the agent to only use a specific directory and only allow it to read or write files that are safe to read or write. Consider further sandboxing the agent by running it in a container.

If you're building applications that access external resources like file systems, APIs or databases, consider speaking with your company's security team to determine how to best design and secure your applications.

Reporting a Vulnerability​

Please report security vulnerabilities by email to security@langchain.dev. This will ensure the issue is promptly triaged and acted upon as needed.

Enterprise solutions​

LangChain may offer enterprise solutions for customers who have additional security requirements. Please contact us at sales@langchain.dev.

Quickstart
Next
LangChain Expression Language (LCEL)
Best Practices
Reporting a Vulnerability
Enterprise solutions
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Quickstart | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/get_started/quickstart)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Get started
Introduction
Installation
Quickstart
Security
LangChain Expression Language
Get started
Why use LCEL
Interface
How to
Cookbook
Modules
Model I/O
Retrieval
Agents
Chains
More
LangServe
LangSmith
LangGraph
Get startedQuickstart
Quickstart

In this quickstart we'll show you how to:

Get setup with LangChain, LangSmith and LangServe
Use the most basic and common components of LangChain: prompt templates, models, and output parsers
Use LangChain Expression Language, the protocol that LangChain is built on and which facilitates component chaining
Build a simple application with LangChain
Trace your application with LangSmith

That's a fair amount to cover! Let's dive in.

Setup​
Jupyter Notebook​

This guide (and most of the other guides in the documentation) use Jupyter notebooks and assume the reader is as well. Jupyter notebooks are perfect for learning how to work with LLM systems because often times things can go wrong (unexpected output, API down, etc) and going through guides in an interactive environment is a great way to better understand them.

You do not NEED to go through the guide in a Jupyter Notebook, but it is recommended. See here for instructions on how to install.

Installation​

To install LangChain run:

Pip
Conda
pip install langchain

For more details, see our Installation guide.

LangSmith​

Many of the applications you build with LangChain will contain multiple steps with multiple invocations of LLM calls. As these applications get more and more complex, it becomes crucial to be able to inspect what exactly is going on inside your chain or agent. The best way to do this is with LangSmith.

Note that LangSmith is not needed, but it is helpful. If you do want to use LangSmith, after you sign up at the link above, make sure to set your environment variables to start logging traces:

export LANGCHAIN\_TRACING\_V2="true"

Building with LangChain​

LangChain enables building application that connect external sources of data and computation to LLMs. In this quickstart, we will walk through a few different ways of doing that. We will start with a simple LLM chain, which just relies on information in the prompt template to respond. Next, we will build a retrieval chain, which fetches data from a separate database and passes that into the prompt template. We will then add in chat history, to create a conversation retrieval chain. This allows you interact in a chat manner with this LLM, so it remembers previous questions. Finally, we will build an agent - which utilizes and LLM to determine whether or not it needs to fetch data to answer questions. We will cover these at a high level, but there are lot of details to all of these! We will link to relevant docs.

LLM Chain​

For this getting started guide, we will provide two options: using OpenAI (a popular model available via API) or using a local open source model.

OpenAI
Local

First we'll need to import the LangChain x OpenAI integration package.

pip install langchain-openai

Accessing the API requires an API key, which you can get by creating an account and heading here. Once we have a key we'll want to set it as an environment variable by running:

export OPENAI\_API\_KEY="..."

We can then initialize the model:

from langchain\_openai import ChatOpenAI

llm = ChatOpenAI()

If you'd prefer not to set an environment variable you can pass the key in directly via the openai\_api\_key named parameter when initiating the OpenAI LLM class:

from langchain\_openai import ChatOpenAI

llm = ChatOpenAI(openai\_api\_key="...")

Once you've installed and initialized the LLM of your choice, we can try using it! Let's ask it what LangSmith is - this is something that wasn't present in the training data so it shouldn't have a very good response.

llm.invoke("how can langsmith help with testing?")

We can also guide it's response with a prompt template. Prompt templates are used to convert raw user input to a better input to the LLM.

from langchain\_core.prompts import ChatPromptTemplate
 ("system", "You are world class technical documentation writer."),
 ("user", "{input}")
])

We can now combine these into a simple LLM chain:

chain = prompt | llm 

We can now invoke it and ask the same question. It still won't know the answer, but it should respond in a more proper tone for a technical writer!

chain.invoke({"input": "how can langsmith help with testing?"})

The output of a ChatModel (and therefore, of this chain) is a message. However, it's often much more convenient to work with strings. Let's add a simple output parser to convert the chat message to a string.

from langchain\_core.output\_parsers import StrOutputParser

output\_parser = StrOutputParser()

We can now add this to the previous chain:

chain = prompt | llm | output\_parser

We can now invoke it and ask the same question. The answer will now be a string (rather than a ChatMessage).

chain.invoke({"input": "how can langsmith help with testing?"})

Diving Deeper​

We've now successfully set up a basic LLM chain. We only touched on the basics of prompts, models, and output parsers - for a deeper dive into everything mentioned here, see this section of documentation.

Retrieval Chain​

In order to properly answer the original question ("how can langsmith help with testing?"), we need to provide additional context to the LLM. We can do this via retrieval. Retrieval is useful when you have too much data to pass to the LLM directly. You can then use a retriever to fetch only the most relevant pieces and pass those in.

In this process, we will look up relevant documents from a Retriever and then pass them into the prompt. A Retriever can be backed by anything - a SQL table, the internet, etc - but in this instance we will populate a vector store and use that as a retriever. For more information on vectorstores, see this documentation.

First, we need to load the data that we want to index. In order to do this, we will use the WebBaseLoader. This requires installing BeautifulSoup:

```shell
pip install beautifulsoup4

After that, we can import and use WebBaseLoader.

from langchain\_community.document\_loaders import WebBaseLoader
loader = WebBaseLoader("https://docs.smith.langchain.com/overview")

docs = loader.load()

Next, we need to index it into a vectorstore. This requires a few components, namely an embedding model and a vectorstore.

For embedding models, we once again provide examples for accessing via OpenAI or via local models.

OpenAI
Local
Make sure you have the `langchain\_openai` package installed an the appropriate environment variables set (these are the same as needed for the LLM).
from langchain\_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

Now, we can use this embedding model to ingest documents into a vectorstore. We will use a simple local vectorstore, FAISS, for simplicity's sake.

First we need to install the required packages for that:

pip install faiss-cpu

Then we can build our index:

from langchain\_community.vectorstores import FAISS
from langchain.text\_splitter import RecursiveCharacterTextSplitter

text\_splitter = RecursiveCharacterTextSplitter()
documents = text\_splitter.split\_documents(docs)

Now that we have this data indexed in a vectorstore, we will create a retrieval chain. This chain will take an incoming question, look up relevant documents, then pass those documents along with the original question into an LLM and ask it to answer the original question.

First, let's set up the chain that takes a question and the retrieved documents and generates an answer.

from langchain.chains.combine\_documents import create\_stuff\_documents\_chain

prompt = ChatPromptTemplate.from\_template("""Answer the following question based only on the provided context:

{context}

Question: {input}""")

document\_chain = create\_stuff\_documents\_chain(llm, prompt)

If we wanted to, we could run this ourselves by passing in documents directly:

from langchain\_core.documents import Document

document\_chain.invoke({
 "input": "how can langsmith help with testing?",
 "context": [Document(page\_content="langsmith can let you visualize test results")]
})

However, we want the documents to first come from the retriever we just set up. That way, for a given question we can use the retriever to dynamically select the most relevant documents and pass those in.

from langchain.chains import create\_retrieval\_chain

retriever = vector.as\_retriever()
retrieval\_chain = create\_retrieval\_chain(retriever, document\_chain)

We can now invoke this chain. This returns a dictionary - the response from the LLM is in the answer key

response = retrieval\_chain.invoke({"input": "how can langsmith help with testing?"})
print(response["answer"])

# LangSmith offers several features that can help with testing:...

This answer should be much more accurate!

Diving Deeper​

We've now successfully set up a basic retrieval chain. We only touched on the basics of retrieval - for a deeper dive into everything mentioned here, see this section of documentation.

Conversation Retrieval Chain​

The chain we've created so far can only answer single questions. One of the main types of LLM applications that people are building are chat bots. So how do we turn this chain into one that can answer follow up questions?

We can still use the create\_retrieval\_chain function, but we need to change two things:

The retrieval method should now not just work on the most recent input, but rather should take the whole history into account.
The final LLM chain should likewise take the whole history into account

Updating Retrieval

In order to update retrieval, we will create a new chain. This chain will take in the most recent input (input) and the conversation history (chat\_history) and use an LLM to generate a search query.

from langchain.chains import create\_history\_aware\_retriever
from langchain\_core.prompts import MessagesPlaceholder

# First we need a prompt that we can pass into an LLM to generate this search query

prompt = ChatPromptTemplate.from\_messages([
 MessagesPlaceholder(variable\_name="chat\_history"),
 ("user", "{input}"),
 ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
])
retriever\_chain = create\_history\_aware\_retriever(llm, retriever, prompt)

We can test this out by passing in an instance where the user is asking a follow up question.

from langchain\_core.messages import HumanMessage, AIMessage

chat\_history = [HumanMessage(content="Can LangSmith help test my LLM applications?"), AIMessage(content="Yes!")]
retriever\_chain.invoke({
 "chat\_history": chat\_history,
 "input": "Tell me how"
})

You should see that this returns documents about testing in LangSmith. This is because the LLM generated a new query, combining the chat history with the follow up question.

Now that we have this new retriever, we can create a new chain to continue the conversation with these retrieved documents in mind.

prompt = ChatPromptTemplate.from\_messages([
 ("system", "Answer the user's questions based on the below context:\n\n{context}"),
 MessagesPlaceholder(variable\_name="chat\_history"),
 ("user", "{input}"),
])
document\_chain = create\_stuff\_documents\_chain(llm, prompt)

retrieval\_chain = create\_retrieval\_chain(retriever\_chain, document\_chain)

We can now test this out end-to-end:

chat\_history = [HumanMessage(content="Can LangSmith help test my LLM applications?"), AIMessage(content="Yes!")]
retrieval\_chain.invoke({
 "chat\_history": chat\_history,
 "input": "Tell me how"
})

We can see that this gives a coherent answer - we've successfully turned our retrieval chain into a chatbot!

Agent​

We've so far create examples of chains - where each step is known ahead of time. The final thing we will create is an agent - where the LLM decides what steps to take.

NOTE: for this example we will only show how to create an agent using OpenAI models, as local models are not reliable enough yet.

One of the first things to do when building an agent is to decide what tools it should have access to. For this example, we will give the agent access two tools:

The retriever we just created. This will let it easily answer questions about LangSmith
A search tool. This will let it easily answer questions that require up to date information.

First, let's set up a tool for the retriever we just created:

from langchain.tools.retriever import create\_retriever\_tool

retriever\_tool = create\_retriever\_tool(
 retriever,
 "langsmith\_search",
 "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
)

The search tool that we will use is Tavily. This will require an API key (they have generous free tier). After creating it on their platform, you need to set it as an environment variable:

export TAVILY\_API\_KEY=...

If you do not want to set up an API key, you can skip creating this tool.

from langchain\_community.tools.tavily\_search import TavilySearchResults

search = TavilySearchResults()

We can now create a list of the tools we want to work with:

tools = [retriever\_tool, search]

Now that we have the tools, we can create an agent to use them. We will go over this pretty quickly - for a deeper dive into what exactly is going on, check out the Agent's Getting Started documentation

Install langchain hub first

pip install langchainhub

Now we can use it to get a predefined prompt

from langchain\_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create\_openai\_functions\_agent
from langchain.agents import AgentExecutor

# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/openai-functions-agent")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent = create\_openai\_functions\_agent(llm, tools, prompt)
agent\_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

We can now invoke the agent and see how it responds! We can ask it questions about LangSmith:

agent\_executor.invoke({"input": "how can langsmith help with testing?"})

We can ask it about the weather:

agent\_executor.invoke({"input": "what is the weather in SF?"})

We can have conversations with it:

chat\_history = [HumanMessage(content="Can LangSmith help test my LLM applications?"), AIMessage(content="Yes!")]
agent\_executor.invoke({
 "chat\_history": chat\_history,
 "input": "Tell me how"
})

Diving Deeper​

We've now successfully set up a basic agent. We only touched on the basics of agents - for a deeper dive into everything mentioned here, see this section of documentation.

Serving with LangServe​

Now that we've built an application, we need to serve it. That's where LangServe comes in. LangServe helps developers deploy LangChain chains as a REST API. You do not need to use LangServe to use LangChain, but in this guide we'll show how you can deploy your app with LangServe.

While the first part of this guide was intended to be run in a Jupyter Notebook, we will now move out of that. We will be creating a Python file and then interacting with it from the command line.

Install with:

pip install "langserve[all]"

Server​

To create a server for our application we'll make a serve.py file. This will contain our logic for serving our application. It consists of three things:

The definition of our chain that we just built above
Our FastAPI app
A definition of a route from which to serve the chain, which is done with langserve.add\_routes
#!/usr/bin/env python
from typing import List

from fastapi import FastAPI
from langchain\_core.prompts import ChatPromptTemplate
from langchain\_openai import ChatOpenAI
from langchain\_community.document\_loaders import WebBaseLoader
from langchain\_openai import OpenAIEmbeddings
from langchain.text\_splitter import RecursiveCharacterTextSplitter
from langchain.tools.retriever import create\_retriever\_tool
from langchain\_community.tools.tavily\_search import TavilySearchResults
from langchain\_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create\_openai\_functions\_agent
from langchain.agents import AgentExecutor
from langchain.pydantic\_v1 import BaseModel, Field
from langserve import add\_routes

# 1. Load Retriever
loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
docs = loader.load()
text\_splitter = RecursiveCharacterTextSplitter()
documents = text\_splitter.split\_documents(docs)
embeddings = OpenAIEmbeddings()
vector = FAISS.from\_documents(documents, embeddings)
retriever = vector.as\_retriever()

# 2. Create Tools
retriever\_tool = create\_retriever\_tool(
 retriever,
 "langsmith\_search",
 "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
)
search = TavilySearchResults()
tools = [retriever\_tool, search]

# 3. Create Agent
prompt = hub.pull("hwchase17/openai-functions-agent")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent = create\_openai\_functions\_agent(llm, tools, prompt)
agent\_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 4. App definition
app = FastAPI(
 title="LangChain Server",
 version="1.0",
 description="A simple API server using LangChain's Runnable interfaces",
)

# 5. Adding chain route

# We need to add these input/output schemas because the current AgentExecutor
# is lacking in schemas.

class Input(BaseModel):
 input: str
 chat\_history: List[BaseMessage] = Field(
 ...,
 extra={"widget": {"type": "chat", "input": "location"}},
 )

class Output(BaseModel):
 output: str

add\_routes(
 app,
 agent\_executor.with\_types(input\_type=Input, output\_type=Output),
 path="/agent",
)

if \_\_name\_\_ == "\_\_main\_\_":
 import uvicorn

 uvicorn.run(app, host="localhost", port=8000)

And that's it! If we execute this file:

python serve.py

we should see our chain being served at localhost:8000.

Every LangServe service comes with a simple built-in UI for configuring and invoking the application with streaming output and visibility into intermediate steps. Head to http://localhost:8000/agent/playground/ to try it out! Pass in the same question as before - "how can langsmith help with testing?" - and it should respond same as before.

Client​

Now let's set up a client for programmatically interacting with our service. We can easily do this with the [langserve.RemoteRunnable](/docs/langserve#client). Using this, we can interact with the served chain as if it were running client-side.

from langserve import RemoteRunnable

remote\_chain = RemoteRunnable("http://localhost:8000/agent/")
remote\_chain.invoke({"input": "how can langsmith help with testing?"})

To learn more about the many other features of LangServe head here.

Next steps​

We've touched on how to build an application with LangChain, how to trace it with LangSmith, and how to serve it with LangServe. There are a lot more features in all three of these than we can cover here. To continue on your journey, we recommend you read the following (in order):

All of these features are backed by LangChain Expression Language (LCEL) - a way to chain these components together. Check out that documentation to better understand how to create custom chains.
Model IO covers more details of prompts, LLMs, and output parsers.
Retrieval covers more details of everything related to retrieval
Agents covers details of everything related to agents
Explore common end-to-end use cases and template applications
Read up on LangSmith, the platform for debugging, testing, monitoring and more
Learn more about serving your applications with LangServe
Previous
Installation
Next
Security
Setup
Jupyter Notebook
Installation
LangSmith
Building with LangChain
LLM Chain
Diving Deeper
Retrieval Chain
Diving Deeper
Conversation Retrieval Chain
Agent
Diving Deeper
Serving with LangServe
Server
Next steps
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Installation | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/get_started/installation)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Get started
Introduction
Installation
Quickstart
Security
LangChain Expression Language
Get started
Why use LCEL
Interface
How to
Cookbook
Modules
Model I/O
Retrieval
Agents
Chains
More
LangServe
LangSmith
LangGraph
Get startedInstallation
Installation
Official release​

To install LangChain run:

Pip
Conda
pip install langchain

This will install the bare minimum requirements of LangChain. A lot of the value of LangChain comes when integrating it with various model providers, datastores, etc. By default, the dependencies needed to do that are NOT installed. You will need to install the dependencies for specific integrations separately.

From source​

If you want to install from source, you can do so by cloning the repo and be sure that the directory is PATH/TO/REPO/langchain/libs/langchain running:

pip install -e .

LangChain community​

The langchain-community package contains third-party integrations. It is automatically installed by langchain, but can also be used separately. Install with:

pip install langchain-community

LangChain core​

The langchain-core package contains base abstractions that the rest of the LangChain ecosystem uses, along with the LangChain Expression Language. It is automatically installed by langchain, but can also be used separately. Install with:

pip install langchain-core

LangChain experimental​

The langchain-experimental package holds experimental LangChain code, intended for research and experimental uses. Install with:

pip install langchain-experimental

LangServe​

LangServe helps developers deploy LangChain runnables and chains as a REST API. LangServe is automatically installed by LangChain CLI. If not using LangChain CLI, install with:

pip install "langserve[all]"

for both client and server dependencies. Or pip install "langserve[client]" for client code, and pip install "langserve[server]" for server code.

LangChain CLI​

The LangChain CLI is useful for working with LangChain templates and other LangServe projects. Install with:

pip install langchain-cli

LangSmith SDK​

The LangSmith SDK is automatically installed by LangChain. If not using LangChain, install with:

pip install langsmith

Introduction
Next
Quickstart
Official release
From source
LangChain community
LangServe
LangChain CLI
LangSmith SDK
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Get started | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/get_started)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Get started
Introduction
Installation
Quickstart
Security
LangChain Expression Language
Get started
Why use LCEL
Interface
How to
Cookbook
Modules
Model I/O
Retrieval
Agents
Chains
More
LangServe
LangSmith
LangGraph
Get started

Get started with LangChain

📄️ Introduction

LangChain is a framework for developing applications powered by language models. It enables applications that:

📄️ Installation

Official release

📄️ Quickstart

In this quickstart we'll show you how to:

📄️ Security

LangChain has a large ecosystem of integrations with various external resources like local and remote file systems, APIs and databases. These integrations allow developers to create versatile applications that combine the power of LLMs with the ability to access, interact with and manipulate external resources.

Next
Introduction
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## YouTube videos | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/additional_resources/youtube)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
YouTube videos

⛓ icon marks a new addition [last update 2023-09-21]

Official LangChain YouTube channel​
Introduction to LangChain with Harrison Chase, creator of LangChain​
Building the Future with LLMs, LangChain, & Pinecone by Pinecone
LangChain and Weaviate with Harrison Chase and Bob van Luijt - Weaviate Podcast #36 by Weaviate • Vector Database
LangChain Demo + Q&A with Harrison Chase by Full Stack Deep Learning
LangChain Agents: Build Personal Assistants For Your Data (Q&A with Harrison Chase and Mayo Oshin) by Chat with data
Videos (sorted by views)​
Using ChatGPT with YOUR OWN Data. This is magical. (LangChain OpenAI API) by TechLead
First look - ChatGPT + WolframAlpha (GPT-3.5 and Wolfram|Alpha via LangChain by James Weaver) by Dr Alan D. Thompson
LangChain explained - The hottest new Python framework by AssemblyAI
Chatbot with INFINITE MEMORY using OpenAI & Pinecone - GPT-3, Embeddings, ADA, Vector DB, Semantic by David Shapiro ~ AI
LangChain for LLMs is... basically just an Ansible playbook by David Shapiro ~ AI
Build your own LLM Apps with LangChain & GPT-Index by 1littlecoder
BabyAGI - New System of Autonomous AI Agents with LangChain by 1littlecoder
Run BabyAGI with Langchain Agents (with Python Code) by 1littlecoder
How to Use Langchain With Zapier | Write and Send Email with GPT-3 | OpenAI API Tutorial by StarMorph AI
Use Your Locally Stored Files To Get Response From GPT - OpenAI | Langchain | Python by Shweta Lodha
Langchain JS | How to Use GPT-3, GPT-4 to Reference your own Data | OpenAI Embeddings Intro by StarMorph AI
The easiest way to work with large language models | Learn LangChain in 10min by Sophia Yang
4 Autonomous AI Agents: “Westworld” simulation BabyAGI, AutoGPT, Camel, LangChain by Sophia Yang
AI CAN SEARCH THE INTERNET? Langchain Agents + OpenAI ChatGPT by tylerwhatsgood
Query Your Data with GPT-4 | Embeddings, Vector Databases | Langchain JS Knowledgebase by StarMorph AI
Weaviate + LangChain for LLM apps presented by Erika Cardenas by Weaviate • Vector Database
Langchain Overview — How to Use Langchain & ChatGPT by Python In Office
LangChain Tutorials by Edrick:
LangChain, Chroma DB, OpenAI Beginner Guide | ChatGPT with your PDF
LangChain 101: The Complete Beginner's Guide
Custom langchain Agent & Tools with memory. Turn any Python function into langchain tool with Gpt 3 by echohive
Building AI LLM Apps with LangChain (and more?) - LIVE STREAM by Nicholas Renotte
ChatGPT with any YouTube video using langchain and chromadb by echohive
How to Talk to a PDF using LangChain and ChatGPT by Automata Learning Lab
Langchain Document Loaders Part 1: Unstructured Files by Merk
LangChain - Prompt Templates (what all the best prompt engineers use) by Nick Daigler
LangChain. Crear aplicaciones Python impulsadas por GPT by Jesús Conde
Easiest Way to Use GPT In Your Products | LangChain Basics Tutorial by Rachel Woods
BabyAGI + GPT-4 Langchain Agent with Internet Access by tylerwhatsgood
Learning LLM Agents. How does it actually work? LangChain, AutoGPT & OpenAI by Arnoldas Kemeklis
Get Started with LangChain in Node.js by Developers Digest
LangChain + OpenAI tutorial: Building a Q&A system w/ own text data by Samuel Chan
Langchain + Zapier Agent by Merk
Connecting the Internet with ChatGPT (LLMs) using Langchain And Answers Your Questions by Kamalraj M M
Build More Powerful LLM Applications for Business’s with LangChain (Beginners Guide) by No Code Blackbox
LangFlow LLM Agent Demo for 🦜🔗LangChain by Cobus Greyling
Chatbot Factory: Streamline Python Chatbot Creation with LLMs and Langchain by Finxter
Chat with a CSV | LangChain Agents Tutorial (Beginners) by GoDataProf
Introdução ao Langchain - #Cortes - Live DataHackers by Prof. João Gabriel Lima
LangChain: Level up ChatGPT !? | LangChain Tutorial Part 1 by Code Affinity
KI schreibt krasses Youtube Skript 😲😳 | LangChain Tutorial Deutsch by SimpleKI
Chat with Audio: Langchain, Chroma DB, OpenAI, and Assembly AI by AI Anytime
QA over documents with Auto vector index selection with Langchain router chains by echohive
Build your own custom LLM application with Bubble.io & Langchain (No Code & Beginner friendly) by No Code Blackbox
Simple App to Question Your Docs: Leveraging Streamlit, Hugging Face Spaces, LangChain, and Claude! by Chris Alexiuk
LANGCHAIN AI- ConstitutionalChainAI + Databutton AI ASSISTANT Web App by Avra
The Future of Data Analysis: Using A.I. Models in Data Analysis (LangChain) by Absent Data
Memory in LangChain | Deep dive (python) by Eden Marco
9 LangChain UseCases | Beginner's Guide | 2023 by Data Science Basics
Use Large Language Models in Jupyter Notebook | LangChain | Agents & Indexes by Abhinaw Tiwari
How to Talk to Your Langchain Agent | 11 Labs + Whisper by VRSEN
LangChain Deep Dive: 5 FUN AI App Ideas To Build Quickly and Easily by James NoCode
LangChain 101: Models by Mckay Wrigley
LangChain with JavaScript Tutorial #1 | Setup & Using LLMs by Leon van Zyl
LangChain Overview & Tutorial for Beginners: Build Powerful AI Apps Quickly & Easily (ZERO CODE) by James NoCode
LangChain In Action: Real-World Use Case With Step-by-Step Tutorial by Rabbitmetrics
Summarizing and Querying Multiple Papers with LangChain by Automata Learning Lab
Using Langchain (and Replit) through Tana, ask Google/Wikipedia/Wolfram Alpha to fill out a table by Stian Håklev
Langchain PDF App (GUI) | Create a ChatGPT For Your PDF in Python by Alejandro AO - Software & Ai
Auto-GPT with LangChain 🔥 | Create Your Own Personal AI Assistant by Data Science Basics
Create Your OWN Slack AI Assistant with Python & LangChain by Dave Ebbelaar
How to Create LOCAL Chatbots with GPT4All and LangChain [Full Guide] by Liam Ottley
Build a Multilingual PDF Search App with LangChain, Cohere and Bubble by Menlo Park Lab
LangChain Memory Tutorial | Building a ChatGPT Clone in Python by Alejandro AO - Software & Ai
Llama Index: Chat with Documentation using URL Loader by Merk
Using OpenAI, LangChain, and Gradio to Build Custom GenAI Applications by David Hundley
LangChain, Chroma DB, OpenAI Beginner Guide | ChatGPT with your PDF
Build AI chatbot with custom knowledge base using OpenAI API and GPT Index by Irina Nik
Build Your Own Auto-GPT Apps with LangChain (Python Tutorial) by Dave Ebbelaar
Chat with Multiple PDFs | LangChain App Tutorial in Python (Free LLMs and Embeddings) by Alejandro AO - Software & Ai
Flowise is an open-source no-code UI visual tool to build 🦜🔗LangChain applications by Cobus Greyling
LangChain & GPT 4 For Data Analysis: The Pandas Dataframe Agent by Rabbitmetrics
GirlfriendGPT - AI girlfriend with LangChain by Toolfinder AI
How to build with Langchain 10x easier | ⛓️ LangFlow & Flowise by AI Jason
Getting Started With LangChain In 20 Minutes- Build Celebrity Search Application by Krish Naik
⛓ Vector Embeddings Tutorial – Code Your Own AI Assistant with GPT-4 API + LangChain + NLP by FreeCodeCamp.org
⛓ Fully LOCAL Llama 2 Q&A with LangChain by 1littlecoder
⛓ Build LangChain Audio Apps with Python in 5 Minutes by AssemblyAI
⛓ Voiceflow & Flowise: Want to Beat Competition? New Tutorial with Real AI Chatbot by AI SIMP
⛓ THIS Is How You Build Production-Ready AI Apps (LangSmith Tutorial) by Dave Ebbelaar
⛓ Build POWERFUL LLM Bots EASILY with Your Own Data - Embedchain - Langchain 2.0? (Tutorial) by WorldofAI
⛓ Code Llama powered Gradio App for Coding: Runs on CPU by AI Anytime
⛓ LangChain Complete Course in One Video | Develop LangChain (AI) Based Solutions for Your Business by UBprogrammer
⛓ How to Run LLaMA Locally on CPU or GPU | Python & Langchain & CTransformers Guide by Code With Prince
⛓ PyData Heidelberg #11 - TimeSeries Forecasting & LLM Langchain by PyData
⛓ Prompt Engineering in Web Development | Using LangChain and Templates with OpenAI by Akamai Developer
⛓ Retrieval-Augmented Generation (RAG) using LangChain and Pinecone - The RAG Special Episode by Generative AI and Data Science On AWS
⛓ LLAMA2 70b-chat Multiple Documents Chatbot with Langchain & Streamlit |All OPEN SOURCE|Replicate API by DataInsightEdge
⛓ Chatting with 44K Fashion Products: LangChain Opportunities and Pitfalls by Rabbitmetrics
⛓ Structured Data Extraction from ChatGPT with LangChain by MG
⛓ Chat with Multiple PDFs using Llama 2, Pinecone and LangChain (Free LLMs and Embeddings) by Muhammad Moin
⛓ Integrate Audio into LangChain.js apps in 5 Minutes by AssemblyAI
⛓ ChatGPT for your data with Local LLM by Jacob Jedryszek
⛓ Training Chatgpt with your personal data using langchain step by step in detail by NextGen Machines
⛓ Use ANY language in LangSmith with REST by Nerding I/O
⛓ How to Leverage the Full Potential of LLMs for Your Business with Langchain - Leon Ruddat by PyData
⛓ ChatCSV App: Chat with CSV files using LangChain and Llama 2 by Muhammad Moin
Prompt Engineering and LangChain by Venelin Valkov​
Getting Started with LangChain: Load Custom Data, Run OpenAI Models, Embeddings and ChatGPT
LangChain Models: ChatGPT, Flan Alpaca, OpenAI Embeddings, Prompt Templates & Streaming
LangChain Chains: Use ChatGPT to Build Conversational Agents, Summaries and Q&A on Text With LLMs
Analyze Custom CSV Data with GPT-4 using Langchain
Build ChatGPT Chatbots with LangChain Memory: Understanding and Implementing Memory in Conversations

⛓ icon marks a new addition [last update 2023-09-21]

Official LangChain YouTube channel
Introduction to LangChain with Harrison Chase, creator of LangChain
Videos (sorted by views)
Prompt Engineering and LangChain by Venelin Valkov
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Tutorials | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/additional_resources/tutorials)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Tutorials

Below are links to tutorials and courses on LangChain. For written guides on common use cases for LangChain, check out the use cases guides.

⛓ icon marks a new addition [last update 2023-09-21]

LangChain on Wikipedia​
Books​
⛓Generative AI with LangChain by Ben Auffrath, ©️ 2023 Packt Publishing​
DeepLearning.AI courses​

by Harrison Chase and Andrew Ng

LangChain for LLM Application Development
LangChain Chat with Your Data
⛓ Functions, Tools and Agents with LangChain
Handbook​

LangChain AI Handbook By James Briggs and Francisco Ingham

Short Tutorials​

LangChain Explained in 13 Minutes | QuickStart Tutorial for Beginners by Rabbitmetrics

LangChain Crash Course: Build an AutoGPT app in 25 minutes by Nicholas Renotte

LangChain Crash Course - Build apps with language models by Patrick Loeber

Tutorials​
LangChain for Gen AI and LLMs by James Briggs​
#1 Getting Started with GPT-3 vs. Open Source LLMs
#2 Prompt Templates for GPT 3.5 and other LLMs
LangChain Data Loaders, Tokenizers, Chunking, and Datasets - Data Prep 101
#4 Chatbot Memory for Chat-GPT, Davinci + other LLMs
#5 Chat with OpenAI in LangChain
#6 Fixing LLM Hallucinations with Retrieval Augmentation in LangChain
#7 LangChain Agents Deep Dive with GPT 3.5
#8 Create Custom Tools for Chatbots in LangChain
#9 Build Conversational Agents with Vector DBs
Using NEW MPT-7B in Hugging Face and LangChain
⛓ Fine-tuning OpenAI's GPT 3.5 for LangChain Agents
⛓ Chatbots with RAG: LangChain Full Walkthrough
LangChain 101 by Greg Kamradt (Data Indy)​
What Is LangChain? - LangChain + ChatGPT Overview
Quickstart Guide
Beginner's Guide To 7 Essential Concepts
Agents Overview + Google Searches
OpenAI + Wolfram Alpha
Ask Questions On Your Custom (or Private) Files
Connect Google Drive Files To OpenAI
YouTube Transcripts + OpenAI
Question A 300 Page Book (w/ OpenAI + Pinecone)
Workaround OpenAI's Token Limit With Chain Types
Build Your Own OpenAI + LangChain Web App in 23 Minutes
Working With The New ChatGPT API
OpenAI + LangChain Wrote Me 100 Custom Sales Emails
Structured Output From OpenAI (Clean Dirty Data)
Connect OpenAI To +5,000 Tools (LangChain + Zapier)
Use LLMs To Extract Data From Text (Expert Mode)
Extract Insights From Interview Transcripts Using LLMs
5 Levels Of LLM Summarizing: Novice to Expert
Control Tone & Writing Style Of Your LLM Output
Build Your Own AI Twitter Bot Using LLMs
ChatGPT made my interview questions for me (Streamlit + LangChain)
Function Calling via ChatGPT API - First Look With LangChain
Extract Topics From Video/Audio With LLMs (Topic Modeling w/ LangChain)
LangChain How to and guides by Sam Witteveen​
LangChain Basics - LLMs & PromptTemplates with Colab
LangChain Basics - Tools and Chains
ChatGPT API Announcement & Code Walkthrough with LangChain
Conversations with Memory (explanation & code walkthrough)
Chat with Flan20B
Using Hugging Face Models locally (code walkthrough)
PAL: Program-aided Language Models with LangChain code
Building a Summarization System with LangChain and GPT-3 - Part 1
Microsoft's Visual ChatGPT using LangChain
LangChain Agents - Joining Tools and Chains with Decisions
Comparing LLMs with LangChain
Using Constitutional AI in LangChain
Talking to Alpaca with LangChain - Creating an Alpaca Chatbot
Talk to your CSV & Excel with LangChain
BabyAGI: Discover the Power of Task-Driven Autonomous Agents!
Improve your BabyAGI with LangChain
Master PDF Chat with LangChain - Your essential guide to queries on documents
Using LangChain with DuckDuckGO, Wikipedia & PythonREPL Tools
Building Custom Tools and Agents with LangChain (gpt-3.5-turbo)
LangChain Retrieval QA Over Multiple Files with ChromaDB
LangChain + Retrieval Local LLMs for Retrieval QA - No OpenAI!!!
Camel + LangChain for Synthetic Data & Market Research
Converting a LangChain App from OpenAI to OpenSource
Using LangChain Output Parsers to get what you want out of LLMs
Building a LangChain Custom Medical Agent with Memory
Understanding ReACT with LangChain
OpenAI Functions + LangChain : Building a Multi Tool Agent
What can you do with 16K tokens in LangChain?
Tagging and Extraction - Classification using OpenAI Functions
HOW to Make Conversational Form with LangChain
⛓ Claude-2 meets LangChain!
⛓ Serving LLaMA2 with Replicate
⛓ NEW LangChain Expression Language
⛓ Building a RCI Chain for Agents with LangChain Expression Language
⛓ How to Run LLaMA-2-70B on the Together AI
⛓ RetrievalQA with LLaMA 2 70b & Chroma DB
⛓ How to use BGE Embeddings for LangChain
⛓ How to use Custom Prompts for RetrievalQA on LLaMA-2 7B
LangChain by Prompt Engineering​
LangChain Crash Course — All You Need to Know to Build Powerful Apps with LLMs
Working with MULTIPLE PDF Files in LangChain: ChatGPT for your Data
Talk to YOUR DATA without OpenAI APIs: LangChain
LangChain: PDF Chat App (GUI) | ChatGPT for Your PDF FILES
LangFlow: Build Chatbots without Writing Code
LangChain: Giving Memory to LLMs
BEST OPEN Alternative to OPENAI's EMBEDDINGs for Retrieval QA: LangChain
LangChain: Run Language Models Locally - Hugging Face Models
⛓ Slash API Costs: Mastering Caching for LLM Applications
⛓ Avoid PROMPT INJECTION with Constitutional AI - LangChain
LangChain by Chat with data​
LangChain Beginner's Tutorial for Typescript/Javascript
GPT-4 Tutorial: How to Chat With Multiple PDF Files (~1000 pages of Tesla's 10-K Annual Reports)
GPT-4 & LangChain Tutorial: How to Chat With A 56-Page PDF Document (w/Pinecone)
LangChain & Supabase Tutorial: How to Build a ChatGPT Chatbot For Your Website
LangChain Agents: Build Personal Assistants For Your Data (Q&A with Harrison Chase and Mayo Oshin)
Codebase Analysis​
Codebase Analysis: Langchain Agents

⛓ icon marks a new addition [last update 2023-09-21]

LangChain on Wikipedia
Books
DeepLearning.AI courses
Handbook
Short Tutorials
LangChain for Gen AI and LLMs by James Briggs
LangChain 101 by Greg Kamradt (Data Indy)
LangChain How to and guides by Sam Witteveen
LangChain by Prompt Engineering
Codebase Analysis
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Templates | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/templates/)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Templates
anthropic-iterative-search
basic-critique-revise
Bedrock JCVD 🕺🥋
cassandra-entomology-rag
cassandra-synonym-caching
Chain-of-Note (Wikipedia)
Chat Bot Feedback Template
cohere-librarian
csv-agent
elastic-query-generator
extraction-anthropic-functions
guardrails-output-parser
Hybrid Search in Weaviate
hyde
llama2-functions
mongo-parent-document-retrieval
neo4j-advanced-rag
neo4j\_cypher
neo4j-generation
neo4j-semantic-layer
nvidia-rag-canonical
OpenAI Functions Agent - Gmail
openai-functions-agent
openai-functions-tool-retrieval-agent
pii-protected-chatbot
pirate-speak
plate-chain
propositional-retrieval
python-lint
rag-astradb
rag-aws-bedrock
rag-chroma-multi-modal-multi-vector
rag-codellama-fireworks
rag-conversation-zep
rag-elasticsearch
rag-fusion
rag-gemini-multi-modal
rag-google-cloud-sensitive-data-protection
rag-gpt-crawler
rag-matching-engine
rag-momento-vector-index
rag-mongo
RAG with Multiple Indexes (Fusion)
rag-multi-modal-local
rag-ollama-multi-query
rag-opensearch
rag-pinecone-multi-query
rag-self-query
rag-semi-structured
rag-singlestoredb
rag\_supabase
rag-timescale-conversation
RAG with Timescale Vector using hybrid search
rag-vectara-multiquery
rag-weaviate
research-assistant
retrieval-agent
rewrite\_retrieve\_read
Langchain - Robocorp Action Server
self-query-qdrant
self-query-supabase
skeleton-of-thought
solo-performance-prompting-agent
sql-llama2
sql-ollama
sql-pgvector
sql-research-assistant
stepback-qa-prompting
summarize-anthropic
vertexai-chuck-norris
xml-agent
Templates

Highlighting a few different categories of templates

⭐ Popular​

These are some of the more popular templates to get started with.

Retrieval Augmented Generation Chatbot: Build a chatbot over your data. Defaults to OpenAI and Pinecone.
Extraction with OpenAI Functions: Do extraction of structured data from unstructured data. Uses OpenAI function calling.
Local Retrieval Augmented Generation: Build a chatbot over your data. Uses only local tooling: Ollama, GPT4all, Chroma.
OpenAI Functions Agent: Build a chatbot that can take actions. Uses OpenAI function calling and Tavily.
📥 Advanced Retrieval​

These templates cover advanced retrieval techniques, which can be used for chat and QA over databases or documents.

Reranking: This retrieval technique uses Cohere's reranking endpoint to rerank documents from an initial retrieval step.
Anthropic Iterative Search: This retrieval technique uses iterative prompting to determine what to retrieve and whether the retriever documents are good enough.
Parent Document Retrieval using Neo4j or MongoDB: This retrieval technique stores embeddings for smaller chunks, but then returns larger chunks to pass to the model for generation.
Semi-Structured RAG: The template shows how to do retrieval over semi-structured data (e.g. data that involves both text and tables).
Temporal RAG: The template shows how to do hybrid search over data with a time-based component using Timescale Vector.
🔍Advanced Retrieval - Query Transformation​

A selection of advanced retrieval methods that involve transforming the original user query, which can improve retrieval quality.

Hypothetical Document Embeddings: A retrieval technique that generates a hypothetical document for a given query, and then uses the embedding of that document to do semantic search. Paper.
Rewrite-Retrieve-Read: A retrieval technique that rewrites a given query before passing it to a search engine. Paper.
Step-back QA Prompting: A retrieval technique that generates a "step-back" question and then retrieves documents relevant to both that question and the original question. Paper.
RAG-Fusion: A retrieval technique that generates multiple queries and then reranks the retrieved documents using reciprocal rank fusion. Article.
Multi-Query Retriever: This retrieval technique uses an LLM to generate multiple queries and then fetches documents for all queries.
🧠Advanced Retrieval - Query Construction​

A selection of advanced retrieval methods that involve constructing a query in a separate DSL from natural language, which enable natural language chat over various structured databases.

Elastic Query Generator: Generate elastic search queries from natural language.
Neo4j Cypher Generation: Generate cypher statements from natural language. Available with a "full text" option as well.
Supabase Self Query: Parse a natural language query into a semantic query as well as a metadata filter for Supabase.
🦙 OSS Models​

These templates use OSS models, which enable privacy for sensitive data.

Local Retrieval Augmented Generation: Build a chatbot over your data. Uses only local tooling: Ollama, GPT4all, Chroma.
SQL Question Answering (Replicate): Question answering over a SQL database, using Llama2 hosted on Replicate.
⛏️ Extraction​

These templates extract data in a structured format based upon a user-specified schema.

Extraction Using OpenAI Functions: Extract information from text using OpenAI Function Calling.
Extraction Using Anthropic Functions: Extract information from text using a LangChain wrapper around the Anthropic endpoints intended to simulate function calling.
Extract BioTech Plate Data: Extract microplate data from messy Excel spreadsheets into a more normalized format.
⛏️Summarization and tagging​

These templates summarize or categorize documents and text.

Summarization using Anthropic: Uses Anthropic's Claude2 to summarize long documents.
🤖 Agents​

These templates build chatbots that can take actions, helping to automate tasks.

OpenAI Functions Agent: Build a chatbot that can take actions. Uses OpenAI function calling and Tavily.
🚨 Safety and evaluation​

These templates enable moderation or evaluation of LLM outputs.

Guardrails Output Parser: Use guardrails-ai to validate LLM output.
Chatbot Feedback: Use LangSmith to evaluate chatbot responses.
Next
anthropic-iterative-search
⭐ Popular
📥 Advanced Retrieval
🔍Advanced Retrieval - Query Transformation
🦙 OSS Models
⛏️ Extraction
⛏️Summarization and tagging
🤖 Agents
🚨 Safety and evaluation
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Welcome Contributors | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/contributing)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Welcome Contributors
Contribute Code
Testing
Contribute Documentation
FAQ
Welcome Contributors

Hi there! Thank you for even being interested in contributing to LangChain. As an open-source project in a rapidly developing field, we are extremely open to contributions, whether they involve new features, improved infrastructure, better documentation, or bug fixes.

🗺️ Guidelines​
👩‍💻 Ways to contribute​

There are many ways to contribute to LangChain. Here are some common ways people contribute:

Documentation: Help improve our docs, including this one!
Code: Help us write code, fix bugs, or improve our infrastructure.
Integrations: Help us integrate with your favorite vendors and tools.
🚩GitHub Issues​

Our issues page is kept up to date with bugs, improvements, and feature requests.

There is a taxonomy of labels to help with sorting and discovery of issues of interest. Please use these to help organize issues.

If you start working on an issue, please assign it to yourself.

If you are adding an issue, please try to keep it focused on a single, modular bug/improvement/feature. If two issues are related, or blocking, please link them rather than combining them.

We will try to keep these issues as up-to-date as possible, though with the rapid rate of development in this field some may get out of date. If you notice this happening, please let us know.

🙋Getting Help​

Our goal is to have the simplest developer setup possible. Should you experience any difficulty getting setup, please contact a maintainer! Not only do we want to help get you unblocked, but we also want to make sure that the process is smooth for future contributors.

In a similar vein, we do enforce certain linting, formatting, and documentation standards in the codebase. If you are finding these difficult (or even just annoying) to work with, feel free to contact a maintainer for help - we do not want these to get in the way of getting good code into the codebase.

🌟 Recognition

If your contribution has made its way into a release, we will want to give you credit on Twitter (only if you want though)! If you have a Twitter account you would like us to mention, please let us know in the PR or through another means.

Next
Contribute Code
🗺️ Guidelines
👩‍💻 Ways to contribute
🚩GitHub Issues
🙋Getting Help
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Changelog | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/changelog)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Changelog
langchain-core
Changelog
📄️ langchain-core

0.1.7 (Jan 5, 2024)

📄️ langchain

0.1.0 (Jan 5, 2024)

Next
langchain-core
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## 📕 Package Versioning | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/packages)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
📕 Package Versioning

As of now, LangChain has an ad hoc release process: releases are cut with high frequency by a maintainer and published to PyPI. The different packages are versioned slightly differently.

langchain-core​

langchain-core is currently on version 0.1.x.

As langchain-core contains the base abstractions and runtime for the whole LangChain ecosystem, we will communicate any breaking changes with advance notice and version bumps. The exception for this is anything marked with the beta decorator (you can see this in the API reference and will see warnings when using such functionality). The reason for beta features is that given the rate of change of the field, being able to move quickly is still a priority.

Minor version increases will occur for:

Breaking changes for any public interfaces marked as beta.

Patch version increases will occur for:

Bug fixes
New features
Any changes to private interfaces
Any changes to beta features
langchain​

langchain is currently on version 0.1.x

Minor version increases will occur for:

Breaking changes for any public interfaces NOT marked as beta.

Patch version increases will occur for:

Bug fixes
New features
Any changes to private interfaces
Any changes to beta features

We are targeting February 2024 for a release of langchain v0.2, which will have some breaking changes to legacy Chains and Agents. Additionally, we will remove langchain-community as a dependency and stop re-exporting integrations that have been moved to langchain-community.

langchain-community​

langchain-community is currently on version 0.0.x

All changes will be accompanied by a patch version increase.

langchain-experimental​

langchain-experimental is currently on version 0.0.x

All changes will be accompanied by a patch version increase.

Partner Packages​

Partner packages are versioned independently.

langchain-core
Partner Packages
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Debugging | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/guides/debugging)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Debugging
Deployment
Evaluation
Fallbacks
Run LLMs locally
Model comparison
Privacy
Pydantic compatibility
Safety
Debugging

If you're building with LLMs, at some point something will break, and you'll need to debug. A model call will fail, or the model output will be misformatted, or there will be some nested model calls and it won't be clear where along the way an incorrect output was created.

Here are a few different tools and functionalities to aid in debugging.

Tracing​

Platforms with tracing capabilities like LangSmith and WandB are the most comprehensive solutions for debugging. These platforms make it easy to not only log and visualize LLM apps, but also to actively debug, test and refine them.

For anyone building production-grade LLM applications, we highly recommend using a platform like this.

set\_debug and set\_verbose​

If you're prototyping in Jupyter Notebooks or running Python scripts, it can be helpful to print out the intermediate steps of a Chain run.

There are a number of ways to enable printing at varying degrees of verbosity.

Let's suppose we have a simple agent, and want to visualize the actions it takes and tool outputs it receives. Without any debugging, here's what we see:

from langchain.agents import AgentType, initialize\_agent, load\_tools
from langchain\_openai import ChatOpenAI

llm = ChatOpenAI(model\_name="gpt-4", temperature=0)
tools = load\_tools(["ddg-search", "llm-math"], llm=llm)
agent = initialize\_agent(tools, llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION)

agent.run("Who directed the 2023 film Oppenheimer and what is their age? What is their age in days (assume 365 days per year)?")

 'The director of the 2023 film Oppenheimer is Christopher Nolan and he is approximately 19345 days old in 2023.'

set\_debug(True)​

Setting the global debug flag will cause all LangChain components with callback support (chains, models, agents, tools, retrievers) to print the inputs they receive and outputs they generate. This is the most verbose setting and will fully log raw inputs and outputs.

from langchain.globals import set\_debug

set\_debug(True)

agent.run("Who directed the 2023 film Oppenheimer and what is their age? What is their age in days (assume 365 days per year)?")

Console output
set\_verbose(True)​

Setting the verbose flag will print out inputs and outputs in a slightly more readable format and will skip logging certain raw outputs (like the token usage stats for an LLM call) so that you can focus on application logic.

from langchain.globals import set\_verbose

set\_verbose(True)

agent.run("Who directed the 2023 film Oppenheimer and what is their age? What is their age in days (assume 365 days per year)?")

Console output
Chain(..., verbose=True)​

You can also scope verbosity down to a single object, in which case only the inputs and outputs to that object are printed (along with any additional callbacks calls made specifically by that object).

# Passing verbose=True to initialize\_agent will pass that along to the AgentExecutor (which is a Chain).
agent = initialize\_agent(
 tools, 
 llm, 
 agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION,
 verbose=True,
)

agent.run("Who directed the 2023 film Oppenheimer and what is their age? What is their age in days (assume 365 days per year)?")

Console output
Other callbacks​

Callbacks are what we use to execute any functionality within a component outside the primary component logic. All of the above solutions use Callbacks under the hood to log intermediate steps of components. There are a number of Callbacks relevant for debugging that come with LangChain out of the box, like the FileCallbackHandler. You can also implement your own callbacks to execute custom functionality.

See here for more info on Callbacks, how to use them, and customize them.

Next
Deployment
Tracing
set\_debug and set\_verbose
set\_debug(True)
set\_verbose(True)
Chain(..., verbose=True)
Other callbacks
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Q&A with RAG | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/use_cases/question_answering/)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Use cases
Q&A with RAG
Quickstart
Returning sources
Add chat history
Streaming
Per-User Retrieval
Using agents
Using local models
Q&A over structured data
Interacting with APIs
Chatbots
Extraction
Summarization
Tagging
Web scraping
Code understanding
Synthetic data generation
Graph querying
Use casesQ&A with RAG
Q&A with RAG
Overview​

One of the most powerful applications enabled by LLMs is sophisticated question-answering (Q&A) chatbots. These are applications that can answer questions about specific source information. These applications use a technique known as Retrieval Augmented Generation, or RAG.

What is RAG?​

RAG is a technique for augmenting LLM knowledge with additional data.

LLMs can reason about wide-ranging topics, but their knowledge is limited to the public data up to a specific point in time that they were trained on. If you want to build AI applications that can reason about private data or data introduced after a model’s cutoff date, you need to augment the knowledge of the model with the specific information it needs. The process of bringing the appropriate information and inserting it into the model prompt is known as Retrieval Augmented Generation (RAG).

LangChain has a number of components designed to help build Q&A applications, and RAG applications more generally.

Note: Here we focus on Q&A for unstructured data. Two RAG use cases which we cover elsewhere are:

Q&A over structured data (e.g., SQL)
RAG Architecture​

A typical RAG application has two main components:

Indexing: a pipeline for ingesting data from a source and indexing it. This usually happens offline.

Retrieval and generation: the actual RAG chain, which takes the user query at run time and retrieves the relevant data from the index, then passes that to the model.

The most common full sequence from raw data to answer looks like:

Indexing​
Load: First we need to load our data. This is done with DocumentLoaders.
Split: Text splitters break large Documents into smaller chunks. This is useful both for indexing data and for passing it in to a model, since large chunks are harder to search over and won’t fit in a model’s finite context window.
Store: We need somewhere to store and index our splits, so that they can later be searched over. This is often done using a VectorStore and Embeddings model.

Retrieval and generation​
Retrieve: Given a user input, relevant splits are retrieved from storage using a Retriever.
Generate: A ChatModel / LLM produces an answer using a prompt that includes the question and the retrieved data

Table of contents​
Quickstart: We recommend starting here. Many of the following guides assume you fully understand the architecture shown in the Quickstart.
Returning sources: How to return the source documents used in a particular generation.
Streaming: How to stream final answers as well as intermediate steps.
Adding chat history: How to add chat history to a Q&A app.
Per-user retrieval: How to do retrieval when each user has their own private data.
Using agents: How to use agents for Q&A.
Previous
Use cases
Next
Quickstart
Overview
What is RAG?
RAG Architecture
Table of contents
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Providers | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/integrations/providers)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Providers
Anthropic
AWS
Google
Hugging Face
Microsoft
OpenAI
More
Components
LLMs
Chat models
Document loaders
Document transformers
Text embedding models
Vector stores
Retrievers
Tools
Agents and toolkits
Memory
Callbacks
Chat loaders
Adapters
Stores
Providers
📄️ Anthropic

All functionality related to Anthropic models.

📄️ AWS

The LangChain integrations related to Amazon AWS platform.

📄️ Google

All functionality related to Google Cloud Platform and other Google products.

📄️ Hugging Face

All functionality related to the Hugging Face Platform.

📄️ Microsoft

All functionality related to Microsoft Azure and other Microsoft products.

📄️ OpenAI

All functionality related to OpenAI

🗃️ More

201 items

Next
Anthropic
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Introduction | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/get_started/introduction)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Get started
Introduction
Installation
Quickstart
Security
LangChain Expression Language
Get started
Why use LCEL
Interface
How to
Cookbook
Modules
Model I/O
Retrieval
Agents
Chains
More
LangServe
LangSmith
LangGraph
Get startedIntroduction
Introduction

LangChain is a framework for developing applications powered by language models. It enables applications that:

Are context-aware: connect a language model to sources of context (prompt instructions, few shot examples, content to ground its response in, etc.)

This framework consists of several parts.

LangChain Libraries: The Python and JavaScript libraries. Contains interfaces and integrations for a myriad of components, a basic run time for combining these components into chains and agents, and off-the-shelf implementations of chains and agents.
LangChain Templates: A collection of easily deployable reference architectures for a wide variety of tasks.
LangServe: A library for deploying LangChain chains as a REST API.
LangSmith: A developer platform that lets you debug, test, evaluate, and monitor chains built on any LLM framework and seamlessly integrates with LangChain.

Together, these products simplify the entire application lifecycle:

Develop: Write your applications in LangChain/LangChain.js. Hit the ground running using Templates for reference.
Productionize: Use LangSmith to inspect, test and monitor your chains, so that you can constantly improve and deploy with confidence.
Deploy: Turn any chain into an API with LangServe.
LangChain Libraries​

The main value props of the LangChain packages are:

Components: composable tools and integrations for working with language models. Components are modular and easy-to-use, whether you are using the rest of the LangChain framework or not
Off-the-shelf chains: built-in assemblages of components for accomplishing higher-level tasks

Off-the-shelf chains make it easy to get started. Components make it easy to customize existing chains and build new ones.

The LangChain libraries themselves are made up of several different packages.

langchain-core: Base abstractions and LangChain Expression Language.
langchain: Chains, agents, and retrieval strategies that make up an application's cognitive architecture.
Get started​

Here’s how to install LangChain, set up your environment, and start building.

We recommend following our Quickstart guide to familiarize yourself with the framework by building your first LangChain application.

Read up on our Security best practices to make sure you're developing safely with LangChain.

NOTE

These docs focus on the Python LangChain library. Head here for docs on the JavaScript LangChain library.

LangChain Expression Language (LCEL)​

LCEL is a declarative way to compose chains. LCEL was designed from day 1 to support putting prototypes in production, with no code changes, from the simplest “prompt + LLM” chain to the most complex chains.

Overview: LCEL and its benefits
Interface: The standard interface for LCEL objects
How-to: Key features of LCEL
Cookbook: Example code for accomplishing common tasks
Modules​

LangChain provides standard, extendable interfaces and integrations for the following modules:

Model I/O​

Interface with language models

Retrieval​

Interface with application-specific data

Agents​

Let models choose which tools to use given high-level directives

Examples, ecosystem, and resources​
Use cases​

Walkthroughs and techniques for common end-to-end use cases, like:

Document question answering
Chatbots
Analyzing structured data
and much more...
Integrations​

LangChain is part of a rich ecosystem of tools that integrate with our framework and build on top of it. Check out our growing list of integrations.

Guides​

Best practices for developing with LangChain.

API reference​

Head to the reference section for full documentation of all classes and methods in the LangChain and LangChain Experimental Python packages.

Developer's guide​

Check out the developer's guide for guidelines on contributing and help getting your dev environment set up.

Community​

Head to the Community navigator to find places to ask questions, share feedback, meet other developers, and dream about the future of LLM’s.

Get started
Next
Installation
LangChain Libraries
Get started
LangChain Expression Language (LCEL)
Modules
Examples, ecosystem, and resources
Use cases
Integrations
Guides
API reference
Developer's guide
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.## Get started | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/expression_language/get_started)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Get started
Introduction
Installation
Quickstart
Security
LangChain Expression Language
Get started
Why use LCEL
Interface
How to
Cookbook
Modules
Model I/O
Retrieval
Agents
Chains
More
LangServe
LangSmith
LangChain Expression LanguageGet started
Get started

LCEL makes it easy to build complex chains from basic components, and supports out of the box functionality such as streaming, parallelism, and logging.

Basic example: prompt + model + output parser​

The most basic and common use case is chaining a prompt template and a model together. To see how this works, let’s create a chain that takes a topic and generates a joke:

%pip install –upgrade –quiet langchain-core langchain-community langchain-openai

from langchain\_core.output\_parsers import StrOutputParser
from langchain\_openai import ChatOpenAI

prompt = ChatPromptTemplate.from\_template("tell me a short joke about {topic}")
model = ChatOpenAI(model="gpt-4")
output\_parser = StrOutputParser()

chain = prompt | model | output\_parser

chain.invoke({"topic": "ice cream"})

"Why don't ice creams ever get invited to parties?\n\nBecause they always drip when things heat up!"

Notice this line of this code, where we piece together then different components into a single chain using LCEL:

chain = prompt | model | output\_parser

The | symbol is similar to a unix pipe operator, which chains together the different components feeds the output from one component as input into the next component.

In this chain the user input is passed to the prompt template, then the prompt template output is passed to the model, then the model output is passed to the output parser. Let’s take a look at each component individually to really understand what’s going on.

1. Prompt​

prompt is a BasePromptTemplate, which means it takes in a dictionary of template variables and produces a PromptValue. A PromptValue is a wrapper around a completed prompt that can be passed to either an LLM (which takes a string as input) or ChatModel (which takes a sequence of messages as input). It can work with either language model type because it defines logic both for producing BaseMessages and for producing a string.

prompt\_value = prompt.invoke({"topic": "ice cream"})
prompt\_value

ChatPromptValue(messages=[HumanMessage(content='tell me a short joke about ice cream')])

prompt\_value.to\_messages()

[HumanMessage(content='tell me a short joke about ice cream')]

prompt\_value.to\_string()

'Human: tell me a short joke about ice cream'

2. Model​

The PromptValue is then passed to model. In this case our model is a ChatModel, meaning it will output a BaseMessage.

message = model.invoke(prompt\_value)
message

AIMessage(content="Why don't ice creams ever get invited to parties?\n\nBecause they always bring a melt down!")

If our model was an LLM, it would output a string.

from langchain\_openai.llms import OpenAI

llm = OpenAI(model="gpt-3.5-turbo-instruct")
llm.invoke(prompt\_value)

'\n\nRobot: Why did the ice cream truck break down? Because it had a meltdown!'

3. Output parser​

And lastly we pass our model output to the output\_parser, which is a BaseOutputParser meaning it takes either a string or a BaseMessage as input. The StrOutputParser specifically simple converts any input into a string.

output\_parser.invoke(message)

"Why did the ice cream go to therapy? \n\nBecause it had too many toppings and couldn't find its cone-fidence!"

4. Entire Pipeline​

To follow the steps along:

We pass in user input on the desired topic as {"topic": "ice cream"}
The prompt component takes the user input, which is then used to construct a PromptValue after using the topic to construct the prompt.
The model component takes the generated prompt, and passes into the OpenAI LLM model for evaluation. The generated output from the model is a ChatMessage object.
Finally, the output\_parser component takes in a ChatMessage, and transforms this into a Python string, which is returned from the invoke method.
Dict
PromptValue
ChatMessage
String
Input: topic=ice cream
PromptTemplate
ChatModel
StrOutputParser
Result

Note that if you’re curious about the output of any components, you can always test out a smaller version of the chain such as prompt or prompt | model to see the intermediate results:

input = {"topic": "ice cream"}

prompt.invoke(input)
# > ChatPromptValue(messages=[HumanMessage(content='tell me a short joke about ice cream')])

(prompt | model).invoke(input)
# > AIMessage(content="Why did the ice cream go to therapy?\nBecause it had too many toppings and couldn't cone-trol itself!")

RAG Search Example​

For our next example, we want to run a retrieval-augmented generation chain to add some context when responding to questions.

# Requires:
# pip install langchain docarray tiktoken

from langchain\_community.vectorstores import DocArrayInMemorySearch
from langchain\_core.runnables import RunnableParallel, RunnablePassthrough
from langchain\_openai.chat\_models import ChatOpenAI
from langchain\_openai.embeddings import OpenAIEmbeddings

vectorstore = DocArrayInMemorySearch.from\_texts(
 ["harrison worked at kensho", "bears like to eat honey"],
 embedding=OpenAIEmbeddings(),
)
retriever = vectorstore.as\_retriever()

template = """Answer the question based only on the following context:
{context}

Question: {question}
"""
prompt = ChatPromptTemplate.from\_template(template)
model = ChatOpenAI()
output\_parser = StrOutputParser()

setup\_and\_retrieval = RunnableParallel(
 {"context": retriever, "question": RunnablePassthrough()}
)
chain = setup\_and\_retrieval | prompt | model | output\_parser

chain.invoke("where did harrison work?")

In this case, the composed chain is:

chain = setup\_and\_retrieval | prompt | model | output\_parser

To explain this, we first can see that the prompt template above takes in context and question as values to be substituted in the prompt. Before building the prompt template, we want to retrieve relevant documents to the search and include them as part of the context.

As a preliminary step, we’ve setup the retriever using an in memory store, which can retrieve documents based on a query. This is a runnable component as well that can be chained together with other components, but you can also try to run it separately:

retriever.invoke("where did harrison work?")

We then use the RunnableParallel to prepare the expected inputs into the prompt by using the entries for the retrieved documents as well as the original user question, using the retriever for document search, and RunnablePassthrough to pass the user’s question:

setup\_and\_retrieval = RunnableParallel(
 {"context": retriever, "question": RunnablePassthrough()}
)
To review, the complete chain is:

setup\_and\_retrieval = RunnableParallel(
 {"context": retriever, "question": RunnablePassthrough()}
)
chain = setup\_and\_retrieval | prompt | model | output\_parser

With the flow being:

The first steps create a RunnableParallel object with two entries. The first entry, context will include the document results fetched by the retriever. The second entry, question will contain the user’s original question. To pass on the question, we use RunnablePassthrough to copy this entry.
Feed the dictionary from the step above to the prompt component. It then takes the user input which is question as well as the retrieved document which is context to construct a prompt and output a PromptValue.
Finally, the output\_parser component takes in a ChatMessage, and transforms this into a Python string, which is returned from the invoke method.
Question
context=retrieved docs
question=Question
PromptValue
ChatMessage
String
Question
RunnableParallel
Retriever
RunnablePassThrough
PromptTemplate
ChatModel
StrOutputParser
Result
Next steps​

We recommend reading our Why use LCEL section next to see a side-by-side comparison of the code needed to produce common functionality with and without LCEL.

LangChain Expression Language (LCEL)
Next
Why use LCEL
Basic example: prompt + model + output parser
1. Prompt
3. Output parser
4. Entire Pipeline
RAG Search Example
Next steps
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## LangChain Expression Language (LCEL) | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/expression_language/)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Get started
Introduction
Installation
Quickstart
Security
LangChain Expression Language
Get started
Why use LCEL
Interface
How to
Cookbook
Modules
Model I/O
Retrieval
Agents
Chains
More
LangServe
LangSmith
LangChain Expression Language

LangChain Expression Language, or LCEL, is a declarative way to easily compose chains together. LCEL was designed from day 1 to support putting prototypes in production, with no code changes, from the simplest “prompt + LLM” chain to the most complex chains (we’ve seen folks successfully run LCEL chains with 100s of steps in production). To highlight a few of the reasons you might want to use LCEL:

Streaming support When you build your chains with LCEL you get the best possible time-to-first-token (time elapsed until the first chunk of output comes out). For some chains this means eg. we stream tokens straight from an LLM to a streaming output parser, and you get back parsed, incremental chunks of output at the same rate as the LLM provider outputs the raw tokens.

Async support Any chain built with LCEL can be called both with the synchronous API (eg. in your Jupyter notebook while prototyping) as well as with the asynchronous API (eg. in a LangServe server). This enables using the same code for prototypes and in production, with great performance, and the ability to handle many concurrent requests in the same server.

Optimized parallel execution Whenever your LCEL chains have steps that can be executed in parallel (eg if you fetch documents from multiple retrievers) we automatically do it, both in the sync and the async interfaces, for the smallest possible latency.

Retries and fallbacks Configure retries and fallbacks for any part of your LCEL chain. This is a great way to make your chains more reliable at scale. We’re currently working on adding streaming support for retries/fallbacks, so you can get the added reliability without any latency cost.

Access intermediate results For more complex chains it’s often very useful to access the results of intermediate steps even before the final output is produced. This can be used to let end-users know something is happening, or even just to debug your chain. You can stream intermediate results, and it’s available on every LangServe server.

Input and output schemas Input and output schemas give every LCEL chain Pydantic and JSONSchema schemas inferred from the structure of your chain. This can be used for validation of inputs and outputs, and is an integral part of LangServe.

Seamless LangSmith tracing integration As your chains get more and more complex, it becomes increasingly important to understand what exactly is happening at every step. With LCEL, all steps are automatically logged to LangSmith for maximum observability and debuggability.

Seamless LangServe deployment integration Any chain created with LCEL can be easily deployed using LangServe.

Security
Next
Get started
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Security | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/security)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Get started
Introduction
Installation
Quickstart
Security
LangChain Expression Language
Get started
Why use LCEL
Interface
How to
Cookbook
Modules
Model I/O
Retrieval
Agents
Chains
More
LangServe
LangSmith
Get startedSecurity
Security

LangChain has a large ecosystem of integrations with various external resources like local and remote file systems, APIs and databases. These integrations allow developers to create versatile applications that combine the power of LLMs with the ability to access, interact with and manipulate external resources.

Best Practices​

When building such applications developers should remember to follow good security practices:

Limit Permissions: Scope permissions specifically to the application's need. Granting broad or excessive permissions can introduce significant security vulnerabilities. To avoid such vulnerabilities, consider using read-only credentials, disallowing access to sensitive resources, using sandboxing techniques (such as running inside a container), etc. as appropriate for your application.
Anticipate Potential Misuse: Just as humans can err, so can Large Language Models (LLMs). Always assume that any system access or credentials may be used in any way allowed by the permissions they are assigned. For example, if a pair of database credentials allows deleting data, it’s safest to assume that any LLM able to use those credentials may in fact delete data.

Risks of not doing so include, but are not limited to:

Data corruption or loss.
Unauthorized access to confidential information.
Compromised performance or availability of critical resources.

Example scenarios with mitigation strategies:

A user may ask an agent with access to the file system to delete files that should not be deleted or read the content of files that contain sensitive information. To mitigate, limit the agent to only use a specific directory and only allow it to read or write files that are safe to read or write. Consider further sandboxing the agent by running it in a container.
A user may ask an agent with write access to an external API to write malicious data to the API, or delete data from that API. To mitigate, give the agent read-only API keys, or limit it to only use endpoints that are already resistant to such misuse.
A user may ask an agent with access to a database to drop a table or mutate the schema. To mitigate, scope the credentials to only the tables that the agent needs to access and consider issuing READ-ONLY credentials.

If you're building applications that access external resources like file systems, APIs or databases, consider speaking with your company's security team to determine how to best design and secure your applications.

Reporting a Vulnerability​

Please report security vulnerabilities by email to security@langchain.dev. This will ensure the issue is promptly triaged and acted upon as needed.

Enterprise solutions​

LangChain may offer enterprise solutions for customers who have additional security requirements. Please contact us at sales@langchain.dev.

Quickstart
Next
LangChain Expression Language (LCEL)
Best Practices
Reporting a Vulnerability
Enterprise solutions
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Quickstart | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/get_started/quickstart)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Get started
Introduction
Installation
Quickstart
Security
LangChain Expression Language
Get started
Why use LCEL
Interface
How to
Cookbook
Modules
Model I/O
Retrieval
Agents
Chains
More
LangServe
LangSmith
Get startedQuickstart
Quickstart

In this quickstart we'll show you how to:

Get setup with LangChain, LangSmith and LangServe
Use the most basic and common components of LangChain: prompt templates, models, and output parsers
Build a simple application with LangChain
Trace your application with LangSmith
Serve your application with LangServe

That's a fair amount to cover! Let's dive in.

Jupyter Notebook​

This guide (and most of the other guides in the documentation) use Jupyter notebooks and assume the reader is as well. Jupyter notebooks are perfect for learning how to work with LLM systems because often times things can go wrong (unexpected output, API down, etc) and going through guides in an interactive environment is a great way to better understand them.

You do not NEED to go through the guide in a Jupyter Notebook, but it is recommended. See here for instructions on how to install.

Installation​

To install LangChain run:

Pip
Conda
pip install langchain

For more details, see our Installation guide.

LangSmith​

Many of the applications you build with LangChain will contain multiple steps with multiple invocations of LLM calls. As these applications get more and more complex, it becomes crucial to be able to inspect what exactly is going on inside your chain or agent. The best way to do this is with LangSmith.

Note that LangSmith is not needed, but it is helpful. If you do want to use LangSmith, after you sign up at the link above, make sure to set your environment variables to start logging traces:

export LANGCHAIN\_TRACING\_V2="true"
export LANGCHAIN\_API\_KEY="..."

Building with LangChain​

LangChain enables building application that connect external sources of data and computation to LLMs. In this quickstart, we will walk through a few different ways of doing that. We will start with a simple LLM chain, which just relies on information in the prompt template to respond. Next, we will build a retrieval chain, which fetches data from a separate database and passes that into the prompt template. We will then add in chat history, to create a conversation retrieval chain. This allows you interact in a chat manner with this LLM, so it remembers previous questions. Finally, we will build an agent - which utilizes and LLM to determine whether or not it needs to fetch data to answer questions. We will cover these at a high level, but there are lot of details to all of these! We will link to relevant docs.

LLM Chain​

For this getting started guide, we will provide two options: using OpenAI (a popular model available via API) or using a local open source model.

OpenAI
Local

First we'll need to import the LangChain x OpenAI integration package.

pip install langchain-openai

Accessing the API requires an API key, which you can get by creating an account and heading here. Once we have a key we'll want to set it as an environment variable by running:

export OPENAI\_API\_KEY="..."

We can then initialize the model:

from langchain\_openai import ChatOpenAI

llm = ChatOpenAI()

If you'd prefer not to set an environment variable you can pass the key in directly via the openai\_api\_key named parameter when initiating the OpenAI LLM class:

from langchain\_openai import ChatOpenAI

llm = ChatOpenAI(openai\_api\_key="...")

Once you've installed and initialized the LLM of your choice, we can try using it! Let's ask it what LangSmith is - this is something that wasn't present in the training data so it shouldn't have a very good response.

llm.invoke("how can langsmith help with testing?")

We can also guide it's response with a prompt template. Prompt templates are used to convert raw user input to a better input to the LLM.

from langchain\_core.prompts import ChatPromptTemplate
prompt = ChatPromptTemplate.from\_messages([
 ("system", "You are world class technical documentation writer."),
 ("user", "{input}")
])

We can now combine these into a simple LLM chain:

chain = prompt | llm 

We can now invoke it and ask the same question. It still won't know the answer, but it should respond in a more proper tone for a technical writer!

chain.invoke({"input": "how can langsmith help with testing?"})

The output of a ChatModel (and therefore, of this chain) is a message. However, it's often much more convenient to work with strings. Let's add a simple output parser to convert the chat message to a string.

from langchain\_core.output\_parsers import StrOutputParser

output\_parser = StrOutputParser()

We can now add this to the previous chain:

chain = prompt | llm | output\_parser

We can now invoke it and ask the same question. The answer will now be a string (rather than a ChatMessage).

chain.invoke({"input": "how can langsmith help with testing?"})

Diving Deeper​

We've now successfully set up a basic LLM chain. We only touched on the basics of prompts, models, and output parsers - for a deeper dive into everything mentioned here, see this section of documentation.

Retrieval Chain​

In order to properly answer the original question ("how can langsmith help with testing?"), we need to provide additional context to the LLM. We can do this via retrieval. Retrieval is useful when you have too much data to pass to the LLM directly. You can then use a retriever to fetch only the most relevant pieces and pass those in.

In this process, we will look up relevant documents from a Retriever and then pass them into the prompt. A Retriever can be backed by anything - a SQL table, the internet, etc - but in this instance we will populate a vector store and use that as a retriever. For more information on vectorstores, see this documentation.

First, we need to load the data that we want to index. In order to do this, we will use the WebBaseLoader. This requires installing BeautifulSoup:

```shell
pip install beautifulsoup4

After that, we can import and use WebBaseLoader.

from langchain\_community.document\_loaders import WebBaseLoader
loader = WebBaseLoader("https://docs.smith.langchain.com/overview")

docs = loader.load()

Next, we need to index it into a vectorstore. This requires a few components, namely an embedding model and a vectorstore.

For embedding models, we once again provide examples for accessing via OpenAI or via local models.

OpenAI
Local
Make sure you have the `langchain\_openai` package installed an the appropriate environment variables set (these are the same as needed for the LLM).
from langchain\_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()

Now, we can use this embedding model to ingest documents into a vectorstore. We will use a simple local vectorstore, FAISS, for simplicity's sake.

First we need to install the required packages for that:

pip install faiss-cpu

Then we can build our index:

from langchain\_community.vectorstores import FAISS

text\_splitter = RecursiveCharacterTextSplitter()
documents = text\_splitter.split\_documents(docs)
vector = FAISS.from\_documents(documents, embeddings)

Now that we have this data indexed in a vectorstore, we will create a retrieval chain. This chain will take an incoming question, look up relevant documents, then pass those documents along with the original question into an LLM and ask it to answer the original question.

First, let's set up the chain that takes a question and the retrieved documents and generates an answer.

from langchain.chains.combine\_documents import create\_stuff\_documents\_chain

prompt = ChatPromptTemplate.from\_template("""Answer the following question based only on the provided context:

{context}

Question: {input}""")

document\_chain = create\_stuff\_documents\_chain(llm, prompt)

If we wanted to, we could run this ourselves by passing in documents directly:

from langchain\_core.documents import Document

document\_chain.invoke({
 "input": "how can langsmith help with testing?",
 "context": [Document(page\_content="langsmith can let you visualize test results")]
})

However, we want the documents to first come from the retriever we just set up. That way, for a given question we can use the retriever to dynamically select the most relevant documents and pass those in.

from langchain.chains import create\_retrieval\_chain

retriever = vector.as\_retriever()
retrieval\_chain = create\_retrieval\_chain(retriever, document\_chain)

We can now invoke this chain. This returns a dictionary - the response from the LLM is in the answer key

response = retrieval\_chain.invoke({"input": "how can langsmith help with testing?"})
print(response["answer"])

# LangSmith offers several features that can help with testing:...

This answer should be much more accurate!

Diving Deeper​

We've now successfully set up a basic retrieval chain. We only touched on the basics of retrieval - for a deeper dive into everything mentioned here, see this section of documentation.

Conversation Retrieval Chain​

The chain we've created so far can only answer single questions. One of the main types of LLM applications that people are building are chat bots. So how do we turn this chain into one that can answer follow up questions?

We can still use the create\_retrieval\_chain function, but we need to change two things:

The retrieval method should now not just work on the most recent input, but rather should take the whole history into account.
The final LLM chain should likewise take the whole history into account

Updating Retrieval

In order to update retrieval, we will create a new chain. This chain will take in the most recent input (input) and the conversation history (chat\_history) and use an LLM to generate a search query.

from langchain.chains import create\_history\_aware\_retriever
from langchain\_core.prompts import MessagesPlaceholder

# First we need a prompt that we can pass into an LLM to generate this search query

prompt = ChatPromptTemplate.from\_messages([
 MessagesPlaceholder(variable\_name="chat\_history"),
 ("user", "{input}"),
 ("user", "Given the above conversation, generate a search query to look up in order to get information relevant to the conversation")
])
retriever\_chain = create\_history\_aware\_retriever(llm, retriever, prompt)

We can test this out by passing in an instance where the user is asking a follow up question.

from langchain\_core.messages import HumanMessage, AIMessage

chat\_history = [HumanMessage(content="Can LangSmith help test my LLM applications?"), AIMessage(content="Yes!")]
retriever\_chain.invoke({
 "chat\_history": chat\_history,
 "input": "Tell me how"
})

You should see that this returns documents about testing in LangSmith. This is because the LLM generated a new query, combining the chat history with the follow up question.

Now that we have this new retriever, we can create a new chain to continue the conversation with these retrieved documents in mind.

prompt = ChatPromptTemplate.from\_messages([
 ("system", "Answer the user's questions based on the below context:\n\n{context}"),
 MessagesPlaceholder(variable\_name="chat\_history"),
 ("user", "{input}"),
])
document\_chain = create\_stuff\_documents\_chain(llm, prompt)

retrieval\_chain = create\_retrieval\_chain(retriever\_chain, document\_chain)

We can now test this out end-to-end:

chat\_history = [HumanMessage(content="Can LangSmith help test my LLM applications?"), AIMessage(content="Yes!")]
retrieval\_chain.invoke({
 "chat\_history": chat\_history,
 "input": "Tell me how"
})

We can see that this gives a coherent answer - we've successfully turned our retrieval chain into a chatbot!

Agent​

We've so far create examples of chains - where each step is known ahead of time. The final thing we will create is an agent - where the LLM decides what steps to take.

NOTE: for this example we will only show how to create an agent using OpenAI models, as local models are not reliable enough yet.

One of the first things to do when building an agent is to decide what tools it should have access to. For this example, we will give the agent access two tools:

The retriever we just created. This will let it easily answer questions about LangSmith
A search tool. This will let it easily answer questions that require up to date information.

First, let's set up a tool for the retriever we just created:

from langchain.tools.retriever import create\_retriever\_tool

retriever\_tool = create\_retriever\_tool(
 retriever,
 "langsmith\_search",
 "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
)
The search tool that we will use is Tavily. This will require an API key (they have generous free tier). After creating it on their platform, you need to set it as an environment variable:

export TAVILY\_API\_KEY=...

If you do not want to set up an API key, you can skip creating this tool.

from langchain\_community.tools.tavily\_search import TavilySearchResults

search = TavilySearchResults()

We can now create a list of the tools we want to work with:

tools = [retriever\_tool, search]

Now that we have the tools, we can create an agent to use them. We will go over this pretty quickly - for a deeper dive into what exactly is going on, check out the Agent's Getting Started documentation

Install langchain hub first

pip install langchainhub

Now we can use it to get a predefined prompt

from langchain\_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create\_openai\_functions\_agent
from langchain.agents import AgentExecutor

# Get the prompt to use - you can modify this!
prompt = hub.pull("hwchase17/openai-functions-agent")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent = create\_openai\_functions\_agent(llm, tools, prompt)
agent\_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

We can now invoke the agent and see how it responds! We can ask it questions about LangSmith:

agent\_executor.invoke({"input": "how can langsmith help with testing?"})

We can ask it about the weather:

agent\_executor.invoke({"input": "what is the weather in SF?"})

We can have conversations with it:

chat\_history = [HumanMessage(content="Can LangSmith help test my LLM applications?"), AIMessage(content="Yes!")]
agent\_executor.invoke({
 "chat\_history": chat\_history,
 "input": "Tell me how"
})

Diving Deeper​

We've now successfully set up a basic agent. We only touched on the basics of agents - for a deeper dive into everything mentioned here, see this section of documentation.

Serving with LangServe​

Now that we've built an application, we need to serve it. That's where LangServe comes in. LangServe helps developers deploy LangChain chains as a REST API. You do not need to use LangServe to use LangChain, but in this guide we'll show how you can deploy your app with LangServe.

While the first part of this guide was intended to be run in a Jupyter Notebook, we will now move out of that. We will be creating a Python file and then interacting with it from the command line.

Install with:

pip install "langserve[all]"

Server​

To create a server for our application we'll make a serve.py file. This will contain our logic for serving our application. It consists of three things:

The definition of our chain that we just built above
Our FastAPI app
A definition of a route from which to serve the chain, which is done with langserve.add\_routes
#!/usr/bin/env python
from typing import List

from fastapi import FastAPI
from langchain\_core.prompts import ChatPromptTemplate
from langchain\_openai import ChatOpenAI
from langchain\_community.document\_loaders import WebBaseLoader
from langchain\_openai import OpenAIEmbeddings
from langchain.tools.retriever import create\_retriever\_tool
from langchain\_community.tools.tavily\_search import TavilySearchResults
from langchain\_openai import ChatOpenAI
from langchain import hub
from langchain.agents import create\_openai\_functions\_agent
from langchain.agents import AgentExecutor
from langchain.pydantic\_v1 import BaseModel, Field
from langserve import add\_routes

# 1. Load Retriever
loader = WebBaseLoader("https://docs.smith.langchain.com/overview")
docs = loader.load()
text\_splitter = RecursiveCharacterTextSplitter()
documents = text\_splitter.split\_documents(docs)
embeddings = OpenAIEmbeddings()
vector = FAISS.from\_documents(documents, embeddings)
retriever = vector.as\_retriever()

# 2. Create Tools
retriever\_tool = create\_retriever\_tool(
 retriever,
 "langsmith\_search",
 "Search for information about LangSmith. For any questions about LangSmith, you must use this tool!",
)
search = TavilySearchResults()
tools = [retriever\_tool, search]

# 3. Create Agent
prompt = hub.pull("hwchase17/openai-functions-agent")
llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0)
agent = create\_openai\_functions\_agent(llm, tools, prompt)
agent\_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

# 4. App definition
app = FastAPI(
 title="LangChain Server",
 version="1.0",
 description="A simple API server using LangChain's Runnable interfaces",
)
# 5. Adding chain route

# We need to add these input/output schemas because the current AgentExecutor
# is lacking in schemas.

class Input(BaseModel):
 input: str
 chat\_history: List[BaseMessage] = Field(
 ...,
 extra={"widget": {"type": "chat", "input": "location"}},
 )
class Output(BaseModel):
 output: str

add\_routes(
 app,
 agent\_executor.with\_types(input\_type=Input, output\_type=Output),
 path="/agent",
)
if \_\_name\_\_ == "\_\_main\_\_":
 import uvicorn

 uvicorn.run(app, host="localhost", port=8000)

And that's it! If we execute this file:

python serve.py

we should see our chain being served at localhost:8000.

Playground​

Every LangServe service comes with a simple built-in UI for configuring and invoking the application with streaming output and visibility into intermediate steps. Head to http://localhost:8000/agent/playground/ to try it out! Pass in the same question as before - "how can langsmith help with testing?" - and it should respond same as before.

Client​

Now let's set up a client for programmatically interacting with our service. We can easily do this with the [langserve.RemoteRunnable](/docs/langserve#client). Using this, we can interact with the served chain as if it were running client-side.

from langserve import RemoteRunnable

remote\_chain = RemoteRunnable("http://localhost:8000/agent/")
remote\_chain.invoke({"input": "how can langsmith help with testing?"})

To learn more about the many other features of LangServe head here.

Next steps​

We've touched on how to build an application with LangChain, how to trace it with LangSmith, and how to serve it with LangServe. There are a lot more features in all three of these than we can cover here. To continue on your journey, we recommend you read the following (in order):

All of these features are backed by LangChain Expression Language (LCEL) - a way to chain these components together. Check out that documentation to better understand how to create custom chains.
Model IO covers more details of prompts, LLMs, and output parsers.
Retrieval covers more details of everything related to retrieval
Agents covers details of everything related to agents
Explore common end-to-end use cases and template applications
Read up on LangSmith, the platform for debugging, testing, monitoring and more
Learn more about serving your applications with LangServe
Previous
Installation
Next
Security
Setup
Jupyter Notebook
Installation
LangSmith
Building with LangChain
LLM Chain
Diving Deeper
Retrieval Chain
Diving Deeper
Conversation Retrieval Chain
Agent
Diving Deeper
Serving with LangServe
Server
Client
Next steps
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Installation | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/get_started/installation)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Get started
Introduction
Installation
Quickstart
Security
LangChain Expression Language
Get started
Why use LCEL
Interface
How to
Cookbook
Modules
Model I/O
Retrieval
Agents
Chains
More
LangServe
LangSmith
Get startedInstallation
Installation
Official release​

To install LangChain run:

Pip
Conda
pip install langchain

This will install the bare minimum requirements of LangChain. A lot of the value of LangChain comes when integrating it with various model providers, datastores, etc. By default, the dependencies needed to do that are NOT installed. You will need to install the dependencies for specific integrations separately.

From source​

If you want to install from source, you can do so by cloning the repo and be sure that the directory is PATH/TO/REPO/langchain/libs/langchain running:

pip install -e .

LangChain community​

The langchain-community package contains third-party integrations. It is automatically installed by langchain, but can also be used separately. Install with:

pip install langchain-community

LangChain core​

The langchain-core package contains base abstractions that the rest of the LangChain ecosystem uses, along with the LangChain Expression Language. It is automatically installed by langchain, but can also be used separately. Install with:

pip install langchain-core

LangChain experimental​

The langchain-experimental package holds experimental LangChain code, intended for research and experimental uses. Install with:

pip install langchain-experimental

LangServe​

LangServe helps developers deploy LangChain runnables and chains as a REST API. LangServe is automatically installed by LangChain CLI. If not using LangChain CLI, install with:

pip install "langserve[all]"

for both client and server dependencies. Or pip install "langserve[client]" for client code, and pip install "langserve[server]" for server code.

LangChain CLI​

The LangChain CLI is useful for working with LangChain templates and other LangServe projects. Install with:

pip install langchain-cli

LangSmith SDK​

The LangSmith SDK is automatically installed by LangChain. If not using LangChain, install with:

pip install langsmith

Introduction
Next
Quickstart
Official release
From source
LangChain community
LangServe
LangChain CLI
LangSmith SDK
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Get started | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/get_started)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Get started
Introduction
Installation
Quickstart
Security
LangChain Expression Language
Get started
Why use LCEL
Interface
How to
Cookbook
Modules
Model I/O
Retrieval
Agents
Chains
More
LangServe
LangSmith
Get started

Get started with LangChain

📄️ Introduction

LangChain is a framework for developing applications powered by language models. It enables applications that:

📄️ Installation

Official release

📄️ Quickstart

In this quickstart we'll show you how to:

📄️ Security

LangChain has a large ecosystem of integrations with various external resources like local and remote file systems, APIs and databases. These integrations allow developers to create versatile applications that combine the power of LLMs with the ability to access, interact with and manipulate external resources.

Next
Introduction
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## YouTube videos | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/additional_resources/youtube)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
YouTube videos

⛓ icon marks a new addition [last update 2023-09-21]

Official LangChain YouTube channel​
Introduction to LangChain with Harrison Chase, creator of LangChain​
LangChain and Weaviate with Harrison Chase and Bob van Luijt - Weaviate Podcast #36 by Weaviate • Vector Database
LangChain Demo + Q&A with Harrison Chase by Full Stack Deep Learning
LangChain Agents: Build Personal Assistants For Your Data (Q&A with Harrison Chase and Mayo Oshin) by Chat with data
Videos (sorted by views)​
Using ChatGPT with YOUR OWN Data. This is magical. (LangChain OpenAI API) by TechLead
First look - ChatGPT + WolframAlpha (GPT-3.5 and Wolfram|Alpha via LangChain by James Weaver) by Dr Alan D. Thompson
LangChain explained - The hottest new Python framework by AssemblyAI
Chatbot with INFINITE MEMORY using OpenAI & Pinecone - GPT-3, Embeddings, ADA, Vector DB, Semantic by David Shapiro ~ AI
LangChain for LLMs is... basically just an Ansible playbook by David Shapiro ~ AI
Build your own LLM Apps with LangChain & GPT-Index by 1littlecoder
How to Use Langchain With Zapier | Write and Send Email with GPT-3 | OpenAI API Tutorial by StarMorph AI
Use Your Locally Stored Files To Get Response From GPT - OpenAI | Langchain | Python by Shweta Lodha
Langchain JS | How to Use GPT-3, GPT-4 to Reference your own Data | OpenAI Embeddings Intro by StarMorph AI
The easiest way to work with large language models | Learn LangChain in 10min by Sophia Yang
4 Autonomous AI Agents: “Westworld” simulation BabyAGI, AutoGPT, Camel, LangChain by Sophia Yang
AI CAN SEARCH THE INTERNET? Langchain Agents + OpenAI ChatGPT by tylerwhatsgood
Query Your Data with GPT-4 | Embeddings, Vector Databases | Langchain JS Knowledgebase by StarMorph AI
Weaviate + LangChain for LLM apps presented by Erika Cardenas by Weaviate • Vector Database
Langchain Overview — How to Use Langchain & ChatGPT by Python In Office
LangChain Tutorials by Edrick:
LangChain, Chroma DB, OpenAI Beginner Guide | ChatGPT with your PDF
LangChain 101: The Complete Beginner's Guide
Custom langchain Agent & Tools with memory. Turn any Python function into langchain tool with Gpt 3 by echohive
Building AI LLM Apps with LangChain (and more?) - LIVE STREAM by Nicholas Renotte
ChatGPT with any YouTube video using langchain and chromadb by echohive
How to Talk to a PDF using LangChain and ChatGPT by Automata Learning Lab
Langchain Document Loaders Part 1: Unstructured Files by Merk
LangChain - Prompt Templates (what all the best prompt engineers use) by Nick Daigler
LangChain. Crear aplicaciones Python impulsadas por GPT by Jesús Conde
Easiest Way to Use GPT In Your Products | LangChain Basics Tutorial by Rachel Woods
BabyAGI + GPT-4 Langchain Agent with Internet Access by tylerwhatsgood
Learning LLM Agents. How does it actually work? LangChain, AutoGPT & OpenAI by Arnoldas Kemeklis
Get Started with LangChain in Node.js by Developers Digest
LangChain + OpenAI tutorial: Building a Q&A system w/ own text data by Samuel Chan
Langchain + Zapier Agent by Merk
Connecting the Internet with ChatGPT (LLMs) using Langchain And Answers Your Questions by Kamalraj M M
Build More Powerful LLM Applications for Business’s with LangChain (Beginners Guide) by No Code Blackbox
LangFlow LLM Agent Demo for 🦜🔗LangChain by Cobus Greyling
Chatbot Factory: Streamline Python Chatbot Creation with LLMs and Langchain by Finxter
Introdução ao Langchain - #Cortes - Live DataHackers by Prof. João Gabriel Lima
LangChain: Level up ChatGPT !? | LangChain Tutorial Part 1 by Code Affinity
KI schreibt krasses Youtube Skript 😲😳 | LangChain Tutorial Deutsch by SimpleKI
Chat with Audio: Langchain, Chroma DB, OpenAI, and Assembly AI by AI Anytime
QA over documents with Auto vector index selection with Langchain router chains by echohive
Build your own custom LLM application with Bubble.io & Langchain (No Code & Beginner friendly) by No Code Blackbox
Simple App to Question Your Docs: Leveraging Streamlit, Hugging Face Spaces, LangChain, and Claude! by Chris Alexiuk
LANGCHAIN AI- ConstitutionalChainAI + Databutton AI ASSISTANT Web App by Avra
The Future of Data Analysis: Using A.I. Models in Data Analysis (LangChain) by Absent Data
Memory in LangChain | Deep dive (python) by Eden Marco
9 LangChain UseCases | Beginner's Guide | 2023 by Data Science Basics
Use Large Language Models in Jupyter Notebook | LangChain | Agents & Indexes by Abhinaw Tiwari
How to Talk to Your Langchain Agent | 11 Labs + Whisper by VRSEN
LangChain Deep Dive: 5 FUN AI App Ideas To Build Quickly and Easily by James NoCode
LangChain 101: Models by Mckay Wrigley
LangChain with JavaScript Tutorial #1 | Setup & Using LLMs by Leon van Zyl
LangChain Overview & Tutorial for Beginners: Build Powerful AI Apps Quickly & Easily (ZERO CODE) by James NoCode
LangChain In Action: Real-World Use Case With Step-by-Step Tutorial by Rabbitmetrics
Summarizing and Querying Multiple Papers with LangChain by Automata Learning Lab
Using Langchain (and Replit) through Tana, ask Google/Wikipedia/Wolfram Alpha to fill out a table by Stian Håklev
Langchain PDF App (GUI) | Create a ChatGPT For Your PDF in Python by Alejandro AO - Software & Ai
Auto-GPT with LangChain 🔥 | Create Your Own Personal AI Assistant by Data Science Basics
Create Your OWN Slack AI Assistant with Python & LangChain by Dave Ebbelaar
How to Create LOCAL Chatbots with GPT4All and LangChain [Full Guide] by Liam Ottley
Build a Multilingual PDF Search App with LangChain, Cohere and Bubble by Menlo Park Lab
LangChain Memory Tutorial | Building a ChatGPT Clone in Python by Alejandro AO - Software & Ai
Llama Index: Chat with Documentation using URL Loader by Merk
Using OpenAI, LangChain, and Gradio to Build Custom GenAI Applications by David Hundley
LangChain, Chroma DB, OpenAI Beginner Guide | ChatGPT with your PDF
Build AI chatbot with custom knowledge base using OpenAI API and GPT Index by Irina Nik
Build Your Own Auto-GPT Apps with LangChain (Python Tutorial) by Dave Ebbelaar
Flowise is an open-source no-code UI visual tool to build 🦜🔗LangChain applications by Cobus Greyling
LangChain & GPT 4 For Data Analysis: The Pandas Dataframe Agent by Rabbitmetrics
GirlfriendGPT - AI girlfriend with LangChain by Toolfinder AI
How to build with Langchain 10x easier | ⛓️ LangFlow & Flowise by AI Jason
Getting Started With LangChain In 20 Minutes- Build Celebrity Search Application by Krish Naik
⛓ Vector Embeddings Tutorial – Code Your Own AI Assistant with GPT-4 API + LangChain + NLP by FreeCodeCamp.org
⛓ Fully LOCAL Llama 2 Q&A with LangChain by 1littlecoder
⛓ Build LangChain Audio Apps with Python in 5 Minutes by AssemblyAI
⛓ Voiceflow & Flowise: Want to Beat Competition? New Tutorial with Real AI Chatbot by AI SIMP
⛓ THIS Is How You Build Production-Ready AI Apps (LangSmith Tutorial) by Dave Ebbelaar
⛓ Build POWERFUL LLM Bots EASILY with Your Own Data - Embedchain - Langchain 2.0? (Tutorial) by WorldofAI
⛓ Code Llama powered Gradio App for Coding: Runs on CPU by AI Anytime
⛓ LangChain Complete Course in One Video | Develop LangChain (AI) Based Solutions for Your Business by UBprogrammer
⛓ How to Run LLaMA Locally on CPU or GPU | Python & Langchain & CTransformers Guide by Code With Prince
⛓ PyData Heidelberg #11 - TimeSeries Forecasting & LLM Langchain by PyData
⛓ Prompt Engineering in Web Development | Using LangChain and Templates with OpenAI by Akamai Developer
⛓ Retrieval-Augmented Generation (RAG) using LangChain and Pinecone - The RAG Special Episode by Generative AI and Data Science On AWS
⛓ LLAMA2 70b-chat Multiple Documents Chatbot with Langchain & Streamlit |All OPEN SOURCE|Replicate API by DataInsightEdge
⛓ Chatting with 44K Fashion Products: LangChain Opportunities and Pitfalls by Rabbitmetrics
⛓ Structured Data Extraction from ChatGPT with LangChain by MG
⛓ Integrate Audio into LangChain.js apps in 5 Minutes by AssemblyAI
⛓ ChatGPT for your data with Local LLM by Jacob Jedryszek
⛓ Training Chatgpt with your personal data using langchain step by step in detail by NextGen Machines
⛓ Use ANY language in LangSmith with REST by Nerding I/O
⛓ How to Leverage the Full Potential of LLMs for Your Business with Langchain - Leon Ruddat by PyData
⛓ ChatCSV App: Chat with CSV files using LangChain and Llama 2 by Muhammad Moin
Prompt Engineering and LangChain by Venelin Valkov​
Getting Started with LangChain: Load Custom Data, Run OpenAI Models, Embeddings and ChatGPT
Build ChatGPT Chatbots with LangChain Memory: Understanding and Implementing Memory in Conversations

⛓ icon marks a new addition [last update 2023-09-21]

Official LangChain YouTube channel
Introduction to LangChain with Harrison Chase, creator of LangChain
Videos (sorted by views)
Prompt Engineering and LangChain by Venelin Valkov
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Tutorials | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/additional_resources/tutorials)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Tutorials

Below are links to tutorials and courses on LangChain. For written guides on common use cases for LangChain, check out the use cases guides.

⛓ icon marks a new addition [last update 2023-09-21]

LangChain on Wikipedia​
Books​
⛓Generative AI with LangChain by Ben Auffrath, ©️ 2023 Packt Publishing​
DeepLearning.AI courses​

by Harrison Chase and Andrew Ng

LangChain for LLM Application Development
LangChain Chat with Your Data
⛓ Functions, Tools and Agents with LangChain
Handbook​

LangChain AI Handbook By James Briggs and Francisco Ingham

Short Tutorials​

LangChain Explained in 13 Minutes | QuickStart Tutorial for Beginners by Rabbitmetrics

LangChain Crash Course: Build an AutoGPT app in 25 minutes by Nicholas Renotte

LangChain Crash Course - Build apps with language models by Patrick Loeber

Tutorials​
LangChain for Gen AI and LLMs by James Briggs​
#1 Getting Started with GPT-3 vs. Open Source LLMs
LangChain Data Loaders, Tokenizers, Chunking, and Datasets - Data Prep 101
#4 Chatbot Memory for Chat-GPT, Davinci + other LLMs
#5 Chat with OpenAI in LangChain
#6 Fixing LLM Hallucinations with Retrieval Augmentation in LangChain
#7 LangChain Agents Deep Dive with GPT 3.5
#8 Create Custom Tools for Chatbots in LangChain
#9 Build Conversational Agents with Vector DBs
Using NEW MPT-7B in Hugging Face and LangChain
⛓ Fine-tuning OpenAI's GPT 3.5 for LangChain Agents
⛓ Chatbots with RAG: LangChain Full Walkthrough
LangChain 101 by Greg Kamradt (Data Indy)​
What Is LangChain? - LangChain + ChatGPT Overview
Quickstart Guide
Beginner's Guide To 7 Essential Concepts
Agents Overview + Google Searches
OpenAI + Wolfram Alpha
Ask Questions On Your Custom (or Private) Files
Connect Google Drive Files To OpenAI
YouTube Transcripts + OpenAI
Question A 300 Page Book (w/ OpenAI + Pinecone)
Workaround OpenAI's Token Limit With Chain Types
Build Your Own OpenAI + LangChain Web App in 23 Minutes
Working With The New ChatGPT API
OpenAI + LangChain Wrote Me 100 Custom Sales Emails
Structured Output From OpenAI (Clean Dirty Data)
Connect OpenAI To +5,000 Tools (LangChain + Zapier)
Use LLMs To Extract Data From Text (Expert Mode)
Extract Insights From Interview Transcripts Using LLMs
5 Levels Of LLM Summarizing: Novice to Expert
Control Tone & Writing Style Of Your LLM Output
Build Your Own AI Twitter Bot Using LLMs
ChatGPT made my interview questions for me (Streamlit + LangChain)
Function Calling via ChatGPT API - First Look With LangChain
Extract Topics From Video/Audio With LLMs (Topic Modeling w/ LangChain)
LangChain How to and guides by Sam Witteveen​
LangChain Basics - LLMs & PromptTemplates with Colab
ChatGPT API Announcement & Code Walkthrough with LangChain
Conversations with Memory (explanation & code walkthrough)
Chat with Flan20B
Using Hugging Face Models locally (code walkthrough)
PAL: Program-aided Language Models with LangChain code
Building a Summarization System with LangChain and GPT-3 - Part 1
Microsoft's Visual ChatGPT using LangChain
LangChain Agents - Joining Tools and Chains with Decisions
Comparing LLMs with LangChain
Using Constitutional AI in LangChain
Talking to Alpaca with LangChain - Creating an Alpaca Chatbot
Talk to your CSV & Excel with LangChain
BabyAGI: Discover the Power of Task-Driven Autonomous Agents!
Improve your BabyAGI with LangChain
Master PDF Chat with LangChain - Your essential guide to queries on documents
Using LangChain with DuckDuckGO, Wikipedia & PythonREPL Tools
Building Custom Tools and Agents with LangChain (gpt-3.5-turbo)
LangChain Retrieval QA Over Multiple Files with ChromaDB
LangChain + Retrieval Local LLMs for Retrieval QA - No OpenAI!!!
Camel + LangChain for Synthetic Data & Market Research
Converting a LangChain App from OpenAI to OpenSource
Using LangChain Output Parsers to get what you want out of LLMs
Building a LangChain Custom Medical Agent with Memory
Understanding ReACT with LangChain
OpenAI Functions + LangChain : Building a Multi Tool Agent
What can you do with 16K tokens in LangChain?
Tagging and Extraction - Classification using OpenAI Functions
HOW to Make Conversational Form with LangChain
⛓ Claude-2 meets LangChain!
⛓ LLaMA2 with LangChain - Basics | LangChain TUTORIAL
⛓ Serving LLaMA2 with Replicate
⛓ NEW LangChain Expression Language
⛓ Building a RCI Chain for Agents with LangChain Expression Language
⛓ How to Run LLaMA-2-70B on the Together AI
⛓ RetrievalQA with LLaMA 2 70b & Chroma DB
⛓ How to use BGE Embeddings for LangChain
⛓ How to use Custom Prompts for RetrievalQA on LLaMA-2 7B
LangChain by Prompt Engineering​
LangChain Crash Course — All You Need to Know to Build Powerful Apps with LLMs
Working with MULTIPLE PDF Files in LangChain: ChatGPT for your Data
Talk to YOUR DATA without OpenAI APIs: LangChain
LangChain: PDF Chat App (GUI) | ChatGPT for Your PDF FILES
LangFlow: Build Chatbots without Writing Code
LangChain: Giving Memory to LLMs
BEST OPEN Alternative to OPENAI's EMBEDDINGs for Retrieval QA: LangChain
LangChain: Run Language Models Locally - Hugging Face Models
⛓ Slash API Costs: Mastering Caching for LLM Applications
⛓ Avoid PROMPT INJECTION with Constitutional AI - LangChain
LangChain by Chat with data​
LangChain Beginner's Tutorial for Typescript/Javascript
GPT-4 Tutorial: How to Chat With Multiple PDF Files (~1000 pages of Tesla's 10-K Annual Reports)
LangChain Agents: Build Personal Assistants For Your Data (Q&A with Harrison Chase and Mayo Oshin)
Codebase Analysis​
Codebase Analysis: Langchain Agents

⛓ icon marks a new addition [last update 2023-09-21]

LangChain on Wikipedia
Books
DeepLearning.AI courses
Handbook
Short Tutorials
LangChain for Gen AI and LLMs by James Briggs
LangChain 101 by Greg Kamradt (Data Indy)
LangChain How to and guides by Sam Witteveen
Codebase Analysis
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Templates | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/templates/)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Templates
anthropic-iterative-search
basic-critique-revise
Bedrock JCVD 🕺🥋
cassandra-entomology-rag
cassandra-synonym-caching
Chain-of-Note (Wikipedia)
Chat Bot Feedback Template
cohere-librarian
csv-agent
elastic-query-generator
extraction-anthropic-functions
extraction-openai-functions
guardrails-output-parser
Hybrid Search in Weaviate
hyde
llama2-functions
mongo-parent-document-retrieval
neo4j-advanced-rag
neo4j-cypher-ft
neo4j-generation
neo4j-semantic-layer
neo4j-vector-memory
nvidia-rag-canonical
OpenAI Functions Agent - Gmail
openai-functions-agent
openai-functions-tool-retrieval-agent
pii-protected-chatbot
pirate-speak-configurable
pirate-speak
plate-chain
propositional-retrieval
python-lint
rag-astradb
rag-aws-bedrock
rag-chroma-multi-modal-multi-vector
rag-codellama-fireworks
rag-conversation-zep
rag-elasticsearch
rag-fusion
rag-gemini-multi-modal
rag-google-cloud-sensitive-data-protection
rag-gpt-crawler
rag-matching-engine
rag-momento-vector-index
rag-mongo
RAG with Multiple Indexes (Fusion)
rag-multi-modal-local
rag-ollama-multi-query
rag-opensearch
rag-pinecone-multi-query
rag-self-query
rag-singlestoredb
rag\_supabase
rag-timescale-conversation
RAG with Timescale Vector using hybrid search
rag-vectara-multiquery
rag-weaviate
research-assistant
retrieval-agent
rewrite\_retrieve\_read
Langchain - Robocorp Action Server
self-query-qdrant
skeleton-of-thought
solo-performance-prompting-agent
sql-llama2
sql-ollama
sql-research-assistant
stepback-qa-prompting
summarize-anthropic
vertexai-chuck-norris
xml-agent
Templates

Highlighting a few different categories of templates

⭐ Popular​

These are some of the more popular templates to get started with.

Retrieval Augmented Generation Chatbot: Build a chatbot over your data. Defaults to OpenAI and Pinecone.
Extraction with OpenAI Functions: Do extraction of structured data from unstructured data. Uses OpenAI function calling.
Local Retrieval Augmented Generation: Build a chatbot over your data. Uses only local tooling: Ollama, GPT4all, Chroma.
OpenAI Functions Agent: Build a chatbot that can take actions. Uses OpenAI function calling and Tavily.
📥 Advanced Retrieval​

These templates cover advanced retrieval techniques, which can be used for chat and QA over databases or documents.

Reranking: This retrieval technique uses Cohere's reranking endpoint to rerank documents from an initial retrieval step.
Anthropic Iterative Search: This retrieval technique uses iterative prompting to determine what to retrieve and whether the retriever documents are good enough.
Parent Document Retrieval using Neo4j or MongoDB: This retrieval technique stores embeddings for smaller chunks, but then returns larger chunks to pass to the model for generation.
Semi-Structured RAG: The template shows how to do retrieval over semi-structured data (e.g. data that involves both text and tables).
Temporal RAG: The template shows how to do hybrid search over data with a time-based component using Timescale Vector.
🔍Advanced Retrieval - Query Transformation​

A selection of advanced retrieval methods that involve transforming the original user query, which can improve retrieval quality.

Hypothetical Document Embeddings: A retrieval technique that generates a hypothetical document for a given query, and then uses the embedding of that document to do semantic search. Paper.
Step-back QA Prompting: A retrieval technique that generates a "step-back" question and then retrieves documents relevant to both that question and the original question. Paper.
RAG-Fusion: A retrieval technique that generates multiple queries and then reranks the retrieved documents using reciprocal rank fusion. Article.
Multi-Query Retriever: This retrieval technique uses an LLM to generate multiple queries and then fetches documents for all queries.
🧠Advanced Retrieval - Query Construction​

A selection of advanced retrieval methods that involve constructing a query in a separate DSL from natural language, which enable natural language chat over various structured databases.

Elastic Query Generator: Generate elastic search queries from natural language.
Neo4j Cypher Generation: Generate cypher statements from natural language. Available with a "full text" option as well.
Supabase Self Query: Parse a natural language query into a semantic query as well as a metadata filter for Supabase.
🦙 OSS Models​

These templates use OSS models, which enable privacy for sensitive data.

Local Retrieval Augmented Generation: Build a chatbot over your data. Uses only local tooling: Ollama, GPT4all, Chroma.
SQL Question Answering (Replicate): Question answering over a SQL database, using Llama2 hosted on Replicate.
⛏️ Extraction​

These templates extract data in a structured format based upon a user-specified schema.

Extraction Using OpenAI Functions: Extract information from text using OpenAI Function Calling.
Extraction Using Anthropic Functions: Extract information from text using a LangChain wrapper around the Anthropic endpoints intended to simulate function calling.
Extract BioTech Plate Data: Extract microplate data from messy Excel spreadsheets into a more normalized format.
⛏️Summarization and tagging​

These templates summarize or categorize documents and text.

Summarization using Anthropic: Uses Anthropic's Claude2 to summarize long documents.
🤖 Agents​

These templates build chatbots that can take actions, helping to automate tasks.

OpenAI Functions Agent: Build a chatbot that can take actions. Uses OpenAI function calling and Tavily.
🚨 Safety and evaluation​

These templates enable moderation or evaluation of LLM outputs.

Guardrails Output Parser: Use guardrails-ai to validate LLM output.
Chatbot Feedback: Use LangSmith to evaluate chatbot responses.
Next
anthropic-iterative-search
⭐ Popular
📥 Advanced Retrieval
🔍Advanced Retrieval - Query Transformation
🦙 OSS Models
⛏️ Extraction
⛏️Summarization and tagging
🤖 Agents
🚨 Safety and evaluation
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Welcome Contributors | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/contributing)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Welcome Contributors
Contribute Code
Testing
Contribute Documentation
Contribute Integrations
FAQ
Welcome Contributors

Hi there! Thank you for even being interested in contributing to LangChain. As an open-source project in a rapidly developing field, we are extremely open to contributions, whether they involve new features, improved infrastructure, better documentation, or bug fixes.

🗺️ Guidelines​
👩‍💻 Ways to contribute​

There are many ways to contribute to LangChain. Here are some common ways people contribute:

Documentation: Help improve our docs, including this one!
Code: Help us write code, fix bugs, or improve our infrastructure.
Integrations: Help us integrate with your favorite vendors and tools.
🚩GitHub Issues​

Our issues page is kept up to date with bugs, improvements, and feature requests.

There is a taxonomy of labels to help with sorting and discovery of issues of interest. Please use these to help organize issues.

If you start working on an issue, please assign it to yourself.

If you are adding an issue, please try to keep it focused on a single, modular bug/improvement/feature. If two issues are related, or blocking, please link them rather than combining them.

We will try to keep these issues as up-to-date as possible, though with the rapid rate of development in this field some may get out of date. If you notice this happening, please let us know.

🙋Getting Help​

Our goal is to have the simplest developer setup possible. Should you experience any difficulty getting setup, please contact a maintainer! Not only do we want to help get you unblocked, but we also want to make sure that the process is smooth for future contributors.

In a similar vein, we do enforce certain linting, formatting, and documentation standards in the codebase. If you are finding these difficult (or even just annoying) to work with, feel free to contact a maintainer for help - we do not want these to get in the way of getting good code into the codebase.

🌟 Recognition

If your contribution has made its way into a release, we will want to give you credit on Twitter (only if you want though)! If you have a Twitter account you would like us to mention, please let us know in the PR or through another means.

Next
Contribute Code
🗺️ Guidelines
👩‍💻 Ways to contribute
🚩GitHub Issues
🙋Getting Help
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Changelog | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/changelog)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Changelog
langchain-core
Changelog
📄️ langchain-core

0.1.7 (Jan 5, 2024)

📄️ langchain

0.1.0 (Jan 5, 2024)

Next
langchain-core
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## 📕 Package Versioning | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/packages)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
📕 Package Versioning

As of now, LangChain has an ad hoc release process: releases are cut with high frequency by a maintainer and published to PyPI. The different packages are versioned slightly differently.

langchain-core​

langchain-core is currently on version 0.1.x.

As langchain-core contains the base abstractions and runtime for the whole LangChain ecosystem, we will communicate any breaking changes with advance notice and version bumps. The exception for this is anything marked with the beta decorator (you can see this in the API reference and will see warnings when using such functionality). The reason for beta features is that given the rate of change of the field, being able to move quickly is still a priority.

Minor version increases will occur for:

Breaking changes for any public interfaces marked as beta.

Patch version increases will occur for:

Bug fixes
New features
Any changes to private interfaces
langchain​

langchain is currently on version 0.1.x

Minor version increases will occur for:

Breaking changes for any public interfaces NOT marked as beta.

Patch version increases will occur for:

Bug fixes
New features
Any changes to private interfaces

We are targeting February 2024 for a release of langchain v0.2, which will have some breaking changes to legacy Chains and Agents. Additionally, we will remove langchain-community as a dependency and stop re-exporting integrations that have been moved to langchain-community.

langchain-community​

langchain-community is currently on version 0.0.x

All changes will be accompanied by a patch version increase.

langchain-experimental​

langchain-experimental is currently on version 0.0.x

All changes will be accompanied by a patch version increase.

Partner Packages​

Partner packages are versioned independently.

langchain-core
Partner Packages
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Debugging | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/guides/debugging)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Debugging
Deployment
Evaluation
Fallbacks
Run LLMs locally
Model comparison
Privacy
Pydantic compatibility
Safety
Debugging

If you're building with LLMs, at some point something will break, and you'll need to debug. A model call will fail, or the model output will be misformatted, or there will be some nested model calls and it won't be clear where along the way an incorrect output was created.

Here are a few different tools and functionalities to aid in debugging.

Tracing​

Platforms with tracing capabilities like LangSmith and WandB are the most comprehensive solutions for debugging. These platforms make it easy to not only log and visualize LLM apps, but also to actively debug, test and refine them.

For anyone building production-grade LLM applications, we highly recommend using a platform like this.

set\_debug and set\_verbose​

If you're prototyping in Jupyter Notebooks or running Python scripts, it can be helpful to print out the intermediate steps of a Chain run.

There are a number of ways to enable printing at varying degrees of verbosity.

Let's suppose we have a simple agent, and want to visualize the actions it takes and tool outputs it receives. Without any debugging, here's what we see:

from langchain.agents import AgentType, initialize\_agent, load\_tools
from langchain\_openai import ChatOpenAI

llm = ChatOpenAI(model\_name="gpt-4", temperature=0)
tools = load\_tools(["ddg-search", "llm-math"], llm=llm)
agent = initialize\_agent(tools, llm, agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION)

agent.run("Who directed the 2023 film Oppenheimer and what is their age? What is their age in days (assume 365 days per year)?")

 'The director of the 2023 film Oppenheimer is Christopher Nolan and he is approximately 19345 days old in 2023.'

set\_debug(True)​

Setting the global debug flag will cause all LangChain components with callback support (chains, models, agents, tools, retrievers) to print the inputs they receive and outputs they generate. This is the most verbose setting and will fully log raw inputs and outputs.

from langchain.globals import set\_debug

set\_debug(True)

agent.run("Who directed the 2023 film Oppenheimer and what is their age? What is their age in days (assume 365 days per year)?")

Console output
set\_verbose(True)​

Setting the verbose flag will print out inputs and outputs in a slightly more readable format and will skip logging certain raw outputs (like the token usage stats for an LLM call) so that you can focus on application logic.

from langchain.globals import set\_verbose

set\_verbose(True)

agent.run("Who directed the 2023 film Oppenheimer and what is their age? What is their age in days (assume 365 days per year)?")

Console output
Chain(..., verbose=True)​

You can also scope verbosity down to a single object, in which case only the inputs and outputs to that object are printed (along with any additional callbacks calls made specifically by that object).

# Passing verbose=True to initialize\_agent will pass that along to the AgentExecutor (which is a Chain).
agent = initialize\_agent(
 tools, 
 llm, 
 agent=AgentType.ZERO\_SHOT\_REACT\_DESCRIPTION,
 verbose=True,
)
agent.run("Who directed the 2023 film Oppenheimer and what is their age? What is their age in days (assume 365 days per year)?")

Console output
Other callbacks​

Callbacks are what we use to execute any functionality within a component outside the primary component logic. All of the above solutions use Callbacks under the hood to log intermediate steps of components. There are a number of Callbacks relevant for debugging that come with LangChain out of the box, like the FileCallbackHandler. You can also implement your own callbacks to execute custom functionality.

See here for more info on Callbacks, how to use them, and customize them.

Next
Deployment
Tracing
set\_debug and set\_verbose
set\_debug(True)
Chain(..., verbose=True)
Other callbacks
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Q&A with RAG | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/use_cases/question_answering/)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Use cases
Q&A with RAG
Quickstart
Returning sources
Add chat history
Streaming
Per-User Retrieval
Using agents
Using local models
Q&A over structured data
Interacting with APIs
Chatbots
Extraction
Summarization
Tagging
Web scraping
Code understanding
Synthetic data generation
Graph querying
Use casesQ&A with RAG
Q&A with RAG
Overview​

One of the most powerful applications enabled by LLMs is sophisticated question-answering (Q&A) chatbots. These are applications that can answer questions about specific source information. These applications use a technique known as Retrieval Augmented Generation, or RAG.

What is RAG?​

RAG is a technique for augmenting LLM knowledge with additional data.

LLMs can reason about wide-ranging topics, but their knowledge is limited to the public data up to a specific point in time that they were trained on. If you want to build AI applications that can reason about private data or data introduced after a model’s cutoff date, you need to augment the knowledge of the model with the specific information it needs. The process of bringing the appropriate information and inserting it into the model prompt is known as Retrieval Augmented Generation (RAG).

LangChain has a number of components designed to help build Q&A applications, and RAG applications more generally.

Note: Here we focus on Q&A for unstructured data. Two RAG use cases which we cover elsewhere are:

Q&A over structured data (e.g., SQL)
RAG Architecture​

A typical RAG application has two main components:

Indexing: a pipeline for ingesting data from a source and indexing it. This usually happens offline.

Retrieval and generation: the actual RAG chain, which takes the user query at run time and retrieves the relevant data from the index, then passes that to the model.

The most common full sequence from raw data to answer looks like:

Indexing​
Load: First we need to load our data. This is done with DocumentLoaders.
Split: Text splitters break large Documents into smaller chunks. This is useful both for indexing data and for passing it in to a model, since large chunks are harder to search over and won’t fit in a model’s finite context window.
Store: We need somewhere to store and index our splits, so that they can later be searched over. This is often done using a VectorStore and Embeddings model.

Retrieval and generation​
Retrieve: Given a user input, relevant splits are retrieved from storage using a Retriever.
Generate: A ChatModel / LLM produces an answer using a prompt that includes the question and the retrieved data

Table of contents​
Quickstart: We recommend starting here. Many of the following guides assume you fully understand the architecture shown in the Quickstart.
Returning sources: How to return the source documents used in a particular generation.
Streaming: How to stream final answers as well as intermediate steps.
Adding chat history: How to add chat history to a Q&A app.
Per-user retrieval: How to do retrieval when each user has their own private data.
Using agents: How to use agents for Q&A.
Using local models: How to use local models for Q&A.
Previous
Use cases
Next
Quickstart
Overview
What is RAG?
RAG Architecture
Table of contents
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Providers | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/integrations/providers)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Providers
Anthropic
AWS
Google
Hugging Face
Microsoft
OpenAI
More
Components
LLMs
Chat models
Document loaders
Document transformers
Text embedding models
Vector stores
Retrievers
Tools
Agents and toolkits
Memory
Callbacks
Chat loaders
Adapters
Stores
📄️ Anthropic

All functionality related to Anthropic models.

📄️ AWS

The LangChain integrations related to Amazon AWS platform.

📄️ Google

All functionality related to Google Cloud Platform and other Google products.

📄️ Hugging Face

All functionality related to the Hugging Face Platform.

📄️ Microsoft

All functionality related to Microsoft Azure and other Microsoft products.

📄️ OpenAI

All functionality related to OpenAI

🗃️ More

201 items

Next
Anthropic
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.

## Introduction | 🦜️🔗 Langchain

[Read More](https://python.langchain.com/docs/get_started/introduction)

Skip to main content
🦜️🔗 LangChain
Docs
Use cases
Integrations
Guides
API
More
Chat
K
Get started
Introduction
Installation
Quickstart
Security
LangChain Expression Language
Get started
Why use LCEL
Interface
How to
Cookbook
Modules
Model I/O
Retrieval
Agents
Chains
More
LangServe
LangSmith
Get startedIntroduction
Introduction

LangChain is a framework for developing applications powered by language models. It enables applications that:

Are context-aware: connect a language model to sources of context (prompt instructions, few shot examples, content to ground its response in, etc.)

This framework consists of several parts.

LangChain Libraries: The Python and JavaScript libraries. Contains interfaces and integrations for a myriad of components, a basic run time for combining these components into chains and agents, and off-the-shelf implementations of chains and agents.
LangChain Templates: A collection of easily deployable reference architectures for a wide variety of tasks.
LangServe: A library for deploying LangChain chains as a REST API.
LangSmith: A developer platform that lets you debug, test, evaluate, and monitor chains built on any LLM framework and seamlessly integrates with LangChain.

Together, these products simplify the entire application lifecycle:

Develop: Write your applications in LangChain/LangChain.js. Hit the ground running using Templates for reference.
Productionize: Use LangSmith to inspect, test and monitor your chains, so that you can constantly improve and deploy with confidence.
Deploy: Turn any chain into an API with LangServe.
LangChain Libraries​

The main value props of the LangChain packages are:

Components: composable tools and integrations for working with language models. Components are modular and easy-to-use, whether you are using the rest of the LangChain framework or not
Off-the-shelf chains: built-in assemblages of components for accomplishing higher-level tasks

Off-the-shelf chains make it easy to get started. Components make it easy to customize existing chains and build new ones.

The LangChain libraries themselves are made up of several different packages.

langchain-core: Base abstractions and LangChain Expression Language.
langchain: Chains, agents, and retrieval strategies that make up an application's cognitive architecture.
Get started​

Here’s how to install LangChain, set up your environment, and start building.

We recommend following our Quickstart guide to familiarize yourself with the framework by building your first LangChain application.

Read up on our Security best practices to make sure you're developing safely with LangChain.

NOTE

These docs focus on the Python LangChain library. Head here for docs on the JavaScript LangChain library.

LangChain Expression Language (LCEL)​

LCEL is a declarative way to compose chains. LCEL was designed from day 1 to support putting prototypes in production, with no code changes, from the simplest “prompt + LLM” chain to the most complex chains.

Overview: LCEL and its benefits
Interface: The standard interface for LCEL objects
How-to: Key features of LCEL
Cookbook: Example code for accomplishing common tasks
Modules​
LangChain provides standard, extendable interfaces and integrations for the following modules:

Model I/O​

Interface with language models

Retrieval​

Interface with application-specific data

Agents​

Let models choose which tools to use given high-level directives

Examples, ecosystem, and resources​
Use cases​

Walkthroughs and techniques for common end-to-end use cases, like:

Document question answering
Chatbots
Analyzing structured data
and much more...
Integrations​

LangChain is part of a rich ecosystem of tools that integrate with our framework and build on top of it. Check out our growing list of integrations.

Guides​

Best practices for developing with LangChain.

API reference​

Head to the reference section for full documentation of all classes and methods in the LangChain and LangChain Experimental Python packages.

Developer's guide​

Check out the developer's guide for guidelines on contributing and help getting your dev environment set up.

Community​

Head to the Community navigator to find places to ask questions, share feedback, meet other developers, and dream about the future of LLM’s.

Get started
Next
Installation
LangChain Libraries
Get started
LangChain Expression Language (LCEL)
Modules
Examples, ecosystem, and resources
Use cases
Integrations
Guides
API reference
Developer's guide
Community
Discord
Twitter
GitHub
Python
JS/TS
More
Homepage
Blog
Copyright © 2024 LangChain, Inc.