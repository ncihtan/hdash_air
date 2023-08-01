"""Validation Rule."""

from hdash.validator.validation_rule import ValidationRule
from hdash.graph.htan_graph import HtanGraph


class ValidateLinks(ValidationRule):
    """Validate all internal links."""

    def __init__(self, htan_graph: HtanGraph):
        """Construct new Validation Rule."""
        super().__init__("H_LINKS", "Links connect.")
        self._htan_graph = htan_graph
        self._validate_edges()
        self._validate_adjacent_edges()

    def _validate_edges(self):
        """Validate Edges."""
        edge_list = self._htan_graph.edge_list
        directed_graph = self._htan_graph.directed_graph
        for edge in edge_list:
            parent_id = edge[0]
            child_id = edge[1]
            if child_id in directed_graph.nodes:
                child_node = directed_graph.nodes[child_id]
                if "EXT" not in parent_id and parent_id not in directed_graph.nodes:
                    error_message = (
                        f"{child_id} references parent ID="
                        f"{parent_id}, but no such ID exists."
                    )
                    self.add_error(
                        error_message, child_node[HtanGraph.DATA_KEY].meta_file
                    )

                if child_id == parent_id:
                    error_message = f"{child_id} references itself as a parent."
                    self.add_error(
                        error_message, child_node[HtanGraph.DATA_KEY].meta_file
                    )

    def _validate_adjacent_edges(self):
        """Validate Adjacent Edges."""
        adjacent_edge_list = self._htan_graph.adjacent_list
        directed_graph = self._htan_graph.directed_graph
        for edge in adjacent_edge_list:
            source_id = edge[0]
            adjacent_id = edge[1]
            source_node = directed_graph.nodes[source_id]

            if adjacent_id not in directed_graph.nodes:
                error_msg = (
                    f"{source_id} references adjacent ID="
                    f"{adjacent_id}, but no such ID exists."
                )
                self.add_error(error_msg, source_node[HtanGraph.DATA_KEY].meta_file)
