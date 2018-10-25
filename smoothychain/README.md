# TODO:

1. PoS майнинг (betepok)
2. Поправить функцию get_balance
3. ​
4. branch for main node (betepok) - в самый последний момент
5. P2P (nikita)
6. checker (nikita)

# API

## methods:

### - /chain/length (public) [GET]

Возвращаем текущую длину цепочки

### - /chain/block?id={ID} (public) [GET]

Возвращаем конкретный блок.

### - /api/public_key (public) [GET]

Возвращаем публичный ключ текущей ноды.

### - /api/get_new_transaction [POST]

...

### - /api/sign_candidate (public) [POST]

??

### - /api/create_block (private) [GET] ???

Создать блок с текущим пейлоадом.

```HTTP
GET /api/create_block?token=0fc677fc7904378deeb2d057ee96d6ca947a06e3c052277bd31facdb5f03d3a3 HTTP/1.1
Host: localhost:8000
Content-Type: application/x-www-form-urlencoded
```

### - /api/create_transaction (private) [POST] ???

Создать новую транзакцию

```HTTP
POST /api/create_transaction?token=0fc677fc7904378deeb2d057ee96d6ca947a06e3c052277bd31facdb5f03d3a3 HTTP/1.1
Host: localhost:8000
Content-Type: application/x-www-form-urlencoded
Content-Length: 948

to_pubkey=129007787299136025904994120015423214458402017278189927455721509946613613371759918809892683242436185202242780144741446060454905083301024137166388270435508673765159863572933907131052385589219829571211822820478435287467659647573336309016186090376384062782587703890857980040812238476428796813159139144631735811167,18036667493436683186281965268161327276194410371342915267286965082681310688928951965397731977554442489357986959732809976837907538057577467019379820342184425188240565259406249472870656543586299655465129403609782306073211386904010771500402174589391749351830409079811059867868371066214294349033637935809686124610,14361218684856120777117758320050044433386800560864012367227493350610807717769946767891002432118544676002750979118019443116013783124634108262262064313491992323880514096872968553385930094267880820415784839702378387067640695975551774781460297735546088577291601245598593240020974668342752730176715415618456814189&amount=123
```

###  - /api/create_contract (private) [POST] ???

Создать новый контракт

```HTTP
POST /api/create_contract?token=0fc677fc7904378deeb2d057ee96d6ca947a06e3c052277bd31facdb5f03d3a3 HTTP/1.1
Host: localhost:8000
Content-Type: application/x-www-form-urlencoded
Content-Length: 13

code=code_will_be_here
```

### - /api/private_key (private) [GET] ??????????

Хз, нужно ли, но можно на основе этого сделать годную багу

### - /api/eval_contract (private) [POST]

# Blockchain

## block

- pub_key
- block_id
- prev_block_id
- prev_block_hash
- payload
- magic
- proof

## transaction

- type = **1**
- from_pubkey
- to_pubkey
- signature
- amount
- timestamp

## contract

- type = **2**
- from_pubkey
- signature
- code
- timestamp

# Logic

## Поиск новых блоков в сети

Раз в определенный промежуток времени проходимся по всем нодам в цикле. Если у ноды длина больше нашей, то достаем блок с id нашей длины + 1, проверяем его и крепим к нашей ноде если всё окей. И так по всем блокам, пока длина не будет такой же. Если блок не подходит к нашей цепочке, то забиваем на него и сразу переходим к новой ноде. 

Никаких конфликтов разрешать мы не будем, поскольку майнит у нас только 1 нода.

## Майнинг нового блока

1. Валидируем все транзакции в блоке и считаем новый баланс, который получится.
2. Смотрим, сколько осталось денег у кошелька текущей ноды. 
3. Если деньги есть, то создаем новую транзакцию самим себе (**важно: с учетом комиссии**) и добавляем её в payload (награда за майнинг учитывается в этой транзакции, просто выход больше, чем вход)
4. На основе денег в транзакции считается новая сложность
5. После этого блок майнится с новой сложностью

## Добавление созданного блока

1. Валидируем все транзакции в блоке
2. Берем первую транзакцию, в которой отправитель равен получателю транзакции и создателю блока. Проверяем её валидность и пересчитываем сложность для этого блока на основе суммы.
3. Добавляем блок, удаляем весь кэш транзакций

## Основная логика таска

1. Бот запрашивает публичный ключ у сервиса команды. (через API) 

   - косяк в апи - приватный ключ тоже можно достать

2. Публичным ключом шифруется симметричный ключ и передается в контракте.

3. Банк майнит блок и добавляет его в блокчейн.

4. Команда синхронизирует блокчейн, достает контракт, выполняет его и получается симметричный ключ. Этот ключ становится глобальным для ноды.

   - RCE

5. Чекер вызывает публичный метод sign_candidate с флагом

   Входные данные (flag, id транзакции с переводом денег, подпись флага, ключ)

6. Проверка входных данных

   Проверка подписи флага

   Поиск транзакции и проверка(что тебе были переведены деньги)

   Сравнение ключей

   - DOS - использованные транзакции не учитываются, что дает возможность потратить баланс команды и положить им сервис.

7. Команда делает контракт для расшифровки флага с использованием симметричного ключа

   - Слабое шифрование
   - Косяк с подписью Эль Гамаля. Можно восстановить закрытый ключ.