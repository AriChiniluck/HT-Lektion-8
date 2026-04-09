# Еволюція Retrieval Augmented Generation: архітектури, метрики та системи до рубежу 2025–початку 2026 року

## Короткий дисклеймер і межі актуальності

Цей звіт є **best-effort оглядом еволюції RAG** станом приблизно до кінця 2025 – початку 2026 року на основі доступних публічних джерел (наукові статті, огляди, промислові whitepapers, документація фреймворків і хмарних сервісів). 

- **Факти й датування підтверджено переважно до 2024–2025 років.**
- Для початку 2026 року ми **не знайшли переконливих публічних джерел про появу принципово нових класів RAG-архітектур або радикально нових бенчмарків/метрик**, які б змінювали вже сформований ландшафт.
- Тому **будь-які твердження про 2026+ як про «наступне покоління RAG» тут свідомо НЕ робляться**. Усе, що стосується періоду після 2025 року, позначається як: «наразі не підтверджено» або описується лише як продовження вже відомих трендів.

## Executive summary

Retrieval-Augmented Generation (RAG) еволюціонував із поєднання класичного IR та генерації (2020) до багатокомпонентних, оркестровано-керованих, агентних систем (2024–2025), що включають multi-hop міркування, довготривалу пам’ять, графові/модульні індекси, інструментальні виклики та streaming-обробку. 

Ключові етапи:
- **2020** – формальне введення RAG (Lewis et al.), dense retriever + генеративна модель.
- **2021–2022** – закріплення dense retrieval, ColBERT/late interaction, перші продакшн-сценарії.
- **2022–2024** – поява й популяризація HyDE, multi-hop RAG, agentic/workflow-підходів, memory RAG, modular/graph RAG, tool-augmented і streaming RAG.
- **2024–2025** – вихід великих survey-паперів і вендорних гідів, формалізація таксономій (retriever-centric, generator-centric, hybrid, agentic/orchestration, robustness-oriented, MoE-RAG). З’являються RAG-специфічні метрики й бенчмарки (RAGAS, CRAG, FreshQA).
- **Початок 2026** – інтенсивний розвиток уже відомих напрямів (agentic, graph, memory, MoE-RAG), але **без публічно зафіксованих радикально нових архітектурних сімейств**.

RAG сьогодні – це не одна архітектура, а **родина патернів**, що комбінують різні retrievers, індекси, агенти, інструменти та механізми оцінки. Метрики виходять за рамки класичних IR- і QA-показників: важливими стають faithfulness/groundedness, hallucination rate, relevance та корисність, часто виміряні через LLM-as-a-judge. Індустрія (Azure, AWS, GCP, Databricks, Snowflake, Pinecone, Qdrant, Weaviate, Milvus тощо) закріпила набір референтних RAG-архітектур, який на рубежі 2025–2026 виглядає зрілим і стабільним.

---

## 1. Вступ: що таке RAG і навіщо він потрібен

Retrieval-Augmented Generation (RAG) — це парадигма, у якій генеративна модель (переважно великий мовний модель — LLM) **умовлюється на зовнішніх знаннях**, витягнутих механізмом інформаційного пошуку (retriever) на етапі інференсу. На відміну від чисто параметричних LLM, що покладаються на знання, «зашиті» в їхні ваги під час тренування, RAG дозволяє:

- **оновлювати знання без перетренування моделі** (заміна/оновлення індексу);
- **зменшувати галюцинації** за рахунок вимоги спиратися на retrieved контекст;
- **адаптуватись до домену** (індексація корпоративних документів, БЗ, баз кодів тощо);
- **пояснювати відповіді** через посилання на першоджерела (documents-as-evidence).

Типова high-level схема RAG:

1. Користувацький запит q.
2. Retriever шукає топ-k релевантних документів/пасажів D = {d1, …, dk} у зовнішньому сховищі (BM25, dense retriever, ColBERT тощо).
3. LLM отримує як вхід (q, D) і генерує відповідь a, часто з посиланнями на D.

Ця базова схема надалі доповнюється: re-ranking, контекстною компресією, multi-hop retrieval, агентами, memory, графами, інструментами тощо.

**Джерела (дефініція)**
- Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS 2020.
- IBM, *What is Retrieval-Augmented Generation (RAG)?* (whitepaper/документація, 2023).
- Microsoft Azure Architecture Center, *Information retrieval in RAG*, 2025-01-10.
- Local: retrieval-augmented-generation.pdf, p.0–1.

---

## 2. Історична еволюція RAG (хронологія)

### 2018–2019: Попередники RAG

- Open-domain QA з архітектурою **retriever + reader** (DrQA, BERT-based readers) фактично реалізують ідею «знайди документи → згенеруй/витягни відповідь», але без терміну «RAG» і без LLM як генератора.
- Датасети типу **Natural Questions, TriviaQA** задають стандарт для knowledge-intensive tasks.

### 2020: Формальне введення RAG

- **Lewis et al., 2020 (NeurIPS)**:
  - Dense passage retriever (DPR) використовує дві BERT-подібні моделі для запитів і документів.
  - Генератор (BART) отримує concatenated passages + запит.
  - Показано покращення на NQ, TriviaQA, KILT тощо.
- У цей же період з’являється **ColBERT** (Khattab & Zaharia, SIGIR 2020) як ефективний late-interaction retriever.

### 2021–2022: Масове прийняття dense retrieval

- DPR, ANCE, ColBERTv2 та інші dense retrievers стають стандартом для open-domain QA і пошуку.
- RAG-підходи застосовуються в різних задачах: fact-checking, entity linking, dialog QA.
- З’являються перші продакшн-рішення на основі RAG у великих компаніях (часто без широкого розголосу деталей).

### 2022–2023: Поява HyDE, поширення RAG разом з LLM

- **HyDE (Gao et al., 2022–2023)**: генеративна модель створює «гіпотетичний документ», який використовують для dense retrieval (Hypothetical Document Embeddings).
- Кінець 2022 – 2023: масова популярність ChatGPT/LLM → різкий інтерес до RAG як способу «підживлювати» LLM корпоративними знаннями.
- OSS-фреймворки **LangChain, LlamaIndex** (2022–2023+) активно просувають RAG-патерни.
- Вендорні гіди (**IBM 2023, Microsoft, Google Cloud, AWS**) починають пропонувати RAG як базову архітектуру для enterprise assistants.

### 2023–2024: Розширення архітектур

Паралельно розвиваються кілька напрямів:

- **ColBERT/late interaction у RAG**: завдяки високій точності й можливості масштабування, ColBERT та його варіанти (ColBERTv2, PLAID, ColBERTer) використовуються як retriever в RAG (напр. фреймворк RAGatouille, 2023+).
- **Multi-hop RAG**: ітеративний retrieval, де LLM генерує проміжні підзапити; використання датасетів HotpotQA, 2WikiMultihopQA, MuSiQue.
- **Agentic / tool-augmented RAG**: 
  - LangChain Agents, LlamaIndex Agents — LLM приймає рішення про те, коли й як звертатись до retriever’ів чи інших tools (SQL, веб-пошук, код).
- **Memory RAG**: 
  - збереження довгострокового контексту (історії діалогів, налаштувань користувача) у векторних БД і його повторне використання (LangChain Memory, LlamaIndex ChatMemory).
- **Modular / Graph RAG**: 
  - Microsoft/Azure та інші публікують приклади Graph RAG: indexing документів у вигляді графа (теми, entities, лінки) і навігація по ньому.

### 2024–2025: Формалізація таксономій та метрик

- Виходять **survey-папери**:
  - *A Survey of Retrieval-Augmented Generation (RAG) for Large Language Models* (IEEE, ≈2024–2025).
  - *Retrieval-Augmented Generation: A Comprehensive Survey of RAG Systems* (arXiv:2506.00054, 2025).
  - *Retrieval-Augmented Generation for AI-Generated Content: A Survey* (Springer, 2025).
- Вони систематизують архітектури за ознаками:
  - retriever-centric / generator-centric / hybrid;
  - orchestration- / agentic-oriented RAG;
  - robustness-oriented RAG (до шуму, розбіжностей у джерелах, атак);
  - graph-based, memory-augmented, multi-hop, streaming, MoE-RAG.
- З’являються й укорінюються **RAG-специфічні метрики та бенчмарки** (RAGAS, CRAG, FreshQA).
- Хмарні провайдери (Azure, AWS, GCP, Databricks, Snowflake, Pinecone) формалізують **reference architectures** для RAG.

### Початок 2026: Стабілізація пейзажу

За наявними публічними джерелами на початок 2026 року:

- **Немає переконливих ознак появи принципово нової сім’ї RAG-архітектур**, яка б якісно відрізнялась від уже описаних (classic, HyDE-based, ColBERT/late interaction, multi-hop, agentic, memory, graph/modular, tool-augmented, streaming, MoE-RAG).
- Відбувається еволюційне посилення наявних напрямів (кращі retrievers, краща оркестрація, cost-aware routing, evaluation). Будь-які гучні маркетингові назви «RAG 2.0/3.0/2026» зазвичай вкладаються в уже відомі патерни.

---

## 3. Ключові архітектурні патерни RAG

У цьому розділі описано основні типи RAG-архітектур, їхню суть, типові сценарії використання та орієнтовний горизонт актуальності.

### 3.1 Classic / baseline RAG

**Ідея.**
- Retrieval (BM25 або dense retriever) → концентрація кількох релевантних пасажів → LLM-генерація відповіді на основі цього контексту.

**Архітектура.**
- Індексація документів (chunking, embeddings / inverted index).
- Під час запиту: q → retriever → top-k chunks → (опційний rerank) → concat (q + chunks) → LLM → відповідь.

**Use cases.**
- Enterprise Q&A, документація, self-service support, юридичні/технічні довідники, внутрішні портали.

**Горизонт актуальності.**
- Від 2020 (Lewis et al.) і далі, активно використовується до 2025–початку 2026 без принципових змін у базовій схемі.

### 3.2 HyDE (Hypothetical Document Embeddings)

**Ідея.**
- Перед retrieval’ом LLM генерує «гіпотетичний документ» чи кандидатну відповідь, яка потім **ембедиться** і використовується як покращений запит для dense retriever.

**Архітектура.**
- q → LLM → d_hyp (гіпотетичний документ) → embed(d_hyp) → vector search → реальні docs → LLM (final answer).

**Use cases.**
- Zero-shot / low-resource retrieval без релевантних label-ів.
- Довгі, неоднозначні чи креативні запити.

**Горизонт актуальності.**
- Публікація: HyDE (Gao et al., 2022–2023), активне використання у RAG-фреймворках 2023–2025. Немає свідчень, що концепт стає «застарілим» на початку 2026.

### 3.3 ColBERT / late interaction у RAG

**Ідея.**
- Токен-рівнева порівняльна оцінка запиту й документа (late interaction) для отримання точного й масштабованого retriever’а.

**Архітектура.**
- Кожен документ і запит кодується у вектори токенів.
- Під час запиту виконується MaxSim/late interaction між токенами.
- ColBERT часто використовується разом із індексаційними структурами для масштабування (PLAID тощо).
- У RAG: ColBERT → top-k пасажів → LLM.

**Use cases.**
- Високоточний пошук в юридичних/медичних/наукових корпусах.
- Великі корпусові системи, де recall і precision критичні.

**Горизонт актуальності.**
- ColBERT: 2020; активна інтеграція в RAG з 2022–2024 (наприклад, RAGatouille). До 2025–2026 залишається одним із сильних класів retrievers.

### 3.4 Multi-hop RAG

**Ідея.**
- Складні запити часто вимагають послідовного отримання різних фрагментів знань. Multi-hop RAG поєднує **ітеративний retrieval і reasoning**: проміжні кроки LLM породжують нові підзапити.

**Архітектура (спрощено).**
- Крок 1: q → retriever → контекст1 → LLM → підзапит q2.
- Крок 2: q2 → retriever → контекст2 → LLM → (можливий q3) …
- Фінальний крок: LLM агрегує всі знайдені контексти й генерує узагальнену відповідь.

**Use cases.**
- Аналітичні запити, що вимагають поєднання кількох фактів.
- Multi-hop QA на датасетах HotpotQA, 2WikiMultihopQA, MuSiQue.

**Горизонт актуальності.**
- Multi-hop QA датасети з 2018–2021, ітеративні RAG-патерни активно розвиваються у 2022–2024 і залишаються предметом досліджень/продакшн-експериментів до 2025.

### 3.5 Agentic RAG

**Ідея.**
- LLM виступає **агентом-оркестратором**, що сам планує ланцюг дій: які retrievers/індекси/інструменти викликати, в якій послідовності, як оцінювати проміжні результати.

**Архітектура.**
- Agent loop (LLM) → планування → виклик tools:
  - «search_corporate_docs», «search_web», «run_sql_query», «call_RAG_index_X», …
- Отримані результати знову подаються в агента, який вирішує наступний крок.

**Use cases.**
- Складні бізнес-процеси: аудит, генерація звітів, юридичний аналіз із витребуванням документів, BI.
- Multi-source / multi-tool інтеграції (RAG як один із інструментів).

**Горизонт актуальності.**
- Широко висвітлюється в туторіалах та блогах LangChain/LlamaIndex 2023–2025, в оглядах 2024–2025 позначається як «agentic RAG» або «orchestration-centric RAG».

### 3.6 Memory RAG

**Ідея.**
- Додати **довготривалу пам’ять** до RAG: зберігати історію користувача, попередні розмови, завдання чи проміжні артефакти в окремому індексі й витягувати їх при подальших зверненнях.

**Архітектура.**
- Окремі retrievers: memory_retriever (history) + knowledge_retriever (docs).
- LLM отримує комбінацію поточного запиту, релевантного історичного контексту й документів.

**Use cases.**
- Персоналізовані асистенти (налаштування, переваги, минулі задачі).
- Довготривалі освітні/коучингові сценарії.
- Support-системи з контекстом попередніх інцидентів.

**Горизонт актуальності.**
- Окремі роботи з memory для LLM (2023–2024), підтримка у LangChain/LlamaIndex, активно використовується 2023–2025. Немає ознак «зникнення» цього підходу у 2026.

### 3.7 Modular / Graph / GraphRAG

**Ідея.**
- Представити знання як **граф** (nodes: документи, секції, entities, теми; edges: посилання, топік-зв’язки) й дозволити retrieval/LLM планувати traversal.
- Розбити RAG на модулі (retrievers, routers, summarizers, tools) з явним workflow.

**Архітектура.**
- GraphRAG:
  - побудова графа із колекції документів (кластеризація, topic modeling, KG extraction);
  - запит → знаходження релевантних вузлів → traversal → агрегація субграфа → LLM.
- Modular RAG:
  - router/agent вирішує, який retriever/індекс/модальність використовувати; вихід кожного модуля може бути перетворений чи стиснений іншими модулями.

**Use cases.**
- Наукові/правові бази знань із великою кількістю посилань.
- Entity-centric запити (про компанії, людей, терміни) з потребою контексту з різних частин графа.

**Горизонт актуальності.**
- Приклади Microsoft/Azure GraphRAG (~2024), розгорнуто описані у survey-паперах 2024–2025. На початок 2026 — це один із активно розвиваних напрямів, а не минулий тренд.

### 3.8 Tool/RAG (tool-augmented RAG)

**Ідея.**
- Включити retrieval як один із **інструментів** у ширшому tool-using/agentic середовищі й поєднати з іншими інструментами (SQL, веб-пошук, код, API).

**Архітектура.**
- LLM (через function calling / tools API) викликає:
  - `retrieve_docs`, `search_web`, `run_sql`, `run_python`, …
- Потім об’єднує результати.

**Use cases.**
- Аналітика (злиття корпоративних БД, документів, зовнішніх API).
- BI-звіти, фінансові/логістичні розрахунки з поясненням.

**Горизонт актуальності.**
- Популярний з 2022–2023 (ReAct, Toolformer-подібні підходи, LangChain/LlamaIndex tools), повністю інтегрований у RAG-сценарії 2023–2025; на 2026 рік — базовий патерн для складних систем.

### 3.9 Streaming RAG

**Ідея.**
- Підтримка **низької затримки та/або безперервного оновлення даних**: нові документи одразу індексуються, відповіді стрімляться користувачу.

**Архітектура.**
- Real-time ingestion у векторну БД (Qdrant, Weaviate, Milvus тощо).
- LLM-streaming відповіді (часткові токени) з уже отриманих доків; опційно — довантаження додаткових документів «на льоту».

**Use cases.**
- Моніторинг логів і алертів.
- Новинні/фінансові стріми.
- Support-системи, де індекс постійно оновлюється новими тікетами.

**Горизонт актуальності.**
- Активний розвиток у 2023–2025; на початку 2026 немає ознак зниження значущості.

### 3.10 Інші важливі модулі: rerankers, context compression, query rewriting, routing, MoE-RAG

Ці компоненти не завжди виділяють як окремі класи RAG, але в survey-паперах 2024–2025 вони розглядаються як ключові складові **просунутих RAG-пайплайнів**.

- **Rerankers**: 
  - Cross-encoder, monoT5, ColBERT як reranker top-k документів.
  - Критично важливі для систем, де precision (а не тільки recall) є головним.

- **Context compression / summarization**:
  - LLM чи окремі моделі стискають великі документи до компактних summary перед промптінгом.
  - Реалізовано в LlamaIndex («Context Compression»), LangChain («ContextualCompressionRetriever»), 2023–2024.

- **Query rewriting / expansion**:
  - LLM переписує запит (нормалізація, уточнення, розбиття на підзапити). HyDE можна розглядати як особливий випадок (генерація гіпотетичного документа).

- **Routing / MoE-RAG (Mixture-of-Experts RAG)**:
  - Router (часто LLM) обирає між кількома retrievers/індексами чи LLM’ами (cheap vs expensive, domain-specific vs general).
  - Перші публікації й реалізації — 2023–2025; у survey-паперах 2025 це вже окремий підтип.

---

## 4. Метрики та методики оцінювання RAG

### 4.1 Класичні IR-метрики (retrieval-рівень)

- **Recall@k, Precision@k** — частка релевантних документів серед top-k і навпаки.
- **MRR (Mean Reciprocal Rank)** — позиція першого релевантного документа.
- **nDCG@k (Normalized Discounted Cumulative Gain)** — оцінка якості ранжування з урахуванням позицій.

Використання:
- При тестуванні retrievers на бенчмарках BEIR, MS MARCO, NQ, KILT та ін.

### 4.2 Task-level метрики (відповідь моделі)

- Open-domain QA: **Exact Match (EM), F1**, інколи BLEU/ROUGE-L.
- Summarization: ROUGE, BERTScore.
- Інші генеративні задачі: BLEU, ROUGE, METEOR, human evaluation.

Обмеження:
- Ці метрики недостатньо добре вимірюють **truthfulness, groundedness, корисність**, особливо в реальних enterprise-сценаріях.

### 4.3 Спеціалізовані RAG-метрики та фреймворки

#### RAGAS

- **RAGAS (Retrieval-Augmented Generation Assessment Suite)** — open-source фреймворк (2023–2024+).
- Метрики:
  - Answer Relevancy
  - Context Relevancy
  - Context Recall
  - Faithfulness (чи узгоджується відповідь з контекстом)
  - Harmfulness тощо.
- Реалізує **LLM-as-a-judge** + допоміжні розрахунки.
- Джерело: офіційна документація RAGAS (2023–2025).

#### CRAG та інші бенчмарки

- **CRAG** — бенчмарк/лідерборд для RAG із фокусом на factuality, grounding, robustness.
- Орієнтовно з’являється у 2024, активні результати/лідерборд до 2025.

#### Інші метрики

- FactScore, Q², TRUE, перевірка конкретних фактів/тверджень.
- Моделі для детекції галюцинацій та оцінки узгодженості відповіді з джерелами.

### 4.4 LLM-as-a-judge

- Підхід, коли **інше (часто сильніше) LLM** оцінює якість відповіді системи за такими критеріями:
  - factuality / truthfulness;
  - faithfulness-to-context;
  - relevance to query;
  - helpfulness, clarity.
- Застосування:
  - RAGAS 
  - внутрішні фреймворки вендорів (OpenAI, Anthropic, хмарні провайдери) 2023–2025.

Горизонт:
- 2023–2025 — стає де-факто стандартом для швидкого автоматизованого оцінювання.
- На початку 2026 **немає свідчень про відмову від цього підходу**, радше навпаки — підвищується його якість і точність.

---

## 5. Бенчмарки та датасети для RAG

### 5.1 Класичні open-domain QA / IR датасети

| Датасет      | Рік   | Тип            | Роль у RAG                                  | Оновлення / статус до 2025 |
|-------------|-------|----------------|---------------------------------------------|----------------------------|
| Natural Questions (NQ) | 2019 | Open-domain QA | Класичний для eval RAG (Lewis et al. 2020) | Активно використовується   |
| TriviaQA    | 2017  | Open-domain QA | Оцінка retriever+generator                  | Активно використовується   |
| MS MARCO    | 2016–18 | Passage ranking / QA | IR-бенчмарк; база для RAG-пайплайнів | Широко використовується    |
| KILT        | 2020  | Knowledge-intensive tasks | Комплексний набір задач для RAG    | Стандарт у дослідженнях    |
| BEIR        | 2021  | IR benchmark   | Тестування retrievers, непрямо RAG          | Базовий IR-бенчмарк        |
| MTEB        | 2022  | Embedding benchmark | Оцінка embedding-моделей для RAG     | Провідний ембеддинг-бенчмарк |

### 5.2 Multi-hop QA

- **HotpotQA (2018)** — multi-hop QA з supporting facts; широко використовується для тестування multi-hop RAG.
- **2WikiMultihopQA** — QA, що вимагає переходу між двома статтями Wikipedia.
- **MuSiQue** — складні багатокрокові запитання, що вимагають reasoning.

У RAG-контексті:
- Оцінюють як якість відповіді (EM/F1), так і **multi-hop recall** (чи всі потрібні пасажі були знайдені retriever’ом).

### 5.3 Спеціалізовані на фактичності / «свіжості» знань

- **FreshQA** — датасет для оцінки, наскільки система встигає за оновленням інформації (time-sensitive QA). Використовується для демонстрації переваг RAG над статичними LLM.
- **CRAG** — RAG benchmark/leaderboard з фокусом на factuality, grounding, robustness.

Горизонт:
- FreshQA і CRAG з’являються/активно обговорюються у 2023–2024, з оновленнями й результатами до 2025.
- Станом на початок 2026 **нема єдиного нового «стандартного» бенчмарка** для RAG, який би витіснив ці набори.

---

## 6. Відомі відкриті та продакшн-системи

### 6.1 Open-source фреймворки та платформи

**LangChain** (2022–2023+)
- Основний OSS-фреймворк для побудови RAG-пайплайнів та агентів.
- Підтримує:
  - classic RAG-ланцюжки (retriever → LLM chain);
  - агентів (agents) із tools, включно з retrievers;
  - memory-модулі;
  - інтеграції з десятками векторних БД.

**LlamaIndex** (раніше GPT Index)
- Орієнтований на побудову різних типів індексів (List, Tree, Graph, KG, SQL) і query-процесорів.
- Містить готові компоненти для graph RAG, context compression, agentic query engines.

**Haystack (deepset)**
- Пайплайни retriever + reader/generator ще до LLM-бума; нині активно використовується для RAG (інтеграції з Qdrant, Weaviate, Elastic, OpenSearch).

**RAGatouille**
- Спеціалізується на ColBERT-based RAG; дозволяє будувати високоточні ColBERT-індекси та використовувати їх у RAG.

### 6.2 Векторні бази / пошукові платформи

- **Qdrant** — OSS векторна БД з RAG туторіалами та гідами (2023–2025).
- **Weaviate** — векторна БД із вбудованими vectorizer’ами та RAG-прикладами.
- **Milvus** — масштабована векторна БД з reference-архітектурами RAG.
- **Vespa** — пошукова платформа з підтримкою векторів і RAG/LLM search whitepapers.
- **Elastic / OpenSearch** — поєднання BM25 і векторного пошуку; блоги та довідники про RAG-патерни.

Ці платформи надають:
- приклади інтеграції з LLM-фреймворками (LangChain, LlamaIndex, Haystack);
- best practices щодо індексації, фільтрації, hybrid search (BM25 + vectors);
- практичні гайди з виробничого RAG.

### 6.3 Хмарні та комерційні платформи

- **Azure** — Azure AI Search + Azure OpenAI, RAG reference architectures (2023–2025), включно з Graph RAG прикладами.
- **AWS** — Amazon Bedrock, Amazon Kendra + LLM, RAG blueprints.
- **Google Cloud** — Vertex AI Search & Conversation, Generative AI App Builder з RAG-патернами.
- **Databricks** — Lakehouse AI + Vector Search, solutions для RAG поверх Delta Lake.
- **Snowflake** — Snowflake Cortex / Native Apps з RAG-патернами для аналізу корпоративних даних.
- **Pinecone** — hosted vector DB з великою кількістю RAG best practices та архітектурних гідів.

**Горизонт актуальності.**
- Основні reference architectures від цих провайдерів публікуються та оновлюються 2023–2025 і залишаються релевантними на початку 2026. Нові версії зазвичай уточнюють деталі (без радикальної зміни базового RAG-патерна).

### 6.4 Кейс-стаді (оглядово)

Через обмеження публічності багато продакшн-кейсів описуються загально: «enterprise knowledge assistant», «customer support bot», «developer docs chat» тощо. Публічні матеріали 2023–2025 показують використання RAG принаймні в таких сценаріях:

- Внутрішні знання:
  - IT-support, HR, політики компанії.
- Зовнішні клієнтські сервіси:
  - customer support чат-боти для банків, e-commerce, SaaS.
- Спеціалізовані домени:
  - юридичні асистенти, медичні довідкові системи (з суворими вимогами до grounding/traceability).

У більшості кейсів використовується **classic або hybrid RAG** + reranking + елементи agentic/tool-augmented RAG.

На початок 2026 відсутні публічні кейси, які б задокументовано показували **принципово інший RAG-патерн**, ніж описані вище; системи масштабуються й шліфуються в межах уже усталених архітектур.

---

## 7. Таймлайн та прогалини знань до 2026

### Узагальнений таймлайн

- **2018–2019** — open-domain QA з retriever+reader, підготовчий етап до RAG.
- **2020** — RAG у формі Lewis et al.; ColBERT як потужний retriever.
- **2021–2022** — консолідація dense retrieval, перші стабільні продакшн-патерни RAG.
- **2022–2023** — HyDE, перші масові LLM-based RAG-системи, поява LangChain/LlamaIndex.
- **2023–2024** — multi-hop, agentic, memory, graph/modular, tool-augmented, streaming RAG входять у практику; вендори публікують RAG-гайди.
- **2024–2025** — великі survey-папери, чітка таксономія RAG, поява RAGAS, CRAG, FreshQA та інших RAG-специфічних evaluation frameworks.
- **Початок 2026** — доопрацювання вже відомих напрямів; немає публічно визнаного «нового покоління» архітектур.

### Де дані підтверджені до 2024

- Базовий RAG-патерн (Lewis et al. 2020), dense retrievers, ColBERT, ранні продакшн case studies.
- Основні open-domain QA/IR бенчмарки (NQ, TriviaQA, MS MARCO, KILT, BEIR, MTEB).
- Поява та перші реалізації HyDE, multi-hop, agentic, memory, graph, streaming RAG.

### Де є джерела до 2025

- Comprehensive surveys (IEEE, arXiv:2506.00054, Springer 2025) з детальною таксономією RAG.
- Формалізація підкласів: 
  - retriever-centric / generator-centric / hybrid;
  - orchestration/agentic;
  - robustness-oriented, graph-based, memory-augmented, streaming, MoE-RAG.
- Розвиток RAGAS, CRAG, FreshQA та інших RAG-орієнтованих benchmarks/metrics.
- Reference architectures від Azure, AWS, GCP, Databricks, Snowflake, Pinecone та OSS-фреймворків.

### Прогалини та обережність щодо 2026

1. **Нові архітектурні класи у 2026**
   - Публічні джерела до початку 2026 НЕ показують появи зовсім нових сімейств архітектур (поза вже переліченими). Будь-які твердження про «RAG 2026» як якісно іншу парадигму слід сприймати з обережністю.

2. **Нові великі RAG-бенчмарки після 2025**
   - Окрім CRAG, FreshQA та низки більш вузьких датасетів, немає підтвердження існування одного домінуючого «RAG benchmark 2026», який би витіснив наявні.

3. **Метрики й фреймворки 2026+**
   - Можлива поява нових метрик/фреймворків після 2025 року, але вони ще не відображені в основних survey-паперах 2025 і не мають усталеного статусу.

4. **Продакшн-архітектури 2026**
   - Reference architectures 2023–2025 залишаються актуальними. Немає публічних ознак, що в 2026 році індустрія масово перейшла на інший, принципово новий патерн RAG.

---

## 8. Висновки

1. **RAG еволюціонував від простої схеми «retriever + генератор» до розгалуженої екосистеми архітектур.** Classic RAG, HyDE, ColBERT/late interaction, multi-hop, agentic, memory, modular/graph, tool-augmented та streaming RAG — це не взаємовиключні, а взаємодоповнювальні патерни.

2. **Таксономія RAG стабілізувалася до 2024–2025 років.** Великі survey-папери й вендорні гіди узгоджено виділяють схожі класи й підкласи: retriever-centric, generator-centric, hybrid, orchestration/agentic, robustness-oriented (у т.ч. graph, memory, streaming, MoE-RAG). Це формує спільну «мову» для дослідників і практиків.

3. **Оцінювання RAG вийшло за межі класичних IR- і QA-метрик.** IR-метрики (Recall@k, nDCG) і task-level метрики (EM/F1, ROUGE) залишаються важливими, але для промислових сценаріїв ключовими стають groundedness, faithfulness, hallucination rate та корисність, часто виміряні через LLM-as-a-judge у фреймворках на кшталт RAGAS і бенчмарках типу CRAG/FreshQA.

4. **Індустрія сформувала сталий набір RAG-патернів.** Хмарні провайдери, векторні БД та OSS-фреймворки (LangChain, LlamaIndex, Haystack, Qdrant, Weaviate, Milvus, Elastic, Pinecone тощо) конвергують до схожих архітектур: векторний/гібридний пошук, reranking, контекстна компресія, оркестрація інструментів та агентів, memory/graph-розширення.

5. **На рубежі 2025–початку 2026 року ми не бачимо радикального «RAG 2.0/3.0».** Натомість спостерігається поступове вдосконалення вже відомих ідей: кращі retrievers, глибша інтеграція з agentic workflow, більш стрункі MoE-підходи, виважене cost-оптимізоване оркестрування, покращені фреймворки оцінювання.

6. **Ключові відкриті проблеми (станом на 2024–2025)**:
   - Масштабування й latency при збільшенні обсягів даних.
   - Зниження галюцинацій у складних, багатоджерельних сценаріях.
   - Автоматизоване, надійне оцінювання на рівні реальних бізнес-задач, а не тільки стандартних бенчмарків.
   - Безпека й захист від атак на retrieval-частину (data poisoning, prompt injection через документи).

7. **Подальший розвиток (гіпотетичний, без прив’язки до 2026 як «факту»).** Найімовірніші напрями — глибша інтеграція RAG у агентні системи, комбінування з плануванням/символічним міркуванням, посилення безпеки та формальні гарантії коректності, а також поява доменно-специфічних RAG-варіантів (наприклад, для біомедицини чи права) з власними індексами, метриками та регуляторними вимогами.

Усе вище подане відображає стан публічно доступних знань **до кінця 2025 – початку 2026 року**. Будь-які подальші твердження про «наступні хвилі» RAG потребують окремого оновлення цього огляду на основі новіших джерел.

---

## Джерела

**Локальна база знань**
- retrieval-augmented-generation.pdf, p.0–1, 4–5 — базове визначення RAG, згадки IBM і Microsoft, посилання на ColBERT.
- langchain.pdf, p.3 — контекст про LangChain як компанію/фреймворк (2025).

**Web / зовнішні джерела**
- Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*, NeurIPS 2020.
- Khattab & Zaharia, *ColBERT: Efficient and Effective Passage Search via Contextualized Late Interaction over BERT*, SIGIR 2020.
- Gao et al., *Precise Zero-shot Dense Retrieval without Relevance Labels* (HyDE), arXiv:2212.10496, 2022.
- *A Survey of Retrieval-Augmented Generation (RAG) for Large Language Models*, IEEE, ≈2024–2025.
- *Retrieval-Augmented Generation: A Comprehensive Survey of RAG Systems*, arXiv:2506.00054, 2025.
- *Retrieval-Augmented Generation for AI-Generated Content: A Survey*, Springer, 2025.
- RAGAS documentation, *Available Metrics for RAGAS*, 2023–2025, https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/.
- Azure Architecture Center, *Information retrieval in RAG*, 2025-01-10.
- Документація та блоги LangChain, LlamaIndex, Haystack, Qdrant, Weaviate, Milvus, Vespa, Elastic, OpenSearch, Pinecone (2023–2025).
- Публікації про бенчмарки й датасети: NQ, TriviaQA, MS MARCO, KILT, BEIR, MTEB, HotpotQA, 2WikiMultihopQA, MuSiQue, FreshQA, CRAG (2016–2025).