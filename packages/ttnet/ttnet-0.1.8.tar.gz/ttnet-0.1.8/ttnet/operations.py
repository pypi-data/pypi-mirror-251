import uunet.multinet as ml

from ttnet.net import TemporalTextNetwork
from ttnet.help import df

import networkx as nx

from result import Result, Ok, Err


def text_discretization(net: TemporalTextNetwork, text_buckets):
    g = ml.empty()
    ml.add_layers(n = g, layers = ['A'], directed = [False])
    ml.add_layers(n = g, layers = list(text_buckets.keys()), directed = [False] * len(list(text_buckets.keys())))

    for layer in list(text_buckets.keys()):
        layers = {
            'layer1': ['A'],
            'layer2': [layer],
            'dir': [True]
        }

        ml.set_directed(g, layers)


    layers = ['A'] * len(net.get_actors())
    ml.add_vertices(g, {'actor': net.get_actors(), 'layer': layers})

    for layer, messages in text_buckets.items():
        for msg in messages:
            producer = net.get_message_producer(msg)
            consumers = net.get_message_consumers(msg)

            ml.add_vertices(g, {'actor': [msg], 'layer': [layer]})

            if isinstance(producer, Ok):
                edges = {
                    "from_actor": [producer.ok_value],
                    "from_layer": ['A'],
                    "to_actor": [msg],
                    "to_layer": [layer],
                    "dir": [True]}
            else:
                edges = {
                    "from_actor": [],
                    "from_layer": [],
                    "to_actor": [],
                    "to_layer": [],
                    "dir": []}


            if isinstance(consumers, Ok):
                for consumer in consumers.ok_value:
                    edges['from_actor'].append(msg)
                    edges['from_layer'].append(layer)
                    edges['to_actor'].append(consumer)
                    edges['to_layer'].append('A')
                    edges['dir'].append(True)

            ml.add_edges(g, edges)

    return g

def temporal_discretization(net: TemporalTextNetwork, time_cuts):
    g = ml.empty()
    ml.add_layers(n = g, layers = ['A'], directed = [False])

    time_layers = [str(i) for i in time_cuts]
    ml.add_layers(n = g, layers = time_layers, directed = [False] * len(time_layers))

    for layer in time_layers:
        layers = {
            'layer1': ['A'],
            'layer2': [layer],
            'dir': [True]
        }

        ml.set_directed(g, layers)

    layers = ['A'] * len(net.get_actors())
    ml.add_vertices(g, {'actor': net.get_actors(), 'layer': layers})

    pt = net._get_production_times()
    msgs_ids = pt['message']
    actors_ids = pt['actor']

    sorted_msgs = dict(sorted(pt['t'].items(), key=lambda item: item[1]))

    last_cut = 0
    for cut in time_cuts:
        for msg_index, t in sorted_msgs.items():
            if t < cut and t >= last_cut:

                layer = str(cut)
                msg = msgs_ids[msg_index]
                producer = net.get_message_producer(msg)
                consumers = net.get_message_consumers(msg)

                ml.add_vertices(g, {'actor': [msg], 'layer': [layer]})

                if isinstance(producer, Ok):
                    edges = {
                        "from_actor": [producer.ok_value],
                        "from_layer": ['A'],
                        "to_actor": [msg],
                        "to_layer": [layer],
                        "dir": [True]}
                else:
                    edges = {
                        "from_actor": [],
                        "from_layer": [],
                        "to_actor": [],
                        "to_layer": [],
                        "dir": []}

                if isinstance(consumers, Ok):
                    for consumer in consumers.ok_value:
                        edges['from_actor'].append(msg)
                        edges['from_layer'].append(layer)
                        edges['to_actor'].append(consumer)
                        edges['to_layer'].append('A')
                        edges['dir'].append(True)

                ml.add_edges(g, edges)

        last_cut = cut

    return g

def project_actors(net: TemporalTextNetwork):
    pass

def project_messages(net: TemporalTextNetwork):
    pass

def project_discrete_network(net):
    g = ml.empty()
    d = df(ml.edges(net))

    layers = ml.layers(net)
    ml.add_layers(n = g, layers = layers, directed = [True] * len(layers))

    actors = ml.vertices(net, ['A']).get('actor')
    for layer in layers:
        dst = [layer] * len(actors)
        ml.add_vertices(net, {'actor': actors, 'layer': dst})

        for msg_id in ml.vertices(net, [layer]).get('actor'):
            if msg_id in actors:
                continue

            producer = d.loc[(d['to_actor'] == msg_id) & (d['from_layer'] == 'A'), 'from_actor'].item()
            consumers = d.loc[(d['from_actor'] == msg_id) & (d['to_layer'] == 'A'), 'to_actor']

            for consumer in consumers:
                print(consumer)
                edge = {
                    "from_actor": [producer],
                    "from_layer": [layer],
                    "to_actor": [consumer],
                    "to_layer": [layer],
                    "dir": [True]}

                ml.add_edges(g, edge)

    return g
