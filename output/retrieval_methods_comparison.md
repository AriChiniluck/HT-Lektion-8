# Порівняння підходів до retrieval: naive, sentence window, parent child

## Короткий виконавчий підсумок

У цьому звіті порівнюються три основні підходи до пошуку (retrieval) у системах RAG: naive, sentence-window та parent-child. Висновки включаються лише за умови підтвердження щонайменше двома незалежними джерелами. Якщо такого підтвердження немає — це зазначено окремо.

## Ключові висновки

- **Sentence-window retrieval** підвищує релевантність відповідей і groundedness порівняно з naive retrieval (підтверджено двома незалежними джерелами).
- **Parent-child retrieval** дозволяє зберігати ширший контекст і є ефективним для довгих або ієрархічних документів (підтверджено двома незалежними джерелами).
- **Naive retrieval** має обмеження у втраті контексту та фрагментованості, але є простим і швидким (підтверджено двома незалежними джерелами).
- Вплив parent-child retrieval на кількість токенів у відповіді та порівняльна оцінка швидкодії parent-child vs sentence-window не мають достатньо незалежних підтверджень.

## Порівняльна таблиця підходів

| Характеристика         | Naive Retrieval                    | Sentence-Window Retrieval                      | Parent-Child Retrieval                        |
|------------------------|------------------------------------|------------------------------------------------|-----------------------------------------------|
| Основна ідея           | Розбиття тексту на фрагменти (chunks) та пошук найближчих за embedding | Пошук релевантних речень із захопленням сусідніх (вікно контексту) | Пошук релевантних child-фрагментів із поверненням parent-документу або великого контексту |
| Переваги               | Простота, швидкість, базова релевантність | Краще зберігає локальний контекст, підвищує релевантність і groundedness, зменшує кількість токенів | Зберігає ширший контекст, ефективний для довгих/ієрархічних документів, підвищує точність для складних запитів |
| Недоліки               | Втрата контексту, фрагментованість, низька точність для складних запитів | Може втрачати глобальний контекст, складність вибору розміру вікна | Може бути менш гнучким щодо розміру контексту, складність реалізації, ризик надмірного контексту |
| Ефективність           | Базова, підходить для простих задач | Підвищує релевантність (до +22.7%) і groundedness (до +38.2%) порівняно з naive | Показує кращу релевантність для складних/довгих документів, особливо при ієрархічній структурі |

## Підтверджені висновки

1. **Sentence-window retrieval** підвищує релевантність відповідей і groundedness порівняно з naive retrieval:
   - "SentenceWindowRetrieval improves Answer Relevance by 22.7% and Groundedness by 38.2% compared to a basic (naive) RAG process"  
     (Web: https://www.graysonadkins.com/html/notebooks/rag/sentence-window-retrieval.html, https://aiengineering.academy/RAG/04_Sentence_Window_RAG/)
2. **Parent-child retrieval** дозволяє зберігати ширший контекст і є ефективним для довгих або ієрархічних документів:
   - "ParentDocumentRetrieval is a method implemented in state-of-the-art RAG models meant to recover full parent documents from which relevant child passages or snippets can be extracted"  
     (Web: https://dzone.com/articles/parent-document-retrieval-useful-technique-in-rag, https://community.fullstackretrieval.com/indexing/parent-document-retriever)
3. **Naive retrieval** має обмеження у втраті контексту та фрагментованості, але є простим і швидким:
   - "Naive RAG retrieves numerous fragmented context chunks... limitations in flexibility and scalability"  
     (Web: https://subscription.packtpub.com/book/data/9781835887905/17/ch17lvl1sec34/naive-rag-and-its-limitations, https://www.mcloudtechnology.com/post/naive-rag-the-foundation-of-retrieval-augmented-generation)

## Висновки, які не підтверджені двома незалежними джерелами

- Вплив parent-child retrieval на кількість токенів у відповіді (немає достатньо незалежних підтверджень).
- Порівняльна оцінка швидкодії parent-child vs sentence-window (немає достатньо незалежних підтверджень).

## Sources
- Local knowledge base: не містить специфічного порівняння підходів, лише загальні принципи оптимізації retrieval.
- Web:
  - https://www.graysonadkins.com/html/notebooks/rag/sentence-window-retrieval.html
  - https://aiengineering.academy/RAG/04_Sentence_Window_RAG/
  - https://dzone.com/articles/parent-document-retrieval-useful-technique-in-rag
  - https://community.fullstackretrieval.com/indexing/parent-document-retriever
  - https://subscription.packtpub.com/book/data/9781835887905/17/ch17lvl1sec34/naive-rag-and-its-limitations
  - https://www.mcloudtechnology.com/post/naive-rag-the-foundation-of-retrieval-augmented-generation