from justwatch import search

response = search("The Matrix", "US", "en", 10, True)
# print(response)

for entry in response:
    print(entry.short_description)

print()
