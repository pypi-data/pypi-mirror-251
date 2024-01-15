import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ngraph.network import Network


class Analyser:
    def __init__(self, network: Network):
        """
        Initializes the Analyser with the network object.
        """
        self.network = network

    def get_links_df(self) -> pd.DataFrame:
        """
        Returns a dataframe with the link attributes.
        """
        links = []
        for link_id, link in self.network.links.items():
            link_dict = link.attributes.copy()
            links.append(link_dict)
        return pd.DataFrame(links)

    def get_nodes_df(self) -> pd.DataFrame:
        """
        Returns a dataframe with the node attributes.
        """
        nodes = []
        for node_id, node in self.network.nodes.items():
            node_dict = node.attributes.copy()
            nodes.append(node_dict)
        return pd.DataFrame(nodes)
