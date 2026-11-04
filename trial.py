import seriousdb


# for key in seriousdb.get_all():
#     seriousdb.delete(key)

# seriousdb.set(1, ("Organic Whole Milk (1 Gallon)", 4.89, True))

print(f"Count: {seriousdb.count()}")

# print(seriousdb.get_all())

result =  [
        {
            "id": item_id,
            "name": seriousdb.get(item_id)[0],
            "price": seriousdb.get(item_id)[1],
            "available": seriousdb.get(item_id)[2],
        }
        for item_id in seriousdb.get_all()
    ]

print(result)



# value = seriousdb.get("1")
# print(f"Value:{value}")