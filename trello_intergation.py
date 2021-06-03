from trello import TrelloClient

KEY = 'ffba680bac049b6e80eac080de3ff457'
SECRET = '159debd0c390f8884edc00a44e08b97eded6bef59fb90d976fa6cf9b96e28873'

client = TrelloClient(api_key=KEY, api_secret=SECRET)
print(client.list_boards())

new_board = client.list_boards()[0]

to_do = new_board.list_lists()[0]
done = new_board.list_lists()[1]
# done = new_board.list_lists()[2]
print(done)

# Верхняя карточка в списке "to do"
card = to_do.list_cards()[0]

card.change_list(new_board.list_lists()[2].id)
# Переместить сразу в done
card.change_list(done.id)


to_do.add_card('Чё-нить сделай да!')
