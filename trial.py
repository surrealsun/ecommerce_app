import seriousdb


# for key in seriousdb.get_all():
#     seriousdb.delete(key)

# seriousdb.set(1, ("Organic Whole Milk (1 Gallon)", 4.89, True))

print(f"Count: {seriousdb.count()}")

print(seriousdb.get_all())



# value = seriousdb.get("1")
# print(f"Value:{value}")