import uunet.multinet as ml
import pandas as pd

from result import Result, Ok, Err

from enum import Enum
from dataclasses import dataclass, field

from ttnet.help import df


class NetworkType(Enum):
    PURE_TEMPORAL = 0,
    PURE = 1,
    MIXED_TEMPORAL = 2,
    MIXED= 3,


class TemporalTextNetwork(object):
    def __init__(self):
        self._network = ml.empty()
        self._type = NetworkType.PURE

        self._content = dict()
        self._tedges_AM = df({"actor": list(), "message": list(), "t": list()})
        self._tedges_MA = df({"message": list(), "actor": list(), "t": list()})

        ml.add_layers(n = self._network, layers = ['A', 'M'], directed = [True, True])

        layers = {
            'layer1': ['A'],
            'layer2': ['M'],
            'dir': [True]
        }

        ml.set_directed(self._network, layers)


    def is_directed(self) -> bool:
        return ml.is_directed(self._network)

    def type(self) -> NetworkType:
        return self._type

    def add_actor(self, name: str) -> None:
        ml.add_vertices(self._network, {'actor': [name], 'layer': ['A']})

    def add_actors(self, names: list[str]) -> None:
        layers = ['A'] * len(names)
        ml.add_vertices(self._network, {'actor': names, 'layer': layers})

    def add_message(self, msg_id: str, producer: str, prod_time: int = None,
                    content: str = None,
                    consumers: list[str] | dict[str, int] | None = None) -> None:        # Add an attribute to the thing.
        actors = ml.vertices(self._network, ['A']).get('actor')
        if producer not in actors:
            self.add_actor(producer)

        if isinstance(consumers, list):
            consumers_actors = consumers
        elif isinstance(consumers, dict):
            consumers_actors = consumers.keys()
        else:
            consumers_actors = list()

        for consumer in consumers_actors:
            if consumer not in actors:
                self.add_actor(consumer)

        ml.add_vertices(self._network, {'actor': [msg_id], 'layer': ['M']})

        if content is not None:
            self._content[msg_id] = content

        edges = {
            "from_actor": [producer],
            "from_layer": ['A'],
            "to_actor": [msg_id],
            "to_layer": ['M'],
            "dir": [True]}

        for consumer in consumers_actors:
            edges['from_actor'].append(msg_id)
            edges['from_layer'].append('M')
            edges['to_actor'].append(consumer)
            edges['to_layer'].append('A')
            edges['dir'].append(True)

        ml.add_edges(self._network, edges)

        # Add time
        if prod_time is not None:
            if self._type == NetworkType.PURE:
                self._type = NetworkType.PURE_TEMPORAL
            elif self._type == NetworkType.MIXED:
                self._type = NetworkType.MIXED_TEMPORAL

            edge_info = pd.DataFrame([{'actor': producer, 'message': msg_id, 't': prod_time}])
            self._tedges_AM = pd.concat([self._tedges_AM, edge_info], ignore_index = True)

        if isinstance(consumers, dict):
            if self._type == NetworkType.PURE:
                self._type = NetworkType.PURE_TEMPORAL
            elif self._type == NetworkType.MIXED:
                self._type = NetworkType.MIXED_TEMPORAL

            for consumer, t in consumers.items():
                edge_info = pd.DataFrame([{'message': msg_id, 'actor': consumer, 't': t}])
                self._tedges_MA = pd.concat([self._tedges_MA, edge_info], ignore_index = True)

    def add_message_content(self, msg_id: str, content: str) -> Result[None, str]:
        messages = ml.vertices(self._network, ['M']).get('actor')
        if msg_id not in messages:
            return Err("Message does not exist")

        self._content[msg_id] = content
        return Ok(None)

    def add_actors_edge(self, from_actor: str, to_actor: str) -> Result[None, str]:
        actors = ml.vertices(self._network, ['A']).get('actor')
        if from_actor not in actors:
            return Err("Source actor does not exist")

        if to_actor not in actors:
            return Err("Destination actor does not exist")

        edge = {
            "from_actor": [from_actor],
            "from_layer": ['A'],
            "to_actor": [to_actor],
            "to_layer": ['A'],
            "dir": [True]}

        ml.add_edges(self._network, edge)

        if self._type == NetworkType.PURE:
            self._type = NetworkType.MIXED
        elif self._type == NetworkType.PURE_TEMPORAL:
            self._type = NetworkType.MIXED_TEMPORAL

        return Ok(None)

    def add_messages_edge(self, from_msg: str, to_msg: str) -> Result[None, str]:
        messages = ml.vertices(self._network, ['M']).get('actor')
        if from_msg not in messages:
            return Err("Source msg does not exist")

        if to_msg not in messages:
            return Err("Destination msg does not exist")

        edge = {
            "from_actor": [from_msg],
            "from_layer": ['M'],
            "to_actor": [to_msg],
            "to_layer": ['M'],
            "dir": [True]}

        ml.add_edges(self._network, edge)

        if self._type == NetworkType.PURE:
            self._type = NetworkType.MIXED
        elif self._type == NetworkType.PURE_TEMPORAL:
            self._type = NetworkType.MIXED_TEMPORAL

        return Ok(None)

    def get_actors(self):
        pass

    def get_messages(self):
        pass

    def get_edges(self):
        pass

    def get_message_times(self):
        pass

    def get_message_producer(self, msg_id: str) -> Result[str, str]:
        if msg_id in ml.vertices(self._network, ['M']).get('actor'):
            d = df(ml.edges(self._network))
            producer = d.loc[(d['to_actor'] == msg_id) & (d['to_layer'] == 'M'), 'from_actor']
            return Ok(producer.item())

        return Err("Message does not exists")

    def get_message_consumers(self, msg_id: str) -> Result[list[str], str]:
        if msg_id in ml.vertices(self._network, ['M']).get('actor'):
            d = df(ml.edges(self._network))
            consumers = d.loc[(d['from_actor'] == msg_id) & (d['to_layer'] == 'A'), 'to_actor']
            return Ok(list(consumers.values))

        return Err("Message does not exists")

    def get_message_content(self, msg_id: str) -> Result[str, str]:
        pass

    def get_producer_messages(self, producer: str) -> Result[list[str], str]:
        if producer in ml.vertices(self._network, ['A']).get('actor'):
            d = df(ml.edges(self._network))
            messages = d.loc[(d['from_actor'] == producer) & (d['to_layer'] == 'M'), 'to_actor']
            return Ok(list(messages.values))

        return Err("Actor does not exists")

    def get_consumer_messages(self, consumer: str) -> Result[list[str], str]:
        if consumer in ml.vertices(self._network, ['A']).get('actor'):
            d = df(ml.edges(self._network))
            messages = d.loc[(d['to_actor'] == consumer) & (d['from_layer'] == 'M'), 'from_actor']
            return Ok(list(messages.values))

        return Err("Actor does not exists")

    def summary(self):
        pass

    def to_mpx(self):
        return self._network
