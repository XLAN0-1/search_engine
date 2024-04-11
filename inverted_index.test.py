from inverted_index import InvertedIndex

index = InvertedIndex()



document1 = "example.com"
document1_tokens = "this is a test by lana to see my index in action is an index".split()
document2 = "ebay.com"
document2_tokens = "ebay is a site where you can buy items via auctioning".split()


index.add_document(document1, document1_tokens)
index.add_document(document2, document2_tokens)

index.search("index")