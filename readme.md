# ChatGPT telegram bot
Этот бот представляет собой прокси-слой для отправки текстовых запросов к генеративным моделям OpenAI. 
В настоящий момент ведётся разработка, в текущей редакции представлен только скелет проекта.

[https://t.me/GhatGPTMeBot](https://t.me/GhatGPTMeBot)


### Некоторые особенности:
+ Для старта работы запрашивается пароль (его можно задать через переменную окружения);
+ Бот отправляет запросы к ChatGPT, хранит историю запросов и ответов;
+ Реализован механизм просмотра всей пользовательской истории, а также поиска в ней (на данный момент простого, 
не полнотекстового из-за используемой СУБД);
+ Реализован механизм очистки истории, а также просмотра баланса аккаунта в токенах.




# ChatGPT telegram bot
This bot is a proxy layer for sending text queries to OpenAI generative models. 
It is currently under development, with only the skeleton of the project presented in the current implementation.

[https://t.me/GhatGPTMeBot](https://t.me/GhatGPTMeBot)


### Project structure:
+ A password is prompted to start (it can be set through via environment variable);
+ Bot sends requests to ChatGPT, stores the history of requests and responses;
+ You can view the entire user history, as well as a search in it (currently simple, not fulltext search cause 
of SQLite);
+ You can also clean history, as well as view the account balance in tokens.
