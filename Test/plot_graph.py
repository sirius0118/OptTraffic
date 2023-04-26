import matplotlib.pyplot as plt
import networkx as nx

graph = {'jaeger.yaml_file': 0, 'media-mongodb.yaml_file': 0, 'post-storage-mongodb.yaml_file': 0, 'social-graph-mongodb.yaml_file': 0,
               'url-shorten-mongodb.yaml_file': 0, 'user-mongodb.yaml_file': 0, 'user-timeline-mongodb.yaml_file': 0,
               'compose-post-service.yaml_file': 0, 'home-timeline-redis.yaml_file': 0, 'home-timeline-service.yaml_file': 0,
               'media-frontend.yaml_file': 0, 'media-memcached.yaml_file': 0, 'media-service.json.yaml_file': 0, 'nginx-thrift.yaml_file': 0,
               'post-storage-memcached.yaml_file': 0, 'post-storage-service.yaml_file': 0, 'social-graph-redis.yaml_file': 0,
               'social-graph-service.yaml_file': 0, 'text-service.yaml_file': 0, 'unique-id-service.yaml_file': 0,
               'url-shorten-memcached.yaml_file': 0, 'url-shorten-service.yaml_file': 0, 'user-memcached.yaml_file': 0,
               'user-mention-service.yaml_file': 0, 'user-service.yaml_file': 0, 'user-timeline-redis.yaml_file': 0,
               'user-timeline-service.yaml_file': 0}

G = nx.DiGraph()

for i in list(graph.keys()):
    G.add_node(i[:-5])

G.add_edge('nginx-thrift', 'compose-post-service')
G.add_edge('compose-post-service', 'home-timeline-service')
G.add_edge('compose-post-service', 'media-service.json')
G.add_edge('compose-post-service', 'unique-id-service')
G.add_edge('compose-post-service', 'text-service')
G.add_edge('compose-post-service', 'user-service')
G.add_edge('compose-post-service', 'user-timeline-service')

G.add_edge('home-timeline-service', 'home-timeline-redis')
G.add_edge('home-timeline-service', 'post-storage-service')
G.add_edge('home-timeline-service', 'social-graph-service')
G.add_edge('post-storage-service', 'post-storage-mongodb')
G.add_edge('post-storage-service', 'post-storage-memcached')
G.add_edge('social-graph-service', 'social-graph-redis')
G.add_edge('social-graph-service', 'social-graph-mongodb')

G.add_edge('text-service', 'user-mention-service')
G.add_edge('user-mention-service', 'user-memcached')
G.add_edge('user-mention-service', 'user-mongodb')
G.add_edge('text-service', 'url-shorten-service')
G.add_edge('url-shorten-service', 'url-shorten-mongodb')

G.add_edge('user-service', 'user-mongodb')

G.add_edge('user-timeline-service', 'post-storage-service')
G.add_edge('user-timeline-service', 'user-timeline-redis')
G.add_edge('user-timeline-service', 'user-timeline-mongodb')


nx.draw(G, with_labels=True)
plt.show()
