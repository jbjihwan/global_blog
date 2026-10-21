import urllib.request

for p in [
    '/assets/images/01_dns_routing_architecture-ea2cb0a9f6fc29f7bd63e0264ab74683.png',
    '/assets/images/02_indexing_pipeline-8f17d9e45c07877c55ba651d6017360f.png'
]:
    url = 'https://globaldevlog.com' + p
    r = urllib.request.urlopen(url)
    print(p, '=> Status:', r.status, 'Size:', len(r.read()), 'bytes')
