with open("catalog-service/app/application/use_cases.py", "r", encoding="utf-8") as f:
    content = f.read()

# Replace all BookResponse calls to include suggested_price
old = "            enriched_flag=book.enriched_flag,\n            published_flag=book.published_flag,\n        )"
new = "            enriched_flag=book.enriched_flag,\n            published_flag=book.published_flag,\n            suggested_price=book.suggested_price,\n        )"
content = content.replace(old, new)

old2 = "            enriched_flag=b.enriched_flag,\n                published_flag=b.published_flag,\n            )"
new2 = "            enriched_flag=b.enriched_flag,\n                published_flag=b.published_flag,\n                suggested_price=b.suggested_price,\n            )"
content = content.replace(old2, new2)

old3 = "            enriched_flag=published.enriched_flag,\n            published_flag=published.published_flag,\n        )"
new3 = "            enriched_flag=published.enriched_flag,\n            published_flag=published.published_flag,\n            suggested_price=published.suggested_price,\n        )"
content = content.replace(old3, new3)

with open("catalog-service/app/application/use_cases.py", "w", encoding="utf-8") as f:
    f.write(content)
print("Done")
print(content.count("suggested_price"), "occurrences of suggested_price")
