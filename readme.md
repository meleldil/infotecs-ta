# REST API для российских городов с использованием базы GeoNames
### Тестовое задание для стажера на позицию «Аналитик (python)»
Выполнил Александр Усов
***

### Получить всю выборку

##### Запрос
`GET /cities`
##### Выдача
`[{"geonameid":"451747","name":"Zyabrikovo","asciiname":"Zyabrikovo","alternatenames":"","latitude":"56.84665","longitude":"34.7048","feature class":"P","feature code":"PPL","country code":"RU","cc2":"","admin1 code":"77","admin2 code":"","admin3 code":"","admin4 code":"","population":"0","elevation":"","dem":"204","timezone":"Europe/Moscow","modification date":"2011-07-09"}, ...`

### Получить информацию о городе по его id

##### Запрос
`GET /cities/id`
##### Пример
Запрос
`/cities/451749`
Выдача
`{"geonameid":"451749","name":"Zhukovo","asciiname":"Zhukovo","alternatenames":"","latitude":"57.26429","longitude":"34.20956","feature class":"P","feature code":"PPL","country code":"RU","cc2":"","admin1 code":"77","admin2 code":"","admin3 code":"","admin4 code":"","population":"0","elevation":"","dem":"237","timezone":"Europe/Moscow","modification date":"2011-07-09"}`

### Получить выборку
Пользователь вводит номер страницы и количество отображаемых на странице городов.

##### Запрос
`GET /cities/select?page=n&count=n`
##### Пример
Запрос
`/cities/select?page=10&count=3`
Выдача
`[{"geonameid":"451774","name":"Yakovlevo","asciiname":"Yakovlevo","alternatenames":"","latitude":"57.3122","longitude":"34.12509","feature class":"P","feature code":"PPL","country code":"RU","cc2":"","admin1 code":"77","admin2 code":"","admin3 code":"","admin4 code":"","population":"0","elevation":"","dem":"280","timezone":"Europe/Moscow","modification date":"2011-07-09"},{"geonameid":"451775","name":"Yakimovo","asciiname":"Yakimovo","alternatenames":"","latitude":"57.14907","longitude":"34.60264","feature class":"P","feature code":"PPL","country code":"RU","cc2":"","admin1 code":"77","admin2 code":"","admin3 code":"","admin4 code":"","population":"0","elevation":"","dem":"193","timezone":"Europe/Moscow","modification date":"2011-07-09"},{"geonameid":"451776","name":"Vysokoye","asciiname":"Vysokoye","alternatenames":"","latitude":"56.98226","longitude":"34.43519","feature class":"P","feature code":"PPL","country code":"RU","cc2":"","admin1 code":"77","admin2 code":"","admin3 code":"","admin4 code":"","population":"0","elevation":"","dem":"202","timezone":"Europe/Moscow","modification date":"2011-07-09"}]`

### Сравнение городов по расположению север-юг и часовому поясу
Пользователь вводит названия двух городов, получает информацию по обоим городам `city_1` и `city_2`, а также дополнительную информацию по сравнению этих городов `extra_info`:
1. какой город находится севернее - **north**
2. совпадают ли часовые пояса для обоих городов - **timezone**
 - 0 - не совпадают
 - 1 - совпадают
3. разница между часовыми поясами - **timezone_diff**
 - число положительное - у второго города часовой пояс отличается в б_о_льшую сторону
 - число отрицательное - наоборот
 - 0 - часовые пояса совпадают

##### Запрос
`GET /cities/compare?city_1=string&city_2=string`
##### Пример
Запрос
`/cities/compare?city_1=Burnyy&city_2=Sukhoy Rovets`
Выдача
`{"city_1:{"geonameid":570740,"name":"Burnyy","asciiname":"Burnyy","alternatenames":"Burnyj,Burnyy,Бурный","latitude":51.4,"longitude":"48.53333","feature class":"P","feature code":"PPL","country code":"RU","cc2":"","admin1 code":"67","admin2 code":"","admin3 code":"","admin4 code":"","population":0,"elevation":"","dem":"90","timezone":"Europe/Saratov","modification date":"2012-01-17"},
"city_2":
{"geonameid":816302,"name":"Sukhoy Rovets","asciiname":"Sukhoy Rovets","alternatenames":"Sukhoj Rovec,Sukhoy Rovets,Сухой Ровец","latitude":52.0442,"longitude":"35.1007","feature class":"P","feature code":"PPL","country code":"RU","cc2":"","admin1 code":"41","admin2 code":"","admin3 code":"","admin4 code":"","population":0,"elevation":"","dem":"160","timezone":"Europe/Moscow","modification date":"2012-01-19"},
"extra_info":{"north":"Sukhoy Rovets","timezone":0,"timezone_diff":-1}}`

### Подсказка городов по началу ввода
Пользователь вводит часть названия города, получает список названий городов, содержащих уже введенную часть строки.

##### Запрос
`GET /cities/autocomplete/string`
##### Пример
Запрос
`/cities/autocomplete/Zola`
Выдача
`["Rodnik Zola-Bulak","Zola"]`
