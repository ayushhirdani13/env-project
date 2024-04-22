## Sample Templates
prompt_with_docs_template = """You are Climate-X, an AI Assistant. You are given a question and extracted abstracts of scientific papers or articles. Provide a clear and structured answer based on the abstracts provided, the context and the guidelines.

Guidelines:
- If the passages have useful facts or numbers, use them in your answer.
- When you use information from a passage, mention where it came from by using [Doc i] at the end of the sentence. i stands for the number of the document.
- Do not use the sentence 'Doc i says ...' to say where information came from.
- If the same thing is said in more than one document, you can mention all of them like this: [Doc i, Doc j, Doc k]
- Do not just summarize each passage one by one. Group your summaries to highlight the key parts in the explanation.
- If it makes sense, use bullet points and lists to make your answers easier to understand.
- Use markdown to format your answer and make it easier to read.
- You do not need to use every passage. Only use the ones that help answer the question.
- If the question is not climate-related, just say that you can only answer questions related to sustainability, environment, etc.
- If the documents do not have the information needed to answer the question, just say YOU do not have enough information.

-----------------------
Abstracts:
{context}

-----------------------
Question: {question}
"""

prompt_without_docs_template = """
You are Climate-X, an AI Assistant. Your role is to answer climate-related questions to the users.
Always stay true to climate science and do not make up information. If you do not know the answer, just say you do not know. Adhere to the Guidelines below strictly.

Guidelines:
- If it's a conversational question such as "hello", "who are you", ..., you can answer directly, but keep them very short and tell the user to ask climate related question only
- You can suggest the users to search on the internet for papers like IPCC, IPBES reports which can help
- Because your role is to explain climate science, you can never be skeptical about climate change. 
- If the question is not related to environmental issues, never never answer it. Say it's not your role.
- Make paragraphs by starting new lines to make your answers more readable.

Question: {question}
"""

QUESTIONS = {
    "Popular Questions": [
        "What evidence do we have of climate change?",
        "Are human activities causing global warming?",
        "What are the impacts of climate change?",
        "Can climate change be reversed?",
        "What is the difference between climate change and global warming?",
        "What can individuals do to address climate change?",
        "What is the Paris Agreement and why is it important?",
        "Is climate change a hoax created by the government or environmental organizations?",
        "What is the relationship between climate change and biodiversity loss?",
        "Is climate change caused by humans?",
        "What is the link between gender equality and climate change?",
        "Is the impact of climate change really as severe as it is claimed to be?",
        "What is the impact of rising sea levels?",
        "What are the different greenhouse gases (GHG)?",
        "What is the warming power of methane?",
        "What is the jet stream?",
        "What is the breakdown of carbon sinks?",
        "How do the GHGs work ? Why does temperature increase ?",
        "What is the impact of global warming on ocean currents?",
        "How much warming is possible in 2050?",
        "Will climate change accelerate diseases and epidemics like COVID?",
        "What are the economic impacts of climate change?",
        "What are the most effective strategies and technologies for reducing greenhouse gas (GHG) emissions?",
        "Is climate change a natural phenomenon ?",
        "Is climate change really happening or is it just a natural fluctuation in Earth's temperature?",
        "Is the scientific consensus on climate change really as strong as it is claimed to be?",
    ],   
    "Climate Science":[
        "How do climate models project the interaction between atmospheric CO2 levels and global temperature changes over the next century?",
        "What are the projected impacts of arctic permafrost thawing on global methane emissions?",
        "How does the IPCC assess the efficacy of different carbon capture and storage technologies in mitigating climate change?",
        "What are the predicted changes in oceanic thermohaline circulation under various greenhouse gas emission scenarios?",
        "How does increased atmospheric CO2 concentration affect the acidification of oceans and its impact on marine biodiversity?",
        "What role do cloud formations play in modulating the Earth's radiative balance, and how are they represented in current climate models?",
        "What are the implications of polar ice sheet dynamics for global sea-level rise under high-emission scenarios?",
        "How do feedback mechanisms in the climate system, such as the albedo effect, influence global warming projections?",
        "What are the latest findings on the sensitivity of the climate to a doubling of pre-industrial CO2 levels?",
        "How do regional climate projections differ in terms of extreme weather events like droughts, floods, and heatwaves?",
    ],
    "Economy":[
        "Which industries have the highest GHG emissions?",
        "How much is the cost of inaction ?",
        "Will technology save us?",
        "What is the relationship between climate change and poverty?",
        "Is economic growth possible? What do you think about degrowth?",
    ],
    "Invasive Species": [
        "What are invasive alien species and how do they threaten biodiversity and ecosystems?",
        "How do invasive alien species contribute to global and local species extinctions?",
        "In what ways do invasive species lead to biotic homogenization?",
        "What are the economic impacts of invasive alien species on global economies?",
        "How do invasive alien species affect food and water security and human health?",
        "What are the challenges in managing invasive alien species in different regions?",
        "How are human activities contributing to the spread of invasive alien species?",
        "What are the current trends and future predictions regarding the threats from invasive alien species?",
        "How can we predict the future impact of invasive alien species given their complex interactions with other factors?",
        "What is the role of international trade in facilitating the introduction of invasive alien species?",
        "What are some effective strategies for managing invasive alien species?",
        "How crucial is prevention in managing the threats from invasive alien species?",
        "What are some successful examples of eradication of invasive alien species?",
        "What are the limitations and successes of containment and control strategies for invasive alien species?",
        "How does adaptive management, including ecosystem restoration, help in dealing with invasive species?",
        "Why is stakeholder and community engagement important in managing biological invasions?",
        "What is integrated governance in the context of biological invasion management?",
        "How can international and regional collaboration improve the management of biological invasions?",
        "What opportunities does the Kunming-Montreal Global Biodiversity Framework provide in addressing invasive species?",
        "How does managing invasive alien species intersect with achieving Sustainable Development Goals?",
        "What are the implications of biological invasions for policies aimed at conserving marine and terrestrial biodiversity?",
        "How do demographic changes influence the spread of invasive alien species?",
        "What are the impacts of invasive alien species on Indigenous Peoples and local communities?",
        "What technologies and tools are available for managing invasive alien species?",
        "How do economic and land-use changes facilitate the introduction and spread of invasive alien species?"
    ],
    "Experimental images":[
        "Is warming unprecedented in the past 200 years ?",
        "Are human activities causing global warming?",
        "What is the distribution of uncertainty in projected precipitation changes across different time frames ?",
        "What are the anticipated changes in the global water cycle by the end of the 21st century under an intermediate emissions scenario ?",
        "How are human activities contributing to the spread of invasive alien species?",
    ],
    "Deep Sea Mining":[
        "What is the motivation behind mining the deep seabed?",
        "What are the arguments in favor of and against deep-sea mining?",
        "Can the global demand for metals and resources be met adequately through land-based sources for the next few decades?",
        "Is it essential for humanity to exploit the deep ocean for minerals, or should we consider alternative pathways?",
        "What are the environmental impacts of deep-sea mining in order of significance, indicating the degree or severity of the impacts?",
        "What specific substances are likely to be released as contaminants through deep-sea mining?",
        "How might the substances released through deep-sea mining pose a threat to marine life?",
        "What are the various environmental stressors associated with deep-sea mining, including factors like noise, vibration, and light?",
        "How would environmental stressors associated with deep-sea mining affect marine ecosystems?",
        "How will the removal of mineral resources as a result of deep-sea mining impact the living components of the ecosystem?",
        "How will deep-sea mining influence ocean currents, large-scale circulation, and biogeochemical cycles?",
        "What are the potential ramifications of deep-sea mining for global ocean processes?",
        "What are the potential repercussions of deep-sea mining on climate regulation, considering the role of deep-sea ecosystems in climate dynamics?",
        "How resilient are the targeted habitats of deep-sea ecosystems (nodules, sulfides, crusts) to the impacts of deep-sea mining?",
        "Apart from the ecological consequences of deep-sea mining, what economic challenges could a state encounter if a deep-seabed mining operation leads to financial losses or third-party liability?",
        "What legal steps would need to be designed to authorize deep-sea mining?",
        "Is the current technological infrastructure sufficiently advanced and tested to support the implementation of deep-sea mining operations effectively?",
        "Provide me with a list of organizations most actively opposing deep-sea mining."
    ]
}