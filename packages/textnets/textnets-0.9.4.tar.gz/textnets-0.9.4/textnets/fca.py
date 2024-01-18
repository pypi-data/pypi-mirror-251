"""Implements experimental features for formal concept analysis."""

from __future__ import annotations

from abc import ABC, abstractmethod
from warnings import warn

from toolz import memoize

import textnets as tn


class FormalContext(ABC):
    """
    Abstract base class providing experimental FCA features.

    Textnets inherits methods from this class for treating its biadjacency
    matrix as a formal context.
    """

    @property
    @abstractmethod
    def m(self):
        pass

    @property
    def context(self):
        """Return formal context of terms and documents."""
        return self._formal_context(alpha=tn.params["ffca_cutoff"])

    @memoize
    def _formal_context(self, alpha: float):
        # The biadjacency matrix is a "fuzzy formal context." We can binarize
        # it by using a cutoff. This is known as an alpha-cut. This feature is
        # experimental.
        try:
            from concepts import Context
        except ImportError:
            warn("Install textnets[fca] to use FCA features.")
            raise
        crisp = self.m.map(lambda x: x >= alpha)
        reduced = crisp[crisp.any(axis=1)].loc[:, crisp.any(axis=0)]
        objects = reduced.index.tolist()
        properties = reduced.columns.tolist()
        bools = reduced.to_numpy().tolist()
        return Context(objects, properties, bools)
