from pysolr import Solr

conn = Solr("http://127.0.0.1:8983/solr/myblog", timeout=10000)
rs = conn.search("java")
print(rs)
